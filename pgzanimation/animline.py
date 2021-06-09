import pygame
import math
from .pgzanimation import PgzAnimation


# Draw a filled polygon based around points
class AnimLine(PgzAnimation):

    def __init__(self, start, end, color, anchor=('center', 'center'), width=1):
        super().__init__(color, anchor)
        self._start = [*start]
        self._end = [*end]
        self._width = width

        # create with a scale of 1 update later if required
        # scale moves start and end - not width
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


    # points - setting either end point replaces the unrotated points and resets angle to 0
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, new_start):
        self._start = [*new_start]
        self._angle = 0

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, new_start):
        self._start = [*new_end]
        self._angle = 0


    # Gets a rect object - can be used for collidepoint etc.
    # Uses a bounding box based on current transformations
    # Not so useful for a line, but included for consistancy
    @property
    def rect(self):
        return self.get_rect()

    def get_rect(self):
        start = self._start
        end = self._end
        low_x = min (start[0], end[0])
        high_x = max (start[0], end[0])
        low_y = min (start[1], end[1])
        high_y = max (start[1], end[1])
        
        return Rect (low_x, low_y, high_x-low_x, high_y-low_y)

    # position anchors are based on bouding rectangle 
    ## Also need to add start and end
    def calc_pos (self):
        start = self._start
        end = self._end
        # pos starts at anchor - based on a bounding rectangle
        low_x = min (start[0], end[0])
        high_x = max (start[0], end[0])
        low_y = min (start[1], end[1])
        high_y = max (start[1], end[1])

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
        rel_scale_x = (newscale[0] - self.scale_start[0]) / (end-start)
        rel_scale_y = (newscale[1] - self.scale_start[1]) / (end-start)

        self._scale[0] = self.scale_start[0] + rel_scale_x * (current-start)
        self._scale[1] = self.scale_start[1] + rel_scale_y * (current-start)
        self._transform()


    # gets vectors from self._start and end 
    # returns as (start,end)
    def _get_vectors (self):
        start_vector = ((self._start[0]-self._pos[0], self._start[1]-self._pos[1]))
        end_vector = ((self._end[0]-self._pos[0], self._end[1]-self._pos[1]))
        return [start_vector, end_vector]
    
    # Borrowed from polygon - takes two vectors (start and end)
    # then returns these as points
    
    # gets a polygon points from vectors
    # used to update rot_points
    def _get_points (self, vectors):
        return_points = []
        for vector in vectors:
            return_points.append((vector[0]+self._pos[0], vector[1]+self._pos[1]))
        return return_points


    # Updates vectors and new points using rotation and scaling
    def _transform (self):
        # use angle in radians - turns opposite way to pygame
        # to be consistant with pygame zero actor which
        # moves up with a positive angle (anti-clockwise)
        angle_rads = math.radians(self._angle) * -1
        s = math.sin(angle_rads)
        c = math.cos(angle_rads)
        # This creates a vector for start and end. It then uses
        # same transformations as for a polygon
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
        transform_points = self._get_points(new_vectors)
        # convert the two vectors into the start and end points
        self._transform_start = transform_points[0]
        self._transform_end = transform_points[1]



    def draw(self):
        if self.hide: return
        pygame.draw.line(self._surface, self._color, self._transform_start, self._transform_end, self._width)




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
        print ("Shape: Line")
        print ("Points: "+str(self._points))
        print ("Anchor: "+str(self._anchor))
        print ("Position: "+str(self._pos))
        print ("Rot Points: "+str(self._transform_start)+" "+str(self._transform_end))


    def update(self):
        pass

