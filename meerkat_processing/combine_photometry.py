from astropy.io.votable import parse
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from numpy import linspace
import glob
from scipy.stats import chisquare
from astropy.visualization import quantity_support
import argparse
import common.data_helper as helper
from common.rms_filter import rms_cut
from shapely.geometry.polygon import LinearRing
import common.image as image

quantity_support()


# For this program, I want to read in the existing tables, check which ones are missing and fill those columns
# with nans

def read_info(single_vot):
    votable = parse(single_vot)
    # Read in the table
    table = votable.get_first_table()
    data = table.array

    return data


def read_info(single_vot):
    votable = parse(single_vot)
    # Read in the table
    table = votable.get_first_table()
    data = table.array

    return data


def get_chan_list(location):
    channel_list = glob.glob(location + "phot_table*.npy")
    return channel_list


def load_phot_table(channel_name):
    phot_table = np.load(channel_name)
    return phot_table


def make_table(shape):
    dtype = [('id', 'int32'), ('field', 'object'), \
             ('chan01', 'float64'), ('chan01err', 'float64'), \
             ('chan02', 'float64'), ('chan02err', 'float64'), \
             ('chan03', 'float64'), ('chan03err', 'float64'), \
             ('chan04', 'float64'), ('chan04err', 'float64'), \
             ('chan05', 'float64'), ('chan05err', 'float64'), \
             ('chan06', 'float64'), ('chan06err', 'float64'), \
             ('chan07', 'float64'), ('chan07err', 'float64'), \
             ('chan08', 'float64'), ('chan08err', 'float64'), \
             ('chan09', 'float64'), ('chan09err', 'float64'), \
             ('chan10', 'float64'), ('chan10err', 'float64'), \
             ('chan11', 'float64'), ('chan11err', 'float64'), \
             ('chan12', 'float64'), ('chan12err', 'float64'), \
             ('chan13', 'float64'), ('chan13err', 'float64'), \
             ('chan14', 'float64'), ('chan14err', 'float64'), \
             ('si_m', 'float64'), ('si_point_num', 'int32'), \
             ('xi', 'float64'), ('pvalue', 'float64'), \
             ('overlap', 'bool'), ('overlap_field', 'object'), \
             ('edge', 'bool')]
    full_table = Table(data=np.zeros(shape, dtype=dtype))
    return full_table


def get_freq(location):
    freq_loc = glob.glob(location + "*freq_list*.npy")
    freq_list = np.load(freq_loc[0])
    return freq_list


def calc_xi_squared(spec_index_arr, spec_index_fit):
    degrees = len(spec_index_arr[np.logical_not(np.isnan(spec_index_arr))])
    xi = chisquare(np.float64(spec_index_arr), f_exp=np.float64(spec_index_fit))

    return xi


def ellipse_polyline(ellipses, n=100):
    t = linspace(0, 2 * np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle in ellipses:
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        p = np.empty((n, 2))
        p[:, 0] = x0 + a * ca * ct - b * sa * st
        p[:, 1] = y0 + a * sa * ct + b * ca * st
        result.append(p)
    return result


def intersections(a, b):
    ea = LinearRing(a)
    eb = LinearRing(b)
    # print(ea,eb)
    mp = ea.intersection(eb)
    if mp.is_empty:
        # print('Geometries do not intersect')
        return [], []
    elif mp.geom_type == 'Point':
        return [mp.x], [mp.y]
    elif mp.geom_type == 'MultiPoint':
        return [p.x for p in mp], [p.y for p in mp]
    else:
        raise ValueError('something unexpected: ' + mp.geom_type)


def check_overlap(table, full_table, location, name):
    a = table['a'].data * 0.000277778
    b = table['b'].data * 0.000277778
    lon = table['lon'].data
    lat = table['lat'].data
    pa = table['pa'].data

    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            ellipses = [(lon[i], lat[i], a[i], b[i], pa[i]), (lon[j], lat[j], a[j], b[j], pa[j])]
            a_out, b_out = ellipse_polyline(ellipses)
            x, y = intersections(a_out, b_out)
            if x != []:
                # print(x)
                full_table['overlap'][i] = True
                full_table['overlap'][j] = True
                plt.plot(x, y, "o")
                plt.plot(a_out[:, 0], a_out[:, 1])
                plt.plot(b_out[:, 0], b_out[:, 1])

    plt.savefig(location + name + 'overlapping_edge.png')
    return full_table


def si_fit(full_table):
    temp_array = np.zeros(14)
    temp_array_err = np.zeros(14)
    temp_array[:] = np.nan
    temp_array_err[:] = np.nan

    for j in range(len(full_table['chan01'])):
        temp_array = np.zeros(14)
        temp_array_err = np.zeros(14)
        temp_array[:] = np.nan
        temp_array_err[:] = np.nan
        # What is going on here?
        for i in range(14):
            # This is getting the jth row value of column channel i
            temp_array[i] = full_table.columns['chan' + "{:02d}".format(i + 1)][j]
            temp_array_err[i] = full_table.columns['chan' + "{:02d}".format(i + 1) + 'err'][j]

        if len(temp_array[~np.isnan(temp_array)]) >= 5:
            m, b = np.polyfit(np.log10(freq_list[~np.isnan(temp_array)]), np.log10(temp_array[~np.isnan(temp_array)]),1)
            line_fit = m * np.log10(freq_list[~np.isnan(temp_array)]) + b
            print(np.log10(temp_array[~np.isnan(temp_array)]))
            print(line_fit)
            xi = calc_xi_squared(np.log10(temp_array[~np.isnan(temp_array)]), line_fit)
            print(xi)
            full_table['si_m'][j] = m
            full_table['xi'][j] = xi[0]
            full_table['pvalue'][j] = xi[1]
            full_table['si_point_num'][j] = len(temp_array[~np.isnan(temp_array)])
    return full_table


def correct_phot(phot):
    # This is correcting the photometry for the beam size. The correction is
    # 1.033* FWHM^2, with the FWHM value in pixel coordiantes. The FWHM is 0.0022.
    correction_val = 1.0133 * np.square(5.308)
    corrected_phot = phot / correction_val

    return corrected_phot

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Must have folder location')
    parser.add_argument("--folder_location")

    args = parser.parse_args()

    if args.folder_location == None:
        print("Must have folder location. Please include --folder_location='filepath'")
        exit()
    location = args.folder_location

    data_cube=image.Image(location)

    for i in range(len(data_cube.channels)):
        phot_table = load_phot_table(location+f'/phot_table_chan{i+1:02d}.npy')
        phot_table['aperture_sum'] = correct_phot(phot_table['aperture_sum'])
        if i == 0:
            shape = len(phot_table['aperture_sum'])
            full_table = make_table(shape)
            full_table[f'chan{i+1:02d}'] = phot_table['aperture_sum']
            full_table[f'chan{i+1:02d}' + 'err'] = phot_table['aperture_sum_err']
            print('First channel')
        else:
            print(f'chan{i+1:02d}')
            full_table[f'chan{i+1:02d}'] = phot_table['aperture_sum']
            full_table[f'chan{i+1:02d}' + 'err'] = phot_table['aperture_sum_err']

    full_table.write(f'{location + data_cube.folder_name}_full_table.vot', format='votable', overwrite=True)

    cut_num, full_table = rms_cut(data_cube, full_table)
    full_table['field'] = data_cube.folder_name
    full_table['edge'] = False
    full_table['overlap'] = np.nan
    full_table['overlap_mask'] = False
    full_table['xi'] = np.nan
    full_table['si_m'] = np.nan
    full_table = si_fit(full_table)
    full_table.write(f'{location + data_cube.folder_name}_full_table_cut.vot', format='votable', overwrite=True)

    np.save(location + data_cube.folder_name + '_full_table_cut', full_table, allow_pickle=True, fix_imports=True)
