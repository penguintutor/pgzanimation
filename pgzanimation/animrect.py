from .animpolygon import AnimFilledPolygon
import pygame

# Must only have 1 movement happening at a time - otherwise confusion over which applies
# Can have a rotate at the same time as a movement

""" Takes a Rect object - could be of the format:
    Rect(left, top, width, height)
    Rect((left, top), (width, height))
"""

class AnimFilledRect(AnimFilledPolygon):

    # Pass a rect object and color, anchor optional
    def __init__(self, rect, color, anchor=("center", "center")):
        """ convert rect into points
        (once changed then can no longer use it as a rect as that would break rotation).
        But it can be replaced with a new rectangle
        (or by replacing the points list it will become a polygon).
        You can also get a rect, but if rotated then that will be bounding rectange
        (but could be useful for collision detection)
        """
        points = self._points = [
            rect.topleft,
            rect.topright,
            rect.bottomright,
            rect.bottomleft,
        ]
        super().__init__(points, color, anchor)

    # Gets a rect object - can be used for collidepoint etc.
    # Uses a bounding box based on current transformations
    @property
    def rect(self):
        return self.get_rect()

    @rect.setter
    def rect(self, new_rect):
        #self._points = self.rect_to_points(new_rect)
        self.rect_to_points(new_rect)
        # reapply any existing transforms
        self._transform()

    def rect_to_points(self, rect):
        self._points = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]

    def get_center(self):
        return self.rect.center


class AnimRect(AnimFilledRect):
    def __init__(self, rect, color, anchor=("center", "center"), width=1):
        super().__init__(rect, color, anchor)
        self.width = width

    def draw(self):
        if self.hide:
            return
        # convert from list of tuples of floats to ints
        points_ints = [
            (round(point[0]), round(point[1])) for point in self._transform_points
        ]
        pygame.draw.polygon(self._surface, self._color, points_ints, self.width)