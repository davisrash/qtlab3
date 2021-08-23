"""
add docstring
"""

import sys
from shutil import copyfile

import source.qt as qt
import Scripts.modules.hbar_dev as hbar


FILENAME = "test"

# get source-measure units
# GS610 = qt.instruments.get("gs610")
KEITH = qt.instruments.get("keithley1")  # TODO update keithley name
# QDAC = qt.instruments.get("qdac1")     # TODO update qdac name

# get lock-in amplifiers
SR830 = qt.instruments.get("sr830")
# SR860 = qt.instruments.get("sr860")

#
INSTRUMENTS = {"meters": [KEITH], "lockins": [SR830]}

CIRCUIT = {
    "input_voltage": 100e-6,
    "sense_resistance": 992.0,
    "num_gates": 1,
    "compliance": None,
    "threshold": None,
}

X_SWEEP = {
    "name": "gate 1",
    "start": 0.0,
    "stop": 0.1,
    "step": 0.02,
    "ramp_rate": 0.01,
    "intrasweep_delay": 0.1,
    "intersweep_delay": 0.1,
    "channel": None,
}

# Y_SWEEP = {
#     "name": "gate 2",
#     "start": 0.0,
#     "stop": 0.1,
#     "step": 0.02,
#     "ramp_rate": 0.01,
#     "intrasweep_delay": 0.1,
#     "intersweep_delay": 0.1,
#     "channel": None,
# }

# QDAC channels
CHANNELS = None


# run gate sweep
data = hbar.gate_sweep(FILENAME, INSTRUMENTS, CIRCUIT, X_SWEEP, CHANNELS)

copyfile(
    sys._getframe().f_code.co_filename,
    data.get_dir() + "\\" + data.get_filename()[:-4] + ".py",
)
