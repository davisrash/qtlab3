"""
add docstring
"""

import source.qt as qt
import Scripts.modules.hbar_dev as hbar


FILENAME = "test_magnet"

# get source-measure units
GS610 = qt.instruments.get("gs610")
KEITH = qt.instruments.get("keithley1")  # TODO update keithley name
# QDAC = qt.instruments.get("qdac1")     # TODO update qdac name

# get lock-in amplifiers
SR830 = qt.instruments.get("sr830")
SR860 = qt.instruments.get("sr860")

# get magnet
MAG = qt.instruments.get("magnet")

#
INSTRUMENTS = {"meters": [GS610, KEITH], "lockins": [SR830, SR860], "magnets": MAG}

CIRCUIT = {
    "input_voltage": 100e-6,
    "sense_resistance": 992.0,
    "num_gates": 2,
    "compliance": None,
    "threshold": None,
}

SWEEPS = {
    "name": "magnetic field",
    "start": 0.0,
    "stop": 6.0,
    "step": 0.1,
    "intrasweep_delay": 0.01,
    "intersweep_delay": 0.1,
    "ramp_rate": 0.01,
    "magnet_ramp_rate": 0.04,
    "v_gate": 0.0,
    "vector": None,
}

# Qdac channels
CHANNELS = [None]

# run magnet sweep
# hbar.magnet_sweep(FILENAME, INSTRUMENTS, CIRCUIT, SWEEPS)
hbar.record(FILENAME, INSTRUMENTS, CIRCUIT, SWEEPS, 10, 1)
