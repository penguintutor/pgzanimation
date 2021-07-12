import pygame
# import local ptext as that supports more granular rotation override resolution
from pgzero import ptext
from pgzero import loaders
from .pgzanimation import PgzAnimation


class AnimText(PgzAnimation):

    # has fixed mandatory fields then kwargs
    def __init__(self, text_string, pos, color="black", anchor=(0,0), angle=0, hide=False,  **kwargs):
        super().__init__(color, anchor, hide=hide)
        self.text = text_string
        # These parameters are common across all pgzanimation so defined here
        self._pos = [*pos]
        self._angle = angle
        self._color = color
        # Text specific fields are stored in kwargs
        self.kwargs = kwargs
        # These are the mandatory defaults
        if not 'fontsize' in self.kwargs:
            kwargs['fontsize'] = 40

        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle
        self.fontsize_start = self.kwargs['fontsize']
        # If fontname specified then load it
        if 'fontname' in self.kwargs:
            self._load_font (self.kwargs['fontname'])



    @property
    def fontsize(self):
        return self.kwargs['fontsize']

    @fontsize.setter
    def fontsize(self, new_size):
        self.kwargs['fontsize'] = new_size
        
    def anchor_to_float(self):
        """ anchor for text should be a float, this converts words to equivelant """
        new_anchor = [0, 0]
        # dictionary of x words
        x_to_val = { "left": 0, "right": 1, "center": 0.5, "middle": 0.5}
        y_to_val = { "top": 0, "bottom": 1, "center": 0.5, "middle": 0.5}
        # ignore if already number
        if (isinstance(self._anchor[0], int) or isinstance(self._anchor[0], float)) :
            new_anchor[0] = self._anchor[0]
        else:
            if self._anchor[0] in x_to_val:
                self._anchor[0] = x_to_val[self._anchor[0]]
        if (isinstance(self._anchor[1], int) or isinstance(self._anchor[1], float)) :
            new_anchor[1] = self._anchor[1]
        else:
            if self._anchor[1] in y_to_val:
                self._anchor[1] = y_to_val[self._anchor[1]]
        return new_anchor

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
        self._anconfsTestZuritestItchor=(0,0)
        self._angle=0

    def _load_font (self, fontname):
        font = loaders.getfont(fontname)

    def draw(self):
        if (self.hide == True): return
        text_anchor = self.anchor_to_float()
        ptext.draw(self.text, self._pos, angle=self._angle, color=self._color, surf=self._surface, anchor=text_anchor, **self.kwargs)

# override ptext loader to use pgzero loader
ptext.getfont = loaders.getfont
# override resolution for text rotation
ptext.ANGLE_RESOLUTION_DEGREES = 1