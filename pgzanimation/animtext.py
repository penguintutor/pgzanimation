import pygame
import math
# import local ptext as that supports more granular rotation override resolution
from pgzero import ptext
from pgzero import loaders
from .pgzanimation import PgzAnimation


class AnimText(PgzAnimation):

    # has fixed mandatory fields then kwargs
    # mode "normal" = display full string
    # mode "typewriter" = reveal 1 char at a time as typewriter
    # Note typewriter does not guarentee a monospace font (may change in future)
    def __init__(
        self,
        text_string,
        pos,
        color="black",
        anchor=(0, 0),
        angle=0,
        hide=False,
        mode= "normal",
        **kwargs,
    ):
        super().__init__(color, anchor, hide=hide)
        # different text strings - eg if only partially displayed
        # _full_text is the complete string
        # _text is what's currently being displayed
        self._full_text = text_string
        self._text = text_string
        self.mode = mode
        if (self.mode == "typewriter"):
            self._text = ""
        # _display_chars only used in typewriter (or reveal modes) - otherwise ignored
        self._display_chars = 0
        # These parameters are common across all pgzanimation so defined here
        self._pos = [*pos]
        self._angle = angle
        self._color = color
        # Text specific fields are stored in kwargs
        self.kwargs = kwargs
        # These are the mandatory defaults
        if not "fontsize" in self.kwargs:
            kwargs["fontsize"] = 40

        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle
        self.fontsize_start = self.kwargs["fontsize"]
        # If fontname specified then load it
        if "fontname" in self.kwargs:
            self._load_font(self.kwargs["fontname"]) 

    @property
    def fontsize(self):
        return self.kwargs["fontsize"]

    @fontsize.setter
    def fontsize(self, new_size):
        self.kwargs["fontsize"] = new_size
    
    # Getter returns full text even if less showed
    @property
    def text(self):
        return self._full_text

    # Sets the complete text - may be partially hidden eg. if typewriter mode
    @text.setter
    def text(self, new_text):
        self._full_text = new_text
        # also update what is being displayed
        self._text = text_string
        # typewriter mode - reset to 0
        if (mode == "typewriter"):
            self._text = ""
            self._display_chars = 0
            self.update_text()
            
    # Typewriter pos - allows jump to appropriate position
    @property
    def typewriter_pos(self):
        return self._display_chars

    @typewriter_pos.setter
    def typewriter_pos(self, new_pos):
        self._display_chars = new_pos
        self.update_text()
        
    # Updates display of text - used for reveal
    def update_text(self):
        # if standard mode then _text = _full_text
        if (self.mode == "normal"):
            self._text = self._full_text
        
        elif self._display_chars <= 0:
            self._text = ""
            
        elif self._display_chars > len(self._full_text):
            self._text = self._full_text
            
        else:
            self._text = self._full_text[0:self._display_chars]


    def anchor_to_float(self):
        """anchor for text should be a float, this converts words to equivelant"""
        new_anchor = [0, 0]
        # dictionary of x words
        x_to_val = {"left": 0, "right": 1, "center": 0.5, "middle": 0.5}
        y_to_val = {"top": 0, "bottom": 1, "center": 0.5, "middle": 0.5}
        # ignore if already number
        if isinstance(self._anchor[0], int) or isinstance(self._anchor[0], float):
            new_anchor[0] = self._anchor[0]
        else:
            if self._anchor[0] in x_to_val:
                self._anchor[0] = x_to_val[self._anchor[0]]
        if isinstance(self._anchor[1], int) or isinstance(self._anchor[1], float):
            new_anchor[1] = self._anchor[1]
        else:
            if self._anchor[1] in y_to_val:
                self._anchor[1] = y_to_val[self._anchor[1]]
        return new_anchor

    # Text alternative to scale - uses fontsize
    def fontsize_tween(self, start, end, current, newfontsize):
        if current < start or current > end:
            return
        if current == start:
            self.fontsize_start = self.kwargs["fontsize"]
        rel_size = (newfontsize - self.fontsize_start) / (end - start)
        self.kwargs["fontsize"] = self.fontsize_start + rel_size * (current - start)

    def move(self, newpos):
        self._pos = newpos

    def rotate(self, angle):
        self._angle = angle

    # Reset angle and anchor to defaults
    def reset(self):
        self._anconfsTestZuritestItchor = (0, 0)
        self._angle = 0

    def _load_font(self, fontname):
        font = loaders.getfont(fontname)
        
    # typewriter mode
    # If not already in typewriter mode then set to typewriter mode
    # start_pos can be used to continue from an existing point
    # it will display all chars to the left it won't hide them
    # end_pos is the last char to display in this tween or 0 = all
    def typewriter_tween(self, start, end, current, start_pos=0, end_pos=0):
        if (current < start or current > end):
            return
        if (current == start):
            self.mode == "typewriter"
            self._display_chars = start_pos
        # if end is 0 then show all - so set end to len of string
        if end_pos == 0:
            end_pos = len(self._full_text)
        # work out num chars to display
        num_frames = end - start
        num_chars = end_pos - start_pos
        self._display_chars = math.floor ((num_chars / num_frames) * (current-start) ) + start_pos
        print ("Pos {}".format(self._display_chars))
        self.update_text()
        

    def draw(self):
        if self.hide == True:
            return
        text_anchor = self.anchor_to_float()
        #print ("Displaying "+self._show_text+" "+str(self._pos))
        ptext.draw(
            self._text,
            self._pos,
            angle=self._angle,
            color=self._color,
            surf=self._surface,
            anchor=text_anchor,
            **self.kwargs
        )


# override ptext loader to use pgzero loader
ptext.getfont = loaders.getfont
# override resolution for text rotation
ptext.ANGLE_RESOLUTION_DEGREES = 1