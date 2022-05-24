from pgzanimation import AnimFilledRect, AnimText, AnimFilledCircle, AnimLine, AnimLed
from random import randrange
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 3600
TITLE = "LED Light Demo"

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
save_files = "/home/stewart/cheerlight-demo/animation-{0:05d}.png"
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame=0
save_frame=0
pause = False

background_color = (0,255,0)
background_image = "world-background.png"

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
    0: AnimLed ((569, 183), 25, "#a7a7a7", led_type="rgb", state="off"),
    1: AnimLed ((154, 145), 25, "#a7a7a7", led_type="rgb", state="off"),
    2: AnimLed ((696, 575), 25, "#c7c7c7", led_type="rgb", state="off"),
    3: AnimLed ((725, 179), 25, "#a7a7a7", led_type="rgb", state="off"),
    4: AnimLed ((379, 508), 25, "#a7a7a7", led_type="rgb", state="off"),
    5: AnimLed ((655, 102), 25, "#a7a7a7", led_type="rgb", state="off"),
    6: AnimLed ((1120, 550), 25, "#a7a7a7", led_type="rgb", state="off"),
    7: AnimLed ((585, 311), 25, "#a7a7a7", led_type="rgb", state="off"),
    8: AnimLed ((121, 246), 25, "#a7a7a7", led_type="rgb", state="off"),
    9: AnimLed ((615, 209), 25, "#a7a7a7", led_type="rgb", state="off"),
    10: AnimLed ((939, 351), 25, "#a7a7a7", led_type="rgb", state="off"),
    11: AnimLed ((1124, 290), 25, "#a7a7a7", led_type="rgb", state="off"),
    12: AnimLed ((223, 392), 25, "#a7a7a7", led_type="rgb", state="off"),
    13: AnimLed ((807, 299), 25, "#a7a7a7", led_type="rgb", state="off"),
    14: AnimLed ((455, 73), 25, "#a7a7a7", led_type="rgb", state="off"),
    15: AnimLed ((1244, 561), 25, "#a7a7a7", led_type="rgb", state="off"),
    16: AnimLed ((725, 303), 25, "#a7a7a7", led_type="rgb", state="off"),
    17: AnimLed ((275, 499), 25, "#a7a7a7", led_type="rgb", state="off"),
    'tweet1': AnimText ("Lighting up the world", (800, 70), fontsize=40, hide=True),
    'tweet2': AnimText ("", (800, 120), fontsize=40, hide=True),
}


num_leds = 18

# Add any pauses to this
pause_frames = []

# key frames (can just use number if preferred, but this allows labels)
kf = {
    'start': 0,
    'intro': 200,
    'introoff': 800,
    'text1': 1000,
    'red': 1050,
    'text1off': 1200,
    'text2': 1500,
    'blue': 1550,
    'text2off': 1700,
    'text3': 2000,
    'green': 2050,
    'text3off': 2200,
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
    if (frame < kf['text1']):
        for i in range (0, num_leds):
            if ((frame - 200) == i * 40):
                shapes[i].led_color=(randrange(0,255),randrange(0,255),randrange(0,255))
                shapes[i].on()
                
    if (frame == kf['intro']):
        shapes['tweet1'].hide = False
        shapes['tweet2'].hide = False
                
    if (frame == kf['text1']):
        shapes['tweet1'].text = "@CheerLights light the world with"
        shapes['tweet2'].text = "red LEDs"
        shapes['tweet1'].hide = False
        shapes['tweet2'].hide = False
        
    if (frame == kf['red']):
        for i in range (0, num_leds):
            shapes[i].led_color=("#ff0000")
        
    if (frame == kf['introoff'] or frame == kf['text1off']
            or frame == kf['text2off'] or frame == kf['text3off']):
        shapes['tweet1'].hide = True
        shapes['tweet2'].hide = True
        
    if (frame == kf['text2']):
        shapes['tweet1'].text = "@CheerLights I'm feeling"
        shapes['tweet2'].text = "blue"
        shapes['tweet1'].hide = False
        shapes['tweet2'].hide = False
        
    if (frame == kf['blue']):
        for i in range (0, num_leds):
            shapes[i].led_color=("#0000ff")
        

    if (frame == kf['text3']):
        shapes['tweet1'].text = "@CheerLights Unite the world with"
        shapes['tweet2'].text = "green lights"
        shapes['tweet1'].hide = False
        shapes['tweet2'].hide = False


    if (frame == kf['green']):
        for i in range (0, num_leds):
            shapes[i].led_color=("#00ff00")
    



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