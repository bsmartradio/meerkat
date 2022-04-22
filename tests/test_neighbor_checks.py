from unittest import TestCase
from unittest.mock import patch, MagicMock
import common.neighbor_checks as n_checks
import numpy as np


class TestNeighborChecks(TestCase):

    def test_check_overlap(self):
        mock_table = MagicMock()
        location = 'test/location'
        name = 'testname'
        mock_table['a'].data = np.array([1, 2])
        mock_table['b'].data = np.array([1, 2])
        mock_table['pa'].data = np.array([1, 2])
        mock_table['lon'].data = np.array([1, 2])
        mock_table['lat'].data = np.array([1, 2])
        mock_overlap = [False, False]
        mock_full_table = {'overlap': mock_overlap}

        with patch('matplotlib.pyplot.plot', return_value=None):
            with patch('matplotlib.pyplot.savefig', return_value=None):
                with patch('common.neighbor_checks.intersections', return_value=[1, 2]):
                    test_overlap = n_checks.check_overlap(mock_table, mock_full_table, location, name)

        self.assertTrue(test_overlap['overlap'][0])
        self.assertTrue(test_overlap['overlap'][1])
