"""
TODO add docstring
"""

import source.qt as qt
import Scripts.modules.hbar as hbar


FILENAME = 'test'

START = (0.0, 0.0)
STOP = (1.0, 0.0)
STEP = (0.1, 0.0)

NAMES = ('Gate 1', 'Gate 2')

RAMP_RATE = 0.01
INPUT_VOLTAGE = 100e-6
SENSE_RESISTANCE = 992.0

NUM_GATES = 6

# get source-measure units
gs610 = qt.instruments.get('gs610')
keith = qt.instruments.get('keithley1')  # TODO update keithley type name

# get lock-in amplifiers
sr830 = qt.instruments.get('sr830')
sr860 = qt.instruments.get('sr860')

hbar.gate_sweep(FILENAME, lockin=sr830, meter=gs610, dims=1,
                channels=(None, None), names=NAMES, start=START, stop=STOP,
                step=STEP, ramp_rate=RAMP_RATE, input_voltage=INPUT_VOLTAGE,
                sense_resistance=SENSE_RESISTANCE, num_gates=NUM_GATES)
