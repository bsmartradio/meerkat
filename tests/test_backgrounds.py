from unittest import TestCase
from unittest.mock import patch
from models.backgrounds import Backgrounds
import numpy as np


class TestBackgrounds(TestCase):

    def test_backgrounds(self):
        path = 'testpath'
        mock_image = np.array([5, 10])

        with patch('common.data_helper.get_image', return_value=mock_image):
            background = Backgrounds(path)

        self.assertEqual('testpath', background.path)
        self.assertEqual(5, background.data)
        self.assertEqual(10, background.header)
