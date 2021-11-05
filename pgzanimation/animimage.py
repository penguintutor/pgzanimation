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