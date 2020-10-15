from time import time, sleep
from numpy import floor
import source.qt as qt
def remainingtime(starttime, numberouterloops, counter): 
    #This function compute the amount of time remaining for 2D or 3D experiment.
    #It must be called after the end of the inner sweep loop. The time for 1 
    #complete inner loop is calculated everything and the remaining time is estimated
    #from the amount of loops remaining
    
    
    #Start time is aquired at the begining of the inner loop using 
    #    import time 
    #    starttime=time()
    #numberouterloops: number of time the inner loop sweep will occur
    #counter: how many inner loop has been perform so far   
    endtime = time()  #end time of the inner loop
    innertime = endtime - starttime #time in second to do 1 loop
    timeleft = innertime * (numberouterloops - counter)

    if timeleft <=60:  
        print("Total remaining time:",timeleft,"seconds")
    elif timeleft<=3600 and timeleft>60:    
        minutes=floor(timeleft/60)
        seconds=round(timeleft-60*minutes,2)
        print("Total remaining time:",minutes," minutes and",seconds,"seconds")
    else:    
        hours=floor(timeleft/3600)
        minutes=floor((timeleft-3600*hours)/60)
        seconds=round(timeleft-3600*hours-60*minutes,2)
        print("Total remaining time:",hours,"hours",minutes," minutes and",seconds,"seconds")
    
def start(counter):
    starttime = time()
    counter = counter + 1
    return [starttime, counter]