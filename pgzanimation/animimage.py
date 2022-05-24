import pygame
from pgzanimation.animactor import AnimActor
from .pgzanimation import PgzAnimation

""" This class inherits from AnimActor
Provides more appropriate name (Image vs Actor)
particularly when used in slide animations

"""
class AnimImage(AnimActor):
    def __init__(
                self,
                image,
                pos=(0, 0),
                anchor=("center", "center"),
                hide=False,
                angle=0,
                imagetransition="appear",
                **kwargs
                ):
        super().__init__(
            image,
            pos,
            anchor,
            hide,
            angle,
            **kwargs)
        self.transition = imagetransition

    # Animate bullet images - these appear and disappear with current bullet

    # animage_start_image handles the image appearing
    # by default this is appear
    # Only currently support appear (also transition is same for start and end)
    def animate_start_image(self, start, end, current):
        if (current < start or current > end):
            return
        # if in range
        if (current >= start and current <= end):
            # appear (appears immediately at start of transition)
            if (self.transition == "appear"):
                self.hide = False

    # animate_end_image handles the image disappearing
    def animate_end_image(self, start, end, current):
        if (current < start or current > end):
            return
        # if in range
        if (current >= start and current <= end):
            # appear (appears immediately at start of transition)
            if (self.transition == "appear"):
                self.hide = True

    # wipe appear - linear reveal
    # direction is angle - start at 0 degrees (top to bottom - rotate clockwise)
    # This relies on new features of Pygame Zero Actor - more recent than the current release 1.2.1
    # Requires a recent install of pygame zero from github (2021)
    def wipe_appear (self, start, end, current, direction=0):
        if (current < start or current > end):
            return

        cache_len = len(self.actor._surface_cache)
        if cache_len == 0:
            last = self.actor._orig_surf
        else:
            last = self.actor._surface_cache[-1]


        #this_image = self._orig_surf
        this_image = last
        img_size = this_image
        # Calculate amount to reveal as fraction (0 to 1)
        reveal = (current - start) / (end - start)

        # update alpha array
        alpha_map = last.pixels_alpha (this_image)

        for y in range (0, img_size[1]):
            for x in range (0, img_size[0]):
                if (y > reveal * img_size[1]):
                    alpha_map[x][y] = 0xFF
                else:
                    alpha_map[x][y] = 0x00


