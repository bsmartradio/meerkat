from astropy.io.votable import parse
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from meerMod import *
import numpy as np
from astropy.table import QTable, Table, Column
import glob
from astropy.io.votable import from_table, writeto

# The purpose of this program is gather all the vot files for
# both aegean and for the photometry tables and
# assign an ID to them. This needs to be done prior to running the neighbor
# program so that the neighbor ID's can be assigned.

# Input keywords
# Full_table - This is when we are processing all of the MeerKAT vot tables
# sub_tale = sub table reads in a file which lists the exact tables which are
# being processed. This is for when someone may want to only look at a small
# subset or is creating a limited area table

def get_vot_list(location, aegean=False):

    if aegean:
        vot_list = sorted(glob.glob(location+"Mom0_comp_catalogs/*Mosaic_Mom0_comp.vot"))
    else:
        vot_list = sorted(glob.glob(location+"Mosaic_Planes/G*/*full_table_cut.vot"))

    return vot_list


def make_table(shape, aegean=False, table_type=[]):

    if aegean:
        dtype = np.dtype([('id', 'int32')] + table_type.dtype.descr)
    else:

        dtype = [('id', 'int32'), ('field', 'object'),
                 ('chan01', 'float64'), ('chan01err', 'float64'),
                 ('chan02', 'float64'), ('chan02err', 'float64'),
                 ('chan03', 'float64'), ('chan03err', 'float64'),
                 ('chan04', 'float64'), ('chan04err', 'float64'),
                 ('chan05', 'float64'), ('chan05err', 'float64'),
                 ('chan06', 'float64'), ('chan06err', 'float64'),
                 ('chan07', 'float64'), ('chan07err', 'float64'),
                 ('chan08', 'float64'), ('chan08err', 'float64'),
                 ('chan09', 'float64'), ('chan09err', 'float64'),
                 ('chan10', 'float64'), ('chan10err', 'float64'),
                 ('chan11', 'float64'), ('chan11err', 'float64'),
                 ('chan12', 'float64'), ('chan12err', 'float64'),
                 ('chan13', 'float64'), ('chan13err', 'float64'),
                 ('chan14', 'float64'), ('chan14err', 'float64'),
                 ('si_m', 'float64'),('si_point_num', 'int32'),
                 ('xi', 'float64'),('pvalue', 'float64'),
                 ('overlap', 'float64'), ('overlap_field', 'object'),
                 ('edge', 'bool'), ('overlap_mask', 'bool')]
    full_table = Table(data=np.zeros(shape, dtype=dtype))
    return full_table


def assign(num, table_name, aegean=False):

    table = read_info(table_name)
    table.mask = False

    if aegean:
        shape = len(table['source'])
        labeled_table = make_table(shape,aegean=True, table_type=table)
    else:
        shape = len(table['id'])
        labeled_table = make_table(shape)

    for i in range(shape):
        if aegean:
            for j in range(len(table[0])):
                labeled_table[i][j+1] = table[i][j]
        else:
            labeled_table[i] = table[i]
    for i in range(len(table)):
        labeled_table['id'][i] = i+num

    print(table_name)
    print(labeled_table['id'][0])

    if aegean:
        image_name = get_name(table_name)
        labeled_table['field'] = image_name
        labeled_table.write(f'{table_name}+id', format='votable', overwrite=True)
        print('Aegean Files')
    else:
        image_name = get_name(table_name)
        labeled_table['field'] = image_name
        labeled_table.write(f'{table_name}', format='votable', overwrite=True)
    #full_table.to_xml('table_name')
    last_id = num+i
    return last_id

location = '/beegfs/car/bsmart/MeerKAT/'

vot_list = get_vot_list(location)

for i, vot_name in enumerate(vot_list):

    if i == 0:
        last_id = assign(0, vot_name)
    else:
        last_id = assign(last_id, vot_name)

    print(last_id)

vot_list = get_vot_list(location, aegean=True)

for i, vot_name in enumerate(vot_list):

    if i == 0:
        last_id = assign(0, vot_name, aegean=True)
    else:
        last_id = assign(last_id, vot_name, aegean=True)

    print(last_id)
