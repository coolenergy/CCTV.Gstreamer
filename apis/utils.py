import glob
import os
import time

def remove_less_1000(dir_name, max, delta):
    print(dir_name)
    i = 0
    list_of_files = filter( os.path.isfile,
                            glob.glob(dir_name + '*') )
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted( list_of_files,
                            key = os.path.getmtime)
    print(list_of_files)
    # Iterate over sorted list of files and print file path 
    # along with last modification time of file 
    if(len(list_of_files) < (max + delta)):
        return
    for file_path in list_of_files:
        if(i == max):
            break
        os.remove(file_path)
        i+=1