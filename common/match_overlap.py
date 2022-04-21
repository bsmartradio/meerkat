import common.neighbor_checks as n_checks
import numpy as np


def match_overlap(data_cubes, lon_range, all_overlapping_points):
    # This marks all the sources in the left image that overlap between the center and left image
    all_overlapping_points.left.overlap_coordinates, all_overlapping_points.left.overlap_index = \
        n_checks.overlap_check(data_cubes[0].vot_table, lon_range[1], lon_range[0])

    # This marks all the sources in the center image that overlap between the center and left image
    all_overlapping_points.center_left.overlap_coordinates, all_overlapping_points.center_left.overlap_index = \
        n_checks.overlap_check(data_cubes[1].vot_table, lon_range[0], lon_range[1])

    # This marks all the sources in the right image that overlap between the center and right image
    all_overlapping_points.right.overlap_coordinates, all_overlapping_points.right.overlap_index = \
        n_checks.overlap_check(data_cubes[2].vot_table, lon_range[1], lon_range[2])

    # This marks all the sources in the center image that overlap between the center and right image
    all_overlapping_points.center_right.overlap_coordinates, all_overlapping_points.center_right.overlap_index = \
        n_checks.overlap_check(data_cubes[1].vot_table,lon_range[2],lon_range[1])

    return all_overlapping_points


def match_duplicates(neigh_cubes, min_res):
    for n_index, lon in enumerate(neigh_cubes.left.overlap_coordinates[0]):
        close_points = []
        center_point_index = []
        val_check = -1
        lat = neigh_cubes.left.overlap_coordinates[1][n_index]

        for c_index, cent_lon in enumerate(neigh_cubes.center_left.overlap_coordinates[0]):

            if lon - min_res <= cent_lon <= lon + min_res:
                close_points.append([cent_lon, neigh_cubes.center_left.overlap_coordinates[1][c_index]])
                center_point_index.append(c_index)
                val_check = 0

        if close_points != [] and val_check != -1:
            close_points = np.array(close_points)
            minimum = min(np.sqrt(np.square(close_points[:, 0] - lon) + np.square(close_points[:, 1] - lat)))

            nearest_point_index = \
                np.where(np.sqrt(np.square(close_points[:, 0] - lon) + np.square(close_points[:, 1]
                                                                                 - lat)) == minimum)[0]

            neigh_cubes.center_left.distance.append(minimum)
            neigh_cubes.left.distance.append(minimum)
            neigh_cubes.center_left.matched_index.append(center_point_index[nearest_point_index[0]])
            neigh_cubes.left.matched_index.append(n_index)

        else:
            neigh_cubes.left.nomatch.append(n_index)

    for n_index, lon in enumerate(neigh_cubes.right.overlap_coordinates[0]):
        close_points = []
        center_point_index = []
        val_check = -1
        lat = neigh_cubes.right.overlap_coordinates[1][n_index]

        for c_index, cent_lon in enumerate(neigh_cubes.center_right.overlap_coordinates[0]):

            if lon - min_res <= cent_lon <= lon + min_res:
                close_points.append([cent_lon, neigh_cubes.center_right.overlap_coordinates[1][c_index]])
                center_point_index.append(c_index)
                val_check = 0

        if close_points != [] and val_check != -1:
            close_points = np.array(close_points)
            minimum = min(np.sqrt(np.square(close_points[:, 0] - lon) + np.square(close_points[:, 1] - lat)))

            nearest_point_index = \
                np.where(np.sqrt(np.square(close_points[:, 0] - lon) + np.square(close_points[:, 1]
                                                                                 - lat)) == minimum)[0]

            neigh_cubes.center_right.distance.append(minimum)
            neigh_cubes.right.distance.append(minimum)
            neigh_cubes.center_right.matched_index.append(center_point_index[nearest_point_index[0]])
            neigh_cubes.right.matched_index.append(n_index)

        else:
            neigh_cubes.right.nomatch.append(n_index)

    return neigh_cubes
