"""
TODO add docstring
"""

import sys
from shutil import copyfile

import numpy as np
import source.qt as qt
from source.data import Data, IncrementalGenerator


def create_data(filename, vectors, names, num_gates=6):
    """
    Generates the data file.

    Parameters
    ----------
    filename : str
        The name of the data file to create.

    lockin : Instrument
        The lockin measuring the data.

    vectors : tuple[np.ndarray[float]]
        An tuple of vectors representing data in the dimensions x, y,
        and z.

    names : tuple[str]
        A tuple of names describing the vectors.

    Returns
    -------
    data : Data
        A special Data object containing all data.
    """
    generator = IncrementalGenerator(qt.config['datadir'] + '\\' + filename)
    Data.set_filename_generator(generator)

    data = Data(name=filename)

    for i, dim in enumerate(['x', 'y', 'z']):
        data.add_coordinate(dim + ' (' + names[i] + ')', size=len(vectors[i]),
                            start=vectors[i][0], end=vectors[i][-1])

    for i in range(1, num_gates + 1):
        data.add_value('Gate {} V meas'.format(i))
        data.add_value('Gate {} leak'.format(i))

    data.add_value('Lockin X raw')
    data.add_value('Lockin X pros')
    data.add_value('Lockin Y raw')

    data.create_file()
    copyfile(sys._getframe().f_code.co_filename,  # pylint: disable=protected-access
             data.get_dir() + '\\' + filename + '_'
             + str(generator.counter - 1) + '.py')

    return data

def take_data(lockins, meter, input_voltage, sense_resistance, num_gates=6):
    """
    TODO add docstring
    """
    gates = [999] * num_gates
    leaks = [999] * num_gates

    if meter.get_type() == 'Keithley_2400':
        gates[0] = meter.get_voltage()
        leaks[0] = meter.get_current()

    elif meter.get_type() == 'GS610':
        meter.set_sense_function('voltage')
        gates[0] = meter.read()

        meter.set_sense_function('current')
        leaks[0] = meter.read()

    #elif meter.get_type() == 'QDevilQdac':
    #    for i in range(1, num_gates + 1):
    #        gates[i] = meter.getDCVoltage(i)
    #        leaks[i] = meter.getCurrentReading(i)

    if isinstance(lockins, (tuple, list)):
        x = y = []

        # x = [lockins[i].get_X() for i, _ in enumerate(lockins)]

        for lockin in lockins:
            if lockin.get_type() == 'SR830':
                x.append(lockin.get_X())
                y.append(lockin.get_Y())

            elif lockin.get_type() == 'SR860':
                x.append(lockin.get_data_param0())
                y.append(lockin.get_data_param1())

            #x_pros = [(input_voltage - x[i]) * sense_resistance / (1e-9 if x[i] == 0.0 else x[i] for i in len(x))]

    else:
        lockin = lockins

        if lockin.get_type() == 'SR830':
            x = lockin.get_X()
            y = lockin.get_Y()

        elif lockin.get_type() == 'SR860':
            x = lockin.get_data_param0()
            y = lockin.get_data_param1()

        x_pros = (input_voltage - x) * sense_resistance \
            / (1e-9 if x == 0.0 else x)

    return [i for j in zip(gates, leaks) for i in j] + [x, x_pros, y]

def gate_sweep(filename, lockin, meter, **kwargs):
    """
    Creates a data file and then performs a voltage sweep with the
    source set by the meter and the output measured by the lockin. The
    data is written to the file.

    This function currently works with either the SR830 or SR860 and
    either the K2400 or GS610 as the lockin and meter, respectively.

    This function only works for one data dimension, namely `x`.

    Parameters
    ----------
    filename : str
        The name of the data file to create.

    lockin : Instrument
        Either the SR830 or the SR860, which measures the results of
        the sweep.

    meter : Instrument
        Either the K2400 or GS610, which sets the source voltage for
        the sweep.

    TODO improve docstring for **kwargs
        name : str
            A name describing the data collected.

        start : float
        stop : float
        step : float
        ramp_rate : float
        input_voltage : float
        sense_resistance : float
        num_gates : int
    """
    qt.mstart()

    ramp = np.linspace(kwargs['start'], kwargs['stop'],
                       int(np.ceil(np.abs((kwargs['start'] - kwargs['stop'])
                                          / kwargs['step'])) + 1))
    vectors = (ramp, [0], [0])
    names = (kwargs['name'], 'none', 'none')

    data = create_data(filename, vectors, names, num_gates=kwargs['num_gates'])

    if meter.get_type() == 'GS610':
        meter.set_output_state('on')

    qt.msleep(0.01)
    for level in vectors[0][1:]:
        meter.ramp_to_voltage(level, kwargs['ramp_rate'])

        qt.msleep(0.001)
        data_vals = take_data(lockin, meter, kwargs['input_voltage'],
                              kwargs['sense_resistance'],
                              num_gates=kwargs['num_gates'])

        data.add_data_point(level, 0, 0, data_vals[0], data_vals[1],
                            data_vals[2], data_vals[3], data_vals[4],
                            data_vals[5], data_vals[6], data_vals[7],
                            data_vals[8], data_vals[9], data_vals[10],
                            data_vals[11], data_vals[12], data_vals[13],
                            data_vals[14])

    if meter.get_type() == 'GS610':
        meter.set_output_state('off')

    data._write_settings_file()  # pylint: disable=protected-access
    data.close_file()

    qt.mend()
