import sys
from numpy import pi, random, arange, size
from time import time, sleep
from shutil import copyfile
import modules.timetrack as timetrack
import modules.getlatest as getlatest

###########################
# Make instances available in this module
###########################

import source.qt as qt

ivvi = qt.instruments.get('ivvi')
keithley = qt.instruments.get('keithley')
awg = qt.instruments.get('awg')


def sweep_voltages(start_voltage, end_voltage, step_size):
    '''
    Sweep a specific gate from a start voltage to an end voltage.
    Input:
        start_voltage (int): Start voltage in mV
        end_voltage (int): End voltage in mV
        step_size (float): Step size in mV
        gate (str): Name of the gate as defined in _dac_map
    Output:
        voltages
    '''

    step_min = 4.0e3/(2**16) # Step size in mV
    step_size = round(step_size/step_min) * step_min
    voltages = arange(start_voltage, end_voltage, step_size)
    return voltages

    
def copy_script(filename, data_dir, name, scripts_folder='d:\\qtlab\\scripts\\B057_measurements'):
    '''
    Make a copy of the current running script.
    Usage: traces.copy_script(sys._getframe().f_code.co_filename,data._dir)
    
    Input:
        filename(str): Filename of the script
        data_dir(str): Data directory of the script
        name(str): Name of the copy file
    Output:
        None
    '''
    copyfile("%s" % filename, "%s\\%s.py" % (data_dir, name))

