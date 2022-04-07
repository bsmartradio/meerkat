#!/usr/bin/env python3                                                                                                                                                                
# -*- coding: utf-8 -*-   

from astropy.io import fits
import os
import subprocess
import shutil
import argparse
import re
import channel_name_check_cluster

#This program is to read in a list of Meerkat moasaic files and split them down each plane, then get the bane files
#This program looks for seperate folders (G330, G331 etc etc) that contain only files for that particular cube and its channel files.
#It then reads in all of the channels and performs bane on each channel after checking if it has already done so.
# --folder_list : filepath to a list of all of the different cube folders.
#For this to work, I need to have this as a stand alone program where

#Read in a list of files containing all of the channels files
def read_file_lists(file_list, table_list):

    with open(file_list, "r") as f:
        fits_files=f.read().splitlines()
    f.close() 

    return fits_files

#This is a check to make sure any other files in the folder that aren't channels don't get included. Also helps check if you have already
#run bane on this particular folder.
def channel_list(fileslist):
    channels_list=[]
    bkg_list=[]
    k=0
    for i in fileslist:
        if 'chan' in i and 'bkg' not in i and 'rms' not in i  and 'list' not in i:
            channels_list.append(i)
        if 'bkg' in i :
            bkg_list.append(i)
    return channels_list, bkg_list

#Reads in a single mosaic name then splits it into its respective level
def run_bane(location, file):
    print(f'File location {location+file}')
    cmd = ['BANE',location+file]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait()
    return 

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1  

#Read in file name argument.
parser = argparse.ArgumentParser(description='Must give folder name')
parser.add_argument("--input_folder")

args = parser.parse_args()

if args.input_folder  == None :
    print("Must have folder name'")
    exit()
files = args.input_folder

location=files.strip()
print(location)
channel_name_check_cluster.file_check(location)

last_char_index = location[:-1].rfind("/")
name=location[last_char_index+1:-1]
print(last_char_index)
print(name +'here is name')
print(location)
fileslist = os.listdir(location.strip())
c_list, b_list=channel_list(fileslist)

#Writes a list of all of the channel files which can be used in other programs
if os.path.isfile(location+name+'_missing_backgrounds_list.txt'):
    c_list=[]
    print('Reading existing channel file.')
    with open(location+name+'_channels_list.txt', 'r') as filehandle:
            c_list=filehandle.read().splitlines() 
else:
    print('Writing new channels file.')
    with open(location+name+'_channels_list.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in c_list)
#Writes a list of all of the backgrounds created files which can be used in other programs
print(c_list)
print(len(c_list))
print(len(b_list))

#checks if bane has already been run on the subfolder
if len(c_list) == len(b_list) :
    print('Bane has already been run on all channels for' + location)
#If bane has been run on some but not all, warns you.
elif len(b_list) > 0 :
    print('Bane has already been run on some channels. Re-running Bane')
    for i in c_list:
        run_bane(location,i)
        print("Testing run")
#Runs bane if there is no existing background files
else:
    for i in c_list:
        run_bane(location,i)
        print("Testing run")

dirs=os.listdir(location)   
with open(location+name+'_background_list.txt', 'w') as filehandle:
    for i in dirs:
        if 'bkg.fits' in i  :        
            filehandle.writelines(i+'\n')
            print(i+' written to background list.')

            
print('Checking that all channels have a background')

if os.path.isfile(location+name+'_missing_background_list.txt'):
    print('Channels missing background files have already been moved into ' + location+name+'_missing_background_list.txt')
else:
    s = b_list
    full_list=listToString(s)
    missing=[]
    print(i)
    print(c_list)
    for i in b_list:
        channel=str(re.findall(r'\_c.*?\.', i))
        channel=channel[3:-3]
        if channel in full_list:
            print('Channel '+ channel + ' has background')
            
        else:
            print('Channel '+ channel + ' does not have background. Channel removed from list')
            with open(location+name+'_channels_list.txt', 'r') as f:
                lines = f.readlines()
            with open(location+name+'_channels_list.txt', 'w') as f:
                for line in lines:
                    if line.strip("\n") != i:
                        f.write(line)
            with open(location+name+'_missing_background_list.txt', 'w') as f:
                missing.append(i)

    if len(missing) > 0:
        print('There are ' + str(len(missing)) + ' missing background files')
        with open(location+name+'_missing_background_list.txt', 'w') as f:
            for k in missing:
                f.write(k)


