import numpy as np
import common.data_helper as helper
import common.phot_helper
import models.image as image
import common.neighbor_checks as n_checks
import common.match_overlap as n_match
import models.neighbors as build
from plotting_tools import bright_sources
import common.match_overlap as match
import logging

# The purpose of this program is to take neighboring cubes from MeerKAT and the Aegean
# source catalogues and identify overlapping sources, then check how well the sources
# match each other positionally and how close their photometry output is

# A catalogue of matching points is made, then a table of how well each channel matches is created
# Input - The input requires the location of the Mosaic Planes. If using the standard file structure,
# the files will be location in Mosaic_Planes.
# It then requires the names of 3 different cubes to be compared.
# Generally, when used in the pipelines, the cubes will be read in via the jobSubmitter_Compare.py,
# however it is possible to use individually as long as three neighboring cubes are provided.


def begin_neighbors(folder_one, folder_two, folder_three):

    min_res = 0.00222222 / 4.0

    folder = [folder_one, folder_two, folder_three]

    data_cubes = [image.Image(folder_one), image.Image(folder_two), image.Image(folder_three)]

    phot_tables = []

    for i in range(3):
        phot_tables.append(
            common.phot_helper.load_phot_table(folder[i] + '/' + data_cubes[i].folder_name + '_full_table_cut.npy'))

    lon_range = np.empty([3, 2])
    lon_range[:] = np.nan

    # Get all the min and max of the longitudes for each cube here
    for i in range(3):
        min_lon, max_lon = helper.minmax_coord(data_cubes[i].channels[0].header)
        lon_range[i, 0] = min_lon
        lon_range[i, 1] = max_lon

    # Check if a point is too close to the edge and mark here
    phot_tables = n_checks.check_edge_points(data_cubes, phot_tables, lon_range)

    # Finds and labels all the sources that should appear in both neighboring images. This is used
    # to improve readability when matching points shared between cubes
    neighbor_sources = build.Neighbors()
    neighbor_sources = n_match.match_overlap(data_cubes, lon_range, neighbor_sources)

    # Find the closest points within the minimum resolution and updates the phot tables with the ID's and which
    phot_tables = match.match_duplicates(neighbor_sources, phot_tables, min_res)

    # Now that all the neighbor processes have been assigned, write out the updated photometry tables
    for i in range(3):
        shape = len(phot_tables[i]['id'])
        full_table = helper.make_table(shape)
        for j in range(shape):
            full_table[j] = phot_tables[i][j]
        full_table.write(f'{folder[i]}/{data_cubes[i].folder_name}_full_table_cut.vot', format='votable',
                         overwrite=True)
        np.save(f'{folder[i]}/{data_cubes[i].folder_name}_full_table_cut', full_table,
                allow_pickle=True, fix_imports=True)
