import math

# get a direction vector (x and y delta) from an angle
# Useful function for setting a tween in a certain direction
def get_dir_vector (angle):
        angle_rads = math.radians(angle)
        s = math.sin(angle_rads)
        c = math.cos(angle_rads)
        
        return [c, s*-1]