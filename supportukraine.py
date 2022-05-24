from pgzanimation import AnimFilledPolygon, AnimText, AnimFilledRect
import pygame, sys

WIDTH = 64
HEIGHT = 32
FRAMES = 220
FRAME_DELAY = 5
TITLE = "Inverting buffer"

# Save options
# Continue to save frames when paused?
SAVE_PAUSED = True
# enable to show frame number on screen (not included in save)
SHOW_FRAME = False
# enable to show mouse position (useful for designing animations)
SHOW_MOUSE = False
# Exit after last frame?
QUIT_END = False

# Is save enabled (otherwise just display animation)
save = True
save_files = "/home/stewart/test-animations/animation-{0:05d}.png"
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame = 0
save_frame = 0
frame_delay = 0
pause = False

background_color = (0, 0, 0)
background_image = ""
flag_top_color = "#006bb7"
flag_bot_color = "#ffcd36"

# Add own variables for convenience
flag_top_rect = Rect(0,0,WIDTH,HEIGHT/2)
flag_bot_rect = Rect(0,HEIGHT/2, WIDTH, HEIGHT)



slides = [
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
    }
shapes = {
    'flag01' : AnimFilledRect (flag_top_rect, flag_top_color ),
    'flag02' : AnimFilledRect (flag_bot_rect, flag_bot_color),
    'standtext' : AnimText ("I stand with  Ukraine", (100, 10), flag_bot_color, fontsize=20),
    }

# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = []

# key frames (can just use number if preferred, but allows labels)
kf = {
    'start': 0,
    'stand': 100,
    'ukraine': 170,
    'ukraine-end': 200
}


# Place your animations here
def animate():
    if (frame == kf['start']):
        shapes['flag01'].hide = False
        shapes['flag02'].hide = False
        shapes['standtext'].hide = True
    if (frame == kf['stand']):
        shapes['flag01'].hide = True
        shapes['flag02'].hide = True
        shapes['standtext'].hide = False
    if (frame == kf['ukraine']):
        pass

    shapes['standtext'].move_tween (kf['stand'], kf['ukraine'], frame, (-72, 10))
    shapes['standtext'].move_tween (kf['ukraine-end'], FRAMES, frame, (-150, 10))

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
    global frame_delay
    # delay updates based on frame delay
    if (FRAME_DELAY > 0):
        if (frame_delay < FRAME_DELAY):
            frame_delay += 1
            return
        else:
            frame_delay = 0
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