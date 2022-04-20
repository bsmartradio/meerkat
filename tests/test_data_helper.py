from unittest import TestCase
from astropy.wcs import WCS

import common.data_checks
import common.data_helper as helper
import common.image as image
import numpy as np


class TestChannel(TestCase):

    location = '/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx'
    name = '/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan01.fits'

    def test_get_name(self):
        name = helper.get_name(self.location)
        self.assertEqual('G282.5-0.5IFx', name)
        name = helper.get_name(self.location)
        self.assertEqual('G282.5-0.5IFx', name)

    def test_find_backgrounds(self):
        background_list = helper.find_backgrounds(self.location,
                                                  background=True)
        rms_list = helper.find_backgrounds(self.location,
                                           rms=True)
        self.assertEqual(14, len(rms_list))
        for rms in rms_list:
            self.assertIn('rms.fits', rms)
        self.assertEqual(14, len(background_list))
        for background in background_list:
            self.assertIn('bkg.fits', background)

    def test_read_vot(self):

        vot = helper.read_vot('/Users/bs19aam/Documents/test_data/Mom0_comp_catalogs/G282.5-0.5IFx_Mosaic_Mom0_comp.vot')

        self.assertIsNotNone(vot)
        self.assertIsNotNone(vot.data)

    def test_get_image(self):

        image = helper.get_image(self.name)
        self.assertIsNotNone(image)
        self.assertIsNotNone(image[0])
        self.assertIsNotNone(image[1])
        self.assertTrue(image[1]['SIMPLE'])

    def test_unify_coords(self):
        vot_location = helper.get_vot_location(self.location)
        name = helper.get_name(self.location)
        vot = helper.read_vot(vot_location + name + '_Mosaic_Mom0_comp.vot')
        files = helper.find_channels(self.location)
        channels = image.Image.get_channels(self, files[0])
        w = WCS(channels[0].header, naxis=2)
        positions = helper.unify_coords(vot, w)

        self.assertAlmostEqual(1331.4798803820217, positions[0][0])
        self.assertAlmostEqual(3.670782204850184, positions[0][1])
        self.assertEqual(8357, len(positions))
        self.assertEqual(len(vot['id']), len(positions))

    def test_minmax_coord(self):
        files = helper.find_channels(self.location)
        channels = image.Image.get_channels(self, files[0])
        min, max = helper.minmax_coord(channels[0].header)

        self.assertLess(min, max)
        self.assertGreaterEqual(min, 0)
        self.assertLessEqual(min, 360)
        self.assertGreaterEqual(max, 0)
        self.assertLessEqual(max, 360)

    def test_find_channels(self):
            channels = helper.find_channels(self.location)

            self.assertIs(14, len(channels))
            for channel in channels:
                self.assertEqual('chan', channel[-11:-7])
                self.assertEqual('.fits', channel[-5:])

    def test_get_vot_list(self):
        vot_list = helper.get_vot_list(self.location, aegean=True)

        for vot in vot_list:
            self.assertIn('.vot', vot)

    def test_get_vot_location(self):
        vot_location = helper.get_vot_location(self.location)

        self.assertIs(type(vot_location), str)
        self.assertIn('Mom0_comp_catalogs', vot_location)

    def test_load_neighbors(self):
        names = ['G279.5-0.5IFx', 'G282.5-0.5IFx', 'G285.5-0.5IFx']
        folder = '/Users/bs19aam/Documents/test_data/Mom0_comp_catalogs'
        neighbors = helper.load_neighbors(names, folder)

        self.assertIsNotNone(neighbors)
        self.assertIs(3, len(neighbors))

    def test_make_table(self):
        small_shape=10
        large_shape=500
        example_dtype=np.dtype([('id', 'int32'), ('field', 'object'),
                 ('chan01', 'float64')])
        example_no_id_dtype = np.dtype([ ('field', 'object'),
                 ('chan01', 'float64')])
        vot = helper.read_vot('/Users/bs19aam/Documents/test_data/Mom0_comp_catalogs/G282.5-0.5IFx_Mosaic_Mom0_comp.vot')
        small_table_aegean = helper.make_table(small_shape, aegean=True, table_type=vot)
        large_table_aegean = helper.make_table(large_shape, aegean=True, table_type=vot)
        small_table = helper.make_table(small_shape)
        large_table = helper.make_table(large_shape)

        self.assertEquals(small_shape, len(small_table))
        self.assertEquals(large_shape, len(large_table))

    def test_check_lists(self):
        all_lists_check, back_list, channels_list = common.data_checks.check_lists(self.location)
        self.assertIs(True, all_lists_check)

        all_lists_check, back_list, channels_list = common.data_checks.check_lists('/Users/bs19aam/Documents/test_data'
                                                                                   '/Mosaic_Planes/Empty')
        self.assertIs(False, all_lists_check)
