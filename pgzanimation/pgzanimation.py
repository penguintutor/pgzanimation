import pygame
import pgzero
import math

# Library for creating animations in pygame zero which can be exported
# as png image files and optionally converted to videos
# For more details see http://www.penguintutor.com/programming/pgzanimation


class PgzAnimation():
    """ PgzAnimation abstract parent class for animation classes

    All the animation classes should be subclassed from this.
    It provides basic functionality which is common across all
    animation classes. All sub classes must provide the basic
    functionality of the attributes, but can add any additional
    one required by that class.
    """

    def __init__(
            self,
            color,
            anchor=('center', 'center'),
            hide=False,
            angle=0):
        """ init for all animation subclasses.

        All the subclasses must call this during __init__ to
        provide access to the Pygame Surface.
        """

        self._color = color

        # angle in degrees
        self._angle = angle
        self.hide = hide
        self._anchor = [*anchor]

        # Get Pygame surface for draw()
        self._surface = pygame.display.get_surface()

    # set color
    # Color is stored as the value given (so user can get back value that was set)
    # To use in a subclass then call color_val()
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

    # Angle should be in degrees
    # Angle increases in ccw direction (implemented in subclass)
    @angle.setter
    def angle(self, new_value):
        new_value %= 360
        self.rotate(new_value)

    # position - starts based on original
    @property
    def pos(self):
        return self._pos

    # setting position moves immediately to new position
    # use a tuple for newpos
    @pos.setter
    def pos(self, new_pos):
        # Uses child move method
        self.move(new_pos)

    # Updating anchor changes anchor (rotation point),
    # the calc_pos() and _transform() methods are used to set position
    # relative to the new anchor
    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, new_anchor):
        # Ensure list and not tuple so can change in other methods
        self._anchor = [*new_anchor]
        self.calc_pos()
        # recalculate vectors
        self._transform()
        
    def color_val(self):
        '''get color value in a format that can be passed to pygame objects

        The main color value is stored in the same format as originally submitted,
        this is not the case for secondary color formats (eg. background color, shadow color which are converted
        to RGBA tuple (A = alpha - normally 255)
        '''
        if isinstance(self._color, pygame.Color):
            return self._color
        return pgzero.screen.make_color(self._color)

    # returns size of surface (screen size)
    def get_screen_size(self):
        '''get_screen_size() - returns screen size in pixels (width, height)'''
        return(self._surface.get_size())

    # show and end_show are same as calling hide, but you need to give
    # a start time of when to start showing or end showing the object
    def show(self, start, current):
        ''' show(start, current) - unhides the instance

        start is the frame to start showing the object
        current is the current frame

        This is the same as changing the .hide attribute when start == current
        '''
        if (current == start):
            self.hide = False

    def end_show(self, end, current):
        ''' end_show(start, current) - hides the instance

        start is the frame to stop showing the object
        current is the current frame

        This is the same as changing the .hide attribute when start == current
        '''
        if (current == end):
            self.hide = True

    # rotate to an absolute from current position
    # direction can be CCW / left (counter clock wise)
    # or CW / right (Clockwise)
    def rotate_tween(self, start, end, current, angle, direction="CCW"):
        if (current < start or current > end):
            return
        if (current == start):
            self.rotate_start_angle = self._angle
        d_angle = (angle - self.rotate_start_angle) / (end-start)
        if ((direction == "CW" or direction == "right") and d_angle > 0):
            d_angle *= -1
        new_angle = self.rotate_start_angle + (d_angle * (current-start))
        self.rotate(new_angle)

    # rotate a relative amount
    def rotate_rel_tween(self, start, end, current, angle, direction="CCW"):
        if (current < start or current > end):
            return
        if (current == start):
            self.rotate_start_angle = self._angle
        rel_angle = (angle) / (end-start)
        if (direction == "CW" or direction == "right"):
            rel_angle *= -1
        self.rotate(self._angle+rel_angle)

    # tweened movement to absolute position
    def move_tween(self, start, end, current, goto):
        if (current < start or current > end):
            return
        if (current == start):
            self.move_start_pos = self._pos
        # work out delta between start and end
        dx = (goto[0] - self.move_start_pos[0]) / (end-start)
        dy = (goto[1] - self.move_start_pos[1]) / (end-start)

        newpos = [0, 0]
        # Add delta to start position
        newpos[0] = self.move_start_pos[0] + dx * (current - start)
        newpos[1] = self.move_start_pos[1] + dy * (current - start)
        self.move(newpos)

    # tweened movement to relative position
    def move_rel_tween(self, start, end, current, delta):
        if (current < start or current > end):
            return
        if (current == start):
            self.move_start_pos = self._pos
        # work out delta between start and end
        dx = delta[0] / (end-start)
        dy = delta[1] / (end-start)

        newpos = [0, 0]
        # Add delta to current position
        newpos[0] = self._pos[0] + dx
        newpos[1] = self._pos[1] + dy
        self.move(newpos)

    # Print test with information about the shape
    # Used for debugging
    # Overwrite in individual classes for more detailed information
    def print_info(self):
        print("Shape: Unknown")
        print("Position: "+str(self._pos))
        print("Implement in individual class for more information")

    # update can take an optional argument of current_frame
    # This is not used on all classes, but allows consistancy with slides
    # which do need the current frame
    # return value is whether to pause - normally that's just false
    # it is used by slides and others that update non tween related
    # eg. dashed line - this will still be updated even if animation paused
    def update(self, current_frame=-1):
        return False
