from unittest import TestCase
import models.build_center as build_center

class TestBuildCenter(TestCase):

    def test_build_center(self):
        test_build = build_center.BuildCenter()

        self.assertEquals([], test_build.matched_index)
        self.assertEquals([], test_build.overlap_index)
        self.assertEquals([], test_build.distance)
