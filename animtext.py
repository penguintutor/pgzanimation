import pygame
from pgzero import ptext
from pgzanimation import PgzAnimation

class AnimText(PgzAnimation):
    
    # has fixed mandatory fields then kwargs
    def __init__(self, text_string, pos, color="black", anchor=(0,0), angle=0,  **kwargs):
        super().__init__(color, anchor)
        self._text_string = text_string
        self._pos = pos
        self._angle = angle
        self._color = color
        self.kwargs = kwargs
        
        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle
        
    # Reset angle and anchor to defaults
    def reset(self):
        self._anchor=(0,0)
        self._angle=0
        
    def draw(self):
        ptext.draw(self._text_string, self._pos, angle=self._angle, color=self._color, surf=self._surface, **self.kwargs)
