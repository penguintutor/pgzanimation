import pygame
# import local ptext as that supports more granular rotation
#from pgzero import ptext
from . import ptext
from .pgzanimation import PgzAnimation


class AnimText(PgzAnimation):

    # has fixed mandatory fields then kwargs
    def __init__(self, text_string, pos, color="black", anchor=(0,0), angle=0,  **kwargs):
        super().__init__(color, anchor)
        self._text_string = text_string
        # These parameters are common across all pgzanimation so defined here
        self._pos = pos
        self._angle = angle
        self._color = color
        # Text specific fields are stored in kwargs
        self.kwargs = kwargs
        # These are the mandatory defaults
        if not 'fontsize' in self.kwargs: kwargs['fontsize'] = 40

        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle
        self.fontsize_start = self.kwargs['fontsize']

    @property
    def fontsize(self):
        return self.kwargs['fontsize']

    @fontsize.setter
    def fontsize(self, new_size):
        self.kwargs['fontsize'] = new_size

    # Text alternative to scale - uses fontsize
    def fontsize_tween (self, start, end, current, newfontsize):
        if (current < start or current > end):
            return
        if (current == start):
            self.fontsize_start = self.kwargs['fontsize']
        rel_size = (newfontsize - self.fontsize_start) / (end-start)
        self.kwargs['fontsize'] = self.fontsize_start + rel_size * (current-start)

    def move(self, newpos):
        self._pos=newpos

    def rotate (self,angle):
        self._angle = angle

    # Reset angle and anchor to defaults
    def reset(self):
        self._anchor=(0,0)
        self._angle=0

    def draw(self):
        ptext.draw(self._text_string, self._pos, angle=self._angle, color=self._color, surf=self._surface, **self.kwargs)