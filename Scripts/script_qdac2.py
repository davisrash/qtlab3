from numpy import pi, random, arange, size, array, sin, cos, linspace, sinc, sqrt, flip
from time import time, sleep
from shutil import copyfile
from os import mkdir
from os.path import exists

import math
import qt
#import timetrack
import sys
sys.path.append(r'C:\Users\physics-svc-laroche\Desktop\qtlab3\Scripts\modules')
import numpy as np
import data as d
import traces
import shutil
import os
import numpy

#keithley1 = qt.instruments.get('keithley1')
lockin1 = qt.instruments.get('lockin1')
qdac1 = qt.instruments.get('qdac1')



class S1():
    
    def __init__(self): 
        self.filename=filename
        self.generator=d.IncrementalGenerator(qt.config['datadir']+'\\'+self.filename,1);
    
    
    # Function generates data file, spyview file and copies the python script.
    def create_data(self,x_vector,x_coordinate,x_parameter,y_vector,y_coordinate,y_parameter,z_vector,z_coordinate,z_parameter):
        qt.Data.set_filename_generator(self.generator)
        data = qt.Data(name=self.filename)
        #print(filename)
        data.add_coordinate(x_parameter+' ('+x_coordinate+')',
                            size=len(x_vector),
                            start=x_vector[0],
                            end=x_vector[-1]) 
        data.add_coordinate(y_parameter+' ('+y_coordinate+')',
                            size=len(y_vector),
                            start=y_vector[0],
                            end=y_vector[-1]) 
        data.add_coordinate(z_parameter+' ('+z_coordinate+')',
                            size=len(z_vector),
                            start=z_vector[0],
                            end=z_vector[-1])
                            

        # Gate 1
        data.add_value('Gate 1 V meas')

        data.add_value('Gate 1 leak')
        
        # Gate 2
        data.add_value('Gate 2 V meas')
        
        data.add_value('Gate 2 leak')
        
        # Lockin 1
        data.add_value('Lockin 1 X raw')
        data.add_value('Lockin 1 X pros')
        data.add_value('Lockin 1 Y raw')
        
                                                  
        data.create_file()    
        traces.copy_script(sys._getframe().f_code.co_filename,data._dir,self.filename+'_'+str(self.generator._counter-1))           # Copy the python script into the data folder
        return data
        
        
    def take_data(self,x):
                qt.msleep(delay2)
                #K1 = keithley1.get_readnextval()                                     # Read out Keithley1            
                #K1_value = K1/GainK1                                                 # Use explained at bottom of the script
                L1_X = lockin1.get_X()                                                 # Read out Lockin1
                L1_X_pro = (V_in-L1_X)/L1_X * R_sense
                L1_Y = lockin1.get_Y()
                
                
                
                gate_1 = qdac1.getDCVoltage(1)
                gate_2 = qdac1.getDCVoltage(2)
                leak_1 = qdac1.getCurrentReading(1)
                leak_2 = qdac1.getCurrentReading(2)
                
                if number_gates ==1 : 
                    datavalues = [gate_1,leak_1,0,0,L1_X,L1_X_pro,L1_Y]
                    
                elif number_gates ==2 : 
                    datavalues = [gate_1,leak_1,gate_2,leak_2,L1_X,L1_X_pro,L1_Y]
                
                     
                
                return datavalues
        
     
    
    def volt_sweep(self,xname,xstart,xend,xstep,rev,threshold):
        qt.mstart()
        
       
        # Create sweep vectors
        x_vector = arange(xstart,xend,xstep)
        y_vector = [0]
        z_vector = [0]
        
        x1_vector = []
        
        data_fwd = self.create_data(x_vector,xname,'Lockin Voltage',y_vector,'none','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
        
        
        
        for x in x_vector:
            
            lockin1.set_amplitude(x)
            qt.msleep(0.2)  
            datavalues = self.take_data(x)                                                                                                 # Go to next sweep value and take data
            data_fwd.add_data_point(x,0,0,datavalues[0],datavalues[1])                                                                     # write datapoint into datafile
                                                                                                                                            # Record data in memory
            if( datavalues[0] > threshold):
                break
                

            x1_vector.append(x)
        
        data_fwd._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
        data_fwd.close_file()
        
        qt.msleep(delay1)
        
        if (rev):
            
            x1_vector = flip(x1_vector)
            data_bck = self.create_data(x1_vector,xname,'Lockin Voltage',y_vector,'none','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
        
            for x1 in x1_vector:
            
                lockin1.set_amplitude(x1)
                qt.msleep(0.2)  
                datavalues = self.take_data(x1)                                                                                                 # Go to next sweep value and take data
                data_bck.add_data_point(x1,0,0,datavalues[0],datavalues[1])                                                                     # write datapoint into datafile
                                                                                                                                                # Record data in memory
            
        
            data_bck._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
            data_bck.close_file()
        
        
        qt.mend()
        return 1
        
    def qdac_1gate(self,channel,xname,xstart,xend,xstep,rev,threshold,compliance):
        
        qt.mstart()
        
       
        # Create sweep vectors
        if (((xstart-xend)/xstep)%2==0):
            xnum = np.int(np.ceil(np.abs(xstart-xend)/xstep+1))
        else:
            xnum = np.int(np.ceil(np.abs((xstart-xend)/xstep)))
        x_vector = np.linspace(xstart,xend,xnum)
        #x_vector = np.append(x_tempvector,[xend])
        print(x_vector)
        y_vector = [0]
        z_vector = [0]
        
        x1_vector = []
        data_fwd = self.create_data(x_vector,'gate_1','x_parameter',y_vector,'none','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
        
               
        for x in x_vector:
            
            xcurrent = qdac1.getDCVoltage(1)                                                                                        #ramp function
            ramp_steps = np.int(np.ceil(np.abs((xcurrent-x)/ramprate)+1))
            temp_ramp = np.linspace(xcurrent,x,ramp_steps)
                
            for y in temp_ramp[1:]:
                if (y > x and xcurrent < x) or (y < x and xcurrent > x):
                    qdac1.setDCVoltage(channel,x)
                    print(x)
                else:
                    qdac1.setDCVoltage(channel,y)
                    print(y)
                qt.msleep(0.05)  
                
            qdac1.setDCVoltage(channel,x)
            qt.msleep(delay2)  
            datavalues = self.take_data(x)                                                                                                 # Go to next sweep value and take data
            data_fwd.add_data_point(x,0,0,datavalues[0],datavalues[1],0,0,datavalues[4],datavalues[5],datavalues[6])                                                                     # write datapoint into datafile
                                                                                                                                            # Record data in memory
            if( datavalues[5] > threshold):
                break
            if( datavalues[1] > compliance):
                break    
            x1_vector.append(x)
        
        data_fwd._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
        data_fwd.close_file()
        
        qt.msleep(delay1)
        
        if (rev):
            
            x1_vector = flip(x1_vector)
            data_bck = self.create_data(x1_vector,xname,'Lockin Voltage',y_vector,'none','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
            print(x1_vector)
            for x1 in x1_vector:
            
                x1current = qdac1.getDCVoltage(1)
                ramp_steps1 = np.int(np.ceil(np.abs((x1current-x1)/ramprate)+1))
                temp_ramp1 = np.linspace(x1current,x1,ramp_steps1)
                for y1 in temp_ramp1[1:]:
                    if (y1 > x1 and x1current < x1) or (y1 < x1 and x1current > x1):
                        qdac1.setDCVoltage(channel,x1)
                        print(x1)
                    else:
                        qdac1.setDCVoltage(channel,y1)
                        print(y1)
                qt.msleep(0.05)  
                qdac1.setDCVoltage(channel,x1)
                qt.msleep(delay2)   
                datavalues = self.take_data(x1)                                                                                                 # Go to next sweep value and take data
                data_bck.add_data_point(x,0,0,datavalues[0],datavalues[1],0,0,datavalues[4],datavalues[5],datavalues[6])                                                                   # write datapoint into datafile
                                                                                                                                                # Record data in memory
            
        
            data_bck._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
            data_bck.close_file()
        
        
        qt.mend()
        return 1

    def qdac_2gate(self,channel,channe2,xname1,xstart1,xend1,xstep1,xname2,xstart2,xend2,xstep2,threshold,compliance):

        qt.mstart()
        
       
        # Create sweep vectors
        
        # Create x sweep vector
        if (((xstart1-xend1)/xstep1)%2==0):
            xnum1 = np.int(np.ceil(np.abs(xstart1-xend1)/xstep1+1))
        else:
            xnum1 = np.int(np.ceil(np.abs((xstart1-xend1)/xstep1)))
        x_vector1 = np.linspace(xstart1,xend1,xnum1)
        print(x_vector1)
        y_vector1 = [0]
        z_vector = [0]
        # Create x2 sweep vector
        if (((xstart2-xend2)/xstep2)%2==0):
            xnum2 = np.int(np.ceil(np.abs(xstart2-xend2)/xstep2+1))
        else:
            xnum2 = np.int(np.ceil(np.abs((xstart2-xend2)/xstep2)))
        x_vector2 = np.linspace(xstart2,xend2,xnum2)
        print(x_vector2)
        y_vector2 = [0]
        
        
        xq1_vector = []
        xq2_vector = []
        data_fwd = self.create_data(x_vector1,'gate_1','x_parameter',x_vector2,'gate_2','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
        
        
        ####
        for x1 in x_vector1:
            
            xcurrent1 = qdac1.getDCVoltage(1)                                                                                        #ramp function
            ramp_steps1 = np.int(np.ceil(np.abs((xcurrent1-x1)/ramprate)+1))
            temp_ramp1 = np.linspace(xcurrent1,x1,ramp_steps1)
                
            for y1 in temp_ramp1[1:]:
                if (y1 > x1 and xcurrent1 < x1) or (y1 < x1 and xcurrent1 > x1):
                    qdac1.setDCVoltage(channel,x1)
                    print(x1)
                else:
                    qdac1.setDCVoltage(channel,y1)
                    print(y1)
                qt.msleep(0.05)  
            print('end Y1')
            
            for x2 in x_vector2:
            
                xcurrent2 = qdac1.getDCVoltage(2)                                                                                        #ramp function
                ramp_steps2 = np.int(np.ceil(np.abs((xcurrent2-x2)/ramprate)+1))
                temp_ramp2 = np.linspace(xcurrent2,x2,ramp_steps2)
                
                for y2 in temp_ramp2[1:]:
                    if (y2 > x2 and xcurrent2 < x2) or (y2 < x2 and xcurrent2 > x2):
                        qdac1.setDCVoltage(channe2,x2)
                        print(x2)
                    else:
                        qdac1.setDCVoltage(channe2,y2)
                        print(y2)
                    qt.msleep(0.05)
                print('end Y2')
                qdac1.setDCVoltage(channe2,x2)
                qt.msleep(delay2)  
                datavalues = self.take_data(x1)                                                                                                 # Go to next sweep value and take data
                data_fwd.add_data_point(x1,x2,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6])  # write datapoint into datafile
            
                if( datavalues[3] > threshold):  # threshold on what the gate leakage is reading
                    break
                    
                    
                    
                if( datavalues[1] > compliance or datavalues[3] > compliance):
                    break
                
                
                xq2_vector.append(x2)
            print('end X2')   
            qdac1.setDCVoltage(channel,x1)
            qt.msleep(delay2)  
           
            xq1_vector.append(x1)
        
        
        print('end X1')
        data_fwd._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
        data_fwd.close_file()
        
        qt.msleep(delay1)
        
        
        
        
        ##### end

GainK1 = 1                    # Gain for Keithley 1
GainL1 = 1

# Initialization of the lockins
V_in = 100.7E-6
lockin1.set_amplitude(0.098)
R_sense = 985

#freq = 17.7
# amplitude1 = 2.0e-6  
#lockin1.set_frequency(freq)
lockin1.set_tau(9)                                      # tau = 9 equals 300 ms, check S830 driver for other integration times
lockin1.set_phase(0)
#lockin1.set_sensitivity(18)                             # current amplitude 
#lockin1.set_amplitude(0.004)  
#lockin1.set_amplitude(amplitude/(Vrange*1e-2))          # Calculates true output excitation voltage lockin

delay1 = 2.
delay2 = .3


filename = 'file_qdac1'
number_gates = 2

a = S1()

start1 = 2.e-1
end1 = 1.0e-1
xstep1 = 5e-2
start2 = 4.e-2
end2 = 2.0e-2
xstep2 = 5e-3
rev = False

threshold = 300e-2
compliance = 40e-2
ramprate = 5E-3

qt.msleep(1)

            #(self,channel,channe2,xname1,xstart1,xend1,xstep1,xname2,xstart2,xend2,xstep2,threshold,compliance):
a.qdac_2gate(1,2,'gate_1',start1,end1,xstep1,'gate_2',start2,end2,xstep2,threshold,compliance)


