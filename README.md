# PgzAnimation

A library for creating animations in Pygame Zero, which can then be 
exported as png image files. These can then be combined into a video animation.

Uses object oriented approproach, where you create an object representing 
a Actor (sprite), a shape / line or Text. You can then manipulate the
object based on keyframes with tweens between the keyframes.

This is different from the Animation feature within Pygame Zero. This
is specifically created to support the keyframes and tweens between them.
It still runs as a pygame zero application and can be used in conjunction with any other pygame zero objects and methods (including Pygame Zero animations).
This handles all objects in an object orientated way and adds additional
features things such as tween scaling and tween rotation. 

## Project status

This is currently in an early development. It includes some basic functionality
which will be expanding in future. The interface and object names may change
significantly in future.


## Features / limitations

There must be only 1 movement happening at a time. This makes sense as 
otherwise there may be confusion on what should happen eg. if a tween 
should still finish at it's current target position or whether that should
be relative.
Having multiple movements at the same time is unpredictable and my result in
strange behaviour.

It is possible to have different types of transformations at the same time. 
You can for example have a scale tween or a rotate tween happening at the same 
time as a move tween.

Do not attempt to hide / unhide during animate transitions eg. animate_bullet
as depending upon the transition type the hide / unhide may be overridden.

## Understanding the methods

Some methods and attribute changes are intended to have a direct effect, 
the tween methods are all designed to happen between certain frames. It is 
important that these are called on every frame within the start and end
keyframes. Where a method refers to goto then that is absolute, 
where it refers to a delta then that is relative to the current value. Where
this is applied to a tween then it is relative to the position at the start
of the tween (see limitations about possible conflicts). It is not possible to
use position relative to original position if that has already changed (unless you record the position yourself). Rotation angles are in degrees
and are normally absolute angles from the original orientation, but can be
relative for some methods.

## Converting from png files to a animation

Animation output files are saved as png files. These can be converted to an
MP4 animation using the below command line (Linux system with ffmpeg
installed).

ffmpeg -framerate 25 -i animation-%05d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p output.mp4


## Future plans

Currently extending the different objects that can be created and adding
additional features.

All tweens are currently linear, but a future feature may include
adding the tween parameter similar to the Pygame Zero animation.

