import pygame
import math
from pgzanimation import PgzAnimation

# Does not support opacity


# Draw a filled polygon based around points
class AnimFilledPolygon(PgzAnimation):

    def __init__(self, points, color, anchor=('center', 'center')):
        super().__init__(color, anchor)
        self._points = [*points] # convert from tuple to list

        # create with a scale of 1 update later if required
        self._scale = [1,1]

        # set pos based on anchor position
        self._pos = [0,0]
        self.calc_pos()

        # These are used for transformations
        self.move_start_pos = self._pos
        self.rotate_start_angle = self._angle
        self.scale_start = self._scale

        # polygon with transformation - start at 0 rotation
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


    # points - setting points replaces the unrotated points and resets angle to 0
    @property
    def points(self):
        return self._transform_points

    @points.setter
    def points(self, new_points):
        self._points = [*new_points]
        self._angle = 0
    
    # Gets a rect object - can be used for collidepoint etc.
    # Uses a bounding box based on current transformations
    @property
    def rect(self):
        return self.get_rect()
        
    def get_rect(self):
        low_x = None
        low_y = None
        high_x = None
        high_y = None
        for this_point in self._transform_points:
            if (low_x == None or this_point[0] < low_x):
                low_x = this_point[0]
            if (high_x == None or this_point[0] > high_x):
                high_x = this_point[0]
            if (low_y == None or this_point[1] < low_y):
                low_y = this_point[1]
            if (high_y == None or this_point[1] > high_y):
                high_y = this_point[1]
        return Rect (low_x, low_y, high_x-low_x, high_y-low_y)

    def calc_pos (self):
        # pos starts at anchor - based on a bounding rectangle
        low_x = None
        low_y = None
        high_x = None
        high_y = None
        # get 4 furthest points
        for this_point in self._points:
            if (low_x == None or this_point[0] < low_x):
                low_x = this_point[0]
            if (high_x == None or this_point[0] > high_x):
                high_x = this_point[0]
            if (low_y == None or this_point[1] < low_y):
                low_y = this_point[1]
            if (high_y == None or this_point[1] > high_y):
                high_y = this_point[1]


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

    def move_rel (self, delta):
        dx = delta[0]
        dy = delta[1]
        for i in range(0, len(self._points)):
            self._points[i] = [
                self._points[i][0] + dx,
                self._points[i][1] + dy
                ]
        # recalculate pos
        self.calc_pos()
        # recalculate rotation
        self._transform()


    # gets vectors from self._pos to points of a polygon
    def _get_vectors (self):
        return_vectors = []
        for vector in self._points:
            return_vectors.append((vector[0]-self._pos[0], vector[1]-self._pos[1]))
        return return_vectors

    # gets a polygon points from vectors
    # used to update rot_points
    def _get_points (self, vectors):
        return_points = []
        for vector in vectors:
            return_points.append((vector[0]+self._pos[0], vector[1]+self._pos[1]))
        return return_points

    # rotate to an absolute from current position
    def rotate_tween (self, start, end, current, angle):
        if (current < start or current > end):
            return
        if (current == start):
            self.rotate_start_angle = self._angle
        d_angle = (angle - self.rotate_start_angle) / (end-start)
        new_angle = self.rotate_start_angle + d_angle * (current-start)
        self.rotate(new_angle)

    # rotate a relative amount
    def rotate_rel_tween (self, start, end, current, angle):
        if (current < start or current > end):
            return
        if (current == start):
            self.rotate_start_angle = self._angle
        rel_angle = angle - rotate_start_angle / (end-start)
        self.rotate(self._angle+rel_angle)

    def rotate (self, angle):
        self._angle = angle
        self._transform()
        
    # scale to newscale from current scale
    def scale_tween (self, start, end, current, newscale):
        if (current < start or current > end):
            return
        if (current == start):
            self.scale_start = self._scale
        # rel between start and end
        rel_scale_x = newscale[0] - self.scale_start[0] / (end-start)
        rel_scale_y = newscale[1] - self.scale_start[1] / (end-start)
        
        self._scale[0] = self.scale_start[0] + rel_scale_x * (current-start)
        self._scale[1] = self.scale_start[1] + rel_scale_y * (current-start)
        self._transform()
        


    # Updates vectors and new points using rotation and scaling
    def _transform (self):
        angle_rads = math.radians(self._angle)
        s = math.sin(angle_rads)
        c = math.cos(angle_rads)
        new_vectors=[]
        # get vectors with 0 degrees rotation
        vectors = self._get_vectors()
        # update vectors with degree rotation
        for this_vector in vectors:
            # scale first (scale original shape)
            scale_x = this_vector[0] * self._scale[0]
            scale_y = this_vector[1] * self._scale[1]
            # rotate scaled shape
            new_x = scale_x * c - scale_y * s
            new_y = scale_x * s + scale_y * c
            new_vectors.append((new_x, new_y))
        self._transform_points = self._get_points(new_vectors)



    def draw(self):
        if self.hide: return
        pygame.draw.polygon(self._surface, self._color, self._transform_points)


    # tweened movement to absolute position
    def move_tween (self, start, end, current, goto):
        if (current < start or current > end):
            return
        if (current == start):
            self.move_start_pos = self._pos
        # work out delta between start and end
        dx = (goto[0] - self.move_start_pos[0]) / (end-start)
        dy = (goto[1] - self.move_start_pos[1]) / (end-start)

        newpos = [0,0]
        # Add delta to start position
        newpos[0] = self.move_start_pos[0] + dx * (current - start)
        newpos[1] = self.move_start_pos[1] + dy * (current - start)
        self.move (newpos)

    # tweened movement to relative position
    def move_rel_tween (self, start, end, current, delta):
        if (current < start or current > end):
            return
        # work out delta between start and end
        dx = delta[0] / (end-start)
        dy = delta[1] / (end-start)

        newpos = [0,0]
        # Add delta to start position
        newpos[0] = self._pos[0] + dx
        newpos[1] = self._pos[1] + dy
        self.move (newpos)

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
class AnimPolygon (AnimFilledPolygon):

    def __init__(self, points, color, anchor=('center', 'center'), width=1):
        super().__init__(points, color, anchor)
        self.width = width

    def draw(self):
        if self.hide: return
        pygame.draw.polygon(self._surface, self._color, self._transform_points, self.width)