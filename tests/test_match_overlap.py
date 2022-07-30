from unittest import TestCase
import common.match_overlap
import common.data_helper as helper
import numpy as np
from models import neighbors


class TestMatchOverlap(TestCase):

    def test_match_duplicates(self):

        mock_neighbor_sources = neighbors.Neighbors()
        mock_neighbor_sources.left.overlap_coordinates = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
        mock_neighbor_sources.center_left.overlap_coordinates = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
        mock_neighbor_sources.center_left.overlap_index = [[[1, 2, 3, 4]]]
        mock_neighbor_sources.right.overlap_index = [[[1, 2, 3, 4]]]
        mock_neighbor_sources.right.overlap_coordinates = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
        mock_neighbor_sources.center_right.overlap_coordinates = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
        mock_neighbor_sources.center_right.overlap_index = [[[1, 2, 3, 4]]]
        mock_neighbor_sources.left.overlap_index = [[[1, 2, 3, 4]]]
        mock_phot_tables=[helper.make_table(10),helper.make_table(10),helper.make_table(10)]
        mock_phot_tables[0]['id']= 1
        mock_phot_tables[1]['id'] = 2
        mock_phot_tables[2]['id'] = 3
        mock_min_res = .3

        neighbor_sources, phot_tables = common.match_overlap.match_duplicates(mock_neighbor_sources,
                                                                              mock_phot_tables, mock_min_res)

        self.assertEqual(2.0, phot_tables[0]['overlap'][0])
        self.assertEqual(0.0, phot_tables[0]['overlap'][9])
