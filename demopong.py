from pgzanimation import AnimFilledRect, AnimText, AnimFilledCircle, AnimLine
import pygame, sys

WIDTH = 800
HEIGHT = 600
FRAMES = 1300
TITLE = "Pong Demo"

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


# create variables (constants) to simplify instructions
# positions
leftbat_x = 50
rightbat_x = WIDTH-50
# timings
time_start = 10
time_bat = [50, 150, 250, 350, 450, 500, 600, 700, 800, 900, 1000, 1100]

shapes = {
    "leftbat": AnimFilledRect (Rect(leftbat_x, HEIGHT/2, 10, 40), (255,255,255), anchor=("right","center")),
    "rightbat": AnimFilledRect (Rect(rightbat_x, HEIGHT/2, 10, 40), (255,255,255), anchor=("left","center")),
    "ball": AnimFilledCircle ((400, 300), 5, (255,255,255)),
    "leftscore": AnimText ("00", (100,50), (255,255,255), fontname="computerspeak"),
    "rightscore": AnimText ("00", (WIDTH-150,50), (255,255,255), fontname="computerspeak"),
    "net": AnimLine ((WIDTH/2,50), (WIDTH/2,HEIGHT-50), (255,255,255), style="dashed", spacing=[5,10])
    }


# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = []


def draw():
    screen.clear()
    screen.fill((0,0,0))

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

    # Add animations here
    shapes['ball'].move_tween(time_start, time_bat[0], frame, (leftbat_x, 150))
    shapes['leftbat'].move_tween(time_start+10, time_bat[0], frame, (leftbat_x, 150))
    shapes['ball'].move_tween(time_bat[0], time_bat[1], frame, (rightbat_x, 250))
    shapes['rightbat'].move_tween(time_bat[0]+10, time_bat[1]-20, frame, (rightbat_x, 240))
    shapes['ball'].move_tween(time_bat[1], time_bat[2], frame, (leftbat_x, 460))
    shapes['leftbat'].move_tween(time_bat[1]+10, time_bat[2], frame, (leftbat_x, 462))
    shapes['ball'].move_tween(time_bat[2], time_bat[3], frame, (rightbat_x, 465))
    shapes['rightbat'].move_tween(time_bat[2]+10, time_bat[3]-5, frame, (rightbat_x, 460))
    shapes['ball'].move_tween(time_bat[3], time_bat[4], frame, (0, 140))
    shapes['leftbat'].move_tween(time_bat[3]+30, time_bat[4], frame, (leftbat_x, 160))
    if (frame == time_bat[4]):
        shapes['rightscore'].text = "01"
        shapes['ball'].pos = shapes['leftbat'].pos 
    shapes['ball'].move_tween(time_bat[4], time_bat[5], frame, (leftbat_x, 150))
    shapes['leftbat'].move_tween(time_bat[4]+10, time_bat[5], frame, (leftbat_x, 150))
    shapes['ball'].move_tween(time_bat[5], time_bat[6], frame, (rightbat_x, 250))
    shapes['rightbat'].move_tween(time_bat[5]+10, time_bat[6]-20, frame, (rightbat_x, 240))
    shapes['ball'].move_tween(time_bat[6], time_bat[7], frame, (leftbat_x, 460))
    shapes['leftbat'].move_tween(time_bat[6]+10, time_bat[7], frame, (leftbat_x, 462))
    shapes['ball'].move_tween(time_bat[7], time_bat[8], frame, (WIDTH, 465))
    shapes['rightbat'].move_tween(time_bat[7]+10, time_bat[8]-5, frame, (rightbat_x, 420))
    if (frame == time_bat[8]):
        shapes['leftscore'].text = "01"
        shapes['ball'].pos = shapes['rightbat'].pos 
    #shapes['rightbat'].move_tween(time_bat[8]+10, time_bat[9]-20, frame, (rightbat_x, 240))
    shapes['ball'].move_tween(time_bat[9], time_bat[10], frame, (leftbat_x, 460))
    shapes['leftbat'].move_tween(time_bat[9]+10, time_bat[10], frame, (leftbat_x, 462))
    shapes['ball'].move_tween(time_bat[10], time_bat[11], frame, (WIDTH, 465))
    shapes['rightbat'].move_tween(time_bat[10]+10, time_bat[11]-5, frame, (rightbat_x, 490))
    if (frame == time_bat[11]):
        shapes['leftscore'].text = "02"

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