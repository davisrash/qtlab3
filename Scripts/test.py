"""
add docstring
"""

from Scripts.gate_sweep import INPUT_VOLTAGE, INTERSWEEP_DELAY, INTRASWEEP_DELAY, RAMP_RATE
import source.qt as qt
import Scripts.modules.hbar_magnet as hbarm


FILENAME = 'test_magnet'

# circuit parameters
INPUT_VOLTAGE = 100e-6
SENSE_RESISTANCE = 992.0
NUM_GATES = 6

# sweep parameters
X_SWEEP = {'name': 'Gate 1', 'start': 0.0, 'stop': 0.5, 'step': 0.1}
Y_SWEEP = {'name': 'Gate 2', 'start': 0.0, 'stop': 0.5, 'step': 0.1}
RAMP_RATE = 0.01
INTRASWEEP_DELAY = 0.01
INTERSWEEP_DELAY = 0.1

