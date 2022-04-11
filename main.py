import argparse
from typing import re

from astropy.units.format import fits

import common.image as image
import common.data_helper as helper
import common.data_checks as checks
import multiprocessing as mp
import numpy as np

def aperture_phot(positions, channels, vot_location, name, channel):
    # Calculates all the photometry for each aperture. Overlapping points are marked
    # in a separate program.
    print(channels[channel])
    print(channel)
    table = helper.read_info(vot_location, name)
    hdul = fits.open(channels[channel])
    print(channels[channel])
    bck_file = [s for s in backgrounds if "chan" + "{:02d}".format(channel + 1) + "_bkg" in s]
    rms_file = re.sub('_bkg.fits$', '', bck_file[0]) + '_rms.fits'
    hdul_bck = fits.open(bck_file[0])
    hdul_rms = fits.open(rms_file)

    axis_coord_inc = 4.166667E-04
    a_pix = table.array['a'].data * 0.000277778 / axis_coord_inc
    b_pix = table.array['b'].data * 0.000277778 / axis_coord_inc
    pa = table.array['pa'].data
    for i in range(len(positions)):

        apertures = EllipticalAperture(positions[i], a_pix[i], b_pix[i], pa[i])

        if i == 0:
            print(f'Processing channel {channel + 1} photometry')
            phot_table = aperture_photometry(hdul[0].data[:, :] - hdul_bck[0].data, apertures,
                                             error=hdul_rms[0].data[:, :])
        else:
            temp_table = aperture_photometry(hdul[0].data[:, :], apertures, error=hdul_rms[0].data[:, :])
            phot_table.add_row(
                [temp_table['id'], temp_table['xcenter'], temp_table['ycenter'], temp_table['aperture_sum'],
                 temp_table['aperture_sum_err']])

    np.save(location + 'phot_table_chan' + "{:02d}".format(channel + 1), phot_table, allow_pickle=True,
            fix_imports=True)
    finished = f"Channel {channel + 1} processed"
    return finished


def error_calc(table, hdul, hdul_rms, channel):
    # I am assuming I am converting here to... arcseconds??
    # The data in the table is in degrees. I want it to be in pixels, so this is translating it
    # To arcseconds and then pixels. This assumes the pixels are square and the axis coordinate
    # increments are the same
    axis_coord_inc = 4.166667E-04
    a_pix = table.array['a'].data * 0.000277778 / axis_coord_inc
    b_pix = table.array['b'].data * 0.000277778 / axis_coord_inc
    pa = table.array['pa'].data

    err = calc_total_error(hdul[0].data, hdul_rms[0].data, effective_gain=100)

    return err

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

    if all_lists_check == True:
        data_cube = image.Image(path)
        total_channels = len(data_cube.channels)

        for k in range(total_channels):
            channels_to_process, phot_exist = checks.process_channels_check(path, data_cube.channels, k)
            print(f'Does Phot exist: {phot_exist} ')
            if phot_exist == False:
                print(channels_to_process)
                pool = mp.Pool()
                func = partial(aperture_phot, positions, channels, vot_location, name)

                #pool.map(func, channels_to_process)
                #pool.close()
                #pool.join()

                phot_list = []

                dirs = os.listdir(location)

                for line in dirs:

                    if 'phot_table_chan' in line:
                        phot_list.append(line)
                if phot_list:
                    with open(location + 'phot_list.txt', 'w') as f:
                        for k in phot_list:
                            f.writelines(k)
                            f.writelines("\n")

            if phot_exist != False:
                # read in the existing photometry files here
                print('Cube has already been processed. Photometry tables in folder.')
