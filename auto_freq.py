import os
import numpy as np
import glob
from astropy.io import fits
import argparse

def get_chan_list(location):
    channel_list=glob.glob(location+"*[0-9].fits")
    return channel_list

def make_chan_list(channel_list,location):
    num_dim=14
    freq_list=np.full([num_dim], float('Nan'))   
    for j in range(num_dim):       
        number_str = str(j+1)
        freq_num='FREQ00'+ number_str.zfill(2)
        hdul = fits.open(channel_list[j])
        freq_list[j]= hdul[0].header['OBSFREQ']
        
    np.save(location+'freq_list', freq_list, allow_pickle=True, fix_imports=True)
    

    
#Read in file name argument.
parser = argparse.ArgumentParser(description='Must have folder location')
parser.add_argument("--folder_loc")

args = parser.parse_args()

if args.folder_loc  == None :
    print("Must have folder location. Please include --folder_loc='filepath/filename'")
    exit()
location = args.folder_loc

channel_list=get_chan_list(location)
make_chan_list(channel_list,location)
