from unittest import TestCase

from common.channel import Channel


class TestChannel(TestCase):
    def test_get_frequency(self):
        channel = Channel('/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/G282.5-0'
                          '.5IFx_Mosaic_chan01.fits')
        frequency = channel.get_frequency(channel.header)

        self.assertTrue(isinstance(channel.frequency, float))
        self.assertTrue(isinstance(frequency, float))
