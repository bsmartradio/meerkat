import glob
from astropy.io import fits
from astropy.io.votable import parse
from astropy.table import Table
from astropy.wcs import WCS
import numpy as np


# This data_helper contains a number of short functions that are used across
# a number of MeerKAT processes. Many of them assume a standard file structure and MeerKAT data labeling.

def get_name(location):
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


def find_backgrounds(location, background=False, rms=False):
    found_list = []
    if not background and not rms:
        background = True

    if location[-1] != '/':
        location = location + '/'
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


def find_channels(location):
    if location[-1] != '/':
        location = location + '/'
    channels = sorted(glob.glob(location + "*[0-9].fits"))

    return channels


def get_vot_list(location, aegean=False):
    if aegean:
        vot_list = sorted(glob.glob(location + "Mom0_comp_catalogs/*Mosaic_Mom0_comp.vot"))
    else:
        vot_list = sorted(glob.glob(location + "Mosaic_Planes/G*/*full_table_cut.vot"))

    return vot_list


def get_vot_location(location):
    folder_name = get_name(location)
    upper_folder = location[0:-len(folder_name) - 1].rfind("/")
    vot_location = location[0:upper_folder] + '/Mom0_comp_catalogs/'

    return vot_location


def load_neighbors(names, folder):
    vot_mid = read_info(folder + '/' + names[1] + '_Mosaic_Mom0_comp.vot')
    vot_left = read_info(folder + '/' + names[0] + '_Mosaic_Mom0_comp.vot')
    vot_right = read_info(folder + '/' + names[2] + '_Mosaic_Mom0_comp.vot')

    vot_list = [vot_left, vot_mid, vot_right]

    return vot_list


def make_table(shape):
    dtype = [('id', 'int32'), ('field', 'object'),
             ('chan01', 'float64'), ('chan01err', 'float64'),
             ('chan02', 'float64'), ('chan02err', 'float64'),
             ('chan03', 'float64'), ('chan03err', 'float64'),
             ('chan04', 'float64'), ('chan04err', 'float64'),
             ('chan05', 'float64'), ('chan05err', 'float64'),
             ('chan06', 'float64'), ('chan06err', 'float64'),
             ('chan07', 'float64'), ('chan07err', 'float64'),
             ('chan08', 'float64'), ('chan08err', 'float64'),
             ('chan09', 'float64'), ('chan09err', 'float64'),
             ('chan10', 'float64'), ('chan10err', 'float64'),
             ('chan11', 'float64'), ('chan11err', 'float64'),
             ('chan12', 'float64'), ('chan12err', 'float64'),
             ('chan13', 'float64'), ('chan13err', 'float64'),
             ('chan14', 'float64'), ('chan14err', 'float64'),
             ('si_m', 'float64'), ('si_point_num', 'int32'),
             ('xi', 'float64'), ('pvalue', 'float64'),
             ('overlap', 'float64'), ('overlap_field', 'object'),
             ('edge', 'bool'), ('overlap_mask', 'bool')]
    full_table = Table(data=np.zeros(shape, dtype=dtype))
    return full_table


def get_chan_list(location):
    channel_list = glob.glob(location + "phot_table*.npy")
    return channel_list


def load_phot_table(channel_name):
    phot_table = np.load(channel_name, allow_pickle=True)
    return phot_table


def get_freq(location):
    if location[-1] != '/':
        location = location + '/'
    freq_loc = glob.glob(location + "*freq_list*.npy")
    freq_list = np.load(freq_loc[0])
    return freq_list
