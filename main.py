import argparse
import os
from functools import partial
from typing import re

from astropy.units.format import fits
from photutils import EllipticalAperture, aperture_photometry
from photutils.utils import calc_total_error

import common.image as image
import common.data_helper as helper
import common.data_checks as checks
import multiprocessing as mp
import numpy as np


def aperture_phot(path, channel_number):
    # Calculates all the photometry for each aperture. Overlapping points are marked
    # in a separate program.
    print(channel_number)
    data_cube = image.Image(path)
    axis_coord_inc = 4.166667E-04
    a_pix = data_cube.vot_table['a'].data * 0.000277778 / axis_coord_inc
    b_pix = data_cube.vot_table['b'].data * 0.000277778 / axis_coord_inc
    pa = data_cube.vot_table['pa'].data
    for i in range(len(data_cube.positions)):

        apertures = EllipticalAperture(data_cube.positions[i], a_pix[i], b_pix[i], pa[i])

        if i == 0:
            print(f'Processing channel {channel_number + 1} photometry')
            phot_table = aperture_photometry(data_cube.channels[channel_number].data[:, :] -
                                             data_cube.background[channel_number].data[:, :], apertures,
                                             error=data_cube.rms[channel_number].data[:, :])
        else:
            temp_table = aperture_photometry(data_cube.channels[channel_number].data[:, :] -
                                             data_cube.background[channel_number].data[:, :], apertures,
                                             error=data_cube.rms[channel_number].data[:, :])
            phot_table.add_row([temp_table['id'], temp_table['xcenter'], temp_table['ycenter'],
                                temp_table['aperture_sum'], temp_table['aperture_sum_err']])

    np.save(data_cube.location + 'phot_table_chan' + "{:02d}".format(channel_number + 1), phot_table,
            allow_pickle=True, fix_imports=True)
    finished = f"Channel {channel_number + 1} processed"
    return finished


def combine_table(current_location, shape):
    dirs = os.listdir(current_location)
    full_phot = np.full([2, total_channels, shape], float('Nan'))
    freq_list = np.full([total_channels], float('Nan'))

    for k in range(total_channels):
        if 'phot_table_chan' + "{:02d}".format(k + 1) + '.dat.npy' in dirs:
            phot_table = np.load(current_location + 'phot_table_chan' + "{:02d}".format(k + 1) + '.dat.npy')
            full_phot[0, k, :] = phot_table['aperture_sum']
            full_phot[1, k, :] = phot_table['aperture_sum_err']
    return full_phot


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Must have folder location')
    parser.add_argument("--folder_loc")

    args = parser.parse_args()

    if args.folder_loc is None:
        print("Must have folder location. Please include --folder_loc='filepath/filename'")
        exit()

    path = args.folder_loc

    # Get all the info for the specific mosaic locations
    channels, backgrounds, vot_table, all_lists_check = helper.find_lists(path)

    if all_lists_check:
        # Constructs the data cube for the specific MeerKAT data, gathering the individual channel data,
        # the background information, and the rms data
        data_cube = image.Image(path)
        total_channels = len(data_cube.channels)
        channels_to_process, phot_exist = checks.process_channels_check(path, data_cube.channels, total_channels,
                                                                        backgrounds)
        print(f'Does Phot exist: {phot_exist} ')
        if not phot_exist:
            pool = mp.Pool()
            func = partial(aperture_phot, path)
            print('Hi')
            pool.map(func, channels_to_process)
            pool.close()
            pool.join()
    print('end')
    phot_list = []

    dirs = os.listdir(path)

    for line in dirs:

        if 'phot_table_chan' in line:
            phot_list.append(line)
            if phot_list:
                with open(path + 'phot_list.txt', 'w') as f:
                    for k in phot_list:
                        f.writelines(k)
                        f.writelines("\n")

        # if phot_exist != False:
        # read in the existing photometry files here
        #   print('Cube has already been processed. Photometry tables in folder.')
