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

    def test_check_lists(self):
        all_lists_check, back_list, channels_list = common.data_checks.check_lists('/Users/bs19aam/Documents/test_data'
                                                                                 '/Mosaic_Planes/G282.5-0.5IFx')
        self.assertIs(True, all_lists_check)

        all_lists_check, back_list, channels_list = common.data_checks.check_lists('/Users/bs19aam/Documents/test_data'
                                                                                 '/Mosaic_Planes/Empty')
        self.assertIs(False, all_lists_check)

    def test_find_channels(self):
        location='/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx'
        channels = helper.find_channels(location)

        self.assertIs(14, len(channels))

    def test_get_vot_list(self):
        location = '/Users/bs19aam/Documents/test_data/'
        vot_list=helper.get_vot_list(location, aegean=True)

        for vot in vot_list:
            self.assertIn('.vot', vot)
