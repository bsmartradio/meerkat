from unittest import TestCase
import models.build_center as build_center


class TestBuildCenter(TestCase):

    def test_build_center(self):
        test_build = build_center.BuildCenter()

        self.assertEqual([], test_build.overlap_coordinates)
        self.assertEqual([], test_build.overlap_index)
        self.assertEqual([], test_build.distance)
