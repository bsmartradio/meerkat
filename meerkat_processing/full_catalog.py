import glob
import common.data_helper as helper
import numpy as np


def get_vots(location):
    vot_list = sorted(glob.glob(location + "*_Mosaic_Mom0_comp.vot+id"))
    for i in range(len(vot_list)):

        # Makes the initial table and then fills it in
        if i == 0:
            table = helper.read_vot(vot_list[i])
            shape = len(table.array)
            full_table = helper.make_table(shape, aegean=True, table_type=table.array)

            for i in range(shape):
                full_table[i] = table.array[i]

        else:
            table = helper.read_vot(vot_list[i])

            for i in range(len(table.array)):
                full_table.add_row(table.array[i])

    return full_table


def get_all_phots(location):
    phot_list = sorted(glob.glob(location + "G*/*_full_table_cut.vot"))

    for i in range(len(phot_list)):

        # Makes the initial table and then fills it in
        if i == 0:
            table = helper.load_phot_table(phot_list[i])
            shape = len(table.array)
            full_table = helper.make_table(shape)

            for i in range(shape):
                full_table[i] = table.array[i]

        # Takes the other tables and concats them onto the end to create one single table
        else:
            table = helper.load_phot_table(phot_list[i])

            for i in range(len(table.array)):
                full_table.add_row(table.array[i])

    return full_table


def begin_full_catalog(path):

    if path[-1] != '/':
        path = path+'/'

    vot_location = path + 'Mom0_comp_catalogs/'
    phot_location = path + 'Mosaic_Planes/'
    full_table = get_all_phots(phot_location)

    for i in range(14):
        for j in range(len(full_table)):
            if full_table['chan' + '{:02d}'.format(i + 1)][j] == 0:
                full_table['chan' + '{:02d}'.format(i + 1)][j] = np.nan

    for i in range(14):
        for j in range(len(full_table)):
            if full_table['si_point_num'][j] == -2147483648:
                full_table['si_point_num'][j] = np.nan

    for i in range(14):
        for j in range(len(full_table)):
            if full_table['overlap'][j] == 1:
                full_table['overlap'][j] = np.nan

    full_table.write(f'{phot_location}MeerKAT_full_phot_catalog.vot', format='votable', overwrite=True)
    full_table_vot = get_vots(vot_location)
    full_table_vot.write(f'{vot_location}MeerKAT_full_Aegean_catalog.vot', format='votable', overwrite=True)
