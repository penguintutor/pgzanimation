# Test suite for pgzero animations
# Run using python3 (not pygame zero)
# Results are displayed on the command line
# Simple tests - test each action individually. A more comprehensive test would
# include multiple transformations

import unittest
from pgzanimation import *

class TestVectors(unittest.TestCase):
    def test_dir_vector_1 (self):
        test_vector = [1,0]
        vector = get_dir_vector(0)
        self.assertAlmostEqual(vector[0], test_vector[0])
        self.assertAlmostEqual(vector[1], test_vector[1])
        
        
    def test_dir_vector_2 (self):
        test_vector = [0,-1]
        vector = get_dir_vector(90)
        self.assertAlmostEqual(vector[0], test_vector[0])
        self.assertAlmostEqual(vector[1], test_vector[1])

    def test_dir_vector_3 (self):
        test_vector = [-1,0]
        vector = get_dir_vector(180)
        self.assertAlmostEqual(vector[0], test_vector[0])
        self.assertAlmostEqual(vector[1], test_vector[1])

    def test_dir_vector_4 (self):
        test_vector = [0,1]
        vector = get_dir_vector(-90)
        self.assertAlmostEqual(vector[0], test_vector[0])
        self.assertAlmostEqual(vector[1], test_vector[1])
        
    def test_dir_vector_4 (self):
        test_vector = [0,1]
        vector = get_dir_vector(270)
        self.assertAlmostEqual(vector[0], test_vector[0])
        self.assertAlmostEqual(vector[1], test_vector[1])
        
    def test_dir_vector_4 (self):
        test_vector = [0.70710678,-0.70710678]
        vector = get_dir_vector(45)
        self.assertAlmostEqual(vector[0], test_vector[0])
        self.assertAlmostEqual(vector[1], test_vector[1])
        
class TestActor(unittest.TestCase):
    """ Test AnimActor class
    
    Unable to test through test.py as needs to be called by pgzrun.
    Most of the operations are handled within the Pygame Zero Actor class
    """
    def test_create(self):
        #actor1 = AnimActor("alien")
        self.assertEqual(True, True)
        
class TestLine(unittest.TestCase):
    def test_create(self):
        line1 = AnimLine((50, 50), (750, 650), (211, 233, 111))
        self.assertEqual(line1.pos, [400, 350])
        
    def test_horizontal(self):
        line1 = AnimLine((100, 100), (400, 100), (10, 10, 10))
        self.assertEqual(line1.pos, [250, 100])

    def test_vertical(self):
        line1 = AnimLine((200, 0), (200, 1080), (255, 255, 255))
        self.assertEqual(line1.pos, [200, 540])
        
    def test_negative(self):
        line1 = AnimLine((-200, -200), (-100, -100), (23, 23, 23))
        self.assertEqual(line1.pos, [-150, -150])
        
    def test_right_to_left(self):
        line1 = AnimLine((800,600), (100, 100), (0, 0, 255))
        self.assertEqual(line1.pos, [450, 350])
                    

class TestPolygon(unittest.TestCase):
    def test_create(self):
        polygon1 = AnimPolygon(((100, 150), (160, 150), (160,250), (100,250)), (255,0,255))
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
        
class TestDashedLine(unittest.TestCase):
    def test_dash_1 (self):
        # Horizontal
        dash_line1 = AnimLine((100,100), (200,100), (128,128,128), spacing=[10,5], style="dashed")
        #dash_line1.dashoffset += 6
        segments = dash_line1._line_to_segments((100,100), (200,100))
        self.assertEqual(segments, [[[100.0, 100.0], [110.0, 100.0]], [[115.0, 100.0], [125.0, 100.0]], [[130.0, 100.0], [140.0, 100.0]], [[145.0, 100.0], [155.0, 100.0]], [[160.0, 100.0], [170.0, 100.0]], [[175.0, 100.0], [185.0, 100.0]], [[190.0, 100.0], [200.0, 100.0]]])
        


if __name__ == '__main__':
    unittest.main()