import glob
import os
import common.data_helper as helper
import numpy as np
import logging

import common.vot_helper


def file_check(location):
    channels = helper.find_channels(location)
    check_filenames(channels, location)

    logging.info(f"Channel name check has been run for cube {location}")


def check_filenames(channels, location):
    for single_channel in channels:

        for chan_num in range(9):

            if any(x in single_channel for x in ["chan" + "{:01d}".format(chan_num + 1) + '.']):
                logging.info('File name will be changed for file: ' + single_channel)

                new_filename = location + single_channel
                new_filename = new_filename.replace(("chan" + "{:01d}".format(chan_num + 1) + '.'),
                                                    ("chan" + "{:02d}".format(chan_num + 1) + '.'), 1)
                os.rename(location + single_channel, new_filename)

                logging.info(new_filename.replace(("chan" + "{:01d}".format(chan_num + 1) + '.'),
                                                  ("chan" + "{:02d}".format(chan_num + 1) + '.'), 1))


def process_channels_check(location, channels, total_channels, backgrounds_list, phot_lookup=True):
    if phot_lookup:
        phot_exist = os.path.isfile(location + 'phot_list.txt')
    else:
        phot_exist = False

    existing_channels = []

    for i in range(total_channels):

        if not phot_exist:

            # Checks if any channels have been removed and ignores them
            channel_exists_check = channels[i].find("chan" + "{:02d}".format(i + 1) + '.')

            logging.info("Does chan" + "{:02d}".format(i + 1) + ' exist?')

            if channel_exists_check:
                logging.info('Yes')
            else:
                logging.info('No')

            if channel_exists_check:

                logging.info('Checking for channels with only nan values and valid background files')
                channel_data = helper.get_image(channels[i])
                check_values = np.isnan(channel_data[0][:, :]).all()
                bck_file = [s for s in backgrounds_list if "chan" + "{:02d}".format(i + 1) + "_bkg" in s]

                if not check_values and bck_file:
                    existing_channels.append(i)
                    logging.info(f'Channel {i + 1} has values and valid background, will process photometry')
                elif not bck_file and check_values:
                    logging.warning(f'Missing background file for {i + 1} channel. Run auto_bane to make file.')
                    logging.warning(f"Skipping file {location} due to missing files")
                elif bck_file and check_values:
                    logging.warning(f'No values for {i + 1} channel')
                else:
                    logging.warning(f'No values for {i + 1} channel and missing background file. '
                                    f'Run auto_bane to make file.')
            else:
                logging.warning('Channel does not exist. Please check if all fits files are present.')

        elif phot_exist and i == 13 and len(existing_channels) == 0:
            logging.info(
                f'Photometry files exists for {location} and processing was skipped. To re-run, remove phot_list '
                f'from directory.')

            exit()

    return existing_channels, phot_exist


def check_required_files_exist(location):
    # Read in full data cube and the vot table
    name = helper.get_name(location)
    vot_location = common.vot_helper.get_vot_location(location)

    channels_list = sorted(glob.glob(location + "/*Mosaic_chan[0-9][0-9].fits"))
    vot_table = sorted(glob.glob(vot_location + name + '_Mosaic_Mom0_comp.vot'))
    back_list = sorted(glob.glob(location + "/*Mosaic_chan[0-9][0-9]_bkg.fits"))

    logging.info(f'Background list file: {back_list}')
    logging.info(f'List of channels file: {channels_list}')
    logging.info(f'Table of values file: {vot_table}')

    # read all the channels and debug if missing files
    if channels_list == [] or back_list == [] or vot_table == []:
        missing_files = ''

        if not channels_list:
            missing_files += 'channels list file, '

        if not back_list:
            missing_files += 'background list file, '

        if not vot_table:
            missing_files += 'aegean vot tables file, '

        missing_files = missing_files[0: missing_files.rfind(', ')]

        logging.warning(
            'You are missing ' + missing_files + '. Please make sure you have run auto_bane first and all files are '
                                                 'in the same folder.')
        all_lists_check = False

    else:
        all_lists_check = True
        logging.info('All lists found. Processing photometry.')

    return all_lists_check, back_list, channels_list
