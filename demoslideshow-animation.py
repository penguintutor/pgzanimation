from pgzanimation import SlideBullets, AnimActor
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 1000
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
save_files = "/home/stewart/test-animations/animation-{0:05d}.png"
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame=0
save_frame=0
pause = False


bullets0 = [
    "Processing circuit animations",
    "Animated Web Applets",
    "No longer work...",
    ]
bullets1 = [
    "Pygame Zero = Pygame but easier",
    "Designed for creating games",
    "Easy to learn (simplified boiler plate)",
    "Create an object oriented set of animation tools",
    "Even easier to learn - perhaps?"
    ]
bullets2 = [
    "Designed for programmers",
    "Don't need to be a programmer",
    "Makes repetition easy",
    "(Almost) everything is an object"
    ]
shapes = {
    'circuit1': AnimActor ("circuit1", (900,200), hide=True),
    'circuit2': AnimActor ("circuit2", (900,500), hide=True)
}

slides = [
    SlideBullets ((WIDTH,HEIGHT), "PGZAnimation - History", bullets0, bulletstartpos=(100,220), bulletpause=True, bullettransition="appear"),
    SlideBullets ((WIDTH,HEIGHT), "PGZAnimation - Why Pygame Zero?", bullets1, bulletstartpos=(100,220), bulletpause=True, bullettransition="slidefromleft"),
    SlideBullets ((WIDTH,HEIGHT), "PGZAnimation - What it provides?", bullets2, bulletstartpos=(100,220), bulletpause=True, bullettransition="slidefrombottom")
    ]
background_color = (255,255,255)
background_image = "background1"

# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = [349]

slides[0].show_slide(0, 350)
slides[0].animate_slide(50,300)
# image show is inserted here
slides[1].show_slide(351, 700)
slides[1].animate_slide(400,700)
slides[2].show_slide(700, 1000)
slides[2].animate_slide(750,1000)

def draw():
    screen.clear()
    screen.fill(background_color)
    if (background_image != ""):
        screen.blit(background_image, (0,0))

    for this_shape in shapes.values():
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

    # Add custom animations here
    # Add image
    shapes['circuit1'].show(340, frame)
    shapes['circuit2'].show(345, frame)
    shapes['circuit1'].end_show(350, frame)
    shapes['circuit2'].end_show(350, frame)

    # special custom operation (calls title within the slide)
    # example of additional flexibility (although more complex)
    title_slide_0 = slides[0].title.move_rel_tween(300, 340, frame, (-250,0))

    # slides need to check for pause
    for this_slide in slides:
        if (this_slide.update(frame) == True): pause=True
    # check for cutom pause
    for this_pause in pause_frames:
        if (frame == this_pause): pause=True

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