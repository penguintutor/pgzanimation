from pgzanimation import AnimFilledRect, AnimText, AnimFilledCircle, AnimLine, AnimActor, get_dir_vector, AnimFilledPolygon
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 1200
TITLE = "PGZAnimation - Game demo"

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
background_image = "starfield"

# create variables (constants) to simplify instructions
shot234_vector_1 = get_dir_vector(-60)
shot2_target = [0,0]
shot3_target = [0,0]
shot4_target = [0,0]

# temporary variables to simplify making polygon
hitx = 800
hity = 310
# polygon for explosion
hit_points = [
    (hitx, hity-20),     #N
    (hitx+10, hity),
    (hitx+30, hity-5),   #NE
    (hitx+10, hity+15),
    (hitx+30, hity+30),  #SE
    (hitx-5, hity+20),
    (hitx-5, hity+35),     #S
    (hitx-15, hity+10),
    (hitx-35, hity+25),  #SW
    (hitx-20, hity+5),
    (hitx-30, hity-10),  #S
    (hitx-10, hity-5)
    ]


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
    'ship4': AnimActor ("spacecraft2", (380,90),  angle=180),

    'hit_outer': AnimFilledPolygon (hit_points, color=(255,0,0), hide=True),
    'hit_inner': AnimFilledPolygon (hit_points, color=(255,255,0), hide=True)

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
    'pursue1': 450,
    'hit-friendly': 485,
    'fire2-target': 520,
    'hit-complete': 540,
    'hit-friendly-recover1': 545,
    'hit-friendly-recover2': 560,
    'hit-enemy1': 580,
    'enemy-explode1': 590,
    'enemy-recover1': 600,
    'hit-enemy2':620,
    'enemy2-gone': 640
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

def update():
    controls()
    animate()


# Place your animations here
def animate():
    global shot2_target, shot3_target, shot4_target, shot234_vector_1
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
        shapes['shot3'].pos = shapes['ship3'].pos
        shapes['shot4'].pos = shapes['ship4'].pos
        shot2_target = [
            shapes['shot2'].pos[0]+shot234_vector_1[0]*600,
            shapes['shot2'].pos[1]+shot234_vector_1[1]*600
        ]
        shot3_target = [
            shapes['shot3'].pos[0]+shot234_vector_1[0]*600,
            shapes['shot3'].pos[1]+shot234_vector_1[1]*600
        ]
        shot4_target = [
            shapes['shot4'].pos[0]+shot234_vector_1[0]*600,
            shapes['shot4'].pos[1]+shot234_vector_1[1]*600
        ]
        shapes['shot2'].hide = False
        shapes['shot3'].hide = False
        shapes['shot4'].hide = False
        shapes['shot2'].angle = 210
        shapes['shot3'].angle = 210
        shapes['shot4'].angle = 210

    # Send shot via motion
    shapes['shot2'].move_tween(kf['aim1'], kf['fire1-target'], frame, shot2_target)
    shapes['shot3'].move_tween(kf['aim1'], kf['fire1-target'], frame, shot3_target)
    shapes['shot4'].move_tween(kf['aim1'], kf['fire1-target'], frame, shot4_target)


    # enemies pursue
    shapes['ship2'].move_tween(kf['aim1'], kf['pursue1'], frame, (550, 380))
    shapes['ship2'].rotate_rel_tween(kf['aim1'], kf['pursue1'], frame, 60)
    shapes['ship3'].move_tween(kf['aim1'], kf['pursue1'], frame, (450, 450))
    shapes['ship3'].rotate_rel_tween(kf['aim1'], kf['pursue1'], frame, 60)
    shapes['ship4'].move_tween(kf['aim1'], kf['pursue1'], frame, (450, 310))
    shapes['ship4'].rotate_rel_tween(kf['aim1'], kf['pursue1'], frame, 60)
    # friendly moves slightly right to avoid
    shapes['ship1'].move_tween(kf['aim1'], kf['pursue1'], frame, (790, 340))
    shapes['ship1'].rotate_rel_tween(kf['aim1'], kf['pursue1'], frame, 20, direction="CW")


    #ships 2 to 4 fire
    if (frame == kf['pursue1']):
        shot234_vector_1 = get_dir_vector(0)
        shapes['shot2'].pos = shapes['ship2'].pos
        shapes['shot3'].pos = shapes['ship3'].pos
        shapes['shot4'].pos = shapes['ship4'].pos
        shot2_target = [
            shapes['shot2'].pos[0]+shot234_vector_1[0]*800,
            shapes['shot2'].pos[1]+shot234_vector_1[1]*800
        ]
        shot3_target = [
            shapes['shot3'].pos[0]+shot234_vector_1[0]*800,
            shapes['shot3'].pos[1]+shot234_vector_1[1]*800
        ]
        shot4_target = [
            shapes['shot4'].pos[0]+shot234_vector_1[0]*350,
            shapes['shot4'].pos[1]+shot234_vector_1[1]*350
        ]
        shapes['shot2'].angle = 210
        shapes['shot3'].angle = 210
        shapes['shot4'].angle = 210

    # Send shot via motion
    shapes['shot2'].move_tween(kf['pursue1'], kf['fire2-target'], frame, shot2_target)
    shapes['shot3'].move_tween(kf['pursue1'], kf['fire2-target'], frame, shot3_target)
    shapes['shot4'].move_tween(kf['pursue1'], kf['hit-friendly'], frame, shot4_target)

    # friendly tries to avoid
    shapes['ship1'].move_tween(kf['pursue1'], kf['hit-friendly'], frame, (800, 310))

    # ship is hit and knocked off course
    if (frame == kf['hit-friendly']):
        shapes['hit_outer'].hide = False
    shapes['ship1'].move_tween(kf['hit-friendly'], kf['hit-friendly-recover1'], frame, (820, 310))
    if (frame == kf['hit-complete']):
        shapes['hit_outer'].hide = True
    # recovers, changes direction and moves up the screen
    shapes['ship1'].rotate_rel_tween(kf['hit-friendly-recover1'], kf['hit-friendly-recover2'], frame, 130)
    shapes['ship1'].move_rel_tween(kf['hit-friendly-recover1'], kf['hit-friendly-recover2'], frame, (0, -50))

    # ships continue to move
    shapes['ship2'].move_rel_tween(kf['hit-friendly'], kf['hit-enemy1'], frame, (20,0))
    shapes['ship3'].move_rel_tween(kf['hit-friendly'], kf['hit-enemy1'], frame, (20,0))
    shapes['ship4'].move_rel_tween(kf['hit-friendly'], kf['hit-enemy1'], frame, (20,0))

    # All ships fire again
    if (frame == kf['hit-friendly-recover2']):
        shapes['shot1'].pos = shapes['ship1'].pos
        shapes['shot2'].pos = shapes['ship2'].pos
        shapes['shot3'].pos = shapes['ship3'].pos
        shapes['shot4'].pos = shapes['ship4'].pos
        shapes['shot1'].hide = False

    shapes['shot1'].move_rel_tween(kf['hit-friendly-recover2'], kf['hit-enemy1'], frame, (-300,45))
    shapes['shot2'].move_rel_tween(kf['hit-friendly-recover2'], kf['enemy-explode1'], frame, (600,0))
    shapes['shot3'].move_rel_tween(kf['hit-friendly-recover2'], kf['enemy-explode1'], frame, (600,0))
    shapes['shot4'].move_rel_tween(kf['hit-friendly-recover2'], kf['enemy-explode1'], frame, (600,0))

    # ship is hit and knocked off course
    if (frame == kf['enemy-explode1']):
        shapes['shot1'].hide = True
        shapes['shot2'].hide = True
        shapes['shot3'].hide = True
        shapes['shot4'].hide = True
        shapes['hit_outer'].pos = shapes['shot1'].pos
        shapes['hit_outer'].hide = False

    shapes['ship4'].move_rel_tween(kf['enemy-explode1'], kf['enemy-recover1'], frame, (-20, 5))

    if (frame == kf['enemy-recover1']):
        shapes['hit_outer'].hide = True

    # friendly attacks again quickly
    if (frame == kf['enemy-recover1']):
        shapes['shot1'].pos = shapes['ship1'].pos
        shapes['shot1'].hide = False

    shapes['shot1'].move_tween(kf['enemy-recover1'], kf['hit-enemy2'], frame, shapes['ship4'].pos)

    # ship is hit and knocked off course
    if (frame == kf['hit-enemy2']):
        shapes['shot1'].hide = True
        shapes['hit_outer'].pos = shapes['shot1'].pos
        shapes['hit_outer'].hide = False
        shapes['hit_inner'].pos = shapes['shot1'].pos
        shapes['hit_inner'].hide = False

    shapes['hit_outer'].scale_tween(kf['hit-enemy2'], kf['enemy2-gone'], frame, (2,2))

    if (frame == kf['enemy2-gone']):
        shapes['hit_inner'].hide=True
        shapes['hit_outer'].hide=True
        shapes['ship4'].hide=True

    shapes['ship2'].move_rel_tween(kf['enemy-recover1'], kf['enemy2-gone'], frame, (50,0))
    shapes['ship3'].move_rel_tween(kf['enemy-recover1'], kf['enemy2-gone'], frame, (50,0))




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