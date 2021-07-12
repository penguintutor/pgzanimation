import pygame
import math
from .pgzanimation import PgzAnimation

# Does not support opacity

# Draw a filled ellipse (contained within a rect)
# Current version can be horizontal or vertical - rotation moves in 90 degree 
# increments - rounding to nearest increment
class AnimFilledEllipse(PgzAnimation):

    def __init__(self, rect, color, anchor=('center', 'center')):
        super().__init__(color, anchor)
        self._rect = rect

        # create with a scale of 1 update later if required
        self._scale = [1,1]

        # set pos based on anchor position
        self._pos = [0,0]
        self.calc_pos()

        # These are used for transformations
        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle
        self.scale_start = self._scale

        # rect with transformation - start at 0 rotation
        self._transform_rect = rect
                                 

    # Gets a rect object - can be used for collidepoint etc.
    # Uses a bounding box based on current transformations
    @property
    def rect(self):
        return self.get_rect()

    @rect.setter
    def rect(self, new_rect):
        self._rect = new_rect
        self._transform()

    # used to transform a object - scale
    # value (1,1) is default size
    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, new_scale):
        self._scale = new_scale
        self._transform()

    def get_rect(self):
        return self._rect

    def calc_pos (self):
        # pos starts at anchor - based on a bounding rectangle
        low_x = self._rect.left
        low_y = self._rect.top
        high_x = self._rect.right
        high_y = self._rect.bottom

        if self._anchor[0] == "left":
            self._pos[0] = low_x
        elif self._anchor[0] == "right":
            self._pos[0] = high_x
        else: # center
            diff = (high_x - low_x) / 2
            self._pos[0] =  low_x + diff
        if self._anchor[1] == "top":
            self._pos[1] = low_y
        elif self._anchor[1] == "bottom":
            self._pos[1] = high_y
        else: # center
            diff = (high_y - low_y) / 2
            self._pos[1] = low_y + diff

    # Reset to defaults - scale, angle and anchor
    def reset(self):
        self._scale = [1,1]
        self._angle = 0
        self._anchor = ("center", "center")
        self._transform()

    def move_rel (self, delta):
        dx = delta[0]
        dy = delta[1]
        self._rect.left += dx
        self._rect.top += dy
        
        # recalculate pos
        self.calc_pos()
        self._transform()
 


    def rotate (self, angle):
        angle %= 360
        self._angle = angle
        self._transform()


    # scale to newscale from current scale
    def scale_tween (self, start, end, current, newscale):
        if (current < start or current > end):
            return
        if (current == start):
            self.scale_start = self._scale
        # rel between start and end
        rel_scale_x = (newscale[0] - self.scale_start[0]) / (end-start)
        rel_scale_y = (newscale[1] - self.scale_start[1]) / (end-start)

        self._scale[0] = self.scale_start[0] + rel_scale_x * (current-start)
        self._scale[1] = self.scale_start[1] + rel_scale_y * (current-start)
        self._transform()


    def _transform(self):
        self._transform_rect = self._rect.copy()
        # Find top left based on anchor position and rotation
        # Only if angle is between 45 and 315 - otherwise just use current rect
        if (self._angle <45 or self._angle>=315):
            return
        # Todo
        # Need to add rotation of rectangle points
        # turns opposite way to pygame
        # limited rotation - so calc manually
        
        # x rotation
        if (self._anchor[0] == "left"):
            if (self._angle >= 135 and self._angle < 225):
                self._transform_rect.left-=self._transform_rect.width
            elif (self._angle >= 225 and self._angle < 315):
                self._transform_rect.left-=self._transform_rect.height
        elif (self._anchor[0] == "right"):
            if (self._angle >= 45 and self._angle < 135):
                self._transform_rect.left+=self._transform_rect.height+self._transform_rect.width
            elif (self._angle >= 135 and self._angle < 225):
                self._transform_rect.left+=self._transform_rect.width*2   
            elif (self._angle >= 225 and self._angle < 315):    
                self._transform_rect.left+=self._transform_rect.width -  self._transform_rect.height          
        elif (self._anchor[0] == "center"):
            if (self._angle >= 45 and self._angle < 135):
                self._transform_rect.left+=self._transform_rect.width/2-self._transform_rect.height/2
            elif (self._angle >= 225 and self._angle < 315):
                self._transform_rect.left+=self._transform_rect.width/2-self._transform_rect.height/2
            
        # y rotation
        if (self._anchor[1] == "top"):
            if (self._angle >= 45 and self._angle < 135):
                self._transform_rect.top-=self._transform_rect.width
            if (self._angle >= 135 and self._angle < 225):
                self._transform_rect.top-=self._transform_rect.height
        if (self._anchor[1] == "bottom"):
            if (self._angle >= 45 and self._angle < 135):
                self._transform_rect.top+=self._transform_rect.height
            if (self._angle >= 135 and self._angle < 225):
                self._transform_rect.top+=self._transform_rect.height*2
            if (self._angle >= 225 and self._angle < 315):  
                self._transform_rect.top+=self._transform_rect.height-self._transform_rect.width
        elif (self._anchor[1] == "center"):
            if (self._angle >= 45 and self._angle < 135):
                self._transform_rect.top+=self._transform_rect.height/2-self._transform_rect.width/2
            elif (self._angle >= 225 and self._angle < 315):
                self._transform_rect.top+=self._transform_rect.height/2-self._transform_rect.width/2
 
        # swap width and height 90 and 270
        if (self._angle >= 45 and self._angle < 135 or self._angle >= 225 and self._angle < 315):
            self._transform_rect.width = self._rect.height
            self._transform_rect.height = self._rect.width
        

        


    def draw(self):
        if self.hide: return
        pygame.draw.ellipse(self._surface, self.color_val(), self._transform_rect)




    # Moves immediately to new position
    def move (self, newpos):
        # work out delta between new and old
        dx = newpos[0] - self._pos[0]
        dy = newpos[1] - self._pos[1]
        self._pos = newpos
        self.move_rel ((dx, dy))


    # Print test with information about the shape
    # Used for debugging
    def print_info (self):
        print ("Shape: Polygon")
        print ("Points: "+str(self._points))
        print ("Anchor: "+str(self._anchor))
        print ("Position: "+str(self._pos))
        print ("Rot Points: "+str(self._transform_points))


    def update(self):
        pass


# Based on filled polygon, but with width set to a value
# Default width is 1, but can be changed for thicker lines
# Setting width to 0 is same as filled polygon - setting less than 0 does not display
class AnimEllipse (AnimFilledEllipse):

    def __init__(self, rect, color, anchor=('center', 'center'), width=1):
        super().__init__(points, color, anchor)
        self.width = width


    def draw(self):
        if self.hide: return
        pygame.draw.ellipse(self._surface, self.color_val(), self._transform_rect, self.width)