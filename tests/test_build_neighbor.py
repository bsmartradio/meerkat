from unittest import TestCase
import models.build_neighbor as build_neighbor


class TestBuildNeighbor(TestCase):

    def test_build_neighbor(self):
        test_neighbor = build_neighbor.BuildNeighbor()

        self.assertEqual([], test_neighbor.overlap_index)
        self.assertEqual([], test_neighbor.overlap_coordinates)
        self.assertEqual([], test_neighbor.distance)
