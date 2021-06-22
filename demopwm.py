from pgzanimation import AnimFilledRect, AnimText, AnimFilledCircle, AnimLine
from pgzanimation import Slide
import pygame, sys

WIDTH = 1280
HEIGHT = 720
FRAMES = 4000
TITLE = "PWM"

# Save options
# Continue to save frames when paused?
SAVE_PAUSED = True
# enable to show frame number on screen (not included in save)
SHOW_FRAME = True
# Exit after last frame?
QUIT_END = False

# Is save enabled (otherwise just display animation)
save = False
# frame is the animation frame number
# when pause then save_frame continues to count to extend video length
frame=0
save_frame=0
pause = False


# create variables (constants) to simplify instructions
# positions
start_trace = 350
end_trace = 950
start_pulse_1 = 550
start_pulse_2 = 750
pulse_width_1 = 25
pulse_width_2 = 25
y_pos_1 = 300
y_pos_2 = 550
height_pulse = 60
static_width = 2
active_width = 5
static_color = (128,128,128)
active_color = (0,0,0)

# timings relative to keyframe that these start from
# each are tuple (start, end) for each object
linedraw_timings = [
    (0,50),
    (50,51),
    (51,60),
    (60,61),
    (61,110),
    (110,111),
    (111,120),
    (120,121),
    (121,170)
    ]


keyframes = [
    0,          # start animation
    20,        # first pulse drawing
    190,         # end first pulse - replace with static
    400,         # change pwm of 2nd line
    570         # change pwm of 2nd line (static)
    ]

slides = [
    Slide ((WIDTH,HEIGHT), "PWM Duty Cycle")
    ]

# create groups - each one being one full trace
shape_groups = {

    "static_line_1" : {
        "horizontal1": AnimLine ((start_trace, y_pos_1), (start_pulse_1,y_pos_1), static_color, width=static_width),
        "startpulse1": AnimLine ((start_pulse_1, y_pos_1), (start_pulse_1,y_pos_1-height_pulse), static_color, width=static_width),
        "toppulse1": AnimLine ((start_pulse_1, y_pos_1-height_pulse), (start_pulse_1+pulse_width_1,y_pos_1-height_pulse), static_color, width=static_width),
        "endpulse1": AnimLine ((start_pulse_1+pulse_width_1, y_pos_1-height_pulse), (start_pulse_1+pulse_width_1,y_pos_1), static_color, width=static_width),
        "horizontal2": AnimLine ((start_pulse_1+pulse_width_1, y_pos_1), (start_pulse_2,y_pos_1), static_color, width=static_width),
        "startpulse2": AnimLine ((start_pulse_2, y_pos_1), (start_pulse_2,y_pos_1-height_pulse), static_color, width=static_width),
        "toppulse2": AnimLine ((start_pulse_2, y_pos_1-height_pulse), (start_pulse_2+pulse_width_1,y_pos_1-height_pulse), static_color, width=static_width),
        "endpulse2": AnimLine ((start_pulse_2+pulse_width_1, y_pos_1-height_pulse), (start_pulse_2+pulse_width_1,y_pos_1), static_color, width=static_width),
        "horizontal3": AnimLine ((start_pulse_2+pulse_width_1, y_pos_1), (end_trace,y_pos_1), static_color, width=static_width)
        },

    "active_line_1" : {
        "horizontal1": AnimLine ((start_trace, y_pos_1), (start_pulse_1,y_pos_1), active_color, width=active_width),
        "startpulse1": AnimLine ((start_pulse_1, y_pos_1), (start_pulse_1,y_pos_1-height_pulse), active_color, width=active_width),
        "toppulse1": AnimLine ((start_pulse_1, y_pos_1-height_pulse), (start_pulse_1+pulse_width_1,y_pos_1-height_pulse), active_color, width=active_width),
        "endpulse1": AnimLine ((start_pulse_1+pulse_width_1, y_pos_1-height_pulse), (start_pulse_1+pulse_width_1,y_pos_1), active_color, width=active_width),
        "horizontal2": AnimLine ((start_pulse_1+pulse_width_1, y_pos_1), (start_pulse_2,y_pos_1), active_color, width=active_width),
        "startpulse2": AnimLine ((start_pulse_2, y_pos_1), (start_pulse_2,y_pos_1-height_pulse), active_color, width=active_width),
        "toppulse2": AnimLine ((start_pulse_2, y_pos_1-height_pulse), (start_pulse_2+pulse_width_1,y_pos_1-height_pulse), active_color, width=active_width),
        "endpulse2": AnimLine ((start_pulse_2+pulse_width_1, y_pos_1-height_pulse), (start_pulse_2+pulse_width_1,y_pos_1), active_color, width=active_width),
        "horizontal3": AnimLine ((start_pulse_2+pulse_width_1, y_pos_1), (end_trace,y_pos_1), active_color, width=active_width)
        },

    "static_line_2" : {
        "horizontal1": AnimLine ((start_trace, y_pos_2), (start_pulse_1,y_pos_2), static_color, width=static_width),
        "startpulse1": AnimLine ((start_pulse_1, y_pos_2), (start_pulse_1,y_pos_2-height_pulse), static_color, width=static_width),
        "toppulse1": AnimLine ((start_pulse_1, y_pos_2-height_pulse), (start_pulse_1+pulse_width_2,y_pos_2-height_pulse), static_color, width=static_width),
        "endpulse1": AnimLine ((start_pulse_1+pulse_width_2, y_pos_2-height_pulse), (start_pulse_1+pulse_width_2,y_pos_2), static_color, width=static_width),
        "horizontal2": AnimLine ((start_pulse_1+pulse_width_2, y_pos_2), (start_pulse_2,y_pos_2), static_color, width=static_width),
        "startpulse2": AnimLine ((start_pulse_2, y_pos_2), (start_pulse_2,y_pos_2-height_pulse), static_color, width=static_width),
        "toppulse2": AnimLine ((start_pulse_2, y_pos_2-height_pulse), (start_pulse_2+pulse_width_2,y_pos_2-height_pulse), static_color, width=static_width),
        "endpulse2": AnimLine ((start_pulse_2+pulse_width_2, y_pos_2-height_pulse), (start_pulse_2+pulse_width_2,y_pos_2), static_color, width=static_width),
        "horizontal3": AnimLine ((start_pulse_2+pulse_width_2, y_pos_2), (end_trace,y_pos_2), static_color, width=static_width)
        },

    "active_line_2" : {
        "horizontal1": AnimLine ((start_trace, y_pos_2), (start_pulse_1,y_pos_2), active_color, width=active_width),
        "startpulse1": AnimLine ((start_pulse_1, y_pos_2), (start_pulse_1,y_pos_2-height_pulse), active_color, width=active_width),
        "toppulse1": AnimLine ((start_pulse_1, y_pos_2-height_pulse), (start_pulse_1+pulse_width_2,y_pos_2-height_pulse), active_color, width=active_width),
        "endpulse1": AnimLine ((start_pulse_1+pulse_width_2, y_pos_2-height_pulse), (start_pulse_1+pulse_width_2,y_pos_2), active_color, width=active_width),
        "horizontal2": AnimLine ((start_pulse_1+pulse_width_2, y_pos_2), (start_pulse_2,y_pos_2), active_color, width=active_width),
        "startpulse2": AnimLine ((start_pulse_2, y_pos_2), (start_pulse_2,y_pos_2-height_pulse), active_color, width=active_width),
        "toppulse2": AnimLine ((start_pulse_2, y_pos_2-height_pulse), (start_pulse_2+pulse_width_2,y_pos_2-height_pulse), active_color, width=active_width),
        "endpulse2": AnimLine ((start_pulse_2+pulse_width_2, y_pos_2-height_pulse), (start_pulse_2+pulse_width_2,y_pos_2), active_color, width=active_width),
        "horizontal3": AnimLine ((start_pulse_2+pulse_width_2, y_pos_2), (end_trace,y_pos_2), active_color, width=active_width)
        }

    }


def change_pulse_width (line, pulse_width):

    # get y from first position
    start_pos = line["horizontal1"].start
    y_pos = start_pos[1]
    # first change in top line end
    line["toppulse1"].end = (start_pulse_1+pulse_width, y_pos-height_pulse)
    line["endpulse1"].start = (start_pulse_1+pulse_width, y_pos-height_pulse)
    line["endpulse1"].end = (start_pulse_1+pulse_width, y_pos)
    line["horizontal2"].start = (start_pulse_1+pulse_width, y_pos)
    # 2nd pulse
    line["toppulse2"].end = (start_pulse_2+pulse_width, y_pos-height_pulse)
    line["endpulse2"].start = (start_pulse_2+pulse_width, y_pos-height_pulse)
    line["endpulse2"].end = (start_pulse_2+pulse_width, y_pos)
    line["horizontal3"].start = (start_pulse_2+pulse_width, y_pos)


# Add any initial setup in here
def setup():
    for this_entry in shape_groups["static_line_1"].values():
        this_entry.hide = True
    for this_entry in shape_groups["static_line_2"].values():
        this_entry.hide = True
    for this_entry in shape_groups["active_line_1"].values():
        this_entry.hide = True
    for this_entry in shape_groups["active_line_2"].values():
        this_entry.hide = True


# Repeat the display
def update_active_line (shapes):
    global frame
    # when to start
    start_frame = keyframes[1]
    # when ends
    end_interval = 175
    # repeat
    repeat_interval = 200

    if (frame < end_interval + start_frame):
        nearest_start = start_frame
    else:
        frame_less_start = frame - start_frame
        # use frame_less_start to work out current interval
        num_intervals = int(frame_less_start / repeat_interval)
        nearest_start = (repeat_interval * num_intervals) + start_frame

    section_count = 0
    for shape in shapes:
        shapes[shape].reveal_tween(nearest_start+linedraw_timings[section_count][0], nearest_start+linedraw_timings[section_count][1], frame)
        section_count+=1
    if (frame == nearest_start + end_interval):
        for shape in shapes:
            shapes[shape].hide = True


# Add any pauses to this
# Pauses can also result from certain animations (eg. after each bullet)
pause_frames = []
slides[0].show_slide(0, FRAMES)


def draw():
    screen.clear()
    screen.fill((255,255,255))

    for this_group in shape_groups:
        for this_shape in shape_groups[this_group].values():
            this_shape.draw()
    for this_slide in slides:
        this_slide.draw()


def update():
    global frame, pause
    if (frame == 0):
        setup()
    controls()

    # Add animations here
    if (frame == keyframes[2]):
        for this_entry in shape_groups["static_line_1"].values():
            this_entry.hide = False
        for this_entry in shape_groups["static_line_2"].values():
            this_entry.hide = False
    # slides need to check for pause
    for this_slide in slides:
        if (this_slide.update(frame) == True): pause=True

    update_active_line(shape_groups["active_line_1"])
    update_active_line(shape_groups["active_line_2"])


    # keyframe 3 change width of bottom line
    if (frame == keyframes[3]):
        change_pulse_width(shape_groups["active_line_2"], 50)
    # keyframe 4 update static with new width
    if (frame == keyframes[4]):
        change_pulse_width(shape_groups["static_line_2"], 50)

    # Save animation frame
    if (save == True and ( pause == False or SAVE_PAUSED == True)):
        pygame.image.save(screen.surface, "/home/stewart/pwm-animation/animation-{0:05d}.png".format(save_frame))



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