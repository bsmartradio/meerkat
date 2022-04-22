import common.neighbor_checks as n_checks
import numpy as np


def match_overlap(data_cubes, lon_range, neighbor_sources):
    # This marks all the sources in the left image that overlap between the center and left image
    neighbor_sources.left.overlap_coordinates, neighbor_sources.left.overlap_index = \
        n_checks.overlap_check(data_cubes[0].vot_table, lon_range[1], lon_range[0])

    # This marks all the sources in the center image that overlap between the center and left image
    neighbor_sources.center_left.overlap_coordinates, neighbor_sources.center_left.overlap_index = \
        n_checks.overlap_check(data_cubes[1].vot_table, lon_range[0], lon_range[1])

    # This marks all the sources in the right image that overlap between the center and right image
    neighbor_sources.right.overlap_coordinates, neighbor_sources.right.overlap_index = \
        n_checks.overlap_check(data_cubes[2].vot_table, lon_range[1], lon_range[2])

    # This marks all the sources in the center image that overlap between the center and right image
    neighbor_sources.center_right.overlap_coordinates, neighbor_sources.center_right.overlap_index = \
        n_checks.overlap_check(data_cubes[1].vot_table, lon_range[2], lon_range[1])

    return neighbor_sources


def match_duplicates(neighbor_sources, phot_tables, min_res):
    for neighbor_index, lon in enumerate(neighbor_sources.left.overlap_coordinates[0]):
        lat = neighbor_sources.left.overlap_coordinates[1][neighbor_index]

        lat_difference = lat - neighbor_sources.center_left.overlap_coordinates[1][:]
        lon_difference = lon - neighbor_sources.center_left.overlap_coordinates[0][:]

        minimum_difference = min(np.sqrt(np.square(lat_difference) + np.square(lon_difference)))

        if minimum_difference < min_res:
            nearest_point = int(
                np.where(np.sqrt(np.square(lat_difference) + np.square(lon_difference)) == minimum_difference)[0])

            center_matched_index = neighbor_sources.center_left.overlap_index[0][0][nearest_point]

            # In the phot tables, fills in the ID to any point that has a match as well as the related cube field.
            phot_tables[0]['overlap'][neighbor_index] = phot_tables[1]['id'][center_matched_index]
            phot_tables[0]['overlap_field'][neighbor_index] = phot_tables[1]['field'][center_matched_index]

            phot_tables[1]['overlap'][center_matched_index] = phot_tables[0]['id'][neighbor_index]
            phot_tables[1]['overlap_field'][center_matched_index] = phot_tables[0]['field'][neighbor_index]

    # Right table fill
    for neighbor_index, lon in enumerate(neighbor_sources.right.overlap_coordinates[0]):
        lat = neighbor_sources.right.overlap_coordinates[1][neighbor_index]

        lat_difference = lat - neighbor_sources.center_right.overlap_coordinates[1][:]
        lon_difference = lon - neighbor_sources.center_right.overlap_coordinates[0][:]

        minimum_difference = min(np.sqrt(np.square(lat_difference) + np.square(lon_difference)))

        if minimum_difference < min_res:
            nearest_point = int(
                np.where(np.sqrt(np.square(lat_difference) + np.square(lon_difference)) == minimum_difference)[0])

            center_matched_index = neighbor_sources.center_right.overlap_index[0][0][nearest_point]

            # In the phot tables, fills in the ID to any point that has a match as well as the related cube field.
            phot_tables[2]['overlap'][neighbor_index] = phot_tables[1]['id'][center_matched_index]
            phot_tables[2]['overlap_field'][neighbor_index] = phot_tables[1]['field'][center_matched_index]

            phot_tables[1]['overlap'][center_matched_index] = phot_tables[2]['id'][neighbor_index]
            phot_tables[1]['overlap_field'][center_matched_index] = phot_tables[2]['field'][neighbor_index]

    return neighbor_sources, phot_tables
