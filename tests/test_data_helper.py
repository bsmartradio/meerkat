from unittest import TestCase

import common.data_checks
import common.data_helper as helper


class TestChannel(TestCase):

    def test_get_name(self):
        name = helper.get_name('/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx')
        self.assertEqual('G282.5-0.5IFx', name)
        name = helper.get_name('/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/')
        self.assertEqual('G282.5-0.5IFx', name)

    def test_find_backgrounds(self):
        background_list=helper.find_backgrounds('/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx',
                                                background=True)
        rms_list = helper.find_backgrounds('/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx',
                                                  rms=True)
        self.assertEqual(14, len(rms_list))
        for rms in rms_list:
            self.assertIn('rms.fits', rms)
        self.assertEqual(14, len(background_list))
        for background in background_list:
            self.assertIn('bkg.fits', background)

    def test_find_lists(self):
        channels_list, back_list, vot_table, all_lists_check = common.data_checks.check_lists('/Users/bs19aam/Documents/test_data'
                                                                                 '/Mosaic_Planes/G282.5-0.5IFx')
        self.assertIs(True, all_lists_check)

        channels_list, back_list, vot_table, all_lists_check = common.data_checks.check_lists('/Users/bs19aam/Documents/test_data'
                                                                                 '/Mosaic_Planes/Empty')
        self.assertIs(False, all_lists_check)
