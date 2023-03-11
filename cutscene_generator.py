import pygame, copy
import time as tm
import textures, maps, sounds
from classes import render_map_blocks, Game, blit_rotated_texture, blit_rotated_rect
from data import keysList, mouseDown, keysDown, mouseHeld, keysHeld, mouseUp, keysUp

"""
manual:

z - load all
x - load selected
r - load scene
c - switch mode
v - switch sub mode

q - cycle selected
e - use mode's function
f - run normal

t - check texture mouse pos

w,a,s,d - move object 1px
shift + w,a,s,d - move object 10px
mouse 1 - set pos to mouse

right/ left arrows - warp 1 frame forward/ backward
shift + right/ left arrows - warp 10 frames forward/ backward
down/ up arrows - warp 1 second forward/ backward
shift + down/ up arrows - warp 5 seconds forward/ backward
mouse 1 on timeline - set time
"""

pygame.init()

texture_list = {**textures.entities, **textures.cutscene_entities}


# def render_map_blocks_centered(_map_list, layer, _camera_x, _camera_y, insert_player=False):
#     h = len(_map_list[0])
#     w = len(_map_list[0][0])
#     render_map_blocks(_map_list, layer, _camera_x - w * 32, _camera_y - h * 32, insert_player)


def render_cutscene_frame(frame, layer):
    for _key in object_list:
        try:
            if _key.calculated[frame][0] == layer:
                temp_obj = _key.calculated[frame]
                if isinstance(_key, Text):
                    win.blit(pygame.font.SysFont(temp_obj[4][0], temp_obj[4][1]).render(temp_obj[3], False,
                                tuple(temp_obj[2])), (temp_obj[1][0] - int(camera_x), temp_obj[1][1] - int(camera_y)))
                elif isinstance(_key, Rect):
                    blit_rotated_rect(temp_obj[1][0] - camera_x + temp_obj[1][2] / 2, temp_obj[1][1] - camera_y + temp_obj[1][3] / 2,
                                      temp_obj[1][2], temp_obj[1][3], tuple(temp_obj[2]), temp_obj[3], temp_obj[4])
                    """
                    last time :
                    update image and texture object rendering and memory
                    maybe sync init and generators
                    """
                    #  pygame.draw.rect(win, tuple(_key.calculated[current_frame][2]), (_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1] - int(camera_y), _key.calculated[current_frame][1][2], _key.calculated[current_frame][1][3]), _key.calculated[current_frame][3])
                else:
                    blit_rotated_texture(texture_list[temp_obj[2]], temp_obj[1][0] - int(camera_x), temp_obj[1][1] - int(camera_y), None, None, temp_obj[3])
                    #  win.blit(texture_list[_key.calculated[current_frame][2]], (_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1] - int(camera_y)))
        except KeyError:
            pass


current_frame = 0
last_current_frame = 0
last_click = (0, 0)
object_list = []
active_object_list = []
selected = None
selected_index = 0
selected_class = ""
frame_commands = {}
runNormal = False


def append_frame_command(frame, command_name, *args):
    if frame in frame_commands:
        frame_commands[frame].append([command_name, *args])
    else:
        frame_commands[frame] = [[command_name, *args]]


def append_command(self, command_name, *args):
    self.function_list.append([command_name, self, *args])
    print(self.function_list[-1])
    sorted(self.function_list, key=lambda x: x[-1])


def move(self, x, y, time, frame):
    step_x = (x - self.calculated[frame][1][0]) / time
    step_y = (y - self.calculated[frame][1][1]) / time
    current = 0
    for i in range(frame, min(self.frame + self.time, frame + time, length)):
        current += 1
        self.calculated[i][1][0] += current * step_x
        self.calculated[i][1][1] += current * step_y

    for j in range(frame + time, min(self.frame + self.time, length)):
        self.calculated[j][1][0] = copy.deepcopy(self.calculated[i][1][0])
        self.calculated[j][1][1] = copy.deepcopy(self.calculated[i][1][1])


def rotate(self, deg, time, frame):

    if obj.__class__.__name__ == "Texture":
        step = (deg - self.calculated[frame][3]) / time
        current = 0
        for i in range(frame, min(self.frame + self.time, frame + time, length)):
            current += 1
            self.calculated[i][3] += current * step

        for j in range(frame + time, min(self.frame + self.time, length)):
            self.calculated[j][3] = copy.deepcopy(self.calculated[i][3])

    elif obj.__class__.__name__ == "Rect":
        step = (deg - self.calculated[frame][4]) / time
        current = 0
        for i in range(frame, min(self.frame + self.time, frame + time, length)):
            current += 1
            self.calculated[i][4] += current * step

        for j in range(frame + time, min(self.frame + self.time, length)):
            self.calculated[j][4] = copy.deepcopy(self.calculated[i][4])


def set_texture(self, texture, frame):
    for i in range(frame, min(self.frame + self.time, length)):
        self.calculated[i][2] = texture


def set_color(self, color, time, frame):
    step_1 = (color[0] - self.calculated[frame][2][0]) / time
    step_2 = (color[1] - self.calculated[frame][2][1]) / time
    step_3 = (color[2] - self.calculated[frame][2][2]) / time
    current = 0
    for i in range(frame, min(self.frame + self.time, frame + time, length)):
        current += 1
        self.calculated[i][2][0] += current * step_1
        self.calculated[i][2][1] += current * step_2
        self.calculated[i][2][2] += current * step_3

    for j in range(frame + time, min(self.frame + self.time, length)):
        self.calculated[j][2][0] = copy.deepcopy(self.calculated[i][2][0])
        self.calculated[j][2][1] = copy.deepcopy(self.calculated[i][2][1])
        self.calculated[j][2][2] = copy.deepcopy(self.calculated[i][2][2])


def set_dimensions(self, width, height, time, frame):
    step_w = (width - self.calculated[frame][1][2]) / time
    step_h = (height - self.calculated[frame][1][3]) / time
    current = 0
    for i in range(frame, min(self.frame + self.time, frame + time, length)):
        current += 1
        self.calculated[i][1][2] += current * step_w
        self.calculated[i][1][3] += current * step_h

    for j in range(frame + time, min(self.frame + self.time, length)):
        self.calculated[j][1][2] = copy.deepcopy(self.calculated[i][1][2])
        self.calculated[j][1][3] = copy.deepcopy(self.calculated[i][1][3])


def set_layer(self, layer, frame):
    for i in range(frame, min(self.frame + self.time, length)):
        self.calculated[i][2] = layer


def set_border_width(self, width, time, frame):
    step_w = (width - self.calculated[frame][3]) / time
    current = 0
    for i in range(frame, min(self.frame + self.time, frame + time, length)):
        current += 1
        self.calculated[i][3] += current * step_w

    for o in range(frame, min(self.frame + self.time, frame + time, length)):
        self.calculated[o][3] = int(self.calculated[o][3])

    for j in range(frame + time, min(self.frame + self.time, length)):
        self.calculated[j][3] = int(copy.deepcopy(self.calculated[i][3]))


def set_text(self, text, frame):
    for i in range(frame, min(self.frame + self.time, self.frame + self.time, length)):
        self.calculated[i][3] = text


def set_font(self, font, frame):
    for i in range(frame, min(self.frame + self.time, length)):
        self.calculated[i][4][0] = font


def set_font_size(self, size, time, frame):
    step_s = (size - self.calculated[frame][4][1]) / time
    current = 0
    for i in range(frame, min(self.frame + self.time, frame + time, length)):
        current += 1
        self.calculated[i][4][1] += current * step_s

    for o in range(frame, min(self.frame + self.time, frame + time, length)):
        self.calculated[o][4][1] = int(self.calculated[o][4][1])

    for j in range(frame + time, min(self.frame + self.time, length)):
        self.calculated[j][4][1] = int(copy.deepcopy(self.calculated[i][4][1]))


def move_x(self, x, frame):
    for i in range(frame, min(self.frame + self.time, length)):
        self.calculated[i][1][0] += x


def move_y(self, y, frame):
    for i in range(frame, min(self.frame + self.time, length)):
        self.calculated[i][1][1] += y


class Texture:
    command_list = ["move", "set_texture", "set_layer", "rotate"]

    def __init__(self, x, y, texture, frame, time, angle=0.0, layer=2):
        self.frames = {i: [layer, [x, y], texture, angle] for i in range(frame, frame + time)}
        self.calculated = {i: [layer, [x, y], texture, angle] for i in range(frame, frame + time)}
        self.frame = frame
        self.time = time
        self.function_list = []
        self.x = x
        self.y = y
        self.layer = layer
        self.texture = texture
        self.deg = angle
        object_list.append(self)
        active_object_list.append(self)
        self.output = {}

    def get_size(self):
        return texture_list[self.calculated[current_frame][2]].get_rect().size


class Rect:
    command_list = ["move", "set_color", "set_dimensions", "set_border_width", "set_layer", "rotate"]

    def __init__(self, x, y, width, height, color, frame, time, border_width=0, angle=0.0, layer=2):
        self.frames = {i: [layer, [x, y, width, height], list(color), border_width, angle] for i in range(frame, frame + time)}
        self.calculated = {i: [layer, [x, y, width, height], list(color), border_width, angle] for i in range(frame, frame + time)}
        self.function_list = []
        self.frame = frame
        self.time = time
        self.x = x
        self.y = y
        self.layer = layer
        self.width = width
        self.height = height
        self.color = list(color)
        self.border_width = border_width
        self.deg = angle
        object_list.append(self)
        active_object_list.append(self)
        self.output = {}

    def get_size(self):
        return self.calculated[current_frame][1][2], self.calculated[current_frame][1][3]


class Text:
    command_list = ["move", "set_text", "set_font", "set_font_size", "set_color", "set_layer"]

    def __init__(self, x, y, text, font, font_size, color, frame, time, layer=2):
        self.frames = {i: [layer, [x, y], list(color), text, [font, font_size]] for i in range(frame, frame + time)}
        self.calculated = {i: [layer, [x, y], list(color), text, [font, font_size]] for i in range(frame, frame + time)}
        self.function_list = []
        self.frame = frame
        self.time = time
        self.x = x
        self.y = y
        self.layer = layer
        self.text = text
        self.font = font
        self.font_size = font_size
        self.color = list(color)
        object_list.append(self)
        active_object_list.append(self)
        self.output = {}

    def get_size(self):
        return pygame.font.SysFont(self.calculated[current_frame][4][0], self.calculated[current_frame][4][1]).render(self.calculated[current_frame][3], False, (0, 0, 0)).get_rect().size


def convert_bool(string):
    return True if string.lower() in ("true", "yes") else False


test = False
if test:
    variable_name = "aa"
    map_str = "house1"
    map_list = maps.map_list[map_str]
    length = 100
    song = "song1"
    window_name = "aaa"
    camera_pos = None
    continue_song = False
    screen_size_x = min(len(map_list[0][0]), 10)
    screen_size_y = min(len(map_list[0]), 7)
else:
    variable_name = input("insert var name: ")
    map_str = input("cut scene map: ")
    map_list = maps.map_list[map_str]
    length = int(input("cut scene length? "))
    song = input("song name: ")
    window_name = input("window name: ")
    continue_song = convert_bool(input("continue music after cutscene? "))
    if convert_bool(input("keep camera pos?")):
        camera_pos = None
    else:
        camera_pos = (int(input("camera pos x? ")), int(input("camera pos y? ")))
    screen_size_x = 13
    screen_size_y = 8
    if convert_bool(input("change screen size? ")):
        screen_size_x = int(input("screen tiles x: "))
        screen_size_y = int(input("screen tiles y: "))


current_map = copy.deepcopy(map_str)

mode_modes = ["(add object) add texture", "(object management) add command", "(scene management) add scene command"]
mode = 0  # 0 - add object, 1 - object command/ edit object command /edit object's default stats/ remove object, 2 - frame function/ edit frame command, 3 - edit cut scene's default stats
mode_1_modes = ["add texture", "add rect", "add text"]
mode_2_modes = ["add command", "edit command", "delete command", "get stats", "edit basic stats", "reset all commands", "delete object"]
mode_3_modes = ["add scene command", "edit scene command", "remove scene command", "edit cut scene stats", "reset all commands"]
sub_mode = 0  # 0 - (0 - add texture, 1 - add rect,  2 - add text), 1 - (dependent on selected), 2 - (see functions with prefix cs_ in game file), 3 - (dependent on selected)

clock = pygame.time.Clock()
win_width = screen_size_x * 64
win_height = screen_size_y * 64 + 20
win = pygame.display.set_mode((win_width, win_height))

if camera_pos is None:
    camera_x = 0
    camera_y = 0
else:
    camera_x = camera_pos[0]
    camera_y = camera_pos[1]

texture_check = False
texture_checked = ""
texture_checked_rot = 0.0


run_frame_fix = False
mouse_pos = (0, 0)
run = True
while run:
    try:
        if Game.delta < 1:
            Game.current_time = tm.time()
            Game.delta += (Game.current_time - Game.last_time) * Game.ticks_per_second
            Game.last_time = float(Game.current_time)
        if tm.time() - Game.time_start > 1:
            Game.time_start += 1
            Game.frame = 0
        if Game.delta < 1:
            continue
        else:
            Game.delta -= 1
            Game.frames += 1
            Game.frame += 1

        win.fill((0, 0, 0))
        if True:
            for reset_key in mouseDown:
                mouseDown[reset_key] = False
            for reset_key in mouseUp:
                mouseUp[reset_key] = False
            for reset_key in keysDown:
                keysDown[reset_key] = False
            for reset_key in keysUp:
                keysUp[reset_key] = False

            if True:
                for reset_key in mouseDown:
                    mouseDown[reset_key] = False
                for reset_key in mouseUp:
                    mouseUp[reset_key] = False
                for reset_key in keysDown:
                    keysDown[reset_key] = False
                for reset_key in keysUp:
                    keysUp[reset_key] = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseDown[event.button] = True
                    mouseHeld[event.button] = True

                if event.type == pygame.MOUSEBUTTONUP:
                    mouseUp[event.button] = True
                    mouseHeld[event.button] = False

                if event.type == pygame.KEYDOWN:
                    for key in keysList:
                        if event.key == keysList[key]:
                            keysDown[key] = True
                            keysHeld[key] = True

                if event.type == pygame.KEYUP:
                    for key in keysList:
                        if event.key == keysList[key]:
                            keysUp[key] = True
                            keysHeld[key] = False

        if keysHeld["shift"]:
            mouse_pos = (pygame.mouse.get_pos()[0], mouse_pos[1])
        elif keysHeld["ctrl"]:
            mouse_pos = (mouse_pos[0], pygame.mouse.get_pos()[1])
        else:
            mouse_pos = pygame.mouse.get_pos()
        ##########################################
        if mouseDown[1]:
            last_click = copy.deepcopy(mouse_pos)
        if keysDown["c"]:
            mode += 1
            if mode >= 3:
                mode = 0
            sub_mode = 0
            print(mode_modes[mode])
        if keysDown["v"]:
            sub_mode += 1
            if mode == 0:
                if sub_mode >= 3:
                    sub_mode = 0
                print(mode_1_modes[sub_mode])
            elif mode == 1:
                if sub_mode >= 7:
                    sub_mode = 0
                print(mode_2_modes[sub_mode])
            elif mode == 2:
                if sub_mode >= 5:
                    sub_mode = 0
                print(mode_3_modes[sub_mode])
        if keysDown["e"]:
            if mode == 0:
                if sub_mode == 0:
                    temp = input("texture: ") #- temp_size[0] / 2  - temp_size[1] / 2
                    temp_size = texture_list[temp].get_rect().size
                    Texture(int(last_click[0] + camera_x), int(last_click[1] + camera_y), temp, current_frame, int(input("duration: ")), float(input("rotation: ")), int(input("layer (1-3): ")))
                elif sub_mode == 1:
                    if mouse_pos[0] > last_click[0]:
                        if mouse_pos[1] > last_click[1]:
                            temp_rect = (last_click[0], last_click[1], mouse_pos[0] - last_click[0], mouse_pos[1] - last_click[1])
                        else:
                            temp_rect = (last_click[0], mouse_pos[1], mouse_pos[0] - last_click[0], last_click[1] - mouse_pos[1])
                    else:
                        if mouse_pos[1] > last_click[1]:
                            temp_rect = (mouse_pos[0], last_click[1], last_click[0] - mouse_pos[0], mouse_pos[1] - last_click[1])
                        else:
                            temp_rect = (mouse_pos[0], mouse_pos[1], last_click[0] - mouse_pos[0], last_click[1] - mouse_pos[1])
                    print(temp_rect)
                    print(camera_x, camera_y)
                    Rect(temp_rect[0] + int(camera_x), temp_rect[1] + int(camera_y), temp_rect[2], temp_rect[3], [int(input("red: ")), int(input("green: ")), int(input("blue: "))], current_frame, int(input("duration: ")), int(input("border width: ")), float(input("rotation: ")), int(input("layer (1-3): ")))
                elif sub_mode == 2:
                    temp_font = input("font: ")
                    temp_font_size = int(input("font size: "))
                    temp_text = input("text: ")
                    #  temp_size = pygame.font.SysFont(temp_font, temp_font_size).render(temp_text, False, (0, 0, 0)).get_rect().size
                    Text(last_click[0] + int(camera_x), last_click[1] + int(camera_y), temp_text, temp_font, temp_font_size, (int(input("red: ")), int(input("green: ")), int(input("blue: "))), current_frame, int(input("duration: ")), int(input("layer (1-3):")))
            elif mode == 1 and selected is not None:
                if sub_mode == 0:
                    temp_input = input("command: ")
                    if temp_input == "move":
                        if mouse_pos[1] >= win_height-20:
                            append_command(selected, temp_input, selected.calculated[current_frame][1][0] + int(input("x {}: ".format(selected.calculated[current_frame][1][0]))), selected.calculated[current_frame][1][1] + int(input("y {}: ".format(selected.calculated[current_frame][1][1]))), int(input("time: ")), current_frame)
                        else:
                            append_command(selected, temp_input, last_click[0] + camera_x, last_click[1] + camera_y, int(input("time: ")), current_frame)
                    elif temp_input == "set_texture":
                        append_command(selected, temp_input, input("texture: "), current_frame)
                    elif temp_input == "set_color":
                        append_command(selected, temp_input, [int(input("red: ")), int(input("green: ")), int(input("blue: "))], int(input("time: ")), current_frame)
                    elif temp_input == "set_dimensions":
                        append_command(selected, temp_input, int(input("width {}: ".format(selected.width))), int(input("height {}: ".format(selected.height))), int(input("time: ")), current_frame)
                    elif temp_input == "set_layer":
                        append_command(selected, temp_input, int(input("layer 1-3: ")), current_frame)
                    elif temp_input == "set_border_width":
                        append_command(selected, temp_input, int(input("border_width {}: ".format(selected.border_width))), int(input("time: ")), current_frame)
                    elif temp_input == "set_text":
                        append_command(selected, temp_input, input("text: "), current_frame)
                    elif temp_input == "set_font":
                        append_command(selected, temp_input, input("font: "), current_frame)
                    elif temp_input == "set_font_size":
                        append_command(selected, temp_input, int(input("font size {}: ".format(selected.font_size))), int(input("time: ")), current_frame)
                    elif temp_input == "move_x":
                        append_command(selected, temp_input, last_click[0] - selected.x - selected.get_size()[0] / 2, current_frame)
                    elif temp_input == "move_y":
                        append_command(selected, temp_input, last_click[1] - selected.y - selected.get_size()[1] / 2, current_frame)
                    elif temp_input == "rotate":
                        if selected.__class__.__name__ == "Texture":
                            append_command(selected, temp_input, selected.calculated[current_frame][1][0] + float(
                            input("degree {}: ".format(selected.calculated[current_frame][3]))), int(input("time: ")), current_frame)
                        elif selected.__class__.__name__ == "Rect":
                            append_command(selected, temp_input, selected.calculated[current_frame][1][0] + float(
                                input("degree {}: ".format(selected.calculated[current_frame][4]))), int(input("time: ")), current_frame)

                elif sub_mode == 1:
                    if len(selected.function_list) > 0:
                        print({h: selected.function_list[h] for h in range(len(selected.function_list))})
                        temp_index = int(input("what index to edit? "))
                        print({h: selected.function_list[temp_index][h] for h in range(2, len(selected.function_list[temp_index]))})
                        temp_index_2 = int(input("what index to edit? "))
                        if isinstance(selected.function_list[temp_index][temp_index_2], str):
                            selected.function_list[temp_index][temp_index_2] = input("change value: ")
                        elif isinstance(selected.function_list[temp_index][temp_index_2], int):
                            selected.function_list[temp_index][temp_index_2] = int(input("change value"))
                        elif isinstance(selected.function_list[temp_index][temp_index_2], list):
                            for h in range(len(selected.function_list[temp_index][temp_index_2])):
                                if isinstance(selected.function_list[temp_index][temp_index_2][h], str):
                                    selected.function_list[temp_index][temp_index_2][h] = input("change value: ")
                                elif isinstance(selected.function_list[temp_index][temp_index_2][h], int):
                                    selected.function_list[temp_index][temp_index_2][h] = int(input("change value"))
                    else:
                        print("no commands associated with object")
                elif sub_mode == 2:
                    if len(selected.function_list) > 0:
                        print({h: selected.function_list[h] for h in range(len(selected.function_list))})
                        selected.function_list.pop(int(input("what index to pop? ")))
                    else:
                        print("no commands associated with object")
                elif sub_mode == 3:
                    print(selected.calculated[current_frame], selected.frames[current_frame])
                elif sub_mode == 4:
                    if selected_class == "Text":
                        selected.x = int(input("x {}:".format(int(selected.x))))
                        selected.y = int(input("y {}:".format(int(selected.y))))
                        selected.text = input("text {}:".format(selected.text))
                        selected.font = input("font {}:".format(selected.font))
                        selected.font_size = int(input("font_size {}:".format(str(selected.font_size))))
                        selected.layer = int(input("layer {}:".format(str(selected.layer))))
                        selected.time = int(input("time {}:".format(str(selected.time))))
                        selected.frame = int(input("frame {}:".format(str(selected.frame))))
                        selected.color = [int(input("red {}:".format(str(selected.color[0])))), int(input("green {}:".format(str(selected.color[1])))), int(input("blue {}:".format(str(selected.color[2]))))]
                        selected.frames = {h: [selected.layer, [selected.x, selected.y], list(selected.color), selected.text, [selected.font, selected.font_size]] for h in range(selected.frame, selected.frame + selected.time)}
                    elif selected_class == "Rect":
                        selected.x = int(input("x {}:".format(int(selected.x))))
                        selected.y = int(input("y {}:".format(int(selected.y))))
                        selected.color = [int(input("red {}:".format(str(selected.color[0])))), int(input("green {}:".format(str(selected.color[1])))), int(input("blue {}:".format(str(selected.color[2]))))]
                        selected.layer = int(input("layer {}:".format(str(selected.layer))))
                        selected.time = int(input("time {}:".format(str(selected.time))))
                        selected.frame = int(input("frame {}:".format(str(selected.frame))))
                        selected.width = int(input("width {}:".format(selected.width)))
                        selected.height = int(input("height {}:".format(selected.height)))
                        selected.border_width = int(input("border width {}:".format(str(selected.border_width))))
                        selected.frames = {h: [selected.layer, [selected.x, selected.y, selected.width, selected.height], list(selected.color), selected.border_width] for h in range(selected.frame, selected.frame + selected.time)}
                    elif selected_class == "Texture":
                        selected.x = int(input("x {}:".format(int(selected.x))))
                        selected.y = int(input("y {}:".format(int(selected.y))))
                        selected.layer = int(input("layer {}:".format(str(selected.layer))))
                        selected.texture = input("texture {}:".format(selected.texture))
                        selected.time = int(input("time {}:".format(str(selected.time))))
                        selected.frame = int(input("frame {}:".format(str(selected.frame))))
                        selected.frames = {h: [selected.layer, [selected.x, selected.y], selected.texture] for h in range(selected.frame, selected.frame + selected.time)}

                elif sub_mode == 5:
                    selected.function_list = []
                elif sub_mode == 6:
                    active_object_list.pop(active_object_list.index(selected))
                    object_list.pop(object_list.index(selected))
                    selected = None
            elif mode == 2:
                if sub_mode == 0:
                    try:
                        frame_commands[current_frame]
                    except KeyError:
                        frame_commands[current_frame] = []
                    finally:
                        command = input("command: ")
                        if command == "set_camera_time":
                            pass
                        else:
                            argument = input("argument (only 1): ")
                            frame_commands[current_frame].append([command, argument])
                            run_frame_fix = True
                elif sub_mode == 1:
                    if len(frame_commands) > 0:
                        print(frame_commands)
                        temp_index = int(input("what index to edit? "))
                        print({h: frame_commands[temp_index][h] for h in range(len(frame_commands[temp_index]))})
                        temp_index_2 = int(input("what index to edit? "))
                        print({h: frame_commands[temp_index][temp_index_2][h] for h in range(len(frame_commands[temp_index][temp_index_2]))})
                        temp_index_3 = int(input("what index to edit? "))
                        if isinstance(frame_commands[temp_index][temp_index_2][temp_index_3], str):
                            frame_commands[temp_index][temp_index_2][temp_index_3] = input("change value: ")
                        elif isinstance(selected.function_list[temp_index][temp_index_2][temp_index_3], int):
                            frame_commands[temp_index][temp_index_2][temp_index_3] = int(input("change value"))
                    else:
                        print("no commands found")
                elif sub_mode == 2:
                    if len(frame_commands) > 0:
                        print(frame_commands)
                        temp_index = int(input("what index to remove? "))
                        print({h: frame_commands[temp_index][h] for h in range(len(frame_commands[temp_index]))})
                        temp_index_2 = int(input("what index to remove? "))
                        frame_commands[temp_index].pop(temp_index_2)
                        if len(frame_commands[temp_index]) == 0:
                            frame_commands.pop(temp_index)
                elif sub_mode == 3:
                    map_str = input("cut scene map: " + f"({map_str}) ")
                    map_list = maps.map_list[map_str]
                    temp_length = int(input("cut scene length? " + f"({length}) "))
                    song = input("song name: " + f"({song}) ")
                    window_name = input("window name: " + f"({window_name}) ")
                    continue_song = convert_bool(input("continue music after cutscene? " + f"({continue_song}) "))
                    if convert_bool(input("keep camera pos?" + f"({camera_pos}) ")):
                        camera_pos = None
                    else:
                        camera_pos = (int(input("camera pos x? ")), int(input("camera pos y? ")))
                    screen_size_x = int(input("screen tiles x: " + f"({screen_size_x}) "))
                    screen_size_y = int(input("screen tiles y: " + f"({screen_size_y}) "))

                    run_frame_fix = True
                    current_map = 0
                    selected = None
                    selected_index = None
                    if temp_length < length:
                        for fr in range(temp_length, length):
                            frame_commands.pop(fr)
                            for obj in object_list:
                                obj.calculated.pop(fr)
                                obj.frames.pop(fr)
                elif sub_mode == 4:
                    frame_commands = {}
        ###########################################
        if mouseDown[1] and mouse_pos[1] >= win_height - 20:
            current_frame = int(length * mouse_pos[0] / win_width)

        if keysHeld["shift"]:
            if keysDown["left"]:
                current_frame -= 10
                if current_frame < 0:
                    current_frame = 0
            elif keysDown["up"]:
                current_frame -= 150
                if current_frame < 0:
                    current_frame = 0
            elif keysDown["right"]:
                current_frame += 10
                if current_frame >= length:
                    current_frame = length - 1
            elif keysDown["down"]:
                current_frame += 150
                if current_frame >= length:
                    current_frame = length - 1
            if keysHeld["num8"]:
                camera_y -= 4
                last_click = (last_click[0], last_click[1] + 4)
            if keysHeld["num5"]:
                camera_y += 4
                last_click = (last_click[0], last_click[1] - 4)
            if keysHeld["num4"]:
                camera_x -= 4
                last_click = (last_click[0] + 4, last_click[1])
            if keysHeld["num6"]:
                camera_x += 4
                last_click = (last_click[0] - 4, last_click[1])
        else:
            if keysDown["left"]:
                current_frame -= 1
                if current_frame < 0:
                    current_frame = 0
            elif keysDown["up"]:
                current_frame -= 30
                if current_frame < 0:
                    current_frame = 0
            elif keysDown["right"]:
                current_frame += 1
                if current_frame >= length:
                    current_frame = length - 1
            elif keysDown["down"]:
                current_frame += 30
                if current_frame >= length:
                    current_frame = length - 1
            if keysHeld["num8"]:
                camera_y -= 1
                last_click = (last_click[0], last_click[1] + 1)
            if keysHeld["num5"]:
                camera_y += 1
                last_click = (last_click[0], last_click[1] - 1)
            if keysHeld["num4"]:
                camera_x -= 1
                last_click = (last_click[0] + 1, last_click[1])
            if keysHeld["num6"]:
                camera_x += 1
                last_click = (last_click[0] - 1, last_click[1])

        if keysDown["f"]:
            selected = None
            selected_index = None
            runNormal = not runNormal
            current_frame = 0
            last_current_frame = 0
            if runNormal:
                sounds.play(song, False, 0, 0)
            else:
                sounds.play("none", False, 0, 0)
            map_list = maps.map_list[map_str]
            win_width = screen_size_x * 64
            win_height = screen_size_y * 64 + 20
            win = pygame.display.set_mode((win_width, win_height))

        if mouseDown[1] and mouse_pos[1] >= win_height - 20 or keysDown["left"] or keysDown["up"] or keysDown["down"] or keysDown["right"] or keysDown["f"] or run_frame_fix:
            run_frame_fix = False
            for obj in object_list:
                try:
                    obj.frames[current_frame]
                except KeyError:
                    if obj in active_object_list:
                        active_object_list.pop(active_object_list.index(obj))
                        if obj is selected:
                            if len(active_object_list) != 0:
                                selected = active_object_list[0]
                                selected_index = 0
                            else:
                                selected = None
                                selected_index = None
                                selected_class = ""
                                print("deselected")
                else:
                    if obj not in active_object_list:
                        active_object_list.append(obj)

            for checked_frames in range(current_frame, -1, -1):
                try:
                    current_map = [h[1] for h in frame_commands[checked_frames] if h[0] == "change_map"][0]
                except (KeyError, IndexError):
                    pass
                else:
                    map_list = maps.map_list[current_map]
                    break
            else:
                map_list = maps.map_list[map_str]

            for checked_frames in range(current_frame, -1, -1):
                try:
                    current_camera = [h[1] for h in frame_commands[checked_frames] if h[0] == "set_camera"][0]
                except (KeyError, IndexError):
                    pass
                else:
                    temp = current_camera.split(" ")
                    camera_x = temp[0]
                    camera_y = temp[1]
                    break
            else:
                if camera_pos is not None:
                    camera_x = camera_pos[0]
                    camera_y = camera_pos[1]
            for checked_frames in range(current_frame, -1, -1):
                try:
                    current_size = [h[1] for h in frame_commands[checked_frames] if h[0] == "set_screen_size"][0]
                except (KeyError, IndexError):
                    pass
                else:
                    temp = current_size.split(" ")
                    win_width = temp[0] * 64
                    win_height = temp[1] * 64 + 20
                    win = pygame.display.set_mode((win_width, win_height))
                    break
            else:
                win_width = screen_size_x * 64
                win_height = screen_size_y * 64 + 20
                win = pygame.display.set_mode((win_width, win_height))

        if keysDown["q"]:
            mode = 1
            sub_mode = 0
            if selected is None:
                if len(active_object_list) != 0:
                    selected_index = 0
                    selected = active_object_list[0]
                    selected_class = selected.__class__.__name__
                    print(selected.__class__.__name__)
                else:
                    print("no active objects")
            else:
                selected_index += 1
                if selected_index >= len(active_object_list):
                    selected_index = 0
                selected = active_object_list[selected_index]
                selected_class = selected.__class__.__name__
                print(selected.__class__.__name__)

        if keysDown["t"]:
            if texture_check:
                print(mouse_pos)
            else:
                texture_checked = input("texture: ")
                texture_checked_rot = float(input("rotation: "))
            texture_check = not texture_check

        if selected is not None:
            if mouseDown[3] and mouse_pos[1] < win_height - 20:
                append_command(selected, "move", int(mouse_pos[0] - selected.get_size()[0] / 2), int(mouse_pos[1] - selected.get_size()[1] / 2), 1, current_frame)

            if keysHeld["shift"]:
                if keysDown["w"]:
                    append_command(selected, "move_y", -5, current_frame)
                elif keysDown["a"]:
                    append_command(selected, "move_x", -5, current_frame)
                elif keysDown["s"]:
                    append_command(selected, "move_y", 5, current_frame)
                elif keysDown["d"]:
                    append_command(selected, "move_x", 5, current_frame)
            else:
                if keysDown["w"]:
                    append_command(selected, "move_y", -1, current_frame)
                elif keysDown["a"]:
                    append_command(selected, "move_x", -1, current_frame)
                elif keysDown["s"]:
                    append_command(selected, "move_y", 1, current_frame)
                elif keysDown["d"]:
                    append_command(selected, "move_x", 1, current_frame)

            if keysDown["x"]:
                selected.calculated = copy.deepcopy(selected.frames)
                for cmd in selected.function_list:
                    globals()[cmd[0]](*cmd[1:])

        if keysDown["z"]:
            for obj in object_list:
                obj.calculated = copy.deepcopy(obj.frames)
                for cmd in obj.function_list:
                    globals()[cmd[0]](*cmd[1:])
        ###########################################
        for i in range(2):
            # for w in range(len(map_list[0][0])):
            #     for h in range(len(map_list[0])):
            #         if not map_list[0][h][w][i] == textures.map_blocks["empty"]:
            #             if isinstance(map_list[0][h][w][i], list):
            #                 win.blit(map_list[0][h][w][i][0], (w * 64 - int(camera_x) + map_list[0][h][w][i][1][0], h * 64 - int(camera_y) + map_list[0][h][w][i][1][1]))
            #             else:
            #                 win.blit(map_list[0][h][w][i], (w * 64 - int(camera_x), h * 64 - int(camera_y)))
            render_map_blocks(map_list, i, camera_x, camera_y)
        # for _key in object_list:
        #     try:
        #         if _key.calculated[current_frame][0] == 1:
        #             if isinstance(_key, Text):
        #                 win.blit(pygame.font.SysFont(_key.calculated[current_frame][4][0], _key.calculated[current_frame][4][1]).render(_key.calculated[current_frame][3], False, tuple(_key.calculated[current_frame][2])), (_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1 - int(camera_y)]))
        #             elif isinstance(_key, Rect):
        #                 pygame.draw.rect(win, tuple(_key.calculated[current_frame][2]), (_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1] - int(camera_y), _key.calculated[current_frame][1][2], _key.calculated[current_frame][1][3]), _key.calculated[current_frame][3])
        #             else:
        #                 win.blit(texture_list[_key.calculated[current_frame][2]], (_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1] - int(camera_y)))
        #     except KeyError:
        #         pass
        # for w in range(len(map_list[0][0])):
        #     for h in range(len(map_list[0])):
        #         if isinstance(map_list[0][h][w][2], list):
        #             win.blit(map_list[0][h][w][2][0], (w * 64 - int(camera_x) + map_list[0][h][w][2][1][0], h * 64 - int(camera_y) + map_list[0][h][w][2][1][1]))
        #         else:
        #             win.blit(map_list[0][h][w][2], (w * 64 - int(camera_x), h * 64 - int(camera_y)))
        render_cutscene_frame(current_frame, 1)
        render_map_blocks(map_list, 2, camera_x, camera_y)
        # for w in range(len(map_list[0][0])):
        #     for h in range(len(map_list[0])):
        #         if not map_list[0][h][w][2] == maps.empty:
        #             win.blit(map_list[0][h][w][2], (w * 64, h * 64))
        for layer_ in (2, 3):
            render_cutscene_frame(current_frame, layer_)
            # for _key in object_list:
            #     try:
            #         if _key.calculated[current_frame][0] == layer_:
            #             if isinstance(_key, Text):
            #                 win.blit(pygame.font.SysFont(_key.calculated[current_frame][4][0], _key.calculated[current_frame][4][1]).render(_key.calculated[current_frame][3], False, tuple(_key.calculated[current_frame][2])), (_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1 - int(camera_y)]))
            #             elif isinstance(_key, Rect):
            #                 blit_rotated_rect(_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1] - int(camera_y), _key.calculated[current_frame][1][2], _key.calculated[current_frame][1][3], tuple(_key.calculated[current_frame][2]), _key.calculated[current_frame][3], (0, 0), 0)
            #                 """
            #                 last time :
            #                 update image and texture object rendering and memory
            #                 maybe sync init and generators
            #                 """
            #                 #  pygame.draw.rect(win, tuple(_key.calculated[current_frame][2]), (_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1] - int(camera_y), _key.calculated[current_frame][1][2], _key.calculated[current_frame][1][3]), _key.calculated[current_frame][3])
            #             else:
            #                 blit_rotated_texture(texture_list[_key.calculated[current_frame][2]])
            #                 #  win.blit(texture_list[_key.calculated[current_frame][2]], (_key.calculated[current_frame][1][0] - int(camera_x), _key.calculated[current_frame][1][1] - int(camera_y)))
            #     except KeyError:
            #         pass
        pygame.draw.rect(win, (0, 0, 40), (0, win_height - 20, win_width, 20))
        for h in range(1, 8):
            pygame.draw.line(win, (80, 80, 80), (int(h * win_width / 8), win_height - 20), (int(h * win_width / 8), win_height), 2)
        pygame.draw.line(win, (80, 80, 255), (int(current_frame / (length - 1) * win_width), win_height - 20), (int(current_frame / (length - 1) * win_width), win_height), 4)
        if texture_check:
            blit_rotated_texture(texture_list[texture_checked], *mouse_pos, rot=texture_checked_rot)

        if selected is not None:
            pygame.draw.circle(win, (255, 255, 0), (int(selected.calculated[current_frame][1][0] - camera_x), int(selected.calculated[current_frame][1][1]) - camera_y), 4)
            pygame.draw.line(win, (255, 255, 255), (int((selected.frame - 0.5) / (length - 1) * win_width), win_height - 10), (int((selected.frame + selected.time - 0.5) / (length - 1) * win_width), win_height - 10), 3)
            win.blit(pygame.font.SysFont("Aharoni", 24).render(str(selected.frame + selected.time - 1), False, (0, 0, 0)), (win_width - 40, win_height - 40))
        win.blit(pygame.font.SysFont("Aharoni", 24).render(str(current_frame), False, (0, 0, 0)), (5, win_height - 40))
        pygame.draw.circle(win, (0, 0, 0), last_click, 2, 1)
        pygame.draw.circle(win, (0, 0, 0), mouse_pos, 2, 1)
        ###########################################
        last_current_frame = copy.deepcopy(current_frame)
        if runNormal:
            current_frame += 1
            if current_frame >= length:
                runNormal = False
                current_frame = 0
            try:
                for cmd in frame_commands[current_frame]:
                    if cmd[0] == "change_map":
                        current_map = cmd[1]
                        map_list = maps.map_list[cmd[1]]
                    elif cmd[0] == "change_song":
                        sounds.play(cmd[1])
                    elif cmd[0] == "effect":
                        sounds.play_effect(cmd[1])
                    elif cmd[0] == "set_camera":
                        temp = cmd[1].split(" ")
                        camera_x = int(temp[0])
                        camera_y = int(temp[1])
                    elif cmd[0] == "set_screen_size":
                        temp = cmd[1].split(" ")
                        win_width = int(temp[0]) * 64
                        win_height = int(temp[1]) * 64 + 20
                        win = pygame.display.set_mode((win_width, win_height))
            except KeyError:
                pass
        pygame.display.update()
    except Exception as e:
        raise e

output = {h: [] for h in range(length)}
for obj in object_list:
    for obj_frame in obj.calculated:
        temp_obj_ = obj.calculated[obj_frame]
        if obj.__class__.__name__ == "Texture":
            obj.output[obj_frame] = [temp_obj_[0], "\'" + temp_obj_[2] + "\'", (int(temp_obj_[1][0]), int(temp_obj_[1][1])), float(temp_obj_[2])]
        elif obj.__class__.__name__ == "Rect":
            obj.output[obj_frame] = [temp_obj_[0], (int(temp_obj_[1][0]), int(temp_obj_[1][1]), int(temp_obj_[1][2]), int(temp_obj_[1][3])), (int(temp_obj_[2][0]), int(temp_obj_[2][1]), int(temp_obj_[2][2])), temp_obj_[3], temp_obj_[4]]
        elif obj.__class__.__name__ == "Text":
            obj.output[obj_frame] = [temp_obj_[0], temp_obj_[3], (int(temp_obj_[1][0]), int(temp_obj_[1][1])), "\'pygame.font.SysFont(\'{}\', {})\'".format(temp_obj_[4][0], temp_obj_[4][1]), (int(temp_obj_[2][0]), int(temp_obj_[2][1]), int(temp_obj_[2][2]))]

for obj in object_list:
    for obj_frame in obj.output:
        output[obj_frame].append(obj.output[obj_frame])

print(variable_name, "=", str(output).replace('\'"', '').replace('"\'', ''))
print("'" + variable_name + "':", "[" + variable_name + ",", str([map_str, length, song, window_name, frame_commands, continue_song, camera_pos, (screen_size_x, screen_size_y)])[1:])
