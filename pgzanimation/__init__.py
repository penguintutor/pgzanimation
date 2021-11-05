""" PGZAnimation, a library for animations

This expands upon Pygame Zero providing a simple way
to create animations. It allows all of the Pygame Zero
methods, but adds new methods that support keyframes
and tweens.
This needs to be run from your own code in Pygame Zero
using pgzrun.
Import the relevant classes that you need from pgzanimation.

** Standard animation classes
*PGZAnimation       - Abstract parent class
*AnimActor          - Sprite based animations
*AnimImage          - Same as AnimActor 
*AnimLine           - Draw a straight line
*AnimMarqueeLine    - Draw a straight line with dash / marching ants
*AnimEllipse        - Create an ellipse
*AnimFilledEllipse  - Filled ellipse
*AnimCircle         - Create circles
*AnimFilledCircle   - Filled circle
*AnimPolygon        - Create polygon from list of points
*AnimFilledPolygon  - Filled polygon
*AnimRect           - Create rectangle from a rectangle object
*AnimFilledRect     - Create a filled rectangle
*AnimText           - Create text
*AnimBullet         - Create bullet text
*AnimTriangle       - Create triangles
*AnimFilledTriangle - Create a filled triangles
*AnimLineEnd        - Line ends (eg. Arrows)

** Slide based animations
*Slide              - Default slide (simple title)
*SlideBullets       - Slide with bullet text
*SlideBulletsImages - Slide with bullet text and (opt) images
*SlideImage         - Slide with an image (Actor)

** Helper functions
*dir_vector         - gets a direction vector from an angle

For more details see http://www.penguintutor.com/pgzanimation
"""

from .animactor import AnimActor
from .animimage import AnimImage
from .animpolygon import AnimFilledPolygon, AnimPolygon
from .animrect import AnimFilledRect, AnimRect
from .animtext import AnimText
from .animbullettext import AnimBulletText
from .animellipse import AnimFilledEllipse, AnimEllipse
from .animcircle import AnimFilledCircle, AnimCircle
from .animtriangle import AnimFilledTriangle, AnimTriangle
from .animline import AnimLine
from .animlineend import AnimLineEnd
from .animmarqueeline import AnimMarqueeLine
from .animvectors import get_dir_vector
from .slide import Slide
from .slidebullets import SlideBullets
from .slidebulletsimages import SlideBulletsImages
from .slideimage import SlideImage

__version__ = '0.1.devel'