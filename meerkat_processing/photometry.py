import os
from functools import partial
from photutils import EllipticalAperture, aperture_photometry
import time
import models.image as image
import common.data_checks as checks
import multiprocessing as mp
import numpy as np
import logging


def aperture_phot(path, channel_number):
    # Calculates all the photometry for each aperture. Overlapping points are marked
    # in a compare_neighbors
    start = time.time()
    data_cube = image.Image(path, single_channel=channel_number)
    axis_coord_inc = 4.166667E-04
    a_pix = data_cube.vot_table['a'].data * 0.000277778 / axis_coord_inc
    b_pix = data_cube.vot_table['b'].data * 0.000277778 / axis_coord_inc
    pa = data_cube.vot_table['pa'].data
    size = range(len(data_cube.positions))

    apertures = [EllipticalAperture(data_cube.positions[i], a_pix[i], b_pix[i], pa[i]) for i in size]

    logging.info(f'Processing channel {channel_number + 1} photometry')

    phot_table = [aperture_photometry(
        data_cube.channels[0].data[:, :] - data_cube.background[0].data[:, :],
        apert, error=data_cube.rms[0].data[:, :]) for apert in apertures]

    np.save(f'{data_cube.location}phot_table_chan' + '{:02d}'.format(channel_number + 1), phot_table,
            allow_pickle=True, fix_imports=True)

    end = time.time()

    logging.info("The time it took to process one channel's photometry is :", end - start)

    return f'Channel {channel_number + 1} processed'


def process_photometry(path):
    # Check if the required files are present, if not exits program and prints advisories.
    required_files_exist, backgrounds, channels = checks.check_required_files_exist(path)

    if not required_files_exist:
        exit()

    # Constructs the data cube for the specific MeerKAT data, gathering the individual channel data,
    # the background information, and the rms data
    total_channels = len(channels)
    # Checks if any of the files have been processed. If some but not all have, only runs photometry on
    # the channels missing files.
    channels_to_process, phot_exist = checks.process_channels_check(path, channels, total_channels,
                                                                    backgrounds)
    logging.info(f'Does Phot exist: {phot_exist} ')

    if not phot_exist:
        # Phot does not exist, so we are going to create the photometry files
        pool = mp.Pool()
        func = partial(aperture_phot, path)
        pool.map(func, channels_to_process)
        pool.close()
        pool.join()

    # Creates a text file containing all processed photometry for quick reference
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

    if phot_exist:
        logging.info('Cube has already been fully processed. Photometry tables in folder.')

