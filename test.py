# Test suite for pgzero animations
# Run using python3 (not pygame zero)
# Results are displayed on the command line
# Simple tests - test each action individually. A more comprehensive test would
# include multiple transformations

import unittest
from pgzanimation import *

class TestPolygon(unittest.TestCase):
    def test_create(self):
        polygon1 = AnimPolygon (((100, 150), (160, 150), (160,250), (100,250)), (255,0,255))
        self.assertEqual(polygon1.pos, [130,200])

    # rotate set angle
    def test_rotate(self):
        polygon1 = AnimPolygon (((200, 50), (260, 50), (260,150), (200,150)), (255,0,255))
        self.assertEqual(polygon1.pos, [230,100])
        polygon1.angle = 45
        # based on center, center so pos does not change
        self.assertEqual(polygon1.pos, [230,100])
        # original points unchanged
        self.assertEqual(polygon1._points, [(200, 50), (260, 50), (260,150), (200,150)])
        # return points updated
        self.assertEqual(polygon1.points, [
                            (173.4314575050762, 85.85786437626905),
                            (215.85786437626905, 43.431457505076196),
                            (286.5685424949238, 114.14213562373095),
                            (244.14213562373095, 156.5685424949238)])


    # Move relative
    def test_move(self):
        polygon1 = AnimPolygon (((200, 50), (260, 50), (220, 100)), (255,0,255))
        self.assertEqual(polygon1.pos, [230,75])
        # move position
        polygon1.move_rel((50,50))
        self.assertEqual(polygon1.pos, [280,125])
        # check both rotated points (angle = 0) and internal points
        self.assertEqual(polygon1.points, [(250, 100), (310, 100), (270, 150)])
        self.assertEqual(polygon1._points, [[250, 100], [310, 100], [270, 150]])


    # Move anchor position
    def test_anchor(self):
        polygon1 = AnimPolygon (((50, 50), (750, 50), (750, 550), (50, 550)), (0,128,128))
        self.assertEqual(polygon1.pos, [400,300])
        # move anchor to top left
        polygon1.anchor = ("left", "top")
        self.assertEqual(polygon1.pos, [50,50])
        # move to bottom right
        polygon1.anchor = ("right", "bottom")
        self.assertEqual(polygon1.pos, [750,550])

    def test_scale(self):
        polygon1 = AnimPolygon(((100, 100), (200, 100), (200, 250), (100, 250)), (0,128,128))
        polygon1.scale = (2,2)
        self.assertEqual(polygon1._points, [(100, 100), (200, 100), (200, 250), (100, 250)])
        self.assertEqual(polygon1.points, [(50, 25), (250, 25), (250, 325), (50, 325)])


if __name__ == '__main__':
    unittest.main()