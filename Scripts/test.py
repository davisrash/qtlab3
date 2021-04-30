"""
TODO add docstring
"""

from modules import hbar
from source.qt import instruments

FILENAME = 'test'

START = 0
STOP = 5
STEP = 0.01

INPUT_VOLTAGE = 100e-6
SENSE_RESISTANCE = 992

NUM_GATES = 6

# get source-measure units
gs610 = instruments.get('gs610')
keith = instruments.get('keithley1')  # TODO update keithley

# get lock-in amplifiers
sr830 = instruments.get('sr830')
sr860 = instruments.get('sr860')

hbar.gate_sweep(FILENAME, lockin=sr830, meter=keith, name='Gate', start=START,
                stop=STOP, step=STEP, input_voltage=INPUT_VOLTAGE,
                sense_resistance=SENSE_RESISTANCE, num_gates=NUM_GATES)
