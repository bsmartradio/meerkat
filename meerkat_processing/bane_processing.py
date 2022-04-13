import argparse
import re
import subprocess

import common.data_checks as checks
import os
import common.data_helper as helper


def run_bane(location, file):
    print(f'File location {location+file}')
    cmd = ['BANE',location+file]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait()
    return

if __name__ == '__main__':
    # Read in file name argument.
    parser = argparse.ArgumentParser(description='Must give folder name')
    parser.add_argument("--folder_location")

    args = parser.parse_args()

    if args.folder_location is None:
        print("Must have folder location. Please include --folder_loc='filepath/foldername'")
        print("Example: --folder_location='/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/'")
        exit()

    location = args.folder_location

    print("Checking if all files are named correctly")
    checks.file_check(location)
    name = helper.get_name(location)
    channels_list = helper.find_channels(location)
    backgrounds_list = helper.find_backgrounds(location)

    # Writes a list of all of the channel files which can be used for quick reference
    if os.path.isfile(location + name + '_missing_backgrounds_list.txt'):
        channels_list = []
        print('Reading existing channel file.')
        with open(location + name + '_channels_list.txt', 'r') as filehandle:
            channels_list = filehandle.read().splitlines()
    else:
        print('Writing new channels file.')
        with open(location + name + '_channels_list.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in channels_list)
    # Writes a list of all of the backgrounds created files which can be used in other programs

    # checks if bane has already been run on the fits files
    if len(channels_list) == len(backgrounds_list):
        print('Bane has already been run on all channels for ' + location)
    # If bane has been run on some but not all, warns you.
    elif len(backgrounds_list) > 0:
        print('Bane has already been run on some channels. Re-running Bane')
        for i in channels_list:
            run_bane(location, i)
    # Runs bane if there is no existing background files
    else:
        for i in channels_list:
            run_bane(location, i)
            print("Running Bane on all channels.")

    dirs = os.listdir(location)
    with open(location + name + '_background_list.txt', 'w') as filehandle:
        for i in dirs:
            if 'bkg.fits' in i:
                filehandle.writelines(i + '\n')
                print(i + ' written to background list.')

    print('Checking that all channels have a background')

    if os.path.isfile(location + name + '_missing_background_list.txt'):
        print(
            'Channels missing background files have already been moved into ' + location + name + '_missing_background_list.txt')

    else:
        #s = b_list
        #full_list = listToString(s)
        missing = []
        #print(i)
        #print(c_list)
        for i in backgrounds_list:
            matched_channel = str(re.findall(r'\_c.*?\.', i))
            matched_channel = matched_channel[3:-3]
            if matched_channel in channels_list:
                print('Channel ' + matched_channel + ' has background')

            else:
                print('Channel ' + matched_channel + ' does not have background. Channel removed from list')
                with open(location + name + '_channels_list.txt', 'r') as f:
                    lines = f.readlines()
                with open(location + name + '_channels_list.txt', 'w') as f:
                    for line in lines:
                        if line.strip("\n") != i:
                            f.write(line)
                with open(location + name + '_missing_background_list.txt', 'w') as f:
                    missing.append(i)

        if len(missing) > 0:
            print('There are ' + str(len(missing)) + ' missing background files')
            with open(location + name + '_missing_background_list.txt', 'w') as f:
                for k in missing:
                    f.write(k)