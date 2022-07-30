from unittest import TestCase
from unittest.mock import patch, MagicMock
import common.vot_helper as vot_helper


class TestChannel(TestCase):

    def test_read_vot(self):
        mock_array = MagicMock()
        mock_array.data = ['1']

        mock_table = MagicMock()
        mock_table.array = mock_array

        mock_vot_table = MagicMock()
        mock_vot_table.get_first_table.return_value = mock_table

        with patch('astropy.io.votable.table.parse', return_value=mock_vot_table):
            vot = vot_helper.read_vot('/Example/test_data/Mom0_comp_catalogs/G282.5-0.5IFx_Mosaic_Mom0_comp.vot')

            self.assertIsNotNone(vot)
            self.assertIsNotNone(vot.data)
            self.assertTrue(mock_vot_table.get_first_table.called)
            self.assertEqual(mock_array.data, vot.data)

    def test_get_vot_list(self):
        mock_vot_return = ['Mosaic_Mom0_comp1.vot', 'Mosaic_Mom0_comp2.vot']
        mock_location = 'test/test/'

        with patch('glob.glob', return_value=mock_vot_return):
            vot_list = vot_helper.get_vot_list(mock_location, aegean=True)

        for vot in vot_list:
            self.assertIn('.vot', vot)

    def test_get_vot_location(self):
        mock_location = '/Example/test_data/Mosaic_Planes/'
        vot_location = vot_helper.get_vot_location(mock_location)

        self.assertIs(type(vot_location), str)
        self.assertIn('Mom0_comp_catalogs', vot_location)

    def test_load_neighbors(self):
        names = ['G279.5-0.5IFx', 'G282.5-0.5IFx', 'G285.5-0.5IFx']
        folder = 'Example/test_data/Mom0_comp_catalogs'
        mock_vot = MagicMock()

        with patch('common.vot_helper.read_vot', return_vaue=mock_vot):
            neighbors = vot_helper.load_neighbors(names, folder)

        self.assertIsNotNone(neighbors)
        self.assertIs(3, len(neighbors))
