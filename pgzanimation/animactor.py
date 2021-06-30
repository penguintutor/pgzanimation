import pygame
from pgzero.actor import Actor
from .pgzanimation import PgzAnimation

class AnimActor(PgzAnimation):

    # has fixed mandatory fields then kwargs
    def __init__(self, image, pos=(0,0), anchor=("center","center"), hide=False, angle=0, **kwargs):
        # Super is called from PgzAnimation
        # color is required parameter, but not used - set to white
        super().__init__((255,255,255), anchor, hide=hide, angle=angle)
        self.image = image                              
        # These parameters are common across pgzanimation so defined here
        self._pos = pos

        # Text specific fields are stored in kwargs
        self.kwargs = kwargs
        # These are the mandatory defaults

        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle

        self.actor = Actor(image, self._pos, actor=self._anchor, **self.kwargs)
        # if initial angle is not 0 then rotate now
        if self._angle != 0:
            self.rotate(self._angle)




    def draw(self):
        if (self.hide == True):
            return
        self.actor.draw()


    def move(self, newpos):
        self._pos=newpos
        self.actor.pos=newpos

    def rotate (self,angle):
        self._angle = angle
        self.actor.angle=angle

    # Reset angle and anchor to defaults
    def reset(self):
        self._anchor=(0,0)
        self.actor.anchor=(0,0)
        self._angle=0
        self.actor.angle=0
