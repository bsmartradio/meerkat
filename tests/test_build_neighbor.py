from unittest import TestCase
import models.build_neighbor as build_neighbor


class TestBuildNeighbor(TestCase):

    def test_build_neighbor(self):
        test_neighbor = build_neighbor.BuildNeighbor()

        self.assertEquals([], test_neighbor.overlap_index)
        self.assertEquals([], test_neighbor.overlap_coordinates)
        self.assertEquals([], test_neighbor.distance)
