"""
add docstring
"""

import sys
from shutil import copyfile

#import numpy as np
import source.data as D
import source.qt as qt

NUM_GATES = 6
QDAC_ENABLED = False

lockins = []
meters = []
for name in qt.instruments.get_instrument_names():
    instrument = qt.instruments.get(name)
    if instrument.get_type() in ['SR830', 'SR860']:
        lockins.append(instrument)
    elif instrument.get_type() in ['Keithley_2400', 'Yokogawa_GS610']:
        meters.append(instrument)

if QDAC_ENABLED:
    qdac1 = qt.instruments.get('qdac1')

def create_data(filename, x_vector, x_coordinate, x_parameter, y_vector, y_coordinate, y_parameter, z_vector, z_coordinate, z_parameter):
    """
    add docstring
    """
    generator = D.IncrementalGenerator(qt.config['datadir'] + '\\' + filename)
    qt.Data.set_filename_generator(generator)

    data = qt.Data(name=filename)
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

    for i, _ in enumerate(lockins):
        data.add_value('Lockin {} X raw'.format(i))
        data.add_value('Lockin {} X pros'.format(i))
        data.add_value('Lockin {} Y raw'.format(i))

    data.create_file()
    copyfile(sys._getframe().f_code.co_filename,
             data.get_dir() + '\\' + filename + '_' + str(generator._counter - 1) + '.py')

    return data
