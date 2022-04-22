from unittest import TestCase
import models.neighbors as neighbors
import models


class TestNeighbors(TestCase):

    def test_neighbors(self):
        test_neighbor = neighbors.Neighbors()

        self.assertIsInstance(models.build_neighbor.BuildNeighbor(), type(test_neighbor.left))
        self.assertIsInstance(models.build_center.BuildCenter(), type(test_neighbor.center_left))
        self.assertIsInstance(models.build_neighbor.BuildNeighbor(), type(test_neighbor.right))
        self.assertIsInstance(models.build_center.BuildCenter(), type(test_neighbor.center_right))
