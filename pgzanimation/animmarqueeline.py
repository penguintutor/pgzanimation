import pygame
import math
from .pgzanimation import PgzAnimation
from .animline import AnimLine


# Special implementation of line
# Marquee / marching ant style line
# Designed for circuit diagrams to create an animated "wire"
# Also useful for highlighting a box (eg. selections)
# Is a single object, but uses a line and a dashed line
# Needs two colours - first color is of the wire, the second is for the "dash"
# style relates to the dash part
# animateenable stops the animation, but still shows the dashed line
# animatedisplay can be used to hide the animateline, but not the solid line
class AnimMarqueeLine(PgzAnimation):

    def __init__(self, start, end, color, dashcolor, anchor=('center', 'center'), width=1, animwidth=-1, style="dashed", spacing=[10,10], dashoffset=0, dashanimate=0.4, animateenable=True, animatedisplay=True):
        super().__init__(color, anchor)
        self._width = width
        self._dashoffset = dashoffset
        self._currentoffset = dashoffset
        self.dashanimate = dashanimate
        self._animateenable = animateenable
        self.animatedisplay = animatedisplay
        
        # if animwidth is -1 (default) then set to same as width
        if (animwidth == -1):
        	animwidth=width

        self.style = style
        self.spacing = spacing

        # reveal is a percentage - how much is currently shown of the
        # line. This is implemented in draw after other transitions
        self.reveal = 100

        # Create as two lines
        self.primaryline = AnimLine (start, end, color, width=width)
        self.animline = AnimLine (start, end, dashcolor, style=style, width=animwidth, spacing=spacing, dashanimate=dashanimate, dashoffset=dashoffset, animateenable=animateenable)


    # Override most of the setters and getters to refer to primaryline / animline as appropriate
    # set color
    @property
    def color(self):
        return self.primaryline.color

    @color.setter
    def color(self, new_color):
        self.primaryline.color = new_color

    @property
    def dashcolor(self):
        return self.animline.color

    @dashcolor.setter
    def dashcolor(self, new_color):
        self.animline.color = new_color


    @property
    def animateenable(self):
        return self._animateenable

    @animateenable.setter
    def animateenable(self, status):
        self.animline.animatenable = status
        self._animateenable = status

    # used to transform a object - scale
    # value (1,1) is default size
    @property
    def scale(self):
        return self.primaryline.scale

    @scale.setter
    def scale(self, new_scale):
        self.primaryline.scale = new_scale
        self.animline.scale = new_scale


    # dashoffset is distance to start of first full printable segment
    @property
    def dashoffset(self):
        return self.animline.dashoffset

    @dashoffset.setter
    def dashoffset(self, new_offset):
        self.animline.dashoffset = new_offset


    # points - setting either end point replaces the unrotated points and resets angle to 0
    @property
    def start(self):
        return self.primaryline.start


    @start.setter
    def start(self, new_start):
        self.primaryline.start = new_start
        self.animline.start = new_start

    @property
    def end(self):
        return self.primaryline.end

    @end.setter
    def end(self, new_end):
        self.primaryline.end = new_end
        self.animline.end = new_end


    # Gets a rect object - can be used for collidepoint etc.
    # Uses a bounding box based on current transformations
    # Not so useful for a line, but included for consistancy
    @property
    def rect(self):
        return self.primaryline.get_rect()


    # Reset to defaults - scale, angle and anchor
    def reset(self):
        self.primaryline.reset()
        self.animline.reset()

    def move_rel (self, delta):
        self.primaryline.move_rel(delta)
        self.animline.move_rel(data)


    def rotate (self, angle):
        self.primaryline.rotate(angle)
        self.animline.rotate(angle)
        

    # scale to newscale from current scale
    def scale_tween (self, start, end, current, newscale):
        self.primaryline.scale_tween(start, end, current, newscale)
        self.animline.scale_tween(start, end, current, newscale)


    def draw(self):
        self.primaryline.draw()
        if self.animatedisplay:
            self.animline.draw()


    # draw the line a little at a time
    # implemented in the draw method
    # reveal will override hide (on start) - so you can hide first and then reveal
    def reveal_tween (self, start, end, current):
        self.primaryline.reveal_tween(start, end, current)
        self.animline.reveal_tween(start, end, current)


    # Moves immediately to new position
    def move (self, newpos):
        self.primaryline.move(newpos)
        self.animline.move(newpos)
        
    def update(self, frame=-1):
        if (self._animateenable and self.animatedisplay):
            self.primaryline.update(frame)
            self.animline.update(frame)


