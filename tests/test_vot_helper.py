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
            self.assertEquals(mock_array.data, vot.data)

    def test_get_vot_list(self):
        vot_list = vot_helper.get_vot_list(self.location, aegean=True)

        for vot in vot_list:
            self.assertIn('.vot', vot)

    def test_get_vot_location(self):
        vot_location = vot_helper.get_vot_location(self.location)

        self.assertIs(type(vot_location), str)
        self.assertIn('Mom0_comp_catalogs', vot_location)