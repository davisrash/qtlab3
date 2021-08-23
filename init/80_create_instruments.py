"""
TODO add docstring
"""

# TODO:
#  - change GP-IB addresses (0-30) to lower numbers with some converntion
#  - determine if creating a `physical` instrument as below requires physical
#    GP-IB connection to not error

import source.qt as qt

# source-measure units
# GS610 = qt.instruments.create('gs610', 'GS610', address='GPIB::1')
print("Successfully connected to a GS610 on GP-IB address 1.")

# lock-in amplifiers
SR830 = qt.instruments.create("sr830", "SR830", address="GPIB::9")
print("Successfully connected to an SR830 on GP-IB address 9.")
# SR860 = qt.instruments.create('sr860', 'SR860', address='GPIB::4')
# print("Successfully connected to an SR860 on GP-IB address 4.")

# ---

##K2400
print("Setting up K2400...")
KEITH = qt.instruments.create(
    "keithley1", "Keithley_2400", address="GPIB::24", change_display=False
)

print("All instruments set up and good to go!")
