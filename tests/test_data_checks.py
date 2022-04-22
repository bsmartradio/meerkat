from unittest import TestCase
from unittest.mock import patch
import common.data_checks as checks
import numpy as np


class TestChecks(TestCase):
    location = 'Example/Mosaic_Planes/G282.5-0.5IFx'

    def test_process_channels_check_phot_lookup_False(self):
        total_channels = 14
        backgrounds = ['chan01_bkg.fits', 'chan02_bkg.fits', 'chan03_bkg.fits', 'chan04_bkg.fits', 'chan05_bkg.fits',
                       'chan06_bkg.fits', 'chan07_bkg.fits', 'chan08_bkg.fits', 'chan09_bkg.fits', 'chan10_bkg.fits',
                       'chan11_bkg.fits', 'chan12_bkg.fits', 'chan13_bkg.fits', 'chan14_bkg.fits']
        channels_list = ['_chan01.fits', '_chan02.fits', '_chan03.fits', '_chan04.fits', '_chan05.fits', '_chan06.fits',
                         '_chan07.fits', '_chan08.fits', '_chan09.fits', '_chan10.fits', '_chan11.fits', '_chan12.fits',
                         '_chan13.fits', '_chan14.fits']
        mock_image = np.array([[[1], [2], [3]], [[1], [2], [3]]])

        with patch('os.path.isfile', return_value=True):
            with patch('common.data_helper.get_image', return_value=mock_image):
                existing_channels, phot_exist = checks.process_channels_check(self.location, channels_list,
                                                                              total_channels, backgrounds,
                                                                              phot_lookup=False)

        self.assertFalse(phot_exist)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], existing_channels)

    def test_check_required_files_exist(self):
        mock_files = ['1', '3', '2']
        with patch('glob.glob', return_value=mock_files):
            all_lists_check, back_list, channels_list = checks.check_required_files_exist(self.location)
            self.assertIs(True, all_lists_check)
            self.assertEquals(['1', '2', '3'], back_list)
            self.assertEquals(['1', '2', '3'], channels_list)

    def test_check_required_files_do_not_exist(self):
        with patch('glob.glob', return_value=[]):
            all_lists_check, back_list, channels_list = checks.check_required_files_exist('test/path')
            self.assertIs(False, all_lists_check)
