import common.image as image
from unittest import TestCase


class TestImage(TestCase):
    multiple_channels = ['/Users/bs19aam/Documents/test_data/Mosaic_Planes/'
                         'G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan01.fits',
                         '/Users/bs19aam/Documents/test_data/Mosaic_Planes/'
                         'G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan02.fits',
                         '/Users/bs19aam/Documents/test_data/Mosaic_Planes/'
                         'G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan03.fits'
                         ]
    multiple_backgrounds = ['/Users/bs19aam/Documents/test_data/Mosaic_Planes/'
                         'G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan01_bkg.fits',
                         '/Users/bs19aam/Documents/test_data/Mosaic_Planes/'
                         'G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan02_bkg.fits',
                         '/Users/bs19aam/Documents/test_data/Mosaic_Planes/'
                         'G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan03_bkg.fits'
                         ]

    one_channel = ['/Users/bs19aam/Documents/test_data/Mosaic_Planes/'
                      'G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan01.fits']

    one_background = ['/Users/bs19aam/Documents/test_data/Mosaic_Planes/'
                      'G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan01_bkg.fits']

    def test_get_channels(self):
        cube_single = image.Image.get_channels(self, self.one_channel)
        cube_multi = image.Image.get_channels(self, self.multiple_channels)

        self.assertIs(1, len(cube_single))
        self.assertIs(3, len(cube_multi))

    def test_get_backgrounds(self):
        background_single = image.Image.get_backgrounds(self, self.one_background)
        background_multi = image.Image.get_backgrounds(self, self.multiple_backgrounds)

        self.assertIs(1, len(background_single))
        self.assertIs(3, len(background_multi))
