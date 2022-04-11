import os
import common.data_helper as helper


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
