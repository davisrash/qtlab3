"""
docstring
"""

import sys
from shutil import copyfile
from time import time

import numpy as np
import source.qt as qt
from source.data import Data, IncrementalGenerator


current_time = time()

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

    # incrementally number file names in the given data directory
    generator = IncrementalGenerator(qt.config['datadir'] + '\\' + filename)
    Data.set_filename_generator(generator)

    # create data object
    data = Data(name=filename)

    # create coordinates
    for i, dim in enumerate(['x', 'y']):
        data.add_coordinate(dim + ' (' + names[i] + ')', size=len(vectors[i]),
                            start=vectors[i][0], end=vectors[i][-1])

    # put lockins into lists if necessary for looping
    if not isinstance(lockins, (list, tuple)):
        lockins = [lockins]

    # create lockin data
    for lockin in lockins:
        for dim in ['x', 'y']:
            data.add_value(dim + ' raw', instrument=lockin.get_name(),
                           units='V')
            data.add_value(dim + ' pros', instrument=lockin.get_name(),
                           units='V')

    # add data for each gate
    for i in range(num_gates):
        data.add_value('gate {} V meas'.format(i + 1),
                       #instrument=meter,
                       units='A')
        data.add_value('gate {} leak'.format(i + 1),
                       #instrument=meter,
                       units='A')

    # add time data
    data.add_value('time', units='s')

    # create data file
    data.create_file()
    copyfile(sys._getframe().f_code.co_filename,
             data.get_dir() + '\\' + filename + '_'
                 + str(generator.counter - 1) + '.py')

    return data

def take_data(lockins, meters, input_voltage, sense_resistance,
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

    # measure X and Y channels on lockins
    for lockin in lockins:
        if lockin.get_type() == 'SR830':
            x.append(lockin.get_X())
            y.append(lockin.get_Y())

        elif lockin.get_type() == 'SR860':
            x.append(lockin.get_data_param0())
            y.append(lockin.get_data_param1())

    # calculate x_pros and y_pros
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

    t = time() - current_time

    return [i for j in zip(x, x_pros, y, y_pros) for i in j] \
        + [i for j in zip(gates, leaks) for i in j] + [t]

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
    if len(sweeps) == 1:
        sweeps.append({'name': 'None', 'start': 0.0, 'stop': 0.0, 'step': 0.1})
        dims = 1
    else:
        dims = 2

    for sweep in sweeps:
        vectors.append(np.linspace(
            sweep['start'], sweep['stop'],
            int(np.ceil(np.abs(
                (sweep['stop'] - sweep['start']) / sweep['step']
            )) + 1)
        ))

    # ensure devices on
    for meter in meters:
        if meter.get_type() == 'Keithley_2400':
            pass
        elif meter.get_type() == 'GS610':
            pass
        elif meter.get_type() == 'QDevilQdac':
            pass

    if dims == 1:
        data = create_data(filename, lockins, vectors, num_gates,
                           [sweep['name'] for sweep in sweeps])

        qt.msleep(intersweep_delay)

        for x in vectors[0][0:]:
            meters[0].ramp_to_voltage(x, ramp_rate, channel=channels[0])

            qt.msleep(intrasweep_delay)
            data_vals = take_data(lockins, meters, input_voltage,
                                  sense_resistance, num_gates, channels)

            data.add_data_point([x, 0] + data_vals)

    elif dims == 2:
        data = create_data(filename, lockins, vectors, num_gates,
                           [sweep['name'] for sweep in sweeps])

        qt.msleep(intersweep_delay)

        for x in vectors[0][0:]:
            meters[0].ramp_to_voltage(x, ramp_rate, channel=channels[0])

            qt.msleep(intrasweep_delay)
            for y in vectors[1][0:]:
                meters[1].ramp_to_voltage(y, ramp_rate, channel=channels[1])

                qt.msleep(intrasweep_delay)
                data_vals = take_data(lockins, meters, input_voltage,
                                      sense_resistance, num_gates, channels)

                data.add_data_point([x, y] + data_vals)

    for meter in meters:
        if meter.get_type() == 'Keithley_2400':
            pass
        elif meter.get_type() == 'GS610':
            pass
        elif meter.get_type() == 'QDevilQdac':
            pass

    data._write_settings_file()
    data.close_file()

    qt.mend()
