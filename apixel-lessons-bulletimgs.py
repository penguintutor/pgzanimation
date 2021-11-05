from pgzanimation import SlideBulletsImages
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 2000


# Save options
# Continue to save frames when paused?
SAVE_PAUSED = True
# enable to show frame number on screen (not included in save)
SHOW_FRAME = True
SHOW_MOUSE = True
# Exit after last frame?
QUIT_END = False

# Is save enabled (otherwise just display animation)
save = True
save_files = "/home/stewart/apixel-animations/animation-01-{0:05d}.png"
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame=0
save_frame=0
# If this is set to True then it will pause before starting
# Normally leave this at False
pause = False

background_color = (255,255,255)
background_image = ""

bullets1 = [
    "2-Stage MOSFET voltage shifter is better",
    "Bigger is better (sometimes)",
    "Arduino power supply",
    "Arduino I2C - no pull-up needed",
    "KiCAD 2N7000 footprint",
    "Using headers"
    ]
    
images1 = [
    "level-shifter.png",
    "terminals.png",
    "arduino-power.png",
    "pullups.png",
    "kicadmosfet.png",
    "headers.png"
    ]

shapes = []

slides = [
    SlideBulletsImages ((WIDTH,HEIGHT), "Lessons Learned",
        bullets1, images1, bulletpause=False, bullettransition="slidefromleft",
        bulletstartpos=(100 , 170), bulletspacing=55
        )
    ]

shapes = []


# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = []

slides[0].title.fontsize = 60
slides[0].show_slide(0, FRAMES)
slides[0].animate_slide(50,1500)


def draw():
    screen.clear()
    screen.fill(background_color)
    if (background_image != ""):
        screen.blit(background_image, (0,0))

    for this_shape in shapes:
        this_shape.draw()
    for this_slide in slides:
        this_slide.draw()

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