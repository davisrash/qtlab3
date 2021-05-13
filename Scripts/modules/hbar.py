"""
TODO add docstring
"""

import sys
from shutil import copyfile

import numpy as np
import source.qt as qt
from source.data import Data, IncrementalGenerator


def create_data(filename, lockin_name, vectors, names, num_gates=6):
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

    for i, dim in enumerate(['x', 'y']):
        data.add_coordinate(dim + ' (' + names[i] + ')', size=len(vectors[i]),
                            start=vectors[i][0], end=vectors[i][-1])
        data.add_value(lockin_name + ' ' + dim + ' raw')
        data.add_value(lockin_name + ' ' + dim + ' pros')

    for i in range(1, num_gates + 1):
        data.add_value('Gate {} V meas'.format(i))
        data.add_value('Gate {} leak'.format(i))

    data.create_file()
    copyfile(sys._getframe().f_code.co_filename,  # pylint: disable=protected-access
             data.get_dir() + '\\' + filename + '_'
             + str(generator.counter - 1) + '.py')

    return data

def take_data(lockins, meter, input_voltage, sense_resistance, num_gates=6):
    """
    TODO add docstring
    """
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

        # TODO standardize these function names!
        if lockin.get_type() == 'SR830':
            x, y = lockin.get_X(), lockin.get_Y()

        elif lockin.get_type() == 'SR860':
            x, y = lockin.get_data_param0(), lockin.get_data_param1()

        x_pros = (input_voltage - x) * sense_resistance \
            / (1e-9 if x == 0.0 else x)
        y_pros = (input_voltage - y) * sense_resistance \
            / (1e-9 if y == 0.0 else y)

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

    return [x, x_pros, y, y_pros] + [i for j in zip(gates, leaks) for i in j]

def gate_sweep(filename, lockin, meter, dims=1, **kwargs):
    """
    Creates a data file and then performs a voltage sweep with the
    source set by the meter and the output measured by the lockin. The
    data is written to the file.

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

    dims : int
        Blah

    **kwargs : dict
        'channels' : tuple[int]
            Blah

        'names' : tuple[str]
            Blah

        'start' : tuple[float]
            Blah

        'stop' : tuple[float]
            Blah

        'step' : tuple[float]
            Blah

        'ramp_rate' : float
            Blah

        'input_voltage' : float
            Blah

        'sense_resistance' : float
            Blah

        'num_gates' : int
            Blah
    """
    qt.mstart()

    # get kwargs
    channels = kwargs['channels']
    start = kwargs['start']
    stop = kwargs['stop']
    step = kwargs['step']

    vectors = [[0], [0]]
    for i in range(dims):
        vectors[i] = np.linspace(start[i], stop[i], int(np.ceil(np.abs(
                            (stop[i] - start[i]) / step[i]
                        )) + 1))

    data = create_data(filename, lockin.get_name(), vectors, kwargs['names'],
                       num_gates=kwargs['num_gates'])

    if meter.get_type() == 'GS610':
        meter.set_output_state('on')
    elif meter.get_type() == 'Keithley_2400':
        pass

    qt.msleep(0.01)
    for x in vectors[0][1:]:
        meter.ramp_to_voltage(x, kwargs['ramp_rate'], channel=channels[0])

        if dims == 2:
            for y in vectors[1][1:]:
                meter.ramp_to_voltage(y, kwargs['ramp_rate'],
                                      channel=channels[1])

                qt.msleep(0.001)
                data_vals = take_data(lockin, meter, kwargs['input_voltage'],
                                      kwargs['sense_resistance'],
                                      num_gates=kwargs['num_gates'])

                data.add_data_point(x, y, data_vals[0], data_vals[1],
                                    data_vals[2], data_vals[3], data_vals[4],
                                    data_vals[5], data_vals[6], data_vals[7],
                                    data_vals[8], data_vals[9], data_vals[10],
                                    data_vals[11], data_vals[12],
                                    data_vals[13], data_vals[14],
                                    data_vals[15])
        else:
            qt.msleep(0.001)
            data_vals = take_data(lockin, meter, kwargs['input_voltage'],
                                  kwargs['sense_resistance'],
                                  num_gates=kwargs['num_gates'])

            data.add_data_point(x, 0, data_vals[0], data_vals[1], data_vals[2],
                                data_vals[3], data_vals[4], data_vals[5],
                                data_vals[6], data_vals[7], data_vals[8],
                                data_vals[9], data_vals[10], data_vals[11],
                                data_vals[12], data_vals[13], data_vals[14],
                                data_vals[15])

    if meter.get_type() == 'GS610':
        meter.set_output_state('off')
    elif meter.get_type() == 'Keithley_2400':
        pass

    data._write_settings_file()  # pylint: disable=protected-access
    data.close_file()

    qt.mend()

def gate_sweep_helper(data, lockin, meter, x, **kwargs):
    meter.ramp_to_voltage(x, kwargs['ramp_rate'], channel=kwargs['channel'])

    qt.msleep(0.001)
    data_vals = take_data(lockin, meter, kwargs['input_voltage'],
                          kwargs['sense_resistance'],
                          num_gates=kwargs['num_gates'])

    data.add_data_point(x, 0, 0, data_vals[0], data_vals[1], data_vals[2],
                        data_vals[3], data_vals[4], data_vals[5], data_vals[6],
                        data_vals[7], data_vals[8], data_vals[9],
                        data_vals[10], data_vals[11], data_vals[12],
                        data_vals[13], data_vals[14])
    
    return data
