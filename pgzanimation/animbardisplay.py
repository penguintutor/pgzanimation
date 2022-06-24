import pygame
from pygame import Rect
import math
from .pgzanimation import PgzAnimation
from .animrect import AnimFilledRect, AnimRect

class AnimBarDisplay(AnimRect):
    """ Provides a bar display - suitable for a completion bar / bar graph / etc
    By default this is horizontal - but can also be vertical
    Creates as a fixed none filled rectangle which covers the full scale
    this rectangle may be empty
    Partially fills based on percentage value
    """
    # Pass a rect object and color, anchor optional
    # outercolor is colour of outside of bar - if not sent then becomes same as color (but doesn't change with color)
    # If outershow = False (whether to display outer rectangle or not)
    # percent allows to set initial display
    # Direction is which way to display (left, right in either order indicates horizontal), (top, bottom in either order indicate vertical)
    # Do not attempt to rotate (unpredictable)
    # percent should be 0 to 100 (>100 or <0 may have unintended results)
    def __init__(self, rect, color, anchor=("center", "center"), outercolor=None, outershow=False, direction="left-right", percent=0):
        if outercolor == None:
            self.outercolor = color
        super().__init__(rect, color, anchor)
        self.outercolor = outercolor
        self.outershow = outershow
        self.direction = direction
        self._percent = percent
        self.filled_bar = AnimFilledRect (rect, color, anchor)
        # Run update to set actuall filled_bar
        self.update()


    # Update filled_rect based on percentage and direction
    #def get_filled_rect(self):
    def update(self):
        # current_rect is the full recetangle (100%)
        # Actually stored as a polygon - so get the rect co-ordinates
        current_rect = self.get_rect()
        if self.direction == "left-right":
            # Get difference between left and right for percentage
            x_delta = int(round((current_rect.right - current_rect.left) * self._percent / 100))
            # Use left co-ordinates
            new_rect = Rect(current_rect.bottomleft, (x_delta, current_rect.height))
            self.filled_bar.rect = new_rect



    # percent getter and setter - setter needs to call update
    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, new_percent):
        self._percent = new_percent
        # Limit to 100 %
        if self._percent > 100:
            self._percent = 100
        # Update filled bar
        self.update()


    #def update(self, current_frame=-1):
    #    # Update the size of the filled_bar rectangle based on the current percentage
    #    self.filled_bar.new_rect = self.get_filled_rect()

    def draw(self):
        if self.outershow:
            super().draw()
        # special case if percentage < 1 don't display anything
        if (self._percent > 1):
            self.filled_bar.draw()


    # animate percentage complete between start and end
    def percent_tween (self, start, end, current, newpercent):
        pass


    # Moves immediately to new position
    def move (self, newpos):
        self.primaryline.move(newpos)
        self.animline.move(newpos)


