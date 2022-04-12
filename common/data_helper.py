import glob
from astropy.io import fits
from astropy.io.votable import parse
from astropy.wcs import WCS
import numpy as np


# This data_helper contains a number of short functions that are used across
# a number of MeerKAT processes. Many of them assume a standard file structure and MeerKAT data labeling.

def get_name(location):
    print(location)
    if location[-1] == '/':
        last_char_index = location[:-1].rfind("/")
        name = location[last_char_index + 1:-1]
    elif location[-1] == 't':
        last_char_index = location[:-1].rfind("/")
        mid_char_index = location[:-last_char_index].rfind("/")
        name = location[mid_char_index + 1:last_char_index]
    else:
        last_char_index = location[:-1].rfind("/")
        name = location[last_char_index + 1:]
    return name


def find_backgrounds(location, background= False, rms = False):
    if background is True:
        found_list = sorted(glob.glob(location + "*[0-9][0-9]_bkg*"))
    if rms is True:
        found_list = sorted(glob.glob(location + "*[0-9][0-9]_rms*"))
    return found_list

def get_list(location):
    folder_list = sorted(glob.glob(location + "G[0-9][0-9][0-9]*"))
    return folder_list


def read_info(vot_location):
    votable = parse(vot_location)
    table = votable.get_first_table()
    data = table.array

    return data

def get_image(image_name):

    fits_file = fits.open(image_name)
    image_data = fits_file[0].data
    hdr = fits_file[0].header
    fits_file.close()

    return image_data, hdr


def unify_coords(table, w):
    # This gets the world coordinate system and also translate the table values to pixel values
    lon = table['lon'].data
    lat = table['lat'].data
    t = 0
    test_arr = []
    for x in lon:
        test = np.array([lon[t], lat[t]], np.float_)
        test_arr.append(test)
        t = t + 1
    positions = w.wcs_world2pix(test_arr, 2)

    return positions


def minmax_coord(header):
    w = WCS(header)
    min_lon = w.pixel_to_world(7500, 7500)
    max_lon = w.pixel_to_world(0, 0)

    return min_lon.l.degree, max_lon.l.degree


def find_files(location):
    channels = sorted(glob.glob(location + "*[0-9].fits"))

    return channels


def get_vot_list(location, aegean=False):
    if aegean:
        vot_list = sorted(glob.glob(location + "Mom0_comp_catalogs/*Mosaic_Mom0_comp.vot"))
    else:
        vot_list = sorted(glob.glob(location + "Mosaic_Planes/G*/*full_table_cut.vot"))

    return vot_list


def get_vot_location(location):
    folder_name=get_name(location)
    upper_folder = location[0:-len(folder_name) - 2].rfind("/")
    vot_location = location[0:upper_folder] + '/Mom0_comp_catalogs/'

    return vot_location

def find_lists(location):
    # Read in full data cube and the vot table
    name = get_name(location)
    vot_location = get_vot_location(location)
    channels_list = sorted(glob.glob(location + "/*Mosaic_chan[0-9][0-9].fits"))
    vot_table = sorted(glob.glob(vot_location + name + '_Mosaic_Mom0_comp.vot'))
    back_list = sorted(glob.glob(location + "/*Mosaic_chan[0-9][0-9]_bkg.fits"))
    print(f'Background list file: {back_list}')
    print(f'List of channels file: {channels_list}')
    print(f'Table of values file: {vot_table}')

    # read all the channels and debug if missing files
    if channels_list == [] or back_list == [] or vot_table == []:
        missing_files = ''
        if not channels_list:
            missing_files = ' channels list file,'
        if not back_list:
            missing_files = 'background list file, '
        if not vot_table:
            missing_files = 'aegean vot tables file,'
        print(
            'You are missing ' + missing_files + '. Please make sure you have run auto_bane first and all files are '
                                                 'in the same folder.')
        all_lists_check = False
        channels = ""
    else:
        all_lists_check = True
        print('All lists found. Processing photometry.')

    return channels_list, back_list, vot_table, all_lists_check
