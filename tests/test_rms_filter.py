from common.rms_filter import rms_cut
from unittest import TestCase
from unittest.mock import patch, MagicMock
import common.data_helper as helper
import numpy as np


class TestRmsFilter(TestCase):

    def test_rms_filter(self):
        mock_data_cube = MagicMock()
        mock_full_table = helper.make_table(10)
        mock_full_table['chan01'] = 4.6
        mock_full_table['chan02'] = .01
        mock_full_table['chan03'] = 10.0
        mock_nan_result = MagicMock()
        mock_nan_result.all.return_value = False

        with patch('numpy.isnan', return_value=mock_nan_result):
            with patch('numpy.nanmean', return_value=.3):
                total_cut, full_table = rms_cut(mock_data_cube, mock_full_table)

        self.assertEqual(4.6, full_table['chan01'][0])
        self.assertTrue(np.isnan(full_table['chan02'][0]))
        self.assertEqual(10, total_cut[1])
        self.assertEqual(14, len(total_cut))
