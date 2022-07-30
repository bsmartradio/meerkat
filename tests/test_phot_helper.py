from unittest import TestCase
from unittest.mock import patch
import common.phot_helper as phot_helper


class TestPhotHelper(TestCase):

    def test_load_phot_table(self):
        mock_phot = 'test_phot'
        mock_name = 'testname'

        with patch('numpy.load', return_vaue=mock_phot):
            test_phot = phot_helper.load_phot_table(mock_name)

        self.assertIsNotNone(test_phot)

    def test_get_chan_list(self):
        mock_location = 'file_one'

        with patch('glob.glob', return_value=['chan01', 'chan02']):
            test_channel_list = phot_helper.get_chan_list(mock_location)

        self.assertIsNotNone(test_channel_list)
        self.assertEqual(2, len(test_channel_list))
