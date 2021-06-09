from Scripts.gate_sweep import INTRASWEEP_DELAY
from numpy import pi, random, arange, size, array, sin, cos, linspace, sinc, sqrt, flip
from time import time, sleep
from shutil import copyfile
from os import mkdir
from os.path import exists
from datetime import datetime

import math
import qt
#import timetrack
import sys
sys.path.append('C:\\Users\\physics-svc-laroche\\Desktop\\qtlab3\\Scripts\\modules')

import numpy as np
import data as d
import traces
import shutil
import os
import numpy
currenttime = time()


##### Declare no of LI'S
numlock = 2
######


keithley1 = qt.instruments.get('keithley1')

qdac1 = qt.instruments.get('qdac1')
magnet = qt.instruments.get('magnet')
lockin1 = qt.instruments.get('lockin1')

if numlock == 2:
    lockin2 = qt.instruments.get('lockin2')
    
class S1():
    
    def __init__(self): 
        self.filename = filename
        self.generator = d.IncrementalGenerator(qt.config['datadir'] + '\\' + self.filename, 1)
    
    
    # Function generates data file, spyview file and copies the python script.
    def create_data(self, x_vector, x_coordinate, x_parameter, y_vector, y_coordinate, y_parameter, z_vector, z_coordinate, z_parameter):
        qt.Data.set_filename_generator(self.generator)
        data = qt.Data(name=self.filename)
        data.add_coordinate(x_parameter + ' (' + x_coordinate + ')',
                            size=len(x_vector),
                            start=x_vector[0],
                            end=x_vector[-1]) 
        data.add_coordinate(y_parameter + ' (' + y_coordinate + ')',
                            size=len(y_vector),
                            start=y_vector[0],
                            end=y_vector[-1]) 
        data.add_coordinate(z_parameter + ' (' + z_coordinate + ')',
                            size=len(z_vector),
                            start=z_vector[0],
                            end=z_vector[-1])
                            

        # Gate 1
        data.add_value('Gate 1 V meas')
        data.add_value('Gate 1 leak')
        
        # Gate 2
        data.add_value('Gate 2 V meas')
        data.add_value('Gate 2 leak')
        
        # Gate 3
        data.add_value('Gate 3 V meas')
        data.add_value('Gate 3 leak')
        
        # Gate 4
        data.add_value('Gate 4 V meas')
        data.add_value('Gate 4 leak')
        
        # Gate 5
        data.add_value('Gate 5 V meas')
        data.add_value('Gate 5 leak')
        
        # keithley 1
        data.add_value('keithley 1 V meas')
        data.add_value('keithley 1 leak')
        
        # Lockin 1
        data.add_value('Lockin 1 X raw')
        data.add_value('Lockin 1 X pros')
        data.add_value('Lockin 1 Y raw')
        
        # Lockin 2
        data.add_value('Lockin 2 X raw')
        data.add_value('Lockin 2 X pros')
        data.add_value('Lockin 2 Y raw')
        
        #Magnet_Z
        data.add_value('Magnet_Z')
        
        #Time
        data.add_value('Time')
                                                  
        data.create_file()    
        traces.copy_script(sys._getframe().f_code.co_filename, data._dir, self.filename + '_' + str(self.generator._counter - 1))           # Copy the python script into the data folder
        return data
        
        
    def take_data(self, x):
                #qt.msleep(delay2)
                #K1 = keithley1.get_readnextval()                                     # Read out Keithley1            
                #K1_value = K1/GainK1                                                 # Use explained at bottom of the script
                
                L1_X = lockin1.get_X()
                L1_X_pro = (V_in - L1_X) / (1e-9 if L1_X == 0.0 else L1_X) * R_sense 
                L1_Y = lockin1.get_Y()
                
                gate_1 = qdac1.getDCVoltage(1)
                gate_2 = qdac1.getDCVoltage(2)
                gate_3 = qdac1.getDCVoltage(3)
                gate_4 = qdac1.getDCVoltage(4)                
                gate_5 = qdac1.getDCVoltage(5)
                gate_6 = keithley1.get_voltage()               
                
                leak_1 = qdac1.getCurrentReading(1)
                leak_2 = qdac1.getCurrentReading(2)
                leak_3 = qdac1.getCurrentReading(3)
                leak_4 = qdac1.getCurrentReading(4)
                leak_5 = qdac1.getCurrentReading(5)
                leak_6 = keithley1.get_current()
                
                #Magnet_Z = magnet.get_fieldZ()
                Magnet_Z = 0 
                Time = time() - currenttime

                if numlock == 1:
                    datavalues = [gate_1, leak_1, gate_2, leak_2, gate_3,
                                  leak_3, gate_4, leak_4, gate_5, leak_5,
                                  gate_6, leak_6, L1_X, L1_X_pro, L1_Y, 0, 0,
                                  0, Magnet_Z, Time]
                elif numlock == 2:
                    L2_X = lockin2.get_data_param(0)
                    L2_X_pro = (V_in - L2_X) / (1e-9 if L2_X == 0.0 else L2_X) * R_sense
                    L2_Y = lockin2.get_data_param(1)
                    
                    datavalues = [gate_1, leak_1, gate_2, leak_2, gate_3,
                                  leak_3, gate_4, leak_4, gate_5, leak_5,
                                  gate_6, leak_6, L1_X, L1_X_pro, L1_Y, L2_X,
                                  L2_X_pro, L2_Y, Magnet_Z, Time]
                     
                return datavalues
        
    def take_data_quick(self,datavalues):
            #qt.msleep(delay2)
            #K1 = keithley1.get_readnextval()                                     # Read out Keithley1            
            #K1_value = K1/GainK1                                                 # Use explained at bottom of the script
            if DMM==False :
                L1_X = lockin1.get_X()
                L1_X_pro = (V_in - L1_X) / (1e-9 if L1_X == 0.0 else L1_X) * R_sense
                L1_Y = lockin1.get_Y()
            
            elif DMM==True : 
                L1_X = DMM1.readnext() / 10 * LIsens
                L1_X_pro = (V_in - L1_X) / (1e-9 if L1_X == 0.0 else L1_X) * R_sense
                L1_Y = DMM2.readnext() / 10 * LIsens  
            
            gate_1 = qdac1.getDCVoltage(1)
            
            leak_1 = qdac1.getCurrentReading(1)
            '''
            gate_1 = qdac1.getDCVoltage(1)
            gate_2 = qdac1.getDCVoltage(2)
            gate_3 = qdac1.getDCVoltage(3)
            gate_4 = qdac1.getDCVoltage(4)                
            gate_5 = qdac1.getDCVoltage(5)
            gate_6 = qdac1.getDCVoltage(6)                
                            
            leak_1 = qdac1.getCurrentReading(1)
            leak_2 = qdac1.getCurrentReading(2)
            leak_3 = qdac1.getCurrentReading(3)
            leak_4 = qdac1.getCurrentReading(4)
            leak_5 = qdac1.getCurrentReading(5)
            leak_6 = qdac1.getCurrentReading(6)
            '''
            
            #Magnet_Z = magnet.get_fieldZ()
            Magnet_Z = 0 
            
            Time = time()-currenttime

            if numlock == 1:
                datavalues = [datavalues[0], datavalues[1], datavalues[2],
                              datavalues[3], datavalues[4], datavalues[5],
                              datavalues[6], datavalues[7], datavalues[8],
                              datavalues[9], datavalues[10], datavalues[11],
                              L1_X, L1_X_pro, L1_Y, 0, 0, 0, Magnet_Z, Time]
            elif numlock ==2:
                L2_X = lockin2.get_X()
                L2_X_pro = (V_in - L2_X) / (1e-9 if L2_X == 0.0 else L2_X) * R_sense
                L2_Y = lockin2.get_Y()
                    
                datavalues = [datavalues[0], datavalues[1], datavalues[2],
                              datavalues[3], datavalues[4], datavalues[5],
                              datavalues[6], datavalues[7], datavalues[8],
                              datavalues[9], datavalues[10], datavalues[11],
                              L1_X, L1_X_pro, L1_Y, L2_X, L2_X_pro, L2_Y, Magnet_Z, Time]

            return datavalues


    
    
    def volt_sweep(self, xname, xstart, xend, xstep, rev, threshold): # pass in lockins with type-checking
        qt.mstart()
       
        # Create sweep vectors
        x_vector = arange(xstart, xend, xstep)
        y_vector = [0]
        z_vector = [0]
        
        x1_vector = []
        
        data_fwd = self.create_data(x_vector, xname, 'Lockin Voltage',
                                    y_vector, 'none', 'y_parameter', z_vector,
                                    'none', 'z_parameter')

        for x in x_vector:
            lockin1.set_amplitude(x)
            qt.msleep(0.2)  
            
            datavalues = self.take_data(x) # Go to next sweep value and take data
            
            data_fwd.add_data_point(x, 0, 0, datavalues[0], datavalues[1]) # write datapoint into datafile
                                                                                                      # Record data in memory
            if datavalues[0] > threshold:
                break

            x1_vector.append(x)
        data_fwd._write_settings_file() # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
        data_fwd.close_file()
        
        qt.msleep(delay1)
        
        if rev:
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
        #print(x_vector)
        y_vector = [0]
        z_vector = [0]
        
        x1_vector = []
        data_fwd = self.create_data(x_vector,xname,'x_parameter',y_vector,'none','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
        
               
        for x in x_vector:
            
            if(x==x_vector[1]):
                print('Scan has started')
            
            xcurrent = qdac1.getDCVoltage(channel)                                                                                        #ramp function
            ramp_steps = np.int(np.ceil(np.abs((xcurrent-x)/ramprate)+1))
            temp_ramp = np.linspace(xcurrent,x,ramp_steps)
                
            for y in temp_ramp[1:]:
                if (y > x and xcurrent < x) or (y < x and xcurrent > x):
                    qdac1.rampDCVoltage(channel,x)
                    #print(x)
                    
                else:
                    qdac1.rampDCVoltage(channel,y)
                    #print(y)
                qt.msleep(0.05)  
                
            qdac1.rampDCVoltage(channel,x)
            qt.msleep(delay2)  
            datavalues = self.take_data(x)                                                                                                 # Go to next sweep value and take data
            #datavalues = [gate_1,leak_1,gate_2,leak_2,gate_3,leak_3,gate_4,leak_4,gate_5,leak_5,gate_6,leak_6,L1_X,L1_X_pro,L1_Y,Magnet_Z]
            data_fwd.add_data_point(x,0,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],datavalues[12],datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])                                                                     # write datapoint into datafile
                                                                                                                                            # Record data in memory
            if threshold is not None : 
                if( datavalues[13] > threshold):
                    break
            if( datavalues[2*channel-1] > compliance):
                break    
            x1_vector.append(x)
        
        data_fwd._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
        data_fwd.close_file()
        
        qt.msleep(delay1)
        
        if (rev):
            
            x1_vector = flip(x1_vector)
            data_bck = self.create_data(x1_vector,xname,'Lockin Voltage',y_vector,'none','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
            print('reverse scan started')
            for x1 in x1_vector:
            
                x1current = qdac1.getDCVoltage(channel)
                ramp_steps1 = np.int(np.ceil(np.abs((x1current-x1)/ramprate)+1))
                temp_ramp1 = np.linspace(x1current,x1,ramp_steps1)
                for y1 in temp_ramp1[1:]:
                    if (y1 > x1 and x1current < x1) or (y1 < x1 and x1current > x1):
                        qdac1.rampDCVoltage(channel,x1)
                        #print(x1)
                    else:
                        qdac1.rampDCVoltage(channel,y1)
                        #print(y1)
                qt.msleep(0.05)  
                qdac1.rampDCVoltage(channel,x1)
                qt.msleep(delay2)   
                datavalues = self.take_data(x1)                                                                                                 # Go to next sweep value and take data
                data_bck.add_data_point(x,0,0,datavalues[0],datavalues[1],0,0,datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],datavalues[12],datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])                                                                   # write datapoint into datafile
                                                                                                                                                # Record data in memory
            
        
            data_bck._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
            data_bck.close_file()
        
        
        qt.mend()
        return 1

    def qdac_2gate(self,channel,channel2,xname1,xstart1,xend1,xstep1,xname2,xstart2,xend2,xstep2,threshold,compliance):

        qt.mstart()
        
       
        # Create sweep vectors
        
        # Create x sweep vector
        if (((xstart1-xend1)/xstep1)%2==0):
            xnum1 = np.int(np.ceil(np.abs((xstart1-xend1)/xstep1)+1))
            #xnum1 = np.int(np.ceil(np.abs(xstart1-xend1)/xstep1+1))
        else:
            xnum1 = np.int(np.ceil(np.abs((xstart1-xend1)/xstep1)))
            #xnum1 = np.int(np.ceil(np.abs((xstart1-xend1)/xstep1)))
        x_vector1 = np.linspace(xstart1,xend1,xnum1)
        
        
        y_vector1 = [0]
        z_vector = [0]
        # Create x2 sweep vector
        if (((xstart2-xend2)/xstep2)%2==0):
            xnum2 = np.int(np.ceil(np.abs((xstart2-xend2)/xstep2)+1))
            #xnum2 = np.int(np.ceil(np.abs(xstart2-xend2)/xstep2+1))
        else:
            xnum2 = np.int(np.ceil(np.abs((xstart2-xend2)/xstep2)))
            #xnum2 = np.int(np.ceil(np.abs((xstart2-xend2)/xstep2)))
        x_vector2 = np.linspace(xstart2,xend2,xnum2)
       
        y_vector2 = [0]
        
        
        xq1_vector = []
        xq2_vector = []
        data_fwd = self.create_data(x_vector1,'gate_1','x_parameter',x_vector2,'gate_2','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
        
        
        for x1 in x_vector1:
            
            xcurrent1 = qdac1.getDCVoltage(channel)                                                                                        #ramp function
            ramp_steps1 = np.int(np.ceil(np.abs((xcurrent1-x1)/ramprate)+1))
            temp_ramp1 = np.linspace(xcurrent1,x1,ramp_steps1)
                
            for y1 in temp_ramp1[1:]:
                if (y1 > x1 and xcurrent1 < x1) or (y1 < x1 and xcurrent1 > x1):
                    qdac1.rampDCVoltage(channel,x1)
                    
                else:
                    qdac1.rampDCVoltage(channel,y1)
                    
                qt.msleep(0.05)  
           
            
            for x2 in x_vector2:
            
                xcurrent2 = qdac1.getDCVoltage(channel2)                                                                                        #ramp function
                ramp_steps2 = np.int(np.ceil(np.abs((xcurrent2-x2)/ramprate)+1))
                temp_ramp2 = np.linspace(xcurrent2,x2,ramp_steps2)
                
                '''for y2 in temp_ramp2[1:]:
                    if (y2 > x2 and xcurrent2 < x2) or (y2 < x2 and xcurrent2 > x2):
                        qdac1.rampDCVoltage(channel2,x2)
                        
                    else:
                        qdac1.rampDCVoltage(channel2,y2)
                       
                    qt.msleep(0.05)'''
               
                qdac1.rampDCVoltage(channel2,x2)
                qt.msleep(delay2)  
                datavalues = self.take_data(x1)                                                                                                 # Go to next sweep value and take data
                
                if( datavalues[1] > compliance or datavalues[3] > compliance): #want to break

                    print('I am broken')
                    break
                    
                    
                if( datavalues[5] > threshold):  # threshold on what the gate leakage is reading and fill with zeros after
                
                #if( qdac1.getDCVoltage(1) > 1):  test function
                    
                    data_fwd.add_data_point(x1,x2,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],np.nan,datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])  # write datapoint into datafile
                    
                    print('I shall continue')
                    continue
                
                    
                else:
                
                    data_fwd.add_data_point(x1,x2,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],datavalues[12],datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])  # write datapoint into datafile
                    print('I am awesome')
                    
                xq2_vector.append(x2)
            print('end X2')   
            qdac1.rampDCVoltage(channel,x1)
            qt.msleep(delay2)  
           
            xq1_vector.append(x1)
        
        
        print('end X1')
        data_fwd._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
        data_fwd.close_file()
        
        qt.msleep(delay1)


    def tunnelcond(self,channel,channel2,xname1,xstart1,xend1,xstep1,xname2,xstart2,xend2,xstep2):

        qt.mstart()
        
       
        # Create sweep vectors
        
        # Create x sweep vector
        if (((xstart1-xend1)/xstep1)%2==0):
            xnum1 = np.int(np.ceil(np.abs((xstart1-xend1)/xstep1)+1))
            #xnum1 = np.int(np.ceil(np.abs(xstart1-xend1)/xstep1+1))
        else:
            xnum1 = np.int(np.ceil(np.abs((xstart1-xend1)/xstep1)))
            #xnum1 = np.int(np.ceil(np.abs((xstart1-xend1)/xstep1)))
        x_vector1 = np.linspace(xstart1,xend1,xnum1)
        
        
        y_vector1 = [0]
        z_vector = [0]
        # Create x2 sweep vector
        if (((xstart2-xend2)/xstep2)%2==0):
            xnum2 = np.int(np.ceil(np.abs((xstart2-xend2)/xstep2)+1))
            #xnum2 = np.int(np.ceil(np.abs(xstart2-xend2)/xstep2+1))
        else:
            xnum2 = np.int(np.ceil(np.abs((xstart2-xend2)/xstep2)))
            #xnum2 = np.int(np.ceil(np.abs((xstart2-xend2)/xstep2)))
        x_vector2 = np.linspace(xstart2,xend2,xnum2)
       
        y_vector2 = [0]
        
        
        xq1_vector = []
        xq2_vector = []
        data_fwd = self.create_data(x_vector1,'gate_1','x_parameter',x_vector2,'gate_2','y_parameter',z_vector,'none','z_parameter')                                # create data file, copy script
        
        
        for x1 in x_vector1:
            
            xcurrent1 = qdac1.getDCVoltage(channel)                                                                                        #ramp function
            ramp_steps1 = np.int(np.ceil(np.abs((xcurrent1-x1)/ramprate)+1))
            temp_ramp1 = np.linspace(xcurrent1,x1,ramp_steps1)
                
            '''for y1 in temp_ramp1[1:]:
                if (y1 > x1 and xcurrent1 < x1) or (y1 < x1 and xcurrent1 > x1):
                    qdac1.rampDCVoltage(channel,x1)
                    
                else:
                    qdac1.rampDCVoltage(channel,y1)
                    
                qt.msleep(0.05)  '''
            qdac1.rampDCVoltage(channel,x1)
            
            for x2 in x_vector2:
            
                xcurrent2 = keithley1.get_current()                                                                                        #ramp function
                ramp_steps2 = np.int(np.ceil(np.abs((xcurrent2-x2)/ramprate)+1))
                temp_ramp2 = np.linspace(xcurrent2,x2,ramp_steps2)
                
                '''for y2 in temp_ramp2[1:]:
                    if (y2 > x2 and xcurrent2 < x2) or (y2 < x2 and xcurrent2 > x2):
                        keithley1.keithley_gateset(1,x2)
                        #qdac1.rampDCVoltage(channel2,x2)
                        
                    else:
                        keithley1.keithley_gateset(1,y2)
                        #qdac1.rampDCVoltage(channel2,y2)
                       
                    qt.msleep(0.05)'''
               
                a.keithley_gateset(channel2,x2)
                #qdac1.rampDCVoltage(channel2,x2)
                
                qt.msleep(delay2)  
                datavalues = self.take_data(x1)                                                                                                 # Go to next sweep value and take data
                
                
                data_fwd.add_data_point(x1,x2,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],datavalues[12],datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])  # write datapoint into datafile    
                xq2_vector.append(x2)
            print('end X2')   
           
            qt.msleep(delay2)  
           
            xq1_vector.append(x1)
        
        
        print('end X1')
        data_fwd._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
        data_fwd.close_file()
        
        qt.msleep(delay1)


        
    def qdac_gateset(self,channel,xend):
        xcurrent = qdac1.getDCVoltage(channel)                                                                                        #ramp function
        ramp_steps = np.int(np.ceil(np.abs((xcurrent-xend)/ramprate)+1))
        temp_ramp = np.linspace(xcurrent,xend,ramp_steps)
        #print(temp_ramp)    
        for y in temp_ramp[1:]:
            if (y > xend and xcurrent < xend) or (y < xend and xcurrent > xend):
                qdac1.rampDCVoltage(channel,xend)
                #print(x)
            else:
                qdac1.rampDCVoltage(channel,y)
                #print(y)
            qt.msleep(0.05)  
            
        qdac1.rampDCVoltage(channel,xend)
        qt.msleep(delay2)    
    
    
    def Magnet_sweep(self,B_end,channel,V_Gate,delay,Bramp):
        #Bramp is ramp rate in T/min
        magnet.set_rampRateZ(Bramp)
        
        # check whether we are setting the gate voltage with the keithley or qdac
        if (keithon==1):
            keithley1.set_voltage(V_Gate)
        
        elif (keithon==0):
            qdac1.rampDCVoltage(channel,V_Gate)
        
        #qt.msleep(INTRASWEEP_DELAY)

        B_now = magnet.get_fieldZ()
        bstep1 = np.int(np.abs((B_end-B_now))/Bramp*60/delay)+5
        x = np.linspace(B_now,B_end,bstep1)
        print('ramping started')
        data_mag = self.create_data(x,'magnetic_field','x_parameter',[0],'none','y_parameter',[0],'none','z_parameter')
        datavalues = self.take_data(x[0])
        data_mag.add_data_point(x[0],0,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],datavalues[12],datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])
        magnet.rampToZ(B_end)
        isramping = True
        counter=1
        print('Start Bnow is:' , B_now , 'and Bend is:', B_end)
        
        while (isramping):
            val=x[counter]
            #print('Bnow is:' , B_now , 'and Bend is:', B_end)
            datavalues = self.take_data_quick(datavalues)
            data_mag.add_data_point(val,0,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],datavalues[12],datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])
            B_now = magnet.get_fieldZ()
            counter = counter + 1
            qt.msleep(delay)
            if magnet.get_rampStateZ() == 2 or magnet.get_rampStateZ() == 3:
                isramping = False
        datavalues = self.take_data(x[counter])        
        data_mag.add_data_point(B_end,0,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],datavalues[12],datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])        
        print('ramp ended')
        ##### end
        
    def keithley_gateset(self,num,xend):
        if num==1 :
            xcurrent = keithley1.get_voltage()
            ramp_steps = np.int(np.ceil(np.abs((xcurrent-xend)/ramprate)+1))
            temp_ramp = np.linspace(xcurrent,xend,ramp_steps)
            #print(temp_ramp)    
            for y in temp_ramp[1:]:
                if (y > xend and xcurrent < xend) or (y < xend and xcurrent > xend):
                    keithley1.set_voltage(xend)
                    #print(x)
                else:
                    keithley1.set_voltage(y)
                    #print(y)
                qt.msleep(0.05)  
                
            keithley1.set_voltage(xend)
            
        qt.msleep(delay2)     
        
        
    def record(self,voltage, time0, timestep):
        
        
        qt.mstart()
        
       
        # Create sweep vectors
        x_vector = np.arange(0,time0,timestep)
        y_vector = [0]
        z_vector = [0]
        
        vals = []
        
        
        data = self.create_data(x_vector,'time','x_parameter',y_vector,'none','y_parameter',z_vector,'none','z_parameter')
        
        datavalues = self.take_data(x_vector[0])
        
        if (keithon==1):
            keithley1.set_voltage(V_Gate)
        
        elif (keithon==0):
            qdac1.rampDCVoltage(channel,V_Gate)
        
        
        qt.msleep(delay1)
        
       
        
        t = 0
        t_offset = time()
        
        while(t<time0):
            tval = time()
            datavalues = self.take_data_quick(datavalues)                                                                                                 
            data.add_data_point(t,0,0,datavalues[0],datavalues[1],datavalues[2],datavalues[3],datavalues[4],datavalues[5],datavalues[6],datavalues[7],datavalues[8],datavalues[9],datavalues[10],datavalues[11],datavalues[12],datavalues[13],datavalues[14],datavalues[15],datavalues[16],datavalues[17],datavalues[18])
            qt.msleep(timestep)
            t = t+timestep
            
            vals.append(datavalues[2])
            
            
        data._write_settings_file()                                                                                                             # Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
        data.close_file()    
    qt.mend()






GainK1 = 1                    # Gain for Keithley 1
GainL1 = 1

# Initialization of the lockins
V_in = 100E-6
#lockin1.set_amplitude(0.098)
R_sense = 992

if DMM ==False : 
    #freq = 17.7
    # amplitude1 = 2.0e-6  
    #lockin1.set_frequency(freq)
    lockin1.set_tau(9)                                      # tau = 9 equals 300 ms, check S830 driver for other integration times
    lockin1.set_phase(0)
    #lockin1.set_sensitivity(18)                             # current amplitude 
    #lockin1.set_amplitude(0.004)  
    #lockin1.set_amplitude(amplitude/(Vrange*1e-2))          # Calculates true output excitation voltage lockin

delay1 = 0.2
delay2 = 0.075


filename = 'VA182B'
number_gates = 1

a = S1()

#parameters for gate scan

start1 = -2.7
end1 = 0
xstep1 = 5E-3
start2 = -12e-3
end2 = 12e-3
xstep2 = 1e-4
rev = False

threshold = None
compliance = 100E-6
ramprate = 5E-3

keithon=1
delay = 1
tstop = 100000


###########

import source.qt as qt
import Scripts.modules.hbar as hbar

