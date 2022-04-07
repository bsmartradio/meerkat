#!/usr/bin/env python
# coding: utf-8

# In[90]:


from astropy.io import fits
import os
import subprocess
import shutil
import argparse
import re

#There should be a list of all of them created by auto_bane
#Currently only looking for isolated vot table, will be adjusted for all vot tables

def read_folder_list(file):

    #Read in full data cubes and the vot tables
    with open(file, "r") as f:
        folder_loc=f.read().splitlines()
    f.close() 

    return folder_loc
    
    

def find_files(location):

    dirs = os.listdir(location)
        
    return dirs


# In[91]:


def check_filenames(dirs,loc):
    
    for file in dirs:
        for chan_num in range(9):
            #("chan"+"{:02d}".format(j+1)+'.')
            if any(x in file for x in ["chan"+"{:01d}".format(chan_num+1)+'.']):
                print('File name needs to be changed for file: '+ file)
                new_filename=loc+file
                new_filename=new_filename.replace(("chan"+"{:01d}".format(chan_num+1)+'.'), ("chan"+"{:02d}".format(chan_num+1)+'.'), 1)
                os.rename(loc+file,new_filename)
                print(new_filename.replace(("chan"+"{:01d}".format(chan_num+1)+'.'), ("chan"+"{:02d}".format(chan_num+1)+'.'), 1))


#location=read_folder_list('/d/MeerKAT/folder_list.text')

#Read in file name argument.


def file_check(folder_location):

    dirs=find_files(folder_location)
    check_filenames(dirs,folder_location)

if __name__ == "__main__":
    main()






