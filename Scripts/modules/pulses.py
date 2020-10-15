import sys
from numpy import pi, random, arange, size, array, sin, cos, round, zeros, ones, concatenate, zeros
from time import time, sleep
from shutil import copyfile

###########################
# Make instances available in this module
###########################

import qt
awg = qt.instruments.get('awg')



def create_constant_wfm():
    AWG_clock = 1e9

    number_waveform = 2
    waveform_prefix = 'katja_'


    burst_amplitude = 1.0

    wfm_length = 2e-6
    wfm_length_pts = round(wfm_length*AWG_clock)

    marker = zeros(wfm_length_pts)

    for k in arange(0,number_waveform,1):
        print 'Creating waveform number %i' %k
        waveform = burst_amplitude*ones(wfm_length_pts)
        filename = '%s%i.wfm' %(waveform_prefix,k)
        awg.send_waveform(waveform,marker,marker,filename,AWG_clock)

def create_rabi_pulses(cycle_time,burst_vec,AWG_clock):
    '''
    some choices which we migh change later:
    Ch1 will create the gate pulse, which is assumed to be a square wave
    Ch2 we will use to create the pulse gating the mixers
    Input:
    cycle_time: cycle time of the burst in s
    burst_vec : length of the microwave burst in s, should not exceed cycletime/2
    Amplitudes in the .wfm files are set to 1    
    '''
    
    N_waveform = len(burst_vec)

    cycle_time_pts = round(cycle_time*AWG_clock)
    # Note that the AWG520 requires that the number of points in a waveform is a integer multiple of 4
    cycle_time_pts = round(cycle_time_pts/4)*4
    max_burst_len = round(cycle_time_pts/2)-101

    #Create the square wave:
    #markers are not used at the moment, only initialize them
        
    print 'Creating square wave' 
    waveform =concatenate((-1.0*ones(round(cycle_time_pts/2)),1.0*ones(round(cycle_time_pts/2))),axis=0)
    marker = concatenate((zeros(round(cycle_time_pts/2)),ones(round(cycle_time_pts/2))),axis=0)
    filename = 'square_wave.wfm'
    awg.send_waveform(waveform,marker,marker,filename,AWG_clock)

    for k in arange(0,N_waveform,1):
        print 'Creating waveform number %i' %k
        waveform = -1.0*ones(cycle_time_pts)
        burst_pts = round(burst_vec[k]*AWG_clock)
        if burst_pts > max_burst_len :
            print 'Desired burst length too long. Make Cycle Time longer.'
            burst_pts = max_burst_len
        indexstart=round(cycle_time_pts/2)-50-burst_pts
        indexstop = round(cycle_time_pts/2)-50
        
        waveform[indexstart:indexstop] = 1
        filename = 'burst_%i.wfm' %(k)
        awg.send_waveform(waveform,marker,marker,filename,AWG_clock)

def create_square_waves(cycle_time,AWG_clock):
    '''
    some choices which we migh change later:
    Ch1 will create the gate pulse, which is assumed to be a square wave
    Ch2 we will use to create the pulse gating the mixers
    Input:
    cycle_time: cycle time of the burst in s
    burst_vec : length of the microwave burst in s, should not exceed cycletime/2
    Amplitudes in the .wfm files are set to 1    
    '''
    
    
    cycle_time_pts = round(cycle_time*AWG_clock)
    # Note that the AWG520 requires that the number of points in a waveform is a integer multiple of 4
    cycle_time_pts = round(cycle_time_pts/4)*4
    
    #Create the square wave:
    #markers are not used at the moment, only initialize them
        
    print 'Creating square wave' 
    waveform =concatenate((-1.0*ones(round(cycle_time_pts/2)),1.0*ones(round(cycle_time_pts/2))),axis=0)
    marker = concatenate((zeros(round(cycle_time_pts/2)),ones(round(cycle_time_pts/2))),axis=0)
    filename = 'square_wave_n.wfm'
    awg.send_waveform(waveform,marker,marker,filename,AWG_clock)

    print 'Creating inverted square wave' 
    waveform =concatenate((1.0*ones(round(cycle_time_pts/2)),-1.0*ones(round(cycle_time_pts/2))),axis=0)
    marker = concatenate((zeros(round(cycle_time_pts/2)),ones(round(cycle_time_pts/2))),axis=0)
    filename = 'square_wave_inv.wfm'
    awg.send_waveform(waveform,marker,marker,filename,AWG_clock)