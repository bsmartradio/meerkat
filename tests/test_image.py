import models.image as image
from unittest import TestCase
from unittest.mock import patch, MagicMock
import models


class TestImage(TestCase):

    def test_get_channels(self):
        mock_multiple_files = ['file_one', 'file_two', 'file_three']
        mock_single_file = 'file_one'
        mock_cube=MagicMock()
        mock_multiple_cubes=MagicMock()
        mock_cube[0]='cube_data'
        mock_multiple_cubes[0] = 'cube_dat1'
        mock_multiple_cubes[1] = 'cube_data2'
        mock_multiple_cubes[2] = 'cube_data3'

        with patch.object(models.channel.Channel(), 'self, path', return_value=mock_cube):
            cube_single = image.Image.get_channels(self, mock_single_file)

        with patch('models.channel.Channel()', return_value=mock_multiple_cubes):
            cube_multi = image.Image.get_channels(self, mock_multiple_files)

        self.assertIs(1, len(cube_single))
        self.assertIs(3, len(cube_multi))

    def test_get_backgrounds(self):
        background_single = image.Image.get_backgrounds(self, self.one_background)
        background_multi = image.Image.get_backgrounds(self, self.multiple_backgrounds)

        self.assertIs(1, len(background_single))
        self.assertIs(3, len(background_multi))
