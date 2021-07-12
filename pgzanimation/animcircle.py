from .animellipse import AnimFilledEllipse
import pygame
import math

# A circle is an ellipse with 1:1 ratio

# Must only have 1 movement happening at a time - otherwise confusion over which applies
# Can have a rotate at the same time as a movement


class AnimFilledCircle(AnimFilledEllipse):

    #Pass a rect object and color, anchor optional
    def __init__(self, pos, radius, color, anchor=('center', 'center')):
        # angle is required but meaningless for a circle as it is the same when rotated
        self._angle = 0
        # create rect from pos and radius
        self._rect = self.circle_to_rect(pos,radius,anchor)
        self.radius = radius
        super().__init__(self._rect, color, anchor)
        
        
    def circle_to_rect(self, pos, radius, anchor):
        xpos = pos[0]
        if (anchor[0] == "center"):
            xpos = pos[0] - radius
        elif (anchor[0] == "right"):
            xpos = pos[0] - 2 * radius
        # If left then leave as pos[0]
        ypos = pos[1]
        if (anchor[1] == "center"):
            ypos = pos[1] - radius
        elif (anchor[1] == "bottom"):
            ypos = pos[1] - 2 * radius
        # If top then leave as pos[1]
        return pygame.Rect(xpos, ypos, 2 * radius, 2 * radius)

    # Gets a rect object - can be used for collidepoint etc.
    # Uses a bounding box based on current transformations
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, new_radius):
        self._radius = new_radius
        self._transform()


class AnimCircle(AnimFilledCircle):

    def __init__(self, pos, radius, color, anchor=('center', 'center'), width=1):
        super().__init__(pos, radius, color, anchor)
        self.width = width

    def draw(self):
        if self.hide: return
        pygame.draw.ellipse(self._surface, self.color_val(), self._transform_rect, self.width)
