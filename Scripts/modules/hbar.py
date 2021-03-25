"""
add docstring
"""

import sys
from shutil import copyfile

import numpy as np
import source.qt as qt
from source.data import IncrementalGenerator

lockins = qt.instruments.get_instruments_by_type('SR830') \
    + qt.instruments.get_instruments_by_type('SR860')
meters = qt.instruments.get_instruments_by_type('Keithley_2400') \
    + qt.instruments.get_instruments_by_type('Yokogawa_GS610') \
    + qt.instruments.get_instruments.by_type('QDevilQdac')


def create_data(filename: str, vectors: dict, coordinates: dict,
                parameters: dict, num_gates: int = 6):
    """
    add docstring
    """
    generator = IncrementalGenerator(qt.config['datadir'] + '\\' + filename)
    qt.Data.set_filename_generator(generator)

    data = qt.Data(name=filename)
    for var in ['x', 'y', 'z']:
        data.add_coordinate(parameters[var] + ' (' + coordinates[var] + ')',
                            size=len(vectors[var]), start=vectors[var][0],
                            end=vectors[var][-1])

    for i in range(num_gates):
        data.add_value('Gate {} V meas'.format(i))
        data.add_value('Gate {} leak'.format(i))

    for i, _ in enumerate(lockins):
        data.add_value('Lockin {} X raw'.format(i))
        data.add_value('Lockin {} X pros'.format(i))
        data.add_value('Lockin {} Y raw'.format(i))

    data.create_file()
    copyfile(sys._getframe().f_code.co_filename,  # pylint: disable=protected-access
             data.get_dir() + '\\' + filename + '_' + str(generator.counter - 1) + '.py')

    return data


def take_data(input_voltage: float, sense_resistance: float,
              num_gates: int = 6, intrasweep_delay: float = 0.001):
    """
    add docstring
    """
    qt.msleep(intrasweep_delay)

    X = []
    X_pros = []
    Y = []

    for i, lockin in enumerate(lockins):
        if lockin.get_type() == 'SR830':
            X.append(lockin.get_X())
            Y.append(lockin.get_Y())
        elif lockin.get_type() == 'SR860':
            X.append(lockin.get_data_param(0))
            Y.append(lockin.get_data_param(1))
        X_pros.append((input_voltage - X[i]) / (1e-9 if X[i] == 0.0 else X[i])
                      * sense_resistance)

    gates = [999] * num_gates
    leaks = [999] * num_gates

    for i, meter in enumerate(meters):
        if meter.get_type() == 'Keithley_2400':
            gates[i] = meter.get_voltage()
            leaks[i] = meter.get_current()

        elif meter.get_type() == 'Yokogawa_GS610':
            meter.set_sense_function(0)
            gates[i] = meter.read()

            meter.set_sense_function(1)
            leaks[i] = meter.read()

        elif meter.get_type() == 'QDevilQdac':
            for j in range(len(meters), num_gates):
                gates[j] = meter.getDCVoltage(j - len(meters) + 1)
                leaks[j] = meter.getCurrentReading(j - len(meters) + 1)

    return [i for j in zip(gates, leaks) for i in j] \
        + [i for j in zip(X, X_pros, Y) for i in j]


def volt_sweep(filename: str, lockin, xname, xstart, xend, xstep, rev, threshold):
    """
    add docstring
    """

    qt.mstart()

    vectors = {'x': np.arange(xstart, xend, xstep),
               'y': np.zeros(1),
               'z': np.zeros(1)}
    coordinates = {'x': xname,
                   'y': 'none',
                   'z': 'none'}
    parameters = {'x': 'Lockin Voltage',
                  'y': 'y_parameter',
                  'z': 'z_parameter'}

    x1_vector = []

    data_fwd = create_data(filename=filename, vectors=vectors,
                           coordinates=coordinates, parameters=parameters)

    for x in vectors['x']:
        if lockin.get_type() == 'SR830':
            lockin.set_amplitude(x)
        elif lockin.get_type() == 'SR860':
            lockin.set_sine_out_amplitude(x)

        qt.msleep(0.2)
        data_values = take_data(
            input_voltage=input_voltage, sense_resistance=sense_resistance)
        data_fwd.add_data_point(x, 0, 0, data_values[0], data_values[1])

        if data_values[0] > threshold:
            break

        x1_vector.append(x)

    data_fwd._write_settings_file()
    data_fwd.close_file()

    qt.msleep(intersweep_delay)

    if rev:
        x1_vector = np.flip(x1_vector)
        vectors['x'] = x1_vector
        data_bck = create_data(filename=filename, vectors=vectors,
                               coordinates=coordinates, parameters=parameters)

        for x1 in x1_vector:
            if lockin.get_type() == 'SR830':
                lockin.set_amplitude(x1)
            elif lockin.get_type() == 'SR860':
                lockin.set_sine_out_amplitude(x1)

            qt.msleep(0.2)
            data_values = take_data()
            data_bck.add_data_point(x1, 0, 0, data_values[0], data_values[1])

        data_bck._write_settings_file()
        data_bck.close_file()

    qt.mend()
    return 1


def qdac_1gate(filename: str, channel, meter, xname, xstart, xend, xstep, rev, threshold, compliance):
    qt.mstart()

    xnum = int(np.ceil(np.abs(xstart - xend) / xstep) + 1)

    x_vector = np.linspace(xstart, xend, xnum)
    y_vector = [0]
    z_vector = [0]

    vectors = {'x': np.linspace(xstart, xend, xnum),
               'y': [0],
               'z': [0]}
    coordinates = {'x': xname,
                   'y': 'none',
                   'z': 'none'}
    parameters = {'x': 'x_parameter',
                  'y': 'y_parameter',
                  'z': 'z_parameter'}

    x1_vector = []
    data_fwd = create_data(filename=filename, vectors=vectors,
                           coordinates=coordinates, parameters=parameters)

    for x in vectors['x']:
        if meter.get_type() == 'Keithley_2400':
            break


def qdac_1gate(self, channel, meter, xname, xstart, xend, xstep, rev, threshold, compliance):
    qt.mstart()

    xnum = int(np.ceil(np.abs(xstart - xend) / xstep) + 1)

    x_vector = np.linspace(xstart, xend, xnum)
    y_vector = [0]
    z_vector = [0]

    x1_vector = []
    data_fwd = self.create_data(x_vector, xname, 'x_parameter', y_vector,
                                'none', 'y_parameter', z_vector, 'none', 'z_parameter')

    for x in x_vector:

        '''
        if meter.get_type() == 'Keithley_2400':
            xcurrent = meter.get_voltage()
        elif meter.get_type() == 'Yokogawa_GS610':
            meter.set_sense_function(0)
            xcurrent = meter.read()
            print(xcurrent)
        elif meter.get_type() == 'QDevilQdac':
            xcurrent = meter.getDCVoltage(channel)

        ramp_steps = int(np.ceil(np.abs((xcurrent - x) / RAMP_RATE) + 1))
        temp_ramp = np.linspace(xcurrent, x, ramp_steps)

        for val in temp_ramp[1:]:
            mask = (val > x) ^ (xcurrent > x)
            if meter.get_type() == 'Keithley_2400':
                a.keithley_gateset(1, x if mask else val)
            elif meter.get_type() == 'Yokogawa_GS610':
                a.yoko_gateset(x if mask else val)
            elif meter.get_type() == 'QDevilQdac':
                meter.rampDCVoltage(channel, x if mask else val)
        '''
        if meter.get_type() == 'Keithley_2400':
            a.keithley_gateset(1, x)
        elif meter.get_type() == 'Yokogawa_GS610':
            a.yoko_gateset(x)
        elif meter.get_type() == 'QDevilQdac':
            meter.rampDCVoltage(channel, x)

        qt.msleep(INTRASWEEP_DELAY)
        data_values = take_data(x)  # x does not affect take_data?

        data_fwd.add_data_point(x, 0, 0, data_values[0], data_values[1], data_values[2], data_values[3], data_values[4], data_values[5], data_values[6], data_values[7],
                                data_values[8], data_values[9], data_values[10], data_values[11], data_values[12], data_values[13], data_values[14], data_values[15], data_values[16], data_values[17])

        if threshold is not None:
            if data_values[13] > threshold:
                break
        if data_values[2 * channel - 1] > compliance:
            break
        x1_vector.append(x)

    data_fwd._write_settings_file()
    data_fwd.close_file()
    qt.mend()
    qt.msleep(INTERSWEEP_DELAY)

    if rev:
        x1_vector = np.flip(x1_vector)
        data_bck = self.create_data(x1_vector, xname, 'Lockin Voltage',
                                    y_vector, 'none', 'y_parameter', z_vector, 'none', 'z_parameter')
        print("Reverse scan started.")
        for x1 in x1_vector:
            x1current = qdac1.getDCVoltage(channel)
            ramp_steps1 = np.int(
                np.ceil(np.abs((x1current - x1) / RAMP_RATE) + 1))
            temp_ramp1 = np.linspace(x1current, x1, ramp_steps1)

            for i in temp_ramp1[1:]:
                if (i > x1) ^ (x1current > x1):
                    qdac1.setDCVoltage(channel, x1)
                else:
                    qdac1.setDCVoltage(channel, i)
            qt.msleep(0.05)
            qdac1.setDCVoltage(channel, x1)
            qt.msleep(INTRASWEEP_DELAY)
            data_values = take_data(x1)

            data_bck.add_data_point(x, 0, 0, data_values[0:14])

        data_bck._write_settings_file()
        data_bck.close_file()

    qt.mend()
    return 1
