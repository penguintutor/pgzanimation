""" PGZAnimation, a library for animations

This expands upon Pygame Zero providing a simple way
to create animations. It allows all of the Pygame Zero
methods, but adds new methods that support keyframes
and tweens.
This needs to be run from your own code in Pygame Zero
using pgzrun.
Import the relevant classes that you need from pgzanimation.

For more details see http://www.penguintutor.com/pgzanimation
"""

from .animactor import AnimActor
from .animpolygon import AnimFilledPolygon, AnimPolygon
from .animrect import AnimFilledRect, AnimRect
from .animtext import AnimText
from .animbullettext import AnimBulletText
from .animellipse import AnimFilledEllipse, AnimEllipse
from .animcircle import AnimFilledCircle, AnimCircle
from .animline import AnimLine
from .animmarqueeline import AnimMarqueeLine
from .animvectors import get_dir_vector
from .slide import Slide
from .slidebullets import SlideBullets

__version__ = '0.1.devel'
