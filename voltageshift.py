from pgzanimation import Slide, AnimLine, AnimMarqueeLine, AnimActor, AnimCircle, AnimText
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 50
TITLE = "Inverting buffer"

# Save options
# Continue to save frames when paused?
SAVE_PAUSED = True
# enable to show frame number on screen (not included in save)
SHOW_FRAME = True
# enable to show mouse position (useful for designing animations)
SHOW_MOUSE = True
# Exit after last frame?
QUIT_END = False

# Is save enabled (otherwise just display animation)
save = False
save_files = "/home/stewart/test-animations/animation-{0:05d}.png"
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame=0
save_frame=0
pause = False

background_color = (255, 255, 255)
background_image = "electronics-background"

# Add own variables for convenience
input_start = (470, 410)
mosfet_pos = (690, 413)
rb_pos = (560, 413)
input_mosfet = (586, 410)
source_mosfet = (713, 469)
drain_mosfet = (713, 354)
ground_start = (432, 550)
rl_bottom = (713, 320)
rl_pos = (714, 275)
rl_top = (714, 229)
plus_start = (432, 180)
out_start = (714, 344)
out_end = (770, 344)


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
    'wires-stage1': {
        'input': AnimMarqueeLine (
                (input_start[0]+5, input_start[1]), (input_start[0] + 62, input_start[1]),
                (255, 165, 0), (0, 0, 0),
                width=4, animwidth=2, style="dashed", spacing=[10,10], animatedisplay=False, dashanimate=1),
        'tomosfet': AnimMarqueeLine (
                input_mosfet, (input_mosfet[0] + 77, input_start[1]),
                (255, 165, 0), (0, 0, 0),
                width=4, animwidth=2, style="dashed", spacing=[10,10], animatedisplay=False, dashanimate=1),
        'toground':  AnimMarqueeLine (
                source_mosfet, (source_mosfet[0], ground_start[1]),
                (40,40,180), (0, 0, 0),
                width=4, animwidth=2, style="dashed", spacing=[10,10], animatedisplay=False, dashanimate=1),
        'plustorl':  AnimMarqueeLine (
                (rl_top[0], plus_start[1]), rl_top,
                (180,40,40), (0, 0, 0),
                width=4, animwidth=2, style="dashed", spacing=[10,10], animatedisplay=False, dashanimate=1),
        'rltodrain':  AnimMarqueeLine (
                rl_bottom, drain_mosfet,
                (180,40,40), (0, 0, 0),
                width=4, animwidth=2, style="dashed", spacing=[10,10], animatedisplay=False, dashanimate=1),
        },
    'fixedwires' : {
        'plus':  AnimLine (
                plus_start, (plus_start[0] + 400, plus_start[1]),
                (180,40,40), (0, 0, 0),
                width=4),
        'ground':  AnimLine (ground_start, (ground_start[0] + 400, ground_start[1]),
                (40,40,180), (0, 0, 0),
                width=4),
        }
    }
shapes = {
    'terminal1' : AnimCircle ((input_start),10, (0,0,0), width=4),
    'inputtext' : AnimText ("Input", (input_start[0] - 50, input_start[1] - 50), (0,0,0), fontsize=40),
    'mosfet1' : AnimActor ("mosfet", mosfet_pos),
    'rb' :  AnimActor ("resistorh", rb_pos),
    'rl' :  AnimActor ("resistorv", rl_pos),
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


# Place your animations here
def animate():
    #shapes['switchlevel'].rotate_tween (kf['start-close'], kf['close'], frame, 0, direction="CW")
    if (frame == kf['close']):
        for this_group in shape_groups:
            for this_shape in shape_groups[this_group].values():
                this_shape.animatedisplay=True
    #shapes['switchlevel'].rotate_tween (kf['start-open'], kf['open'], frame, 30, direction="CCW")
    if (frame == kf['start-open']):
        for this_group in shape_groups:
            for this_shape in shape_groups[this_group].values():
                this_shape.animatedisplay=False

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

    # Save animation frame
    if (save == True and ( pause == False or SAVE_PAUSED == True)):
        pygame.image.save(screen.surface, save_files.format(save_frame))
    # Anything below here is displayed on screen, but not included in saves
    if SHOW_FRAME:
        # frame is incremented at end - so display number of previous frame
        screen.draw.text("Frame "+str(frame-1), (20, 20), color=(250, 50, 50), fontsize=60)
    if SHOW_MOUSE:
        screen.draw.text("Mouse "+str(pygame.mouse.get_pos()), (20, 60), color=(50, 50, 250), fontsize=60)

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