from unittest import TestCase
import common.data_checks as checks
import common.image as image
import logging
from app_logging import logger


class TestChecks(TestCase):
    location = '/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx'
    logger.init(logging.DEBUG, '.', 'app_logging')

    def test_process_channels_check(self):
        all_lists_check, backgrounds, channels_list = checks.check_lists(self.location)
        total_channels = len(channels_list)

        existing_channels, phot_exist = checks.process_channels_check(self.location, channels_list,
                                                                      total_channels, backgrounds, phot_lookup=False)

        self.assertFalse(phot_exist)
        self.assertEquals([0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13], existing_channels)

        existing_channels, phot_exist = checks.process_channels_check(self.location, channels_list,
                                                                      total_channels, backgrounds)
        self.assertTrue(phot_exist)

    def test_check_lists(self):
        all_lists_check, back_list, channels_list = checks.check_lists(self.location)
        self.assertIs(True, all_lists_check)

        all_lists_check, back_list, channels_list = checks.check_lists('/Users/bs19aam/Documents/test_data'
                                                                       '/Mosaic_Planes/Empty')
        self.assertIs(False, all_lists_check)
