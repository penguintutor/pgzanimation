import pygame
import math

# Library for creating animations in pygame zero which can be exported
# as png image files and optionally converted to videos

# For more details see http://www.penguintutor.com/programming/pgzanimation 



class PgzAnimation():

    # start from top left and goes width across and height down
    def __init__(self, color, anchor=('center', 'center')):
        self._color = color
        
        # angle in degrees
        self._angle = 0
        self.hide = False
        self._anchor = [*anchor]

        # Get Pygame surface for draw()
        self._surface = pygame.display.get_surface()

    # set color
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    # rotation angle can be set in degrees
    @property
    def angle(self):
        return self._angle

    # angle should be between -359 and +359
    # if this has been changed slightly then correct
    # If outside that range then add / subtract 360 - attempt to fix
    @angle.setter
    def angle(self, new_value):
        if (new_value >= 360):
            new_value -= 360
        if (new_value <= -360):
            new_value += 360
        self.rotate (new_value)

    # position - starts based on original
    @property
    def pos(self):
        return self._pos

    # setting position moves immediately to new position
    # use a tuple for newpos
    @pos.setter
    def pos(self, newpos):
        # Uses child move method
        self.move (newpos)

    # Updating anchor changes anchor (rotation point), without changing the _points
    # The pos will change to the new anchor pos
    # The rot_points needs to be recalculated to make them relative to the new anchor
    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, new_anchor):
        self._anchor = new_anchor
        self.calc_pos()
        # recalculate vectors
        self._transform()


    # Print test with information about the shape
    # Used for debugging
    def print_info (self):
        print ("Shape: Polygon")
        print ("Points: "+str(self._points))
        print ("Anchor: "+str(self._anchor))
        print ("Position: "+str(self._pos))
        print ("Rot Points: "+str(self._transform_points))


    def update(self):
        pass