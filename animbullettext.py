import pygame
import pgzero.screen
# import local ptext as that supports more granular rotation
#from pgzero import ptext
import ptext
from pgzanimation import PgzAnimation
from animtext import AnimText

# Special text which has bullets
# bulletstyle can be circle (default) or none (use for spacing to line up with other bullets)
# Distance from pos is bulletpad + bulletsize + bulletpad

class AnimBulletText(AnimText):

    # has fixed mandatory fields then kwargs
    def __init__(self, text_string, pos, color="black", anchor=(0,0), angle=0, bulletstyle="circle", bulletsize=10, bulletpad=5, bulletcolor=(0,0,0), **kwargs):
        super().__init__(text_string, pos, color, anchor, angle, **kwargs)
        
        # bullet parameters
        self.bulletstyle = bulletstyle
        self.bulletsize = bulletsize
        self._bulletpad = [0,0] # override by checking if pad is tuple or value
        self._setbulletpad (bulletpad)
        self.bulletcolor = bulletcolor
        
    @property  
    # bullet pad always returns list
    def bulletpad(self):
        return (self._bulletpad)
        
    @bulletpad.setter
    def bulletpad(self, bulletpad):
        self._setbulletpad (bulletpad)
        
    def _setbulletpad(self, bulletpad):
        # check if it's a list / tuple - if so save
        if type(bulletpad) == tuple or type(bulletpad) == list:
            self._bulletpad[0] = bulletpad[0]
            self._bulletpad[1] = bulletpad[1]
        elif type(bulletpad) == int:
            self._bulletpad[0] = bulletpad
            self._bulletpad[1] = bulletpad



    def draw(self):
        text_pos = [
            self._pos[0]+2*self._bulletpad[0]+self.bulletsize,
            self._pos[1]
            ]
        ptext.draw(self._text_string, text_pos, angle=self._angle, color=self._color, surf=self._surface, **self.kwargs)
        # draw bullet
        bullet_pos = [
            self._pos[0]+self._bulletpad[0]+round(self.bulletsize/2),
            self._pos[1]+self._bulletpad[1]
            ]
        if (self.bulletstyle == "circle"):
            #screen.draw.filled_circle (bullet_pos, (self.bulletsize/2), bulletcolor)
            pygame.draw.circle (self._surface, self.bulletcolor, bullet_pos, round(self.bulletsize/2), 0)
        # if not one of above then either invalid or none - either case ignore
