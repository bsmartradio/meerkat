from unittest import TestCase
from unittest.mock import patch

import common.data_checks as checks
import common.image as image


class TestChecks(TestCase):
    location = '/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx'

    def test_process_channels_check(self):
        all_lists_check, backgrounds, channels_list = checks.check_required_files_exist(self.location)
        total_channels = len(channels_list)

        existing_channels, phot_exist = checks.process_channels_check(self.location, channels_list,
                                                                      total_channels, backgrounds, phot_lookup=False)

        self.assertFalse(phot_exist)
        self.assertEquals([0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13], existing_channels)

    def test_check_required_files_exist(self):
        all_lists_check, back_list, channels_list = checks.check_required_files_exist(self.location)
        self.assertIs(True, all_lists_check)

    def test_check_required_files_do_not_exist(self):
        with patch('glob.glob', return_value=[]):
            all_lists_check, back_list, channels_list = checks.check_required_files_exist('test/path')
            self.assertIs(False, all_lists_check)
