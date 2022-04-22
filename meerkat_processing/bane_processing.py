import re
import subprocess
import logging
import common.data_checks as checks
import os
import common.data_helper as helper

# This program looks for individual Mosaic Planes in a cube folder and runs the Bane background processing from the
# Aegean data-reduction pipeline.
def run_bane(location, file):
    logging.info(f'File location {location + file}')
    cmd = ['BANE', location + file]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait()

    return


def begin_bane(path):
    checks.file_check(path)
    name = helper.get_name(path)
    channels_list = helper.find_channels(path)
    backgrounds_list = helper.find_backgrounds(path)

    # Writes a list of all the channel files which can be used for quick reference
    if os.path.isfile(path + name + '_missing_backgrounds_list.txt'):
        logging.info('Reading existing channel file.')

        with open(path + name + '_channels_list.txt', 'r') as filehandle:
            channels_list = filehandle.read().splitlines()
    else:
        logging.info('Writing new channels file.')

        with open(path + name + '_channels_list.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in channels_list)

    if len(channels_list) == len(backgrounds_list):
        logging.info('Bane has already been run on all channels for ' + path)
        exit()

    # If bane has been run on some but not all, warns you.
    elif len(backgrounds_list) > 0:
        logging.info('Bane has already been run on some channels. Re-running Bane on missing channels')

        for i in channels_list:
            run_bane(path, i)

    # Runs bane if there is no existing background files
    else:

        for i in channels_list:
            run_bane(path, i)
            logging.info("Running Bane on all channels.")

    dirs = os.listdir(path)

    with open(path + name + '_background_list.txt', 'w') as filehandle:
        for i in dirs:
            if 'bkg.fits' in i:
                filehandle.writelines(i + '\n')
                logging.info(i + ' written to background list.')

    logging.info('Checking that all channels have a background')

    if os.path.isfile(path + name + '_missing_background_list.txt'):
        logging.info(
            'Channels missing background files have already been moved into ' + path + name +
            '_missing_background_list.txt')

    else:
        missing = []

        for i in backgrounds_list:
            matched_channel = str(re.findall(r'_c.*?\.', i))
            matched_channel = matched_channel[3:-3]

            if matched_channel in channels_list:
                logging.info('Channel ' + matched_channel + ' has background')

            else:
                logging.info('Channel ' + matched_channel + ' does not have background. Channel removed from list')

                with open(path + name + '_channels_list.txt', 'r') as f:
                    lines = f.readlines()

                with open(path + name + '_channels_list.txt', 'w') as f:

                    for line in lines:

                        if line.strip("\n") != i:
                            f.write(line)

                with open(path + name + '_missing_background_list.txt', 'w') as f:
                    missing.append(i)

        if len(missing) > 0:
            logging.info('There are ' + str(len(missing)) + ' missing background files')

            with open(path + name + '_missing_background_list.txt', 'w') as f:

                for k in missing:
                    f.write(k)
