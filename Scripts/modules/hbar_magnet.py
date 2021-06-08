"""
docstring
"""

import sys
from shutil import copyfile

import numpy as np
import source.qt as qt
from source.data import Data, IncrementalGenerator


def create_data(filename, lockins, vectors, num_gates, names):
    """
    Generates the data file.

    Parameters
    ----------
    filename : str
        The name of the data file to create.

    lockins : Instrument | list[Instrument] | tuple[Instrument]
        One or multiple of the SR830 and the SR860, which measure the
        channel parameters X and Y.

    vectors : list[np.ndarray[float]]
        An list of vectors representing data for the channel parameters
        X and Y.

    names : list[str]
        A list of names describing the vectors.

    Returns
    -------
    data : Data
        A special Data object containing all data.
    """
    # TODO investigate use of additional add_value parameters

    # incrementally number file names in the given data directory
    generator = IncrementalGenerator(qt.config['datadir'] + '\\' + filename)
    Data.set_filename_generator(generator)

    # create data object
    data = Data(name=filename)

    # create coordinates
    for i, (dim, vector) in enumerate(vectors.items()):
        data.add_coordinate(dim + ' (' + names[i] + ')', size=len(vector),
                            start=vector[0], end=vector[-1])

    # add data fields for multiple lockins
    if isinstance(lockins, (list, tuple)):
        for lockin in lockins:
            for dim in vectors:
                data.add_value(lockin.get_name() + ' ' + dim + ' raw')
                data.add_value(lockin.get_name() + ' ' + dim + ' pros')

    # add data fields for a single lockin
    else:
        lockin = lockins
        for dim in vectors:
            data.add_value(lockin + ' ' + dim + ' raw')
            data.add_value(lockin + ' ' + dim + ' pros')

    # add data for each gate
    for i in range(num_gates):
        data.add_value('Gate {} V meas'.format(i + 1))
        data.add_value('Gate {} leak'.format(i + 1))

    # create data file
    data.create_file()
    copyfile(sys._getframe().f_code.co_filename,  # pylint: disable=protected-access
             data.get_dir() + '\\' + filename + '_'
             + str(generator.counter - 1) + '.py')

    return data

def take_data(lockins, meters, num_sweeps, input_voltage, sense_resistance,
              num_gates, channels=None):
    """
    Measures and returns the voltage on the X and Y channels using the
    meter and the gate voltage and leakage current using the lockin.

    Parameters
    ----------
    lockins : Instrument | list[Instrument] | tuple[Instrument]
        One or multiple of the SR830 and the SR860, which measure the
        channel parameters X and Y.

    meters : Instrument | list[Instrument] | tuple[Instrument]
        One or multiple of K2400, GS610, or QDAC, which measure the
        voltage and leakage current on one or more gates.

    num_sweeps : int | list[int] | tuple[int]
        If using one lockin, then `num_sweeps` should be `1` or `2`
        corresponding to a sweep across the lockin's X channel or both
        X and Y channels. If using two lockins, then `num_sweeps`
        should be either `[2, 0]`, `[0, 2]`, or `[1, 1]`
        corresponding to the number of sweeps to be run on the lockins
        enumerated by `lockins`.

    input_voltage : float
        TODO add description

    sense_resistance : float
        TODO add description

    channels : tuple[int] | None
        TODO add description

    num_gates : int
        The number of gates on the device. The lockin may not have
        sufficiently many channels for the gates.
    """
    # TODO standardize parameter measuring, i.e. get_X()
    # and get_data_param0()

    # define lists for data
    x, y = [], []
    gates, leaks = [], []

    # put variables into lists if necessary for looping
    if not isinstance(lockins, (list, tuple)):
        lockins = [lockins]

    if not isinstance(meters, (list, tuple)):
        meters = [meters]

    if not isinstance(num_sweeps, (list, tuple)):
        num_sweeps = [num_sweeps]

    # measure X and Y channels on lockins
    for i, lockin in enumerate(lockins):
        if lockin.get_type() == 'SR830':
            if num_sweeps[i] == 1:
                x.append(lockin.get_X())
            elif num_sweeps[i] == 2:
                x.append(lockin.get_X())
                y.append(lockin.get_Y())

        elif lockin.get_type() == 'SR860':
            if num_sweeps[i] == 1:
                x.append(lockin.get_data_param0())
            elif num_sweeps[i] == 2:
                x.append(lockin.get_data_param0())
                y.append(lockin.get_data_param1())

    # calculate x_pros and y_pros
    # TODO calculate y_pros only if necessary
    x_pros = [(input_voltage - x[i]) * sense_resistance /
              (1e-9 if x[i] == 0.0 else x[i]) for i in range(len(x))]
    y_pros = [(input_voltage - y[i]) * sense_resistance /
              (1e-9 if y[i] == 0.0 else y[i]) for i in range(len(y))]

    # measure gate voltage and leakage current for meters
    for meter in meters:
        if meter.get_type() == 'Keithley_2400':
            gates.append(meter.get_voltage())
            leaks.append(meter.get_current())

        elif meter.get_type() == 'GS610':
            meter.set_sense_function('voltage')
            gates.append(meter.read())

            meter.set_sense_function('current')
            leaks.append(meter.read())

        elif meter.get_type() == 'QDevilQdac':
            for channel in channels:
                gates.append(meter.getDCVoltage(channel))
                leaks.append(meter.getCurrentReading(channel))

    # set all other gate voltages and leakage currents to 999
    for _ in range(num_gates - len(gates)):
        gates.append(999)
        leaks.append(999)

    data = []
    for num in num_sweeps:
        if num == 1:
            data.append([i for j in zip(x, x_pros) for i in j])
        elif num == 2:
            data.append([i for j in zip(x, x_pros, y, y_pros) for i in j])

    return [i for j in data for i in j] \
        + [i for j in zip(gates, leaks) for i in j]

def gate_sweep(filename, lockins, meters, input_voltage, sense_resistance,
               num_gates, sweeps, ramp_rate, intrasweep_delay,
               intersweep_delay, channels):
    """
    Creates a data file and then performs a voltage sweep with the
    source set by the meter and the output measured by the lockin. The
    data is written to the file.

    Parameters
    ----------
    filename : str
        The name of the data file to create.

    lockins : Instrument | list[Instrument] | tuple[Instrument]
        One or multiple of the SR830 and the SR860, which measure the
        results of the sweep.

    meters : Instrument | list[Instrument] | tuple[Instrument]
        One or multiple of K2400, GS610, or QDAC, which set the source
        voltage for the sweep and measure the voltage and leakage
        current on one or more gates.

    input_voltage : float
        TODO add description

    sense_resistance : float
        TODO add description
    """

    qt.mstart()

    if not isinstance(lockins, (list, tuple)):
        lockins = [lockins]
    if not isinstance(meters, (list, tuple)):
        meters = [meters]

    vectors = []
    for sweep in sweeps:
        vectors.append(np.linspace(
            sweep['start'], sweep['stop'],
            int(np.ceil(np.abs(
                (sweep['stop'] - sweep['start']) / sweep['step']
            )) + 1)
        ))

    for meter in meters:
        if meter.get_type() == 'Keithley_2400':
            pass
        elif meter.get_type() == 'GS610':
            meter.set_output_state('on')
        elif meter.get_type() == 'QDevilQdac':
            pass

    if len(sweeps) == 1:
        data = create_data(filename, lockins, dict(zip(['x'], vectors)),
                           num_gates, [sweep['name'] for sweep in sweeps])

        qt.msleep(intersweep_delay)

        for x in vectors[0][1:]:
            meters[0].ramp_to_voltage(x, ramp_rate, channel=channels[0])

            qt.msleep(intrasweep_delay)
            data_vals = take_data(lockins, meters, 1, input_voltage,
                                  sense_resistance, num_gates, channels)

            data.add_data_point([x] + data_vals)
            print([x] + data_vals)
            print(len([x] + data_vals))

    elif len(sweeps) == 2:
        data = create_data(filename, lockins, dict(zip(['x', 'y'], vectors)),
                           num_gates, [sweep['name'] for sweep in sweeps])

        qt.msleep(intersweep_delay)

        for x in vectors[0][1:]:
            meters[0].ramp_to_voltage(x, ramp_rate, channel=channels[0])

            qt.msleep(intrasweep_delay)
            for y in vectors[1][1:]:
                meters[1].ramp_to_voltage(y, ramp_rate, channel=channels[1])

                qt.msleep(intrasweep_delay)
                data_vals = take_data(lockins, meters, [1, 1],
                                      input_voltage, sense_resistance,
                                      num_gates, channels)

                data.add_data_point([x, y] + data_vals)

    for meter in meters:
        if meter.get_type() == 'Keithley_2400':
            pass
        elif meter.get_type() == 'GS610':
            meter.set_output_state('off')
        elif meter.get_type() == 'QDevilQdac':
            pass

    data._write_settings_file()  # pylint: disable=protected-access
    data.close_file()

    qt.mend()
