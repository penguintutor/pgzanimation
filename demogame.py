from pgzanimation import AnimFilledRect, AnimText, AnimFilledCircle, AnimLine, AnimActor, get_dir_vector
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 700
TITLE = "PGZAnimation - Game demo"

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
background_image = "starfield"

# create variables (constants) to simplify instructions
shot234_vector_1 = get_dir_vector(-60)
shot2_target = [0,0]

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
    # One shot per spacecraft
    # shots come first so they don't go over a ship
    'shot1': AnimActor ("shot", (0,0), hide=True),
    'shot2': AnimActor ("shot", (0,0), hide=True),
    'shot3': AnimActor ("shot", (0,0), hide=True),
    'shot4': AnimActor ("shot", (0,0), hide=True),

    'ship1': AnimActor ("spacecraft1", (700,750)),
    'ship2': AnimActor ("spacecraft2", (300,150),  angle=180),
    'ship3': AnimActor ("spacecraft2", (220,90),  angle=180),
    'ship4': AnimActor ("spacecraft2", (380,90),  angle=180)
}



# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = []

# key frames (can just use number if preferred, but this allows labels)
kf = {
    'start': 0,
    'see_ship1': 100,
    'see_others': 130,
    'aim1': 190,
    'fire1-target': 260,
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

def update():
    controls()
    animate()


# Place your animations here
def animate():
    global shot2_target
    # Add animations here
    # ships fly forwards
    shapes['ship1'].move_tween(kf['start'], kf['see_others'], frame, (700, 630))
    shapes['ship2'].move_tween(kf['start'], kf['see_ship1'], frame, (300, 280))
    # ship 3 and 4 are deliberately slightly slower
    shapes['ship3'].move_tween(kf['start'], kf['see_ship1'], frame, (220, 200))
    shapes['ship4'].move_tween(kf['start'], kf['see_ship1'], frame, (380, 200))
    # enemies spot ship and turn towards it
    shapes['ship2'].move_tween(kf['see_ship1'], kf['aim1'], frame, (400, 330))
    shapes['ship2'].rotate_rel_tween(kf['see_ship1'], kf['aim1'], frame, 30)
    shapes['ship3'].move_tween(kf['see_ship1'], kf['aim1'], frame, (280, 360))
    shapes['ship3'].rotate_rel_tween(kf['see_ship1'], kf['aim1'], frame, 30)
    shapes['ship4'].move_tween(kf['see_ship1'], kf['aim1'], frame, (390, 210))
    shapes['ship4'].rotate_rel_tween(kf['see_ship1'], kf['aim1'], frame, 30)
    # friendly moves slightly right to avoid
    shapes['ship1'].move_tween(kf['see_others'], kf['aim1'], frame, (720, 590))
    shapes['ship1'].rotate_rel_tween(kf['see_others'], kf['aim1'], frame, 20, direction="CW")

    #ships 2 to 4 fire
    if (frame == kf['aim1']):
        shapes['shot2'].pos = shapes['ship2'].pos
        shot2_target = [
            shapes['shot2'].pos[0]+shot234_vector_1[0]*600,
            shapes['shot2'].pos[1]+shot234_vector_1[1]*600
        ]
        shapes['shot3'].pos = shapes['ship3'].pos
        shapes['shot4'].pos = shapes['ship4'].pos
        shapes['shot2'].hide = False
        shapes['shot3'].hide = False
        shapes['shot4'].hide = False
        shapes['shot2'].angle = 210
        shapes['shot3'].angle = 210
        shapes['shot4'].angle = 210

    # Send shot via motion
    shapes['shot2'].move_tween(kf['aim1'], kf['fire1-target'], frame, shot2_target)


    #shapes['leftbat'].move_tween(time_bat[3]+30, time_bat[4], frame, (leftbat_x, 160))
    #if (frame == time_bat[4]):
    #    shapes['rightscore'].text = "01"

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