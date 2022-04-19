import common.data_helper as helper
import glob
import numpy as np


# The purpose of this program is gather all the vot files for
# both aegean and for the photometry tables and
# assign an ID to them. ID numbers will be present in both the aegean vot tables after this and the
# photometry tables. This needs to be done prior to running the neighbor
# program so that the neighbor ID's can be assigned when matching sources. Without it, neighbors will
# give an empty assignment to matching sources. When run, the program will look at the tables named with the
# lowest longitude first and work its way up.

# Input keywords
# data_location: This is asking for the location where your data is stored. In our example, it wants test_data,
# which contains the sub folders Mosaic_Planes and Mosaic_Mom0_catalogs.
# Full_table - This is when we are processing all the MeerKAT vot tables
# sub_table = sub table reads in a file which lists the exact tables which are
# being processed. This is for when someone may want to only look at a small
# subset or is creating a limited area table

def get_vot_list(location, aegean=False):

    if aegean:
        vot_list = sorted(glob.glob(location+"Mom0_comp_catalogs/*Mosaic_Mom0_comp.vot"))
    else:
        vot_list = sorted(glob.glob(location+"Mosaic_Planes/G*/*full_table_cut.vot"))

    return vot_list


def assign(num, table_name, aegean=False):

    table = helper.read_info(table_name)
    table.mask = False
    id_present= False

    if aegean:
        shape = len(table['source'])
        if not table['id'].any():
            labeled_table = helper.make_table(shape, aegean=True, table_type=table)
        else:
            labeled_table = helper.make_table(shape, aegean=True, table_type=table)
            print('Id already column present in table')
            id_present = True
    else:
        shape = len(table['id'])
        if not table['id'].any():
            labeled_table = helper.make_table(shape)
        else:
            labeled_table = helper.make_table(shape)
            print('Id column already  present in table')
            id_present = True

    for i in range(shape):
        if aegean and not id_present:
            for j in range(len(table[0])):
                labeled_table[i][j+1] = table[i][j]
        else:
            if len(table[i]) != len(labeled_table[i]):
                print('uhoh')
            labeled_table[i] = table[i]
    for i in range(len(table)):
        labeled_table['id'][i] = i+num

    print(table_name)
    print(labeled_table['id'][0])

    if aegean:
        image_name = helper.get_name(table_name)
        labeled_table['field'] = image_name
        labeled_table.write(f'{table_name}', format='votable', overwrite=True)
        #The 0:-4 is needed as otherwise the table will save as .vot.npy which we do not want.
        np.save(f'{table_name[0:-4]}', labeled_table, allow_pickle=True, fix_imports=True)
        print('Aegean Files')
    else:
        image_name = helper.get_name(table_name)
        labeled_table['field'] = image_name
        labeled_table.write(f'{table_name}', format='votable', overwrite=True)
        np.save(f'{table_name[0:-4]}', labeled_table, allow_pickle=True, fix_imports=True)

    if not i:
        print('Something went wrong, table was not looped through')
        exit()

    last_id = num+i
    return last_id


if __name__ == "__main__":

    location = '/Users/bs19aam/Documents/test_data/'

    vot_list = helper.get_vot_list(location)

    last_id = None

    for i, vot_name in enumerate(vot_list):

        if i == 0:
            last_id = assign(0, vot_name)
        else:
            last_id = assign(last_id, vot_name)

        print(f"The last ID assigned for {vot_name} is {last_id}")

    vot_list = get_vot_list(location, aegean=True)

    for i, vot_name in enumerate(vot_list):

        if i == 0:
            last_id = assign(0, vot_name, aegean=True)
        else:
            last_id = assign(last_id, vot_name, aegean=True)

        print(f"The last ID assigned for {vot_name} is {last_id}")
