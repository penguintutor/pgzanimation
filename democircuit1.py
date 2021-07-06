from pgzanimation import Slide, AnimLine, AnimMarqueeLine, AnimActor
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 50
TITLE = "Basic Electrical Circuit"

# Save options
# Continue to save frames when paused?
SAVE_PAUSED = True
# enable to show frame number on screen (not included in save)
SHOW_FRAME = False
# Exit after last frame?
QUIT_END = False

# Is save enabled (otherwise just display animation)
save = True
save_files = "/home/stewart/test-animations/animation-{0:05d}.png"
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame=0
save_frame=0
pause = False

background_color = (255,255,255)
background_image = "electronics-background"

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
# allows you to group items together to make changes to all simultaneously
# often it is simpler to use shapes, but useful when you want to make changes to lots of objects
# order is important for overlapping, shape_groups are written first (so get overwritten)
# then shapes in order they appear in list
# It's not possible to change order, but you can have multiple entries with the same image and
# swap which is displayed as a way of positioning in the stack
shape_groups = {
    'wires': {
        'left': AnimMarqueeLine (bottom_left, top_left, (0,0,0), (200,200,200), width=4, animwidth=2, style="dashed", spacing=[10,10], animatedisplay=False, dashanimate=1),
        'top-start': AnimMarqueeLine (top_left, top_right, (0,0,0), (200,200,200), width=4, animwidth=2, animatedisplay=False, dashanimate=1),
        'right': AnimMarqueeLine (top_right, bottom_right, (0,0,0), (200,200,200), width=4, animwidth=2, style="dashed", spacing=[10,10], animatedisplay=False, dashanimate=1),
        'bottom': AnimMarqueeLine (bottom_right, bottom_left, (0,0,0), (200,200,200), width=4, animwidth=2, animatedisplay=False, dashanimate=1),
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
    'start-close': 5,
    'close': 10,
    'start-open': 40,
    'open': 45 
    }

# Set any initial states
# Show slide for entire animation
slides[0].show_slide(0, FRAMES)
shapes['switchlevel'].angle = 30

# Place your animations here
def animate():
    shapes['switchlevel'].rotate_tween (kf['start-close'], kf['close'], frame, 0, direction="CW")
    if (frame == kf['close']):
        for this_group in shape_groups:
            for this_shape in shape_groups[this_group].values():
                this_shape.animatedisplay=True
    shapes['switchlevel'].rotate_tween (kf['start-open'], kf['open'], frame, 30, direction="CCW")
    if (frame == kf['start-open']):
        for this_group in shape_groups:
            for this_shape in shape_groups[this_group].values():
                this_shape.animatedisplay=False

def draw():
    if (frame >= FRAMES):
        return
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
        
    # Save animation frame
    if (save == True and ( pause == False or SAVE_PAUSED == True)):
        pygame.image.save(screen.surface, save_files.format(save_frame))
    # Anything below here is displayed on screen, but not included in saves
    if SHOW_FRAME:
        # frame is incremented at end - so display number of previous frame
        screen.draw.text(str(frame-1), (20,20), color=(250, 50, 50), fontsize=60)

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