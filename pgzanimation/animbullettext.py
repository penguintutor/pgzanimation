import pygame
import pgzero.screen
from pgzero import ptext
from .pgzanimation import PgzAnimation
from .animtext import AnimText

""" Provides an object for a single bullet. Use for bulleted text lists
# bulletstyle can be circle (default) or none (use for spacing to line up with other bullets)
# Distance from pos is bulletpad + bulletsize + bulletpad
# bullettransition is how the bullet will appear when called using
animate_bullet. Currently supports: 
* appear = appear immediately when start frame reached
* slidefromleft = slide in from left hand side
* slidefromright = slide in from righ hand side
* slidefromtop = slide in from top of screen
* slidefrombutton = slide in from bottom of screen
"""

class AnimBulletText(AnimText):

    # has fixed mandatory fields then kwargs
    # hide is new field as common to hide bullet text and then let it appear
    def __init__(self, text_string, pos, color="black", anchor=(0,0), angle=0,
        bulletstyle="circle", bulletsize=10, bulletpad=10, bulletcolor=(0,0,0), bullettransition="appear", hide=False, **kwargs):

        super().__init__(text_string, pos, color, anchor, angle, **kwargs)

        # bullet parameters
        self.bulletstyle = bulletstyle
        self.bulletsize = bulletsize
        self._bulletpad = [0,0] # override by checking if pad is tuple or value
        self._setbulletpad (bulletpad)
        self.bulletcolor = bulletcolor
        self.bullettransition = bullettransition
        ## todo add a method that handles bullettransition (eg. may need to place bullet offscreen)
        # overwrite default hide state with init hide parameter
        self.hide = hide

        # used for transitions - bullet slide
        self._goto_pos = []

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
        if self.hide:
            return
        text_pos = [
            self._pos[0]+2*self._bulletpad[0]+self.bulletsize,
            self._pos[1]
            ]
        ptext.draw(self.text, text_pos, angle=self._angle, color=self._color, surf=self._surface, **self.kwargs)
        # draw bullet
        bullet_pos = [
            round(self._pos[0]+self._bulletpad[0]+round(self.bulletsize/2)),
            round(self._pos[1]+self._bulletpad[1])
            ]
        if (self.bulletstyle == "circle"):
            pygame.draw.circle (self._surface, self.bulletcolor, bullet_pos, round(self.bulletsize/2), 0)
        # if not one of above then either invalid or none - either case ignore


    # animate bullet appearing - start transition at start and end by end
    # after end will continue to show until slide complete
    def animate_bullet(self, start, end, current):
        if (current < start or current > end):
            return
        # appear (appears immediately at start of transition)
        if (self.bullettransition == "appear"):
            self.hide = False
        # move from left
        elif (self.bullettransition == "slidefromleft"):
            # first frame use pos as the goto
            if (current == start):
                self.hide = False
                self._goto_pos = [*self._pos]
                # now move offscreen
                # calculate width - that's how far we move to left
                self._pos[0] -= self._surface.get_width()
            # call the normal move tween
            self.move_tween(start, end, current, self._goto_pos)
        elif (self.bullettransition == "slidefromright"):
            # first frame use pos as the goto
            if (current == start):
                self.hide = False
                self._goto_pos = [*self._pos]
                # now move offscreen
                # calculate width - that's how far we move to left
                self._pos[0] += self._surface.get_width()
            # call the normal move tween
            self.move_tween(start, end, current, self._goto_pos)
        elif (self.bullettransition == "slidefromtop"):
            # first frame use pos as the goto
            if (current == start):
                self.hide = False
                self._goto_pos = [*self._pos]
                # now move offscreen
                # calculate width - that's how far we move to left
                self._pos[1] -= self._surface.get_height()
            # call the normal move tween
            self.move_tween(start, end, current, self._goto_pos)
        elif (self.bullettransition == "slidefrombottom"):
            # first frame use pos as the goto
            if (current == start):
                self.hide = False
                self._goto_pos = [*self._pos]
                # now move offscreen
                # calculate width - that's how far we move to left
                self._pos[1] += self._surface.get_height()
            # call the normal move tween
            self.move_tween(start, end, current, self._goto_pos)