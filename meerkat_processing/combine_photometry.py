import numpy as np
from scipy.stats import chisquare
import common.data_helper as helper
import common.phot_helper
from common.rms_filter import rms_cut
import models.image as image
import logging


# Combine photometry takes all the phot_table_chan*.npy files and combines the tables into a single table
# for the specific data cube. Several additional columns are added to allow for further storing information
# about the specific data cubes. The added columns are id, field, edge, overlap, overlap_id, si_m, si_m_point_num,
# xi, overlap_mask, and pvalue which are used in other programs.

# Input required:
# path: This is asking for the location where your data is stored. In our example, Example/test_data/ it wants
# the location of test_data as that folder should contain Mosaic_Planes and Mom0_comp_catalogs.


def calc_xi_squared(spec_index_arr, spec_index_fit):
    xi = chisquare(np.float64(spec_index_arr), f_exp=np.float64(spec_index_fit))

    return xi


# noinspection PyTupleAssignmentBalance
def si_fit(table, freq_list):
    for j in range(len(table['chan01'])):
        temp_array = np.zeros(14)
        temp_array_err = np.zeros(14)
        temp_array[:] = np.nan
        temp_array_err[:] = np.nan

        # Create a temporary array
        for i in range(14):
            # This is getting the jth row value of column channel i
            temp_array[i] = table.columns['chan' + "{:02d}".format(i + 1)][j]
            temp_array_err[i] = table.columns['chan' + "{:02d}".format(i + 1) + 'err'][j]

        if len(temp_array[~np.isnan(temp_array)]) >= 5:
            # Fit to the aperture photometry
            m, b = np.polyfit(np.log10(freq_list[~np.isnan(temp_array)]),
                              np.log10(temp_array[~np.isnan(temp_array)]), 1)
            line_fit = m * np.log10(freq_list[~np.isnan(temp_array)]) + b
            xi = calc_xi_squared(np.log10(temp_array[~np.isnan(temp_array)]), line_fit)

            table['si_m'][j] = m
            table['xi'][j] = xi[0]
            table['pvalue'][j] = xi[1]
            table['si_point_num'][j] = len(temp_array[~np.isnan(temp_array)])

    return table


def correct_phot(phot):
    # This is correcting the photometry for the beam size. The correction is
    # 1.033* FWHM^2, with the FWHM value in pixel coordinates. The FWHM is 0.0022.
    correction_val = 1.0133 * np.square(5.308)
    corrected_phot = phot / correction_val

    return corrected_phot


def begin_combine(path):
    data_cube = image.Image(path)

    if path[-1] != '/':
        path = path + '/'

    for i in range(14):
        phot_table = common.phot_helper.load_phot_table(path + f'phot_table_chan{i + 1:02d}.npy')
        phot_table['aperture_sum'] = correct_phot(phot_table['aperture_sum'])
        if i == 0:
            shape = len(phot_table['aperture_sum'])
            full_table = helper.make_table(shape)
            full_table[f'chan{i + 1:02d}'] = phot_table['aperture_sum']
            full_table[f'chan{i + 1:02d}' + 'err'] = phot_table['aperture_sum_err']
        else:
            full_table[f'chan{i + 1:02d}'] = phot_table['aperture_sum']
            full_table[f'chan{i + 1:02d}' + 'err'] = phot_table['aperture_sum_err']

    full_table.write(f'{path + data_cube.folder_name}_full_table.vot', format='votable', overwrite=True)
    np.save(f'{path + data_cube.folder_name}_full_table', full_table, allow_pickle=True, fix_imports=True)

    cut_num, full_table = rms_cut(data_cube, full_table)
    full_table['field'] = data_cube.folder_name
    full_table['edge'] = False
    full_table['overlap'] = np.nan
    full_table['overlap_mask'] = False
    full_table['xi'] = np.nan
    frequency_list = np.empty(14)

    for i in range(14):
        frequency_list[i] = data_cube.channels[i].frequency

    full_table['si_m'] = np.nan
    # Fits the photometry points and calculates a spectral index
    full_table = si_fit(full_table, frequency_list)

    full_table.write(f'{path + data_cube.folder_name}_full_table_cut.vot', format='votable', overwrite=True)
    np.save(f'{path + data_cube.folder_name}_full_table_cut', full_table, allow_pickle=True, fix_imports=True)
    logging.info(f'Combined and RMS/Error cut photometry tables written to {path} as'
                 f'{data_cube.folder_name}_full_table_cut')
