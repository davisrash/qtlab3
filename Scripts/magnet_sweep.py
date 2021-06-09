"""
add docstring
"""

import source.qt as qt
import Scripts.modules.hbar_test as hbar


FILENAME = 'test_magnet'

# get source-measure units
GS610 = qt.instruments.get('gs610')
KEITH = qt.instruments.get('keithley1')  # TODO update keithley name
#qdac = qt.instruments.get('qdac1')  # TODO update qdac name

# get lock-in amplifiers
SR830 = qt.instruments.get('sr830')
SR860 = qt.instruments.get('sr860')

# get magnet
MAG = qt.instruments.get('magnet')

#
INSTRUMENTS = {'meters' : [GS610, KEITH],
               'lockins': [SR830, SR860],
               'magnet' : MAG}

# circuit parameters
INPUT_VOLTAGE = 100e-6
SENSE_RESISTANCE = 992.0
NUM_GATES = 2

# sweep parameters
SWEEP = {'name': 'magnetic field', 'start': 0.0, 'stop': 10, 'step': 0.1}
RAMP_RATE = 0.01
INTRASWEEP_DELAY = 0.01
INTERSWEEP_DELAY = 0.1

# Qdac channels
CHANNELS = [None]

# run magnet sweep
hbar.magnet_sweep(FILENAME, INSTRUMENTS, END, RAMP_RATE)
