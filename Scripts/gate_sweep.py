"""
add docstring
"""

import source.qt as qt
import Scripts.modules.hbar as hbar


FILENAME = 'test'

# circuit parameters
INPUT_VOLTAGE = 100e-6
SENSE_RESISTANCE = 992.0
NUM_GATES = 2

# sweep parameters
X_SWEEP = {'name': 'Gate 1', 'start': 0.0, 'stop': 0.1, 'step': 0.1}
Y_SWEEP = {'name': 'Gate 2', 'start': 0.0, 'stop': 0.1, 'step': 0.1}
RAMP_RATE = 0.01
INTRASWEEP_DELAY = 0.01
INTERSWEEP_DELAY = 0.1

# Qdac channels (must be same size as num sweeps)
CHANNELS = [None, None]

# get source-measure units
gs610 = qt.instruments.get('gs610')
keith = qt.instruments.get('keithley1')  # TODO update keithley name
#qdac = qt.instruments.get('qdac1')  # TODO update qdac name

# get lock-in amplifiers
sr830 = qt.instruments.get('sr830')
sr860 = qt.instruments.get('sr860')

# run gate sweep
hbar.gate_sweep(FILENAME, [sr830, sr860], [gs610, keith], INPUT_VOLTAGE,
                SENSE_RESISTANCE, NUM_GATES, [X_SWEEP, Y_SWEEP], RAMP_RATE,
                INTRASWEEP_DELAY, INTERSWEEP_DELAY, CHANNELS)
