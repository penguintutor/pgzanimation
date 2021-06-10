from .pgzanimation import PgzAnimation
from pgzanimation import AnimBulletText
from .slide import Slide
import math
class SlideBullets(Slide):
    
    # bullet spacing is distance between bullets (including the bullet)
    # bulletstartpos = top left 
    # bulletspacing = y distance
    # bulletanimate - if True then reveal each bullet one at a time
    #           if False then show all immediately
    # bulletpause will pause after each frame (if return value from update checked)
    def __init__(self, size, title, bullets, bulletstartpos=(50,220), bulletspacing=80, bulletanimate=True, bulletpause=False):
        super().__init__(size, title)
        self._bullets = []
        # bullet position is always top left
        self._bullet_pos = bulletstartpos
        # list of tuples for start and end of each bullet transition
        self._bullet_startendtime = []
        # to prevent crashing must be at least one bullet - set to blank
        if len(bullets) == 0:
            bullets.append("")
        # Bullets must have their position defined when created so calculate here
        this_y_pos = self._bullet_pos[1]
        for this_bullet in bullets:
            self._bullets.append(AnimBulletText(this_bullet, (self._bullet_pos[0],this_y_pos), hide=bulletanimate))
            this_y_pos += bulletspacing
        self.bulletpause = bulletpause
        # Set pause to True so that frame is paused
        self.pause = False
            
    def draw(self):
        # if not enabled then we don't show anything
        if (super().draw() == False):
            return
        for this_bullet in self._bullets:
            this_bullet.draw()
            
    def unpause (self):
        self.pause = False
    
    # Can only call animate slide once per time period
    # If want to run slide a second time then wait until after end
    # then call this again
    def animate_slide (self, start, end):
        # reset animation times
        self._bullet_startendtime = []
        # work out time delta between start and end (share between bullets)
        # bullets is +1 to delay between end of animate 
        # so in time we have pause before showing each bullet (inc 0)
        # and after last bullet 
        # must be frames between end and start than there are bullets
        time_delta = math.floor((end - start) / (len(self._bullets)+1))
        print ("Time delta {} - {} bullets".format(time_delta, (len(self._bullets))))
        current_start = start + time_delta      # track start frame add delay for first frame
        # set all start and ends based on time_delta
        for this_bullet_num in range(0, len(self._bullets)):
            self._bullet_startendtime.append((current_start, current_start+time_delta))
            print ("Animate enabled for {} {}".format(current_start, current_start+time_delta))
            # next transition always starts one position after (allows for pause)
            current_start+=time_delta+1
        
        
    # return True to pause the slides or False to continue
    def update(self, current_frame = -1):
        # super supports enable based on show_slide
        super().update(current_frame)
        # if we are not getting current frame then just display all bullets
        # thanks to draw it will still only show if slide is not hidden through hide attribute
        if (current_frame == -1):
            self._enable = True
            for this_bullet in self._bullets:
                this_bullet.hide = False
            return False
            
        # only update other objects if enabled
        if (self._enable == False):
            return False
            
        # update all bullet objects that have had start and end time set
        # otherwise skip
        for this_bullet_num in range(0, len( self._bullet_startendtime)):
            self._bullets[this_bullet_num].animate_bullet (*self._bullet_startendtime[this_bullet_num], current_frame)
            # if this is an end frame then set pause
            if (self._bullet_startendtime[this_bullet_num][1] == current_frame):
                self.pause = True
            
        # return pause value to pause if required
        # returning true will pause the slide
        return self.pause