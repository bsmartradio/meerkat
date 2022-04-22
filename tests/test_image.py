import models.image as image
from unittest import TestCase
from unittest.mock import patch, MagicMock

from models.channel import Channel
from models.backgrounds import Backgrounds


class TestImage(TestCase):

    def test_get_channels_single(self):
        mock_single_file = 'file_one'
        mock_cube = MagicMock()
        mock_cube[0] = 'cube_data'

        with patch.object(Channel, '__init__', return_value=None):
            cube_single = image.Image.get_channels(self, mock_single_file)

        self.assertIs(1, len(cube_single))

    def test_get_channels_multi(self):
        mock_multiple_files = ['file_one', 'file_two', 'file_three']
        mock_multiple_cubes = MagicMock()
        mock_multiple_cubes[0] = 'cube_dat1'
        mock_multiple_cubes[1] = 'cube_data2'
        mock_multiple_cubes[2] = 'cube_data3'

        with patch.object(Channel, '__init__', return_value=None):
            cube_multi = image.Image.get_channels(self, mock_multiple_files)

        self.assertIs(3, len(cube_multi))

    def test_get_backgrounds_single(self):
        mock_single_background = 'file_one'

        with patch.object(Backgrounds, '__init__', return_value=None):
            single_background = image.Image.get_backgrounds(self, mock_single_background)

        self.assertIs(1, len(single_background))

    def test_get_backgrounds_multi(self):
        mock_multiple_background = ['file_one', 'file_two']

        with patch.object(Backgrounds, '__init__', return_value=None):
            multiple_background = image.Image.get_backgrounds(self, mock_multiple_background)

        self.assertIs(2, len(multiple_background))


