import glob
import logging
from astropy.io.votable import table
from common.data_helper import get_name


def read_vot(vot_location):
    try:
        votable = table.parse(vot_location)
        first_table = votable.get_first_table()
        data = first_table.array
    except ValueError as ve:
        logging.exception(msg='Failed to read VOT table', exc_info=ve)
        raise ve

    return data


def get_vot_list(location, aegean=False):
    if aegean:
        vot_list = sorted(glob.glob(location + "Mom0_comp_catalogs/*Mosaic_Mom0_comp.vot"))
    else:
        vot_list = sorted(glob.glob(location + "Mosaic_Planes/G*/*full_table_cut.vot"))

    return vot_list


def get_vot_location(location):
    folder_name = get_name(location)
    upper_folder = location[0:-len(folder_name) - 2].rfind("/")
    vot_location = location[0:upper_folder] + '/Mom0_comp_catalogs/'

    return vot_location


def load_neighbors(names, folder):
    if folder[-1] != '/':
        folder += '/'

    vot_mid = read_vot(folder + names[1] + '_Mosaic_Mom0_comp.vot')
    vot_left = read_vot(folder + names[0] + '_Mosaic_Mom0_comp.vot')
    vot_right = read_vot(folder + names[2] + '_Mosaic_Mom0_comp.vot')

    return [vot_left, vot_mid, vot_right]
