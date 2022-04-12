from unittest import TestCase
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

        self.assertCountEqual()