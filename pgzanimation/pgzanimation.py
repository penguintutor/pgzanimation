import pygame
import math

# Library for creating animations in pygame zero which can be exported
# as png image files and optionally converted to videos

# For more details see http://www.penguintutor.com/programming/pgzanimation



class PgzAnimation():

    # start from top left and goes width across and height down
    def __init__(self, color, anchor=('center', 'center'), hide=False):
        self._color = color

        # angle in degrees
        self._angle = 0
        self.hide = hide
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
        new_value %= 360
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

    # returns size of surface (screen size)
    def get_screen_size(self):
        return (self._surface.get_size())
        
    # show and end_show are same as calling hide, but you need to give a start time of when to start showing or end showing the object
    def show (self, start, current):
        if (current == start):
            self.hide = False
            
    def end_show (self, end, current):
        if (current == end):
            self.hide = True


    # rotate to an absolute from current position
    def rotate_tween (self, start, end, current, angle):
        if (current < start or current > end):
            return
        if (current == start):
            self.rotate_start_angle = self._angle
        d_angle = (angle - self.rotate_start_angle) / (end-start)
        new_angle = self.rotate_start_angle + d_angle * (current-start)
        self.rotate(new_angle)

    # rotate a relative amount
    def rotate_rel_tween (self, start, end, current, angle):
        if (current < start or current > end):
            return
        if (current == start):
            self.rotate_start_angle = self._angle
        rel_angle = (angle - rotate_start_angle) / (end-start)
        self.rotate(self._angle+rel_angle)

    # tweened movement to absolute position
    def move_tween (self, start, end, current, goto):
        if (current < start or current > end):
            return
        if (current == start):
            self.move_start_pos = self._pos
        # work out delta between start and end
        dx = (goto[0] - self.move_start_pos[0]) / (end-start)
        dy = (goto[1] - self.move_start_pos[1]) / (end-start)

        newpos = [0,0]
        # Add delta to start position
        newpos[0] = self.move_start_pos[0] + dx * (current - start)
        newpos[1] = self.move_start_pos[1] + dy * (current - start)
        self.move (newpos)

    # tweened movement to relative position
    def move_rel_tween (self, start, end, current, delta):
        if (current < start or current > end):
            return
        if (current == start):
            self.move_start_pos = self._pos
        # work out delta between start and end
        dx = delta[0] / (end-start)
        dy = delta[1] / (end-start)

        newpos = [0,0]
        # Add delta to current position
        newpos[0] = self._pos[0] + dx
        newpos[1] = self._pos[1] + dy
        self.move (newpos)


    # Print test with information about the shape
    # Used for debugging
    # Overwrite in individual classes for more detailed information
    def print_info (self):
        print ("Shape: Unknown")
        print ("Position: "+str(self._pos))
        print ("Implement in individual class for more information")


    # update can take an optional argument of current_frame
    # This is not used on all classes, but allows consistancy with slides
    # which do need the current frame
    # return value is whether to pause - normally that's just false
    # it is normally only used by slides
    def update(self, current_frame=-1):
        return False

# get size from surface
        self._surface = pygame.display.get_surface()
        self._size = self._surface.get_size()

        print ("Surface size {} {}".format(self._size[0], self._size[1]))
