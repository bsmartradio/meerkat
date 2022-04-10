from astropy.io import fits
import os
import subprocess
import shutil
import argparse
import re

# There should be a list of all files created by auto_bane
# The current state of the progrm requires ordered files, so this changes the naming convention
# Currently only looking for isolated vot table, will be adjusted for all vot tables

def read_folder_list(file):

    #Read in full data cubes and the vot tables
    with open(file, "r") as f:
        folder_loc=f.read().splitlines()
    f.close() 

    return folder_loc


def find_files(location):

    #Read in full data cube and the vot table
    dirs = os.listdir(location)
        
    return dirs


def check_filenames(dirs, loc):
    
    for file in dirs:
        for chan_num in range(9):
            if any(x in file for x in ["chan"+"{:01d}".format(chan_num+1)+'.']):
                print('File name needs to be changed for file: '+ file)
                new_filename=loc+file
                new_filename=new_filename.replace(("chan"+"{:01d}".format(chan_num+1)+'.'), ("chan"+"{:02d}".format(chan_num+1)+'.'), 1)
                os.rename(loc+file,new_filename)
                print(new_filename.replace(("chan"+"{:01d}".format(chan_num+1)+'.'), ("chan"+"{:02d}".format(chan_num+1)+'.'), 1))


def file_check(folder_list):

    location = open(folder_list, "r")

    for x in location:
        dirs=find_files(x.strip())
        check_filenames(dirs,x.strip())
        print(f"Channel name check has been run for cube {x}")


if __name__ == "__main__":
    main()






