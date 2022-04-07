from astropy.io.votable import parse
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
#from astropy.utils.data import get_pkg_data_filename
from astropy.wcs import WCS
import math 
import sys
from astropy.coordinates import Angle
from regions import PixCoord, EllipsePixelRegion,EllipseSkyRegion
import numpy as np
from photutils import aperture_photometry
from photutils import EllipticalAperture,SkyEllipticalAperture,SkyCircularAperture
import time
from astropy.io import fits
import os
import subprocess
import shutil
import argparse
#from photutils.utils import calc_total_error
import re
from multiprocessing.pool import Pool
import multiprocessing as mp
import glob


#what needs to be done in this program
#This program needs to read in a cube (possibly a list of cubes)
#It then needs to plot the cube and the respective source positions (possibly to a file)
#It then needs to take the soure positions, translate them into pixel coordinates (easiest thing to do)
#After translating to pixel coordinates, aperture photometry needs to be run (needs to be prioritized fitting)
#Possibly for prioritized fitting, I need to use the output total intensity from the aegean file to order which ones
#get fit together
#I then need to add all of the related fits all together to make one single source fit. I use aegean numbers to do that

#To do: Clean up imports
#The program slows down a lot once the errors are calculated. I've added saving the error and apperture array files, and
#a check so that everything isn't re-run if the files already exist.

#This program will be altered to only process all of the files.
#A seperate program will be written to graph all of the photometry

#read in the location folder containing the full mosaic, the channels, and the backgrounds.
#There should be a list of all of them created by auto_bane

def read_folder_list(file):

    #Read in full data cubes and the vot tables
    with open(file, "r") as f:
        folder_loc=f.read().splitlines()
    f.close() 

    return folder_loc

#read in the location folder containing the full mosaic, the channels, and the backgrounds.
#There should be a list of all of them created by auto_bane
#Currently only looking for isolated vot table, will be adjusted for all vot tables

def find_lists(location,vot_location,filename):

    #Read in full data cube and the vot table
    dirs = os.listdir(location)
    dirs_vot=os.listdir(vot_location)
    channels_list=sorted(glob.glob(location+"*Mosaic_chan[0-9][0-9].fits"))
    vot_table=sorted(glob.glob(vot_location+filename+'_Mosaic_Mom0_comp.vot'))
    back_list=sorted(glob.glob(location+"*Mosaic_chan[0-9][0-9]_bkg.fits"))
    all_lists_check=""
    phot_list=""
    #for i in dirs:
        #if 'Mosaic.fits' in i  :
            #single_mosaic=i
        #if 'background_list.txt' in i  :
            #back_list=i
        #if 'channels_list.txt' in i  :
            #channels_list=i
        #if 'comp.vot' in i  :
            #vot_table=i
        #if 'phot_list.txt' in i  :
            #phot_list=i
        #missing_files=''
    #for j in dirs_vot:
        #if filename+'_Mosaic_Mom0_comp.vot' in j  :
            #vot_table=j
    print(f'Background list file: {back_list}')
    print(f'List of channels file: {channels_list}')
    print(f'Table of values file: {vot_table}')

    #read all of the channels
    
    if channels_list ==[] or back_list ==[]or vot_table ==[]:
        #if single_mosaic == "":
        #    missing_files=+' single mosaic fits file,'
        if channels_list == []:
            missing_files==' channels list file,'
        if back_list == []:
            missing_files='background list file, '
        if vot_table == []:
            missing_files='aegean vot tables file,'
        print('You are missing ' + missing_files + '. Please make sure you have run auto_bane first and all files are in the same folder.')
        all_lists_check= False
        channels=""
    else:
        all_lists_check=True
        
    return channels_list, back_list, vot_table, all_lists_check

def read_info(location,name):
    
    votable = parse(location+name+'_Mosaic_Mom0_comp.vot')
    #Read in the table

    for resource in votable.resources:
      for table in resource.tables:
        # ... do something with the table ...
        pass
    
    return table

def unify_coords(table,w):
    #This is it get the world coordinate system and also translate the table values to pixel values
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

def aperture_phot(positions,table,channels,location,channel):
    #Calculates all of the photometry for each aperture. Current issue is there is overlap which is not dealt with
    print(channels[channel])
    print(channel)
    hdul = fits.open(channels[channel])
    print(channels[channel])
    bck_file =[s for s in backgrounds if "chan"+"{:02d}".format(channel+1)+"_bkg" in s]
    rms_file =re.sub('_bkg.fits$', '', bck_file[0])+'_rms.fits'
    hdul_bck = fits.open(bck_file[0])
    hdul_rms = fits.open(rms_file)
    
    axis_coord_inc=4.166667E-04
    a_pix=table.array['a'].data*0.000277778/axis_coord_inc
    b_pix=table.array['b'].data*0.000277778/axis_coord_inc
    pa=table.array['pa'].data
    for i in range(len(positions)):
            
        apertures=EllipticalAperture(positions[i], a_pix[i], b_pix[i], pa[i])
            
        if i == 0:   
            print(f'Processing channel {channel+1} photometry')
            phot_table = aperture_photometry(hdul[0].data[:,:]-hdul_bck[0].data, apertures,error=hdul_rms[0].data[:,:]) 
        else:  
            temp_table = aperture_photometry(hdul[0].data[:,:], apertures,error=hdul_rms[0].data[:,:])
            phot_table.add_row([temp_table['id'], temp_table['xcenter'],temp_table['ycenter'],temp_table['aperture_sum'],temp_table['aperture_sum_err']])         
            
        
    np.save(location+'phot_table_chan'+"{:02d}".format(channel+1), phot_table, allow_pickle=True, fix_imports=True) 
    finished=f"Channel {channel+1} processed"
    return finished

def error_calc(table,hdul,hdul_rms,channel):
    #I am assuming I am converting here to... arcseconds??
    #The data in the table is in degrees. I want it to be in pixels, so this is translating it
    #To arcseconds and then pixels. This assumes the pixels are square and the axis coordinate 
    #increments are the same
    axis_coord_inc=4.166667E-04
    a_pix=table.array['a'].data*0.000277778/axis_coord_inc
    b_pix=table.array['b'].data*0.000277778/axis_coord_inc
    pa=table.array['pa'].data

    err = calc_total_error(hdul[0].data, hdul_rms[0].data, effective_gain=100)
    
    return err

def process_channels_check(location,channels,k):
    
    phot_exist=os.path.isfile(location+'phot_list.txt')
    existing_channels=[]
    if phot_exist == False:
        #I need to add a skip here
        #Everything below here needs to be in a single function thrown into multiprocessing.
        bck_file=" "
        #Checks if any channels have been removed and ignores them
        chan_check=any(("chan"+"{:02d}".format(k+1)+'.') in string for string in channels)
        print("Does chan"+"{:02d}".format(k+1)+' exist?')
        print(chan_check)
        #I need something here that will not have the dimension number overflow since the channels
        #are going to be off. Currently there is an offset if the number of channels and total dont 
        #match up correctly.
        if chan_check != False:
                
            #Need to check if these are empty files
            hdul = fits.open(channels[k])
            print(k)
            print(channels[k])
            check=np.isnan(hdul[0].data[:,:]).all()
            bck_file =[s for s in backgrounds if "chan"+"{:02d}".format(k+1)+"_bkg" in s]
            print(f'{bck_file}')
            print(f'{check}')
                
            if check == False and bck_file != " ":
                #Load in the background fits files
                print('Processing Apertures')
                bck_file =[s for s in backgrounds if "chan"+"{:02d}".format(k+1)+"_bkg" in s]
                rms_file =re.sub('_bkg.fits$', '', bck_file[0])+'_rms.fits'
                hdul_bck = fits.open(bck_file[0])
                hdul_rms = fits.open(rms_file)
                        
                existing_channels.append(k)
                        
                print('Channel ', k+1, ' has values')
                             
            elif bck_file == " " and check != False:
                print('Missing background file for ', k+1, ' channel. Run auto_bane to make file')
            
            else:
                print('No values for ', k+1, ' channel')
        else:
            print('No values for ', k+1, ' channel')
                 
    elif phot_exist != False :
        print('Photometry file exists for ' + location + 'and was skipped. To re-run, remove phot_list from directory.')

    else:
        print(f"Skipping folder {x} due to missing files")

    print(phot_exist)
    
    return existing_channels, phot_exist

def combine_table(current_location,shape):
    dirs = os.listdir(current_location)
    full_phot=np.full([2,num_dim,shape], float('Nan'))
    freq_list=np.full([num_dim], float('Nan')) 
    
    for k in range(num_dim):   
        if 'phot_table_chan'+"{:02d}".format(k+1)+'.dat.npy' in dirs:
            phot_table =np.load(current_location+'phot_table_chan'+"{:02d}".format(k+1)+'.dat.npy')
            full_phot[0,k,:]=phot_table['aperture_sum']
            full_phot[1,k,:]=phot_table['aperture_sum_err']
    return full_phot

#vot_location='/Volumes/200GB/MeerKAT/G005.5+0.0IFx/'

#Read in file name argument.
parser = argparse.ArgumentParser(description='Must have folder location')
parser.add_argument("--folder_loc")

args = parser.parse_args()

if args.folder_loc  == None :
    print("Must have folder location. Please include --folder_loc='filepath/filename'")
    exit()
location = args.folder_loc

#Read in vot location argument

last_char_index = location[:-1].rfind("/")
name=location[last_char_index+1:-1]
vot_cat_index=location[:last_char_index-1].rfind("/")
vot_location=location[:vot_cat_index+1]+'Mom0_comp_catalogs/'
print(location)
print(vot_location)
fileslist = os.listdir(location.strip())

#Get all the info for the specific mosaic locations
channels, backgrounds, vot_table, all_lists_check=find_lists(location,vot_location,name)
    
if all_lists_check == True: 
    
    print(channels[0])
    
    #Read in the table and load in all channels
    dirs = os.listdir(location)
    table = read_info(vot_location,name)
    #Need to move this into a def
    #f = open(location+back_list, "r")
    #backgrounds=f.read().splitlines()
    #hdul = fits.open(location+channels[0])
    hdul = fits.open(channels[0])
    #dimension number is always 14 unless specified otherwise
    num_dim=14
    w = WCS(hdul[0].header,naxis=2)
    positions = unify_coords(table,w)
    shape=len(table.array)
    #Full array of apertures 
    app_list=np.full([num_dim,shape], float('Nan'))
    err_list=np.full([num_dim,shape], float('Nan'))
    #List of frequencies
    freq_list=np.full([num_dim], float('Nan'))   
    count=0
    last_char_index = location[:-1].rfind("/")
    name=location[last_char_index+1:-1]
    for j in range(num_dim):
        
        number_str = str(j+1)
        freq_num='FREQ00'+ number_str.zfill(2)
        chan_check=any(("chan"+"{:02d}".format(j+1)+'.') in string for string in channels)
        if chan_check != False:
            #This is getting fucked up here
            hdul = fits.open(channels[count])
            freq_list[j]= hdul[0].header['OBSFREQ']
            count=count+1
            
    #Save the frequency list from the headers. Could split the whole frequency bit into its own program
    if not name+'freq_list' in dirs:
        np.save(location+name+'_freq_list', freq_list, allow_pickle=True, fix_imports=True) 

    channels_to_process=[]
    #Needs to ignore the first two channels as they are not normal channels  
    #just edited location to [i] from [0]. Shouldn't mess things up
    #Right here check if the photometry tables have been processed
    for k in range(num_dim):
        channels_to_process,phot_exist=process_channels_check(location,channels,k)
        print(f'Phot exist: {phot_exist} ')
        if phot_exist == False:
            print(f'Processing Channel {channels_to_process}')
            processes=[mp.Process(target=aperture_phot, args=(positions, table,channels,location,x)) for x in channels_to_process]
            # Run processes
            for p in processes:
                p.start()

            # Exit the completed processes
            for p in processes:
                p.join()

            phot_list=[]

            for line in dirs:
                
                if 'phot_table_chan' in line:
                    phot_list.append(line)
            if phot_list:
                with open(location+'phot_list.txt', 'w') as f:
                    for k in phot_list:
                        f.writelines(k)
                        f.writelines("\n")
    
        if phot_exist != False:            
            #read in the existing photometry files here
            print('Cube has already been processed. Photometry table in folder.')