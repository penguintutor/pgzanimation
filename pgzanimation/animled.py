from .animellipse import AnimFilledEllipse
import pygame
import math
from copy import copy
from pygame import Color
# LED - currently a circle with an inner brighter circles when on
# Adds ability to turn on and off
# LED on then outer is color and #40404, #808080, #a0a0a0
# When off then Center is color and outer circle is color / 2
# Suggestion if want bright white then use #c7c7c7 - inner is slightly lighter
#led_type "standard" (color when off), "clear" or "rgb" - grey when off regardless of color (fixed color)

# Must only have 1 movement happening at a time - otherwise confusion over which applies
class AnimLed(AnimFilledEllipse):

    #Pass a rect object and color, anchor optional
    def __init__(self, pos, radius, color, anchor=('center', 'center'), led_type="standard", state="on"):
        # angle is required but meaningless for a circle as it is the same when rotated
        self._angle = 0
        # create rect from pos and radius
        self._rect = self.circle_to_rect(pos,radius,anchor)
        self.radius = radius
        # state can be "on" or "off"
        self.state = state
        self.led_type = led_type
        self._led_color = color
        #self._color = color
        
        # Create the outer circle
        super().__init__(self._rect, self.get_outer_color(), anchor)
        # Create a smaller circle
        self.inner_circles = []
        self.inner_circles.append (AnimFilledEllipse(self.sml_rect(0.75), self.get_inner_color(1), anchor=('center', 'center')))
        self.inner_circles.append (AnimFilledEllipse(self.sml_rect(0.5), self.get_inner_color(2), anchor=('center', 'center')))
        self.inner_circles.append (AnimFilledEllipse(self.sml_rect(0.25), self.get_inner_color(3), anchor=('center', 'center')))


    def on(self):
        self.state = "on"
        self.update()

    def off(self):
        self.state = "off"
        self.update()


    # override methods to add inner led_type

    def draw(self):
        super().draw()
        for this_circle in self.inner_circles:
            this_circle.draw()

    def move_rel (self, delta):
        super().move_rel(delta)
        for this_circle in self.inner_circles:
            this_circle.move_rel(delta)

    # convert current rect to a smaller version factor should be value 0 to 1
    # Uses center of circle and factor * radius
    def sml_rect(self, factor):
        return self.circle_to_rect(self.get_center(), self.radius * factor, ('center', 'center'))


    def get_outer_color(self):
        #print ("Color is "+str(type(self._color)))

        # First convert to a color object
        # If it's a tuple then need to expand
        if (type(self._led_color) == pygame.Color):
            set_color = copy(self._led_color)
        elif (type(self._led_color) == tuple):
            set_color = Color(*self._led_color)
        else:
            set_color = Color(self._led_color)
        if (self.state == "on"):
            return set_color
        # if off then outer is color / 2
        elif (self.led_type == "standard"):
            print ("R is {}".format(set_color.r))
            set_color.r = math.floor(set_color.r / 2)
            set_color.g = math.floor(set_color.g / 2)
            set_color.b = math.floor(set_color.b / 2)
        # Otherwise clear / rgb (grey color)
        else:
            set_color = Color('#575757')

        return set_color

    # also takes variable level to determine factor
    # level 0 would be outer (so don't use this)
    # level 1 to 3 are decreasing to middle
    def get_inner_color(self, level):
        on_factor = [0x00, 0x40, 0x80, 0xa0]
        #print ("Color is "+str(type(self._color)))
        # First convert to a color object
        # If it's a tuple then need to expand
        if (type(self._led_color) == pygame.Color):
            set_color = copy(self._led_color)
        elif (type(self._color) == tuple):
            set_color = Color(*self._led_color)
        else:
            set_color = Color(self._led_color)

        # if on then inner is color * 2
        if (self.state == "on"):
            # sat_value is the value at which it becomes white
            # in that case set to white instead of going beyond 255
            sat_value = 255 - on_factor[level]
            if (set_color.r > sat_value):
                set_color.r = 255
            else:
                set_color.r += on_factor[level]
            if (set_color.g > sat_value):
                set_color.g = 255
            else:
                set_color.g += on_factor[level]
            if (set_color.b > sat_value):
                set_color.b = 255
            else:
                set_color.b += on_factor[level]
        # If off and standard then return color
        elif (self.led_type == "standard"):
            return set_color
        # Otherwise clear / rgb (grey color)
        else:
            set_color = Color('#727272')
        return set_color


    def circle_to_rect(self, pos, radius, anchor):
        xpos = pos[0]
        if (anchor[0] == "center"):
            xpos = pos[0] - radius
        elif (anchor[0] == "right"):
            xpos = pos[0] - 2 * radius
        # If left then leave as pos[0]
        ypos = pos[1]
        if (anchor[1] == "center"):
            ypos = pos[1] - radius
        elif (anchor[1] == "bottom"):
            ypos = pos[1] - 2 * radius
        # If top then leave as pos[1]
        return pygame.Rect(xpos, ypos, 2 * radius, 2 * radius)
    
    def update(self):
        # Update colors
        self.color = self.get_outer_color()
        # Update inner circles
        inner_level = 1
        for inner_circle in self.inner_circles:
            inner_circle.color = self.get_inner_color(inner_level)
            inner_level += 1

    # Color needs to be applied across inner LEDs
    @property
    def led_color(self):
        return self._led_color

    @led_color.setter
    def led_color(self, new_color):
        self._led_color = new_color
        self.update()
       
    

    # Gets a rect object - can be used for collidepoint etc.
    # Uses a bounding box based on current transformations
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, new_radius):
        self._radius = new_radius
        self._transform()
