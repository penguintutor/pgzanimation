import pygame
from pgzero.actor import Actor
from .pgzanimation import PgzAnimation


class AnimActor(PgzAnimation):
    """ AnimActor - Class for creating Actors (sprites) with animation

    Uses the Pygame Zero Actor class
    """

    # has fixed mandatory fields then kwargs
    def __init__(
                self,
                image,
                pos=(0, 0),
                anchor=("center", "center"),
                hide=False,
                angle=0,
                **kwargs
                ):
        """ AnimActor contstructor __init__. Creates a Pygame Zero Actor

        * image - filename for image - uses Pygame Zero Loader
                if in images directory then no path required
                if png or jpg file then no extension required
        * pos - x, y position
        * anchor - anchor point for rotation
        * hide - if true then don't display
        * angle - rotation angle
        * **kwargs - any other Actor class arguments
        """
        # color is required parameter for PGZAnimation
        # It is now however used - set to white
        super().__init__((255, 255, 255), anchor, hide=hide, angle=angle)
        self.image = image
        self._pos = [*pos]
        self.kwargs = kwargs

        # save positions for use by future tween methods
        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle

        # Create the actor class
        self.actor = Actor(image, self._pos, actor=self._anchor, **self.kwargs)
        # if initial angle is not 0 then rotate now
        if self._angle != 0:
            self.rotate(self._angle)

    def draw(self):
        """ Draw the object on the surface """
        if (self.hide is True):
            return
        self.actor.draw()

    def move(self, newpos):
        """ Immediately move to the new position """
        self._pos = newpos
        self.actor.pos = newpos

    def rotate(self, angle):
        """ Rotate to a set angle (absolute) """
        self._angle = angle
        self.actor.angle = angle

    def reset(self):
        """ Reset angle and anchor to defaults """
        self._anchor = (0, 0)
        self.actor.anchor = (0, 0)
        self._angle = 0
        self.actor.angle = 0
