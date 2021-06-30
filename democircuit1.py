from pgzanimation import Slide, AnimLine, AnimMarqueeLine, AnimActor
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 1000
TITLE = "Basic Electrical Circuit"

# Save options
# Continue to save frames when paused?
SAVE_PAUSED = True
# enable to show frame number on screen (not included in save)
SHOW_FRAME = True
# Exit after last frame?
QUIT_END = False

# Is save enabled (otherwise just display animation)
save = True
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame=0
save_frame=0
pause = False

background_color = (255,255,255)
background_image = ""

# Add own variables for convenience
top_left = (335,250)
top_right = (935,250)
bottom_right = (935,600)
bottom_left = (335,600)

slides = [
    Slide((WIDTH,HEIGHT), TITLE)
    ]

# Can use shapes and/or shape_groups
# shape groups are a dictionary of shape dictionaries
# allows you to group items together to make changes to all simulataneously
# often simpler to use shapes, but useful when you want to make changes to lots of objects
# order is important for overlapping, shape_groups are written first (so get overwritten)
# then shapes in order they appear in list
# It's not possible to change order, but you can have multiple entries with the same image and
# swap which is displayed as a way of positioning in the stack
shape_groups = {
    'wires': {
        'left': AnimMarqueeLine (bottom_left, top_left, (0,0,0), (128,128,128), width=4, style="dashed", spacing=[10,10]),
        'top-start': AnimMarqueeLine (top_left, top_right, (0,0,0), (128,128,128), width=4),
        'right': AnimMarqueeLine (top_right, bottom_right, (0,0,0), (128,128,128), width=4, style="dashed", spacing=[10,10]),
        'bottom': AnimMarqueeLine (bottom_right, bottom_left, (0,0,0), (128,128,128), width=4),
        }
    }
shapes = {
    'battery' : AnimActor ("battery", (340,425)),
    'light' : AnimActor ("light-off", (935,425)),
    'switchshape' : AnimActor ("switchnodes", (650, 250)),
    'switchlevel' : AnimLine ((615,246), (687,246), (0,0,0), anchor=("left","top"), width=4)
    }

# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = []

# key frames (can just use number if preferred, but allows labels)
kf = {
    'start': 0,
    'start-close': 200,
    'close': 205,
    'start-open': 400,
    'close': 405
    
    }

# Show slide for entire animation
slides[0].show_slide(0, FRAMES)

# Place your animations here
def animate():
    pass



def draw():
    screen.clear()
    screen.fill(background_color)
    if (background_image != ""):
        screen.blit(background_image, (0,0))

    for this_slide in slides:
        this_slide.draw()
    for this_group in shape_groups:
        for this_shape in shape_groups[this_group].values():
            this_shape.draw()
    for this_shape in shapes.values():
        this_shape.draw()

def update():
    controls()
    animate()
    # Call update for all objects in case they need to animate
    for this_slide in slides:
        this_slide.update()
    for this_group in shape_groups:
        for this_shape in shape_groups[this_group].values():
            this_shape.update()
    for this_shape in shapes.values():
        this_shape.update()



def controls():
    global frame, save_frame, pause
    # Stop updating once end reached
    if (frame > FRAMES):
        if (QUIT_END):
            pygame.quit()
            sys.exit()
        return
        # Are we currently paused
    if (pause == True):
        if (SAVE_PAUSED):
            save_frame += 1
        return
    # slides need to check for pause
    for this_slide in slides:
        if (this_slide.update(frame) == True): pause=True

    frame += 1
    save_frame += 1
    print ("Frame is {}".format(frame))

# Handle keys - when released
def on_key_up (key, mod):
    global pause
    # quit on q / esc
    if (key == keys.ESCAPE or key == keys.Q):
        pygame.quit()
        sys.exit()
    # Space / p to pause / unpause
    if (key == keys.SPACE or key == keys.P):
        pause = not pause

# Handle mouse up (to remove pause)
def on_mouse_up (pos, button):
    global pause
    pause = False