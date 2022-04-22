import models.rms as rms
from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestRms(TestCase):
    rms_example = 'Example/test_data/Mosaic_Planes/G282.5-0.5IFx/G282.5-0.5IFx_Mosaic_chan01_rms.fits'

    def test_rms(self):
        mock_image = MagicMock()
        mock_image.header = ['header']
        mock_image.data = [1, 2, 3, 4]

        with patch('common.data_helper.get_image', return_value=[mock_image.data, mock_image.header]):
            rms_output = rms.Rms(self.rms_example)

        self.assertIsNotNone(rms_output.header)
        self.assertIsNotNone(rms_output.data)
