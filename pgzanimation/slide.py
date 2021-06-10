from .pgzanimation import PgzAnimation
from pgzanimation import AnimText

# Slides are templates which can be used for view slides
# or animations.
# Start with a fixed layout, but many of the parameters can be
# changed after initialising
# Starts disabled and then needs to be called through show_slide
# animate_slide calls default actions (eg. for bullets is showing each 
# bullet)

class Slide():
    
    def __init__(self, size, title, titlealign="center", titley=100, titlefontsize=80):
        self._enable = False        # User should not change this except by calling show_slide
        self._hide = False
        self._size = size
        # title x pos - default to left
        self._titlex = 200
        if (titlealign=="center"):
            self._titlex = self._size[0]/2
        self._titley = titley
        self._titlefontsize = titlefontsize
        self._title = AnimText (title, (self._titlex,self._titley), anchor=(0.5,0.5), fontsize=self._titlefontsize)
        self._slide_start_frame = 0
        self._slide_end_frame = 0
        
    # set title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title._text_string = new_title
        
    # enables the slide (eg. shows the title)
    # This doesn't take the current frame, it allows you to define
    # slide to show without needing to call animate
    # For this to work then update must be provided with current frame
    def show_slide (self, start_frame, end_frame):
        self._slide_start_frame = start_frame
        self._slide_end_frame = end_frame
        

    # slides act differently to anim objects
    # for slides we normally don't use current frame - just set start and end
    # then let the slide manage through update(current_frame)
    
    # animates slide - eg. show bullets
    def animate_slide (self, start_frame, end_frame):
        pass
    
    def draw(self):
        if (self._hide == True or self._enable == False):
            # return is normally ignored, but in the case of a slide
            # returning False means do not show rest of slide
            return False
        self._title.draw()
        return True

    
    # current_frame is an optional parameter, but is required for some
    # features to work (eg. show_slide), without current_frame then 
    # elements would need to be turned on / off using hide
    def update(self, current_frame=-1):
        # special case if current frame is -1 then does not support frames in updates (may need to manually disable using hide
        if (current_frame == -1):
            self._enable = True
        # enable / disable based on current frame number
        elif (current_frame >= self._slide_start_frame and current_frame <= self._slide_end_frame):
            self._enable = True
        else:
            self._enable = False
        # master slide class does not support pausing (but subclasses can
        # by overloading update)
        return False
        