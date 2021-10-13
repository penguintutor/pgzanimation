from pgzanimation import AnimRect, AnimFilledRect, AnimText, AnimFilledCircle, AnimLine, AnimLineEnd, AnimTriangle
from pgzanimation import Slide
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 1400
TITLE = "Pixel Server"

save_files = "/home/stewart/demoserver/pixelserver-{0:05d}.png"

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
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame=0
save_frame=0
pause = False


# create variables (constants) to simplify instructions
# positions


kf = {
    'pixelserver': 80,
    'mt_line1': 505,
    'mt' : 520,
    'ft_line1': 765,
    'ft' : 780,
    'mem' : 900,
    'memps': 940,
    'memmt' : 1100,
    'memft' : 1160
    }

slides = [
    Slide ((WIDTH,HEIGHT), "Pixel Server")
    ]

ps_box_rect = Rect(300,170,400,100)
mt_box_rect = Rect(250,350,200,100)
ft_box_rect = Rect(550,350,200,100)
mem_box_rect = Rect(900,180,260,500)
mem_box1_rect = Rect(mem_box_rect.left + 5, mem_box_rect.top + 270, mem_box_rect.width-10, 100) #globals
mem_box2_rect = Rect(mem_box_rect.left + 5, mem_box_rect.top + 372, mem_box_rect.width-10, 100) #pixelserver
mem_box3_rect = Rect(mem_box_rect.left + 5, mem_box_rect.top + 120, mem_box_rect.width-10, 100) #mt
mem_box4_rect = Rect(mem_box_rect.left + 5, mem_box_rect.top + 18, mem_box_rect.width-10, 100) #ft


# create groups
shape_groups = {

    "pixelserver" : {
        "box": AnimRect (ps_box_rect, (0,0,0) , width=2),
        "box_label": AnimText ("pixelserver.py", ps_box_rect.center, anchor=("center","center")),
        },
    "mt": {
        "box": AnimRect (mt_box_rect, (0,0,0) , width=2),
        "box_label": AnimText ("mt", mt_box_rect.center, anchor=("center","center")),
        "key_text": AnimText ("mt = mainThread - used for pixelstrip", (100, 550)),
        "arrow": AnimLineEnd ((350,345), (0,0,255), angle=180)
        },
    "ft": {
        "box": AnimRect (ft_box_rect, (0,0,0) , width=2),
        "box_label": AnimText ("ft", ft_box_rect.center, anchor=("center","center")),
        "key_text": AnimText ("ft = flaskThread - used for Flask web server", (100, 600)),
        "arrow": AnimLineEnd ((650,345), (0,0,255), angle=180)
        },
    "memory": {
        "mem_label": AnimText ("Memory", (mem_box_rect.centerx, 160), anchor=("center","center")),
        "mem_box": AnimFilledRect (mem_box_rect, (153, 204, 255)),
        "mem_box_border": AnimRect (mem_box_rect, (0, 0, 0), width=2),
        },
    "memps": {
        "mem_box_1": AnimFilledRect (mem_box1_rect, (255,255,255)),
        "mem_box_2": AnimFilledRect (mem_box2_rect, (255,255,255)),
        "box1_label": AnimText ("Variables\nupd_time\nseq_set", mem_box1_rect.center, anchor=("center","center")),
        "box2_label": AnimText ("pixelserver.ps", mem_box2_rect.center, anchor=("center","center"))
        },
    "memmt": {
        "mem_box_3": AnimFilledRect (mem_box3_rect, (255,255,255)),
        "box3_label": AnimText ("mt\nmemory", mem_box3_rect.center, anchor=("center","center"))
        },
    "memft": {
        "mem_box_4": AnimFilledRect (mem_box4_rect, (255,255,255)),
        "box4_label": AnimText ("ft\nmemory", mem_box4_rect.center, anchor=("center","center"))
        }

    }

shapes = {
    "st_thread1": AnimLine ((350,275), (350,345), (0,0,255), width=2),
    "st_thread2": AnimLine ((650,275), (650,345), (0,0,255), width=2)
}

# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = []


slides[0].show_slide(0, FRAMES)
slides[0].animate_slide(5,FRAMES)

# Add any initial setup in here
def setup():
    # Hide all shapes initially - add as required
    for this_group in shape_groups.values():
        for this_entry in this_group.values():
            this_entry.hide = True
    for this_shape in shapes.values():
        this_shape.hide = True



def draw():
    screen.clear()
    screen.fill((255,255,255))

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
    if SHOW_MOUSE:
        screen.draw.text("Mouse "+str(pygame.mouse.get_pos()), (20, 60), color=(50, 50, 250), fontsize=60)


def update():
    global frame, pause
    if (frame == 0):
        setup()
    controls()

    # Add animations here
    if (frame == kf['pixelserver']):
        for this_shape in shape_groups['pixelserver'].values():
            this_shape.hide=False
    elif (frame == kf['mt']):
        for this_shape in shape_groups['mt'].values():
            this_shape.hide=False
    elif (frame == kf['ft']):
        for this_shape in shape_groups['ft'].values():
            this_shape.hide=False
    elif (frame == kf['mem']):
        for this_shape in shape_groups['memory'].values():
            this_shape.hide=False
    elif (frame == kf['memps']):
        for this_shape in shape_groups['memps'].values():
            this_shape.hide=False
    elif (frame == kf['memmt']):
        for this_shape in shape_groups['memmt'].values():
            this_shape.hide=False
    elif (frame == kf['memft']):
        for this_shape in shape_groups['memft'].values():
            this_shape.hide=False

    shapes["st_thread1"].reveal_tween(kf["mt_line1"], kf["mt_line1"]+15, frame)
    shapes["st_thread2"].reveal_tween(kf["ft_line1"], kf["ft_line1"]+15, frame)

      # slides need to check for pause
    for this_slide in slides:
        if (this_slide.update(frame) == True): pause=True




def controls():
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

    frame += 1
    save_frame += 1
    #print ("Frame is {}".format(frame))

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