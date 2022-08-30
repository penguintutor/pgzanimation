from pgzanimation import AnimFilledTriangle, AnimText, AnimFilledCircle, AnimLine, AnimActor, get_dir_vector, AnimFilledPolygon
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 720
TITLE = "PGZAnimation - Clock demo"

# Save options
# Continue to save frames when paused?
SAVE_PAUSED = True
# enable to show frame number on screen (not included in save)
SHOW_FRAME = False
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

background_color = (0,255,0)
background_image = ""

# min hand from y 218 to 380
hand_width = 10
hand_min_len = 380-218
hand_min_pos = (WIDTH/2, hand_min_len/2 + 218)


# Can use shapes and/or shape_groups
# shape groups are a dictionary of shape dictionaries
# allows you to group items together to make changes to all simulataneously
# often simpler to use shapes, but useful when you want to make changes to lots of objects
# order is important for overlapping, shape_groups are written first (so get overwritten)
# then shapes - in order they appear in list
# It's not possible to change order, but you can have multiple entries with the same image and
# swap which is displayed as a way of positioning in the stack
shape_groups = {}
shapes = {
    'clock': AnimActor ("clock-background", (WIDTH/2,HEIGHT/2)),
    'hand-min': AnimActor ("handmin", (WIDTH/2,HEIGHT/2)),
    'hand-hour': AnimActor ("handhour", (WIDTH/2,HEIGHT/2)),
    'hand-centre': AnimActor ("handcentre", (WIDTH/2,HEIGHT/2))
}

# Add any pauses to this
pause_frames = []

# key frames (can just use number if preferred, but this allows labels)
kf = {
    'start': 0,
    'end': 3600
    }


def draw():
    screen.clear()
    screen.fill(background_color)
    if (background_image != ""):
        screen.blit(background_image, (0,0))

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
    if SHOW_MOUSE:
        screen.draw.text("Mouse "+str(pygame.mouse.get_pos()), (20, 60), color=(50, 50, 250), fontsize=60)

def update():
    controls()
    animate()


# Place your animations here
def animate():
    # Add animations here
    shapes['hand-min'].angle-=6
    shapes['hand-hour'].angle-=0.5
    pass




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