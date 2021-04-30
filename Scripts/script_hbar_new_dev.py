"""
TODO add docstring
"""

import sys
from shutil import copyfile

import numpy as np
from source import qt
from source.data import Data, IncrementalGenerator

gs610 = qt.instruments.get('gs610')
sr860 = qt.instruments.get('sr860')

NUM_GATES = 6


class Script():
    """
    TODO add docstring
    """

    def __init__(self):
        self.generator = IncrementalGenerator(qt.config['datadir'] + '\\'
                                              + FILENAME)

    def create_data(self, x_vector, x_coordinate, x_parameter, y_vector,
                    y_coordinate, y_parameter, z_vector, z_coordinate,
                    z_parameter):
        """
        TODO add docstring
        """
        Data.set_filename_generator(self.generator)
        data = Data(name=FILENAME)
        data.add_coordinate(x_parameter + ' (' + x_coordinate + ')',
                            size=len(x_vector), start=x_vector[0],
                            end=x_vector[-1])
        data.add_coordinate(y_parameter + ' (' + y_coordinate + ')',
                            size=len(y_vector), start=y_vector[0],
                            end=y_vector[-1])
        data.add_coordinate(z_parameter + ' (' + z_coordinate + ')',
                            size=len(z_vector), start=z_vector[0],
                            end=z_vector[-1])

        for i in range(NUM_GATES):
            data.add_value('Gate {} V meas'.format(i))
            data.add_value('Gate {} leak'.format(i))

        data.add_value('Lockin 1 X raw')
        data.add_value('Lockin 1 X pros')
        data.add_value('Lockin 1 Y raw')

        data.create_file()
        copyfile(sys._getframe().f_code.co_filename,  # pylint: disable=protected-access
                 data.get_dir() + '\\' + FILENAME + '_' + str(self.generator.counter - 1) + '.py')

        return data

    def qdac_1gate(self, channel, xname, xstart, xend, xstep,
                   threshold, compliance):
        """
        add docstring
        """
        qt.mstart()

        xnum = int(np.ceil(np.abs((xstart - xend) / xstep) + 1))

        x_vector = np.linspace(xstart, xend, xnum)
        y_vector = [0]
        z_vector = [0]

        x1_vector = []
        data_fwd = self.create_data(x_vector, xname, 'x_parameter', y_vector,
                                    'none', 'y_parameter', z_vector, 'none',
                                    'z_parameter')

        for x in x_vector:
            if x == x_vector[1]:
                print("Scan has started.")
            
            xcurrent = gs610.get_source_voltage_level()

            ramp_steps = int(np.ceil(np.abs((xcurrent - x) / xstep) + 1))

            qt.msleep(INTRASWEEP_DELAY)
            data_values = take_data()

            data_fwd.add_data_point(x, 0, 0, data_values[0], data_values[1],
                                    data_values[2], data_values[3],
                                    data_values[4], data_values[5],
                                    data_values[6], data_values[7],
                                    data_values[8], data_values[9],
                                    data_values[10], data_values[11],
                                    data_values[12], data_values[13],
                                    data_values[14], data_values[15],
                                    data_values[16], data_values[17])

            if threshold is not None:
                if data_values[13] > threshold:
                    break
            if data_values[2 * channel - 1] > compliance:
                break
            x1_vector.append(x)


        data_fwd._write_settings_file()  # pylint: disable=protected-access
        data_fwd.close_file()
        qt.mend()
        qt.msleep(INTERSWEEP_DELAY)


def take_data():
    """
    TODO add docstring
    """
    qt.msleep(INTRASWEEP_DELAY)

    X = sr860.get_data_param0()
    X_pros = (V_IN - X) / (1e-9 if X == 0.0 else X) * R_SENSE
    Y = sr860.get_data_param1()

    gates = [999] * NUM_GATES
    leaks = [999] * NUM_GATES
    
    gs610.set_sense_function('voltage')
    gates[0] = gs610.read()

    gs610.set_sense_function('current')
    leaks[0] = gs610.read()

    return [i for j in zip(gates, leaks) for i in j] \
        + [i for j in zip(X, X_pros, Y) for i in j]


FILENAME = 'test'
INTRASWEEP_DELAY = 0.001
INTERSWEEP_DELAY = 1
THRESHOLD = 200000
COMPLIANCE = 5e-6
RAMP_RATE = 1e-2

R_SENSE = 992

START1 = 0
END1 = 0.5
XSTEP1 = 0.1
REV = False

V_IN = 100e-6
# lockin1.set_amplitude(0.1)
# a.yoko_gateset(1)
# a.yoko_gateset(1)

a = Script()
a.qdac_1gate(1, 'Gate', START1, END1, XSTEP1, THRESHOLD, COMPLIANCE)