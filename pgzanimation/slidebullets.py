from .pgzanimation import PgzAnimation
from pgzanimation import AnimBulletText
from .slide import Slide
import math

""" Slide showing title and bullets 
text for bullets is provided in a list bullets
 default is to place bullet in a single depth, 
 to increment depth prefix with *
 eg. 
 "bullet depth 0"
 "*bullet depth 1"
 "**bullet depth 2"
 There must not be any characters before *
 The asterix will be stripped.
 Any additional * get ignored after MAX_DEPTH (treated as normal characters)
 Escape with a \ (before first only)
 "\* bullet depth 0"
 First \ will be removed and then returned so use \\ to escape the \
bullet spacing is distance between bullets (including the bullet)
 bulletstartpos = top left
 bulletspacing = y distance
 bulletanimate - if True then reveal each bullet one at a time
        if False then show all immediately
 Other options are lists to support multiple depths
    If a depth is not included then it uses bulletstyle[0] (not previous depth)
 bulletpause will pause after each frame 
        (if return value from update checked)
 bulletstyle is list supporting each depth. 
 bulletpad can be a list of tuples (tuple representing before and after padding)
 
 Limitations: Does not currently support multiline single bullets
 Possible future addition is to add - at beginning (after *) to indicate override bulletstyle with none which would result in lining up but no
 additional bullet signal
    
 """

class SlideBullets(Slide):
    MAX_DEPTH = 10
    def __init__(self, size, title, bullets, bulletstartpos=(50,220),
            bulletspacing=80, bulletanimate=True, bulletpause=False,
            bullettransition=["appear"], bulletstyle=["circle"], bulletsize=[10], bulletpad=[10]
            ):
        super().__init__(size, title)
        self._bullets = []
        # bullet position is always top left of all bullets
        self._bullet_pos = bulletstartpos
        self.bullettransition=bullettransition
        # list of tuples for start and end of each bullet transition and after the after time (start transition, end transition, after)
        self._bullet_transitiontime = []
        # to prevent crashing must be at least one bullet - set to blank
        if len(bullets) == 0:
            bullets.append("")
        # Bullets must have their position defined when created so calculate here
        # this_y_pos is updated at the end of the for loop as each entry added
        this_y_pos = self._bullet_pos[1]
        # x_positions is a list based on each depth - start with x pos
        # (recalculated each time we encounter an additional depth of depth) 
        x_positions = [self._bullet_pos[0]]
        for this_bullet in bullets:
            # Is bullet below first depth
            this_bullet_text, this_bullet_depth = self._get_depth(this_bullet)
            # If this is first time we've seen this depth then calculate 
            # x_positions to that depth
            if (this_bullet_depth > len(x_positions)-1):
                x_positions = self._calc_x_positions(x_positions, this_bullet_depth, bulletsize, bulletpad)
            # get entries from lists (allowing for entry not defined)
            this_bullettransition = self._depth_value(
                    bullettransition, this_bullet_depth)
            this_bulletstyle = self._depth_value(
                    bulletstyle, this_bullet_depth)
            this_bulletpad = self._depth_value(
                    bulletpad, this_bullet_depth)
            this_bulletsize = self._depth_value(
                    bulletsize, this_bullet_depth)
                
            #print ("Text {}, pos {}, hide {}, transition {}, style {}, size{}, pad {}".format(this_bullet_text , 
            #    (x_positions[this_bullet_depth] , this_y_pos), bulletanimate, this_bullettransition,
            #    this_bulletstyle, this_bulletsize,
            #    this_bulletpad
            #    ))
            self._bullets.append(AnimBulletText(this_bullet_text , 
                (x_positions[this_bullet_depth] , this_y_pos), hide=bulletanimate, bullettransition=this_bullettransition,
                bulletstyle=this_bulletstyle, bulletsize=this_bulletsize,
                bulletpad=this_bulletpad
                ))
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
        
    ### Internal methods for calculating values for bullets
    
    """ get depth of bullet (based on * prefix)
    return as a tuple with edited string (* stripped) 
    and depth number (starting at 0 if no *)
    """
    def _get_depth(self, bulletstring) :
        # Most common case - top depth just return
        if (bulletstring[0] != "*" and bulletstring[0] != "\\"):
            return (bulletstring, 0)
        current_depth = 0
        current_string = bulletstring
        while (current_depth < self.MAX_DEPTH):
            # Strip one character at a time and increment depth
            if (current_string[0] == "\\"):
                current_string = current_string[1:]
                break
            elif (current_string[0] == "*"):
                current_string = current_string[1:]
                current_depth += 1
            else:
                break
        return (current_string, current_depth)
    
    """ calculate x_positions that are not yet defined
    it works out spacing of where the next depth up will be
    which becomes the starting point for this depth
    """
    def _calc_x_positions(self, 
            positions, this_bullet_depth, bulletsize, bulletpad
            ) :
        # start at end of current calculations
        for i in range(len(positions), this_bullet_depth+1):
            # do we have a bulletpad & size at this depth
            # if not use bulletpad[0] & size
            if (len(bulletsize) > i-1):
                this_bulletsize = bulletsize[i-1]
            else:
                this_bulletsize = bulletsize[0]
            if (len(bulletpad) > i-1):
                this_bulletpad = bulletpad[i-1]
            else:
                this_bulletpad = bulletpad[0]
            # this_bulletpad is either single entry or two for pre and post
            if (type(this_bulletpad) == tuple or type(this_bulletpad) == list):
                total_this_pad = this_bulletpad[0] + this_bulletpad[1]
            else:
                total_this_pad = this_bulletpad * 2
                
            # calculate this depth
            positions.append(positions[i-1] + total_this_pad + this_bulletsize)
        return positions
        
    """ Generic method which will allow for entry not defined in a list
    pass a list and index number and it will either return that value
    or if that doesn't exist it will return the default [0] value
    """
    def _depth_value (self, value_list, position):
        # If it's not a list then single value passed, so return that 
        if (type(value_list) != tuple and type(value_list) != list):
            return value_list
        if (len(value_list) > position):
            return value_list[position]
        else :
            return value_list[0]