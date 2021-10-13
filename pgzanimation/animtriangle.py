from .animpolygon import AnimFilledPolygon
import pygame
import math

""" This creates a triangle
pos is center of triangle, size is (w x h) which is before any rotation / transformations
this represents a triangle pointing upwards
"""

# Must only have 1 movement happening at a time - otherwise confusion over which applies
# Can have a rotate at the same time as a movement


class AnimFilledTriangle(AnimFilledPolygon):

    # Pass a rect object and color, anchor optional
    def __init__(self, pos, color, angle=0, w=10, h=10, anchor=("center", "center")):
        self._pos = pos
        self._w = w
        self._h = h
        self._angle = angle
        # calc positions based on anchor - get bottom left
        if (anchor[0] == "right"):
            left = pos[0]-w
        elif (anchor[0] == "left"):
            left = pos[0]
        else:   # default is center
            left = pos[0]-round(w/2)
        if (anchor[1] == "top"):
            bottom = pos[1]+h
        elif (anchor[1]== "bottom"):
            bottom = pos[1]
        else:
            bottom = pos[1]+round(h/2)

        points = [
            (left, bottom),
            (left+w, bottom),
            (left+round(w/2), bottom-h)
        ]
        super().__init__(points, color, anchor)
        if (angle != 0) :
            self.rotate(angle)



class AnimTriangle(AnimFilledTriangle):
    def __init__(self,  pos, color, angle=0, w=10, h=10, anchor=("center", "center"), width=1):
        super().__init__(pos, color, angle, w, h, anchor=anchor)
        self.width = width

    def draw(self):
        if self.hide:
            return
        pygame.draw.polygon(self._surface, self._color, points_ints, self.width)