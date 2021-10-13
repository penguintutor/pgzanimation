import pygame
import math
from .animpolygon import AnimFilledPolygon
from .animcircle import AnimFilledCircle
from .animtriangle import AnimFilledTriangle
from .pgzanimation import PgzAnimation

""" Adds an end to a line (eg. Arrow)
Needs line end position, angle and type of shape (eg. arrow)
"""

class AnimLineEnd(PgzAnimation):

    def __init__(self, pos, color, angle=0, style="arrow", size=10, anchor=('center', 'center'), hide=False, scale=[1,1]):
        super().__init__(color, anchor, hide=hide)
        self._pos = pos

        self._size = size       # Size of end (e.g diameter of circle or width of arrow)

        # create with a scale of 1 (not currently supposed)
        self._scale = [*scale]

        self._angle = angle         # 0 deg = arrow pointing upwards, rotate anti-clockwise (same as pygame zero)

        # These are used for transformations
        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle
        self.scale_start = self._scale

        # Create as appropriate object
        if (style == "arrow"):
            self.end_object = AnimFilledTriangle(self._pos, self._color, angle=self._angle, w=self._size, h=self._size, anchor=("center", "center"))


    def draw(self):
        if self.hide: return
        # convert from list of tuples of floats to ints
        self.end_object.draw()