import argparse
import glob
from astropy.io import fits
from astropy.io.votable import parse
from astropy.wcs import WCS 
import os
import numpy as np

# This module contains a number of short functions that are used across
# a number of MeerKAT processes. Many of them assume a standard
# file structure and MeerKAT data labeling.

def get_name(location):
    if location[-1] == '/':
        last_char_index = location[:-1].rfind("/")
        name=location[last_char_index+1:-1]
    elif location[-1] == 't':
        last_char_index = location[:-1].rfind("/")
        mid_char_index = location[:-last_char_index].rfind("/")
        name=location[mid_char_index+1:last_char_index]
    else:
        last_char_index = location[:-1].rfind("/")
        name=location[last_char_index+1:]
    return name

def get_list(location):
    folder_list=sorted(glob.glob(location+"G[0-9][0-9][0-9]*"))
    return folder_list

def read_info(single_vot):
    
    votable = parse(single_vot)
    table = votable.get_first_table()
    data = table.array
    
    return data

def get_image(image_name):
    fits_file = fits.open(image_name)
    image_data = fits_file[0].data
    hdr=fits_file[0].header
    fits_file.close()
    
    return image_data,hdr

def unify_coords(table,w):
    #This gets the world coordinate system and also translate the table values to pixel values
    lon=table.array['lon'].data
    lat=table.array['lat'].data
    t=0
    test_arr=[]
    for x in lon:
        test=np.array([lon[t], lat[t]], np.float_)
        test_arr.append(test)               
        t=t+1
    positions=w.wcs_world2pix(test_arr, 2)
    
    return positions

def minmax_coord(header):
    
    w = WCS(header)
    min_lon= w.pixel_to_world(7500, 7500)
    max_lon= w.pixel_to_world(0, 0)

    return min_lon.l.degree,max_lon.l.degree

def check_filenames(channels,location):

    for single_channel in channels:
        for chan_num in range(9):
            if any(x in single_channel for x in ["chan"+"{:01d}".format(chan_num+1)+'.']):
                print('File name needs to be changed for file: '+ single_channel)
                new_filename=location+single_channel
                new_filename=new_filename.replace(("chan"+"{:01d}".format(chan_num+1)+'.'), ("chan"+"{:02d}".format(chan_num+1)+'.'), 1)
                os.rename(location+single_channel,new_filename)
                print(new_filename.replace(("chan"+"{:01d}".format(chan_num+1)+'.'), ("chan"+"{:02d}".format(chan_num+1)+'.'), 1))

def find_files(location):

    channels = os.listdir(location)
        
    return channels

def file_check(location):

    channels=find_files(location)
    check_filenames(channels,location)
    print(f"Channel name check has been run for cube {location}")
