import glob
from astropy.io import fits
from astropy.io.votable import parse
from astropy.wcs import WCS
import numpy as np


# This data_helper contains a number of short functions that are used across
# a number of MeerKAT processes. Many of them assume a standard
# file structure and MeerKAT data labeling.

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
    lon = table.array['lon'].data
    lat = table.array['lat'].data
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
