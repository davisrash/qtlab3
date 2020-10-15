import os
import time
from time import sleep
from shutil import copyfile
# Usage:
# import getlatest
#
# Reloading:
# reload(getlatest)
import qt

def getlatest(path='W:\\'): # The path where the \\lecroy\Documents folder is mapped to
    '''
    This script checks the path W:\ for the latest updated file.
    Input:
        path (str) : Path where the script has to look (default: 'W:\\')
    Output:
        (prints Date/time modified (Y-m-d H:M), this is for debugging)
        filename(str) : Filename
    '''
    li = get_list(path)

    # From this list, pick the biggest value and get the time modified and filename.
    modifiedtime = li[-1:][0][0]
    filename = li[-1:][0][1]

    # Convert the seconds into Y-m-d H:M and print, and print filename
    timestamp = time.strftime('%Y-%m-%d %H:%M', time.localtime(modifiedtime))
    result = [path + filename, timestamp]
    return result

def get_list(path='W:\\'):
    seconds = {} # initialize seconds dictionary
    # Loop over all files in the directory
    for filename in os.listdir(path):
        #Ignore subfolders
        if os.path.isdir(os.path.join(path,filename)):
            continue
        # Get the modified time of the file
        seconds[filename] = os.path.getmtime(path + filename)
    # Get a list of tuples, with time modified (in seconds) in 1st position,
    # filename in 2nd
    li = [(t, f) for f, t in seconds.items()]
    # Sort the list
    li.sort()
    return li

def get_timestamp(path='W:\\'):
    '''
    Returns the timestamp of the latest modified file
    Input:
        path (str) : Path where the script has to look (default: 'W:\\')
    Output:
        timestamp (str) : Timestamp in Y-m-d H:M
    '''
    result = getlatest(path)
    return result[1]

def get_filename(path='W:\\'):
    '''
    Returns the filename of the latest modified file
    Input:
    
        path (str) : Path where the script has to look (default: 'W:\\')
    Output:
        filename(str) : Filename
    '''
    result = getlatest(path)
    return result[0]

def get_filenames(path='D:\\qtlab\\scripts\\meas_stack\\'):
    # Get the directory listing
    li = get_list(path)
    # Turn around the tuple; (filename, time) instead of (time, filename)
    filenames = [(f) for t,f in li]
    # Sort by filename
    filenames.sort()
    return filenames

def execute_stack(path='D:\\qtlab\\scripts\\meas_stack\\'):
    '''
    Executes all files in a specific folder according to filename
    '''
    changed = True
    filenames = get_filenames(path)
    filenames_done = []
    while changed == True:
        try:
            changed = False
            for filename in filenames:
                if filenames_done.__contains__(filename) == False:
                    print('Now executing ' + filename + '...')
                    # Execute file
                    execfile(path + filename)
                    # Add the filename to the filenames_done list
                    filenames_done.append(filename)
                    # Check if the directory listing has changed
                    filenames_new = get_filenames(path)
                    if filenames.__eq__(filenames_new) == False:
                        # The directory listing has changed
                        filenames = filenames_new
                        changed = True
                        break
        except Exception as e:
            print('An exception occured:')
            print(e)
            break
    if filenames_done.__len__() != 0:
        print('QTLab has executed the following measurement scripts:')
        for filename in filenames_done:
            print(filename)
def execute_file(filename, data_dir, scripts_folder='D:\\qtlab\\scripts\\meas_stack'):
    '''
    Run the current script and proceed running all the files in the measurement stack folder.
    Make a copy of the current running script to the measurement stack folder.
    Usage: qttools.copy_script(sys._getframe().f_code.co_filename,data._dir)
    
    Input:
        filename(str): Filename of the script
        data_dir(str): Data directory of the script
    Output:
        None
    '''
    name = '10_%s' %filename
    copyfile("%s" % filename, "%s\\%s" % (data_dir, name))

def copy_temp(name,copypath, path):
    name = name[0:-4]
    copyfile(copypath,("%s\\%s" % (path, name)))
