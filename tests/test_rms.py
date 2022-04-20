import common.rms as rms
from unittest import TestCase


class TestRms(TestCase):
    rms_example = '/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan01_rms.fits'

    def test_rms(self):
        rms_output=rms.Rms(self.rms_example)

        self.assertIsNotNone(rms_output.header)
        self.assertIsNotNone(rms_output.data)
        self.assertTrue(rms_output.header[0])

