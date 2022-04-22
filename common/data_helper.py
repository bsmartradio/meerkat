import glob
from astropy.io import fits
from astropy.table import Table
from astropy.wcs import WCS
import numpy as np


# This data_helper contains a number of short functions that are used across
# a number of MeerKAT processes. Many of them assume a standard file structure and MeerKAT data labeling.

def get_name(location):
    if not location:
        raise ValueError('Location cannot be none or empty')

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

    if not location.endswith('/'):
        location += '/'

    if background is True:
        found_list = sorted(glob.glob(f"{location}*[0-9][0-9]_bkg*"))

    if rms is True:
        found_list = sorted(glob.glob(location + "*[0-9][0-9]_rms*"))

    return found_list


def get_image(image_name):
    fits_file = fits.open(image_name)
    image_data = fits_file[0].data
    header = fits_file[0].header
    fits_file.close()

    return image_data, header


def unify_coords(table, w):
    # This gets the world coordinate system and also translate the table values to pixel values
    lon = table['lon'].data
    lat = table['lat'].data
    coordinate_array = []

    for index, lon in enumerate(lon):
        coord_pair = np.array([lon, lat[index]], np.float_)
        coordinate_array.append(coord_pair)

    positions = w.wcs_world2pix(coordinate_array, 2)

    return positions


def minmax_coord(header):
    wcs = WCS(header)
    min_lon = wcs.pixel_to_world(7500, 7500)
    max_lon = wcs.pixel_to_world(0, 0)

    return min_lon.l.degree, max_lon.l.degree


def find_channels(location):
    if location[-1] != '/':
        location += '/'
    channels = sorted(glob.glob(location + "*[0-9].fits"))

    return channels


def make_table(shape, aegean=False, table_type=None):
    if aegean and not 'id' in table_type.dtype.names:
        dtype = np.dtype([('id', 'int32')] + table_type.dtype.descr)

    elif aegean and 'id' in table_type.dtype.names:
        dtype = np.dtype(table_type.dtype.descr)

    else:
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

    return Table(data=np.zeros(shape, dtype=dtype))


def get_freq(location):
    if location[-1] != '/':
        location = location + '/'
    freq_loc = glob.glob(location + "*freq_list*.npy")

    return np.load(freq_loc[0])
