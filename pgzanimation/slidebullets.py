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
    def __init__(self, size, title, bullets, bulletstartpos=(50,220), bulletspacing=80, bulletanimate=True, bulletpause=False, bullettransition="appear"):
        super().__init__(size, title)
        self._bullets = []
        # bullet position is always top left
        self._bullet_pos = bulletstartpos
        self.bullettransition=bullettransition
        # list of tuples for start and end of each bullet transition and after the after time (start transition, end transition, after)
        self._bullet_transitiontime = []
        # to prevent crashing must be at least one bullet - set to blank
        if len(bullets) == 0:
            bullets.append("")
        # Bullets must have their position defined when created so calculate here
        this_y_pos = self._bullet_pos[1]
        for this_bullet in bullets:
            self._bullets.append(AnimBulletText(this_bullet, (self._bullet_pos[0],this_y_pos), hide=bulletanimate, bullettransition=self.bullettransition))
            this_y_pos += bulletspacing
        self.bulletpause = bulletpause


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
    # if timings is unset then default used, if not then should be a list
    # of timings for each transition [(before,during,after)] - in frame numbers (allows overlapping)
    # after of 1st transition will be added to before of next transition
    # pause occurs after the after value, but before the next before
    def animate_slide (self, start, end, timings=None):
        # reset animation times
        self._bullet_transitiontime = []
        # Default timings
        if (timings == None):
            # work out time delta between start and end (share between bullets)
            # must be min 2x more frames between end and start than there are bullets
            # 2 x because we have transitiontime, aftertime (no before time)
            # if pause enabled then pause after aftertime
            time_delta = math.floor((end - start) / ((len(self._bullets)+1) * 2))
            current_start = start + time_delta      # track start frame add delay for first frame
            # set all start and ends based on time_delta
            for this_bullet_num in range(0, len(self._bullets)):
                self._bullet_transitiontime.append((
                    current_start,
                    current_start+time_delta,
                    current_start+(time_delta*2)-1 # pause if applicable after display # -1 so as to pause before next transition starts
                    ))
                current_start+=time_delta*2
        # otherwise we have timings provided
        else:
            # transitions needs to be same as number of timings, if not
            # uses whichever has least number of entries (otherwise it would crash)
            num_transitions = len(timings)
            if (len(self._bullets) < len(timings)):
                num_transitions = len(self._bullets)
            for i in range (0, num_transitions):
                self._bullet_transitiontime.append(timings[i])




    # return True to pause the slides or False to continue
    # always unpause at start as once paused this is not called until unpause
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
        for this_bullet_num in range(0, len( self._bullet_transitiontime)):
            self._bullets[this_bullet_num].animate_bullet (self._bullet_transitiontime[this_bullet_num][0], self._bullet_transitiontime[this_bullet_num][1], current_frame)
            # if this is an end frame then set pause
            if (self._bullet_transitiontime[this_bullet_num][2] == current_frame and self.bulletpause==True):
                print ("**** Pausing ****")
                self.pause = True

        # return pause value to pause if required
        # returning true will pause the slide
        return self.pause