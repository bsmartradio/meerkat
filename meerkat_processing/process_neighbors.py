import numpy as np
import argparse
import common.data_helper as helper
import common.image as image
import common.neighbor_checks as n_checks
import common.match_overlap as n_match
import common.build_neighbors as build
import plotting_tools.neighbor_channels as n_plot

# The purpose of this program is to take neighboring cubes from MeerKAT and the Aegean
# source catalogues and identify overlapping sources, then check how well the sources
# match each other positionally and how close their photometry output is

# A catalogue of matching points is made, then a table of how well each channel matches is created
# Input - The input requires the location of the Mosaic Planes. If using the standard file structure,
# the files will be location in Mosaic_Planes.
# It then requires the names of 3 different cubes to be compared.
# Generally, when used in the pipelines, the cubes will be read in via the jobSubmitter_Compare.py,
# however it is possible to use individually as long as three neighboring cubes are provided.

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Must have folder location')
    parser.add_argument("--folder_one")
    parser.add_argument("--folder_two")
    parser.add_argument("--folder_three")

    args = parser.parse_args()

    if not args.folder_one:
        print("Must have folder locations. Please include --folder_one='filepath',--folder_two='filepath',"
              "--folder_three='filepath'")
        exit()

    folder_one = args.folder_one
    folder_two = args.folder_two
    folder_three = args.folder_three

    min_res = 0.00222222 / 4.0

    folder = [folder_one, folder_two, folder_three]

    data_cubes = [image.Image(folder_one), image.Image(folder_two), image.Image(folder_three)]

    phot_tables = []
    for i in range(3):
        phot_tables.append(helper.load_phot_table(folder[i] + '/' + data_cubes[i].folder_name + '_full_table_cut.npy'))

    lon_range = np.empty([3, 2])
    lon_range[:] = np.nan

    # Get all the min and max of the longitudes for each cube here
    for i in range(3):
        min_lon, max_lon = helper.minmax_coord(data_cubes[i].channels[0].header)
        lon_range[i, 0] = min_lon
        lon_range[i, 1] = max_lon

    # Check if a point is too close to the edge and mark here
    phot_tables = n_checks.check_edge_points(data_cubes, phot_tables, lon_range)

    # Finds and labels all of the sources that should appear in both neighboring images
    all_neighbors = build.Neighbors()
    all_neighbors = n_match.match_overlap(data_cubes, lon_range, all_neighbors)

    neighbor_match = []
    center_match = []
    neighbor_nomatch = []

    # I am matching the overlapping points here. In here, when I select the one matching point, the corresponding
    # value in phot list must be switched to overlapping point, as well as the overlapping field + ID value

    for x in range(2):
        matched_index_neighbor = []
        nomatch_center = []
        nomatch_neighbor = []
        matched_index_center = []
        distance_arr = []
        for idx_first, lon in enumerate(all_neighbors.overlap_lon_neighbor[x]):
            close_points_lon = []
            close_points_lat = []
            index_close = []
            val_check = -1
            lat = all_neighbors.overlap_lat_neighbor[x][idx_first]
            for idx_second, m in enumerate(all_neighbors.overlap_lon_center[x]):
                if lon - min_res <= m <= lon + min_res:
                    close_points_lon.append(m)
                    close_points_lat.append(all_neighbors.overlap_lat_center[x][idx_second])
                    index_close.append(idx_second)
                    val_check = 0
            if close_points_lon != [] and val_check != -1:
                # Pretty sure the match happens here
                minimum = min(np.sqrt(np.square(close_points_lon - lon) + np.square(close_points_lat - lat)))
                close_index = \
                    np.where(np.sqrt(np.square(close_points_lon - lon) + np.square(close_points_lat - lat)) == minimum)[
                        0]
                print('Close index')
                print(index_close[close_index[0]])
                distance_arr.append(minimum)
                matched_index_center.append(index_close[close_index[0]])
                matched_index_neighbor.append(idx_first)

            else:
                nomatch_neighbor.append(idx_first)

        neighbor_match.append(matched_index_neighbor)
        neighbor_nomatch.append(nomatch_neighbor)
        center_match.append(matched_index_center)

    for i in range(2):
        for j, name in enumerate(center_match[i]):
            if i == 0:
                phot_tables[0]['overlap'][all_neighbors.overlap_index_neighbor[0][0][neighbor_match[i][j]]] = \
                    phot_tables[1]['id'][
                        all_neighbors.overlap_index_center[i][0][center_match[i][j]]]
                phot_tables[0]['overlap_field'][all_neighbors.overlap_index_neighbor[0][0][neighbor_match[i][j]]] = \
                    phot_tables[1]['field'][0]
                phot_tables[1]['overlap'][all_neighbors.overlap_index_center[0][0][center_match[i][j]]] = \
                    phot_tables[0]['id'][
                        all_neighbors.overlap_index_neighbor[i][0][neighbor_match[i][j]]]
                phot_tables[1]['overlap_field'][all_neighbors.overlap_index_center[0][0][center_match[i][j]]] = \
                    phot_tables[0]['field'][0]
                phot_tables[1]['overlap_mask'][all_neighbors.overlap_index_center[0][0][center_match[i][j]]] = True
            else:
                phot_tables[2]['overlap'][all_neighbors.overlap_index_neighbor[i][0][neighbor_match[i][j]]] = \
                    phot_tables[1]['id'][
                        all_neighbors.overlap_index_center[i][0][center_match[i][j]]]
                phot_tables[2]['overlap_field'][all_neighbors.overlap_index_neighbor[i][0][neighbor_match[i][j]]] = \
                    phot_tables[1]['field'][0]
                phot_tables[1]['overlap'][all_neighbors.overlap_index_center[1][0][center_match[i][j]]] = \
                    phot_tables[2]['id'][
                        all_neighbors.overlap_index_neighbor[i][0][neighbor_match[i][j]]]
                phot_tables[1]['overlap_field'][all_neighbors.overlap_index_center[1][0][center_match[i][j]]] = \
                    phot_tables[2]['field'][0]
                phot_tables[2]['overlap_mask'][all_neighbors.overlap_index_neighbor[i][0][neighbor_match[i][j]]] = True


    valuesArr = []
    for channel in range(14):
        val_list = []
        for x in range(2):
            x_line = np.linspace(0, 2, 100)
            print(f'Values for {channel}')
            values = []
            values2 = []
            for n in range(len(center_match[x])):
                values.append(
                    phot_tables[1]['chan' + '{:02d}'.format(channel + 1)][
                        all_neighbors.overlap_index_center[x][0][center_match[x][n]]])
                values2.append(phot_tables[0 + x * 2]['chan' + '{:02d}'.format(channel + 1)][
                                   all_neighbors.overlap_index_neighbor[x][0][neighbor_match[x][n]]])
            # Skips the empty planes
            if np.isnan(values).all() is True and np.isnan(values2).all() is True:
                print('No values')
            else:
                # This checks both arrays at the same time.
                # This one is the left one
                # They contain the good matches, all the values, and a separate list of matches  that are bad
                if x == 0:
                    val_list[0:] = [values, ]
                    val_list[1:] = [values2, ]
                    matchedArr = n_checks.fit_deviation(values, values2)
                    val_list[2:] = [matchedArr, ]

                    outliers = np.where(abs(matchedArr) >= 0.15)
                    val_list[3:] = [outliers, ]
                # This is the rightmost image
                else:
                    print(channel)
                    val_list[4:] = [values, ]
                    val_list[5:] = [values2, ]
                    matchedArr = n_checks.fit_deviation(values, values2)
                    val_list[6:] = [matchedArr, ]

                    outliers = np.where(abs(matchedArr) >= 0.15)
                    val_list[7:] = [outliers, ]

    for i in range(3):
        shape = len(phot_tables[i]['id'])
        full_table = helper.make_table(shape)
        for j in range(shape):
            full_table[j] = phot_tables[i][j]
        full_table.write(f'{folder[i]}/{data_cubes[i].folder_name}_full_table_cut.vot', format='votable',
                         overwrite=True)
        np.save(f'{folder[i]}/{data_cubes[i].folder_name}_full_table_cut', full_table,
                allow_pickle=True, fix_imports=True)

    n_plot.all_sources(data_cubes)
    n_plot.plot_channels(data_cubes, all_neighbors.overlap_index_center, all_neighbors.overlap_index_neighbor, val_list)