from .pgzanimation import PgzAnimation
from pgzanimation import AnimActor
from .slide import Slide
import math
class SlideImage(Slide):
    """ SlideImage slide with one image which can be animated
    
    Slide showing one image and title
    
    Image is positioned in the center of the screen 
    after taking the title into consideration.

    imageanimate - if True then animate the image
    imagetransition - type of transition 
        appear (from nothing to full display), fadein (fade in)
        To use transparency (eg. fade in) then needs Pygame Zero 1.3
        If at < 1.3 then this is the same as appear
    imagepause will cause the animation to pause after the image if enabled
    
    for imagepause to work then timings must be set when calling animate_slide 
    indicating how long after showing image before pause,
    otherwise this value is ignored.
    """
    def __init__(self, size, title, image, 
                    imageanimate = True, imagetransition = "appear",
                    imagepause = False):
        super().__init__(size, title)
        self.imagetransition=imagetransition
        # list of tuples for start and end of each bullet transition and after the after time (start transition, end transition, after)
        self._image_transitiontime = []
        # Must define start position so calculate here
        ##TODO if move then set position here
        if (imagetransition == "move"):
            pass
        else:
            # set to centre of screen (minus top menu)
            position = (size[0] / 2, (size[1] - 220) / 2 + 220)  
        # Create actor
        self._actor = AnimActor (image, position)
        # If hidden / fade then set here
        if (imagetransition == "appear" or imagetransition == "fadein"):
            self._actor.hide = True

    def draw(self):
        # if not enabled then we don't show anything
        if (super().draw() == False):
            return
        self._actor.draw()

    def unpause (self):
        self.pause = False


    def animate_slide (self, start, end, timings=None):
        """ Set the animation going 
        
        Can only call once in each time period
        to run a second time then wait until after end and call again
        
        timings is a list of transition [before,during,after]
        if not set then goes default.
        """
        
        # reset animation times
        self._image_transitiontime = []
        # Default timings
        if (timings == None):
            # default - before = 1, then start and the end is set to the end of 
            # the transition (end stops 1 frame before). After is used if pausing
            # end only used if image pause set
            self._image_transitiontime = [start, end]
        else:
            self._image_transitiontime = timings


    # return True to pause the slides or False to continue
    # always unpause at start as once paused this is not called until unpause
    def update(self, current_frame = -1):
        # super supports enable based on show_slide
        super().update(current_frame)
        # if we are not getting current frame then just display image
        # thanks to draw it will still only show if slide is not hidden through hide attribute
        if (current_frame == -1):
            self._enable = True
            self._actor.hide = False
            return False

        # only update other objects if enabled
        if (self._enable == False):
            return False

        # animate the bullet if in range
        if (current_frame >= self._image_transitiontime[0] 
                and current_frame <= self._image_transitiontime[1]):

            if self.imagetransition == "fadein":
                self._actor.animate_fadein(
                        self._image_transitiontime[0],
                        self._image_transitiontime[1],
                        current_frame)
                # also unhide
                self._actor.hide = False
                
            #todo animate here eg. move
            
            # otherwise must be default (appear)
            else:
                 # must be between frames show show
                self._actor.hide = False
        # entry 2 is pause
        elif (len(self._image_transitiontime) > 2 
                and current_frame == self._image_transitiontime[2]
                and self.imagepause == True):
            print ("**** Pausing ****")
            self.pause = True
            
        # return pause value to pause if required
        # returning true will pause the slide
        return self.pause