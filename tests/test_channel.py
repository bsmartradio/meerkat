from unittest import TestCase
from unittest.mock import patch, MagicMock
from models.channel import Channel
import numpy as np


class TestChannel(TestCase):
    def test_get_frequency(self):
        mock_channel = MagicMock()
        mock_channel.header = {'OBSFREQ': 12345.534}
        frequency = Channel.get_frequency(mock_channel.header)

        self.assertTrue(isinstance(frequency, float))

    def test_get_frequency_fail(self):
        mock_channel = MagicMock()
        mock_channel.header = {'OBSFREQ': None}
        frequency = Channel.get_frequency(mock_channel.header)

        self.assertFalse(isinstance(frequency, float))

    def test_get_frequency_missing_key(self):
        mock_channel = MagicMock()
        mock_channel.header = {'TEST': 12345.534}
        frequency = Channel.get_frequency(mock_channel.header)

        self.assertIsNone(frequency, float)

    def test_channel_build(self):
        mock_header = {'OBSFREQ': 12345.534}
        mock_data = np.array([1.4, 2.4, 3.4, 4.4, 5.4])
        path = 'test/path'

        with patch('common.data_helper.get_image', return_value=[mock_data, mock_header]):
            channel = Channel(path)

        self.assertIsNotNone(channel.header)
        self.assertIsNotNone(channel.frequency)
        self.assertIsNotNone(channel.data)
        self.assertIsNotNone(channel.photometry_error)
        self.assertIsNotNone(channel.path)
