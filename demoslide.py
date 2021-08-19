from pgzanimation import SlideBullets
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 700
TITLE = "PgzAnimation"

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


bullets1 = [
    "Bullet 1",
    "Bullet 2",
    "Bullet 3"
    ]
bullets1_timings = [
    (119, 186, 254),
    (255, 322, 390),
    (391, 458, 526)
    ]
shapes = []

slides = [
    SlideBullets ((WIDTH,HEIGHT), "Slide Title", bullets1, bulletpause=False, bullettransition=["slidefrombottom"])
    ]


# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = []

slides[0].show_slide(0, 600)
#slides[0].animate_slide(50,600)
slides[0].animate_slide(50,600,bullets1_timings)

def draw():
    screen.clear()
    screen.fill((255,255,255))

    for this_shape in shapes:
        this_shape.draw()
    for this_slide in slides:
        this_slide.draw()


def update():
    global frame, save_frame, pause
    # Stop updating once end reached
    if (frame >= FRAMES):
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