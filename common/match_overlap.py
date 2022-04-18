import common.neighbor_checks as n_checks

def match_overlap(data_cubes,lon_range, all_n):


    all_n.overlap_lon_neighbor, all_n.overlap_lat_neighbor, all_n.overlap_index_neighbor = n_checks.overlap_check(data_cubes[1].vot_table,
                                                                                                data_cubes[0].vot_table,
                                                                                                all_n.overlap_lon_neighbor,
                                                                                                all_n.overlap_lat_neighbor,
                                                                                                all_n.overlap_index_neighbor,
                                                                                                lon_range[1],
                                                                                                lon_range[0])
    all_n.overlap_lon_neighbor, all_n.overlap_lat_neighbor, all_n.overlap_index_neighbor = n_checks.overlap_check(data_cubes[1].vot_table,
                                                                                                data_cubes[2].vot_table,
                                                                                                all_n.overlap_lon_neighbor,
                                                                                                all_n.overlap_lat_neighbor,
                                                                                                all_n.overlap_index_neighbor,
                                                                                                lon_range[1],
                                                                                                lon_range[2])

    all_n.overlap_lon_center, all_n.overlap_lat_center, all_n.overlap_index_center = n_checks.overlap_check(data_cubes[0].vot_table,
                                                                                          data_cubes[1].vot_table,
                                                                                          all_n.overlap_lon_center,
                                                                                          all_n.overlap_lat_center,
                                                                                          all_n.overlap_index_center,
                                                                                          lon_range[0],
                                                                                          lon_range[1])
    all_n.overlap_lon_center, all_n.overlap_lat_center, all_n.overlap_index_center = n_checks.overlap_check(data_cubes[2].vot_table,
                                                                                          data_cubes[1].vot_table,
                                                                                          all_n.overlap_lon_center,
                                                                                          all_n.overlap_lat_center,
                                                                                          all_n.overlap_index_center,
                                                                                          lon_range[2],
                                                                                          lon_range[1])

    return all_n