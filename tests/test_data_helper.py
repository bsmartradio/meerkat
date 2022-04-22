from unittest import TestCase
from unittest.mock import patch, MagicMock
from astropy.wcs import WCS
import common.data_checks
import common.data_helper as helper
import numpy as np

import common.vot_helper


class TestChannel(TestCase):
    location = 'Example/test_data/Mosaic_Planes/G282.5-0.5IFx'
    name = 'Example/test_data/Mosaic_Planes/G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan01.fits'

    def test_get_name(self):
        name = helper.get_name(self.location)
        self.assertEqual('G282.5-0.5IFx', name)
        name = helper.get_name(self.location + '/')
        self.assertEqual('G282.5-0.5IFx', name)

    def test_find_backgrounds(self):
        return_value = ['01_bkg.fits', '02_bkg.fits', '03_bkg.fits', '04_bkg.fits', '05_bkg.fits', '06_bkg.fits',
                        '07_bkg.fits', '08_bkg.fits', '09_bkg.fits', '10_bkg.fits', '11_bkg.fits', '12_bkg.fits',
                        '13_bkg.fits', '14_bkg.fits']

        with patch('glob.glob', return_value=return_value):
            background_list = helper.find_backgrounds(self.location, background=True)

            self.assertEqual(14, len(background_list))
            for background in background_list:
                self.assertIn('bkg.fits', background)

    def test_get_image(self):
        mock_list = MagicMock()
        mock_list[0].data = 'mock_fits_file'
        mock_list[0].header = {'SIMPLE': True}
        mock_list.close.return_value = None

        with patch('astropy.io.fits.open', return_value=mock_list):
            image, header = helper.get_image(self.name)
            self.assertIsNotNone(image)
            self.assertEquals('mock_fits_file', image)
            self.assertIsNotNone(header)
            self.assertTrue(header['SIMPLE'])
            self.assertTrue(mock_list.close.called)


    def test_unify_coords(self):
        mock_lon = MagicMock()
        mock_lon.data = [200]
        mock_lat = MagicMock()
        mock_lat.data = [-5]
        mock_vot = {'lon': mock_lon, 'lat': mock_lat}
        mock_w = MagicMock()
        mock_w.wcs_world2pix.return_value = [1, 2]

        with patch('numpy.array', return_value=[4, 5]):
            positions = helper.unify_coords(mock_vot, mock_w)

            self.assertEquals([1, 2], positions)
            self.assertTrue(mock_w.wcs_world2pix.called)

    def test_minmax_coord(self):
        mock_min_lon = MagicMock()
        mock_min_lon.l.degree = 1
        mock_max_lon = MagicMock()
        mock_max_lon.l.degree = 100

        with patch.object(WCS, 'pixel_to_world', side_effect=[mock_min_lon, mock_max_lon]):
            min, max = helper.minmax_coord(None)

        self.assertLess(min, max)

    def test_find_channels(self):

        return_value = ['_chan01.fits', '_chan02.fits', '_chan03.fits', '_chan04.fits', '_chan05.fits', '_chan06.fits',
                        '_chan07.fits', '_chan08.fits', '_chan09.fits', '_chan10.fits', '_chan11.fits', '_chan12.fits',
                        '_chan13.fits', '_chan14.fits']

        with patch('glob.glob', return_value=return_value):
            channels = helper.find_channels(self.location)

        self.assertIs(14, len(channels))
        for channel in channels:
            self.assertEqual('chan', channel[-11:-7])
            self.assertEqual('.fits', channel[-5:])


    def test_make_table_aegean_no_id(self):
        shape = 10
        mock_vot = MagicMock()
        mock_vot.dtype = np.dtype([('field', 'object'),('chan01', 'float64')])

        table_aegean = helper.make_table(shape, aegean=True, table_type=mock_vot)

        self.assertEquals(shape, len(table_aegean))
        self.assertIn('id', table_aegean.dtype.names)

    def test_make_table(self):
        shape = 10
        mock_vot = MagicMock()
        mock_vot.dtype = np.dtype([('id', 'int'),('field', 'object'),('chan01', 'float64')])

        table_aegean = helper.make_table(shape, aegean=True, table_type=mock_vot)

        self.assertEquals(shape, len(table_aegean))
        self.assertIn('id', table_aegean.dtype.names)

    def test_make_table_aegean_with_id(self):
        shape = 10

        table= helper.make_table(shape)

        self.assertEquals(shape, len(table))
        self.assertEquals(38, len(table.dtype))


