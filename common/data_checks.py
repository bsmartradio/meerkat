import os
import common.data_helper as helper
import numpy as np

def file_check(location):
    channels = helper.find_files(location)
    check_filenames(channels, location)
    print(f"Channel name check has been run for cube {location}")


def check_filenames(channels, location):
    for single_channel in channels:
        for chan_num in range(9):
            if any(x in single_channel for x in ["chan" + "{:01d}".format(chan_num + 1) + '.']):
                print('File name needs to be changed for file: ' + single_channel)
                new_filename = location + single_channel
                new_filename = new_filename.replace(("chan" + "{:01d}".format(chan_num + 1) + '.'),
                                                    ("chan" + "{:02d}".format(chan_num + 1) + '.'), 1)
                os.rename(location + single_channel, new_filename)
                print(new_filename.replace(("chan" + "{:01d}".format(chan_num + 1) + '.'),
                                           ("chan" + "{:02d}".format(chan_num + 1) + '.'), 1))

def process_channels_check(location, channels, total_channels, backgrounds):
    phot_exist = os.path.isfile(location + 'phot_list.txt')
    existing_channels = []

    for k in range(total_channels):
        if phot_exist == False:

            # Checks if any channels have been removed and ignores them
            chan_check = None
            channel_exists_check = channels[k].name.find("chan" + "{:02d}".format(k + 1) + '.')
            print("Does chan" + "{:02d}".format(k + 1) + ' exist?')

            if channel_exists_check:

                # Need to check if these are empty files
                print('Checking for channels with only nan values and valid background files')
                check_values = np.isnan(channels[k].data[:, :]).all()
                bck_file = [s for s in backgrounds if "chan" + "{:02d}".format(k + 1) + "_bkg" in s]

                if check_values == False and bck_file != " ":
                    # Load in the background fits files
                    existing_channels.append(k)
                    print('Channel ', k + 1, ' has values and valid background, will process photometry')
                    print(existing_channels)

                elif bck_file == " " and check_values != False:
                    print('Missing background file for ', k + 1, ' channel. Run auto_bane to make file')

                else:
                    print('No values for ', k + 1, ' channel')
            else:
                print('No values for ', k + 1, ' channel')

        elif phot_exist != False:
            print('Photometry file exists for ' + location + 'and was skipped. To re-run, remove phot_list from directory.')
            exit()
        else:
            print(f"Skipping folder {location} due to missing files")


    return existing_channels, phot_exist
