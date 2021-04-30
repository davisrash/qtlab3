"""
TODO add docstring
"""

import sys
from shutil import copyfile

import numpy as np
from source import qt
from source.data import Data, IncrementalGenerator

def create_data(filename, lockin, vectors, names, num_gates=6):
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

    data.add_value('{} X raw'.format(lockin.get_name()))
    data.add_value('{} X pros'.format(lockin.get_name()))
    data.add_value('{} Y raw'.format(lockin.get_name()))

    data.create_file()
    copyfile(sys._getframe().f_code.co_filename,  # pylint: disable=protected-access
             data.get_dir() + '\\' + filename + '_'
             + str(generator.counter - 1) + '.py')

    return data

def take_data(lockin, meter, input_voltage, sense_resistance, num_gates=6):
    """
    TODO add docstring
    """

    if lockin.get_type() == 'SR830':
        x = lockin.get_X()
        y = lockin.get_Y()

    elif lockin.get_type() == 'SR860':
        x = lockin.get_data_param(0)
        y = lockin.get_data_param(1)

    x_pros = (input_voltage - x) * sense_resistance / (1e-9 if x == 0.0 else x)

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
    sweep_params : dict[str, float]
        A dict of the three parameters `start`, `stop`, and `step`,
        which define the sweep.
    """
    qt.mstart()

    vectors = (np.arange(kwargs['start'], kwargs['stop'], kwargs['step']),
               [], [])
    names = (kwargs['name'], 'none', 'none')

    data = create_data(filename, lockin, vectors, names)

    for x in vectors[0]:
        meter.ramp_to_voltage(x, kwargs['step'])

        #elif meter.get_type() == 'QDevilQdac':
        #    meter.rampDCVoltage(kwargs['channel'], i)

        data_vals = take_data(lockin, meter, kwargs['input_voltage'],
                              kwargs['sense_resistance'])
        data.add_data_point([x, 0, 0] + data_vals)

    data._write_settings_file()  # pylint: disable=protected-access
    data.close_file()

    qt.mend()
