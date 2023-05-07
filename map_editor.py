import pygame
import copy
import textures
import maps
from classes import render_map_blocks

save_image = False
"""
manual:
  a - print info
  b - print list and save screenshot
  z - switch between modes
  s - change map settings
  middle click - place/ remove map portal
  front thumb button - place/ remove  text box
  rear thumb button - place/ remove entity
  v - toggle viewed layer
  x - change layer
  l - hide lines
  r - freestyle hitbox
  p - precision for freestyle hitbox
  t - remove freestyle hitbox
  visual mode:
    left click - place block
    right click - remove block
    c - cycle block
    d - cycle block backwards
    e - copy block
    o - offset placement
    scroll up - next block folder
    scroll down - previous block folder
  hitbox mode:
    left click - place hitbox
    right click - remove hitbox
    c - cycle hitbox
    d - cycle hitbox backwards
    q - change hitbox side form
    w - change hitbox side
    e - copy hitbox
  quit - print list and save screenshot
"""
pygame.init()
clock = pygame.time.Clock()

block_list = textures.map_blocks

hitbox_list = {
    "normal": True,
    "tree": (22, 7, 20, 50),
    "center": (32, 32, 0, 0),
    "flower pot": (18, 37, 26, 20),

    "desk1": (7, 22, 56, 42),
    "desk2": (0, 22, 56, 42),
    "desk3": (0, 0, 56, 59),
    "desk4": (7, 0, 56, 59),
}

reverse_block = {value: key for (key, value) in block_list.items()}

entities_list = textures.entities

reverse_entity = {value: key for (key, value) in entities_list.items()}

event_list = []
event_list2 = []
event_list3 = []
setting_desc = ["is enemy encounter? ", "song name: ", "battle table: ", "displayed name: ", "more than 1 map picture: "]


def map_setting():
    global copyable, setting_desc
    copyable[4] = []
    for b in range(len(setting_desc)):
        if b in (0, 4):
            temp_str = convert_bool(input(setting_desc[b]))
            copyable[4].append(temp_str)
        elif b == 2:
            print("battle table: ")
            temp_dict = dict()
            try:
                while True:
                    temp_id = input("insert enemy id: ")
                    temp_weight = float(input("insert enemy weight: "))
                    temp_dict[temp_id] = temp_weight
            except ValueError:
                pass
            copyable[4].append(temp_dict)
        else:
            temp_str = input(setting_desc[b])
            copyable[4].append(temp_str)


def convert_bool(string):
    return True if string.lower() in ("true", "yes") else False


max_screen_y = 15
max_screen_x = 15
testMode = False

if testMode:
    x = 20
    y = 20
    screen_height = min(y, max_screen_y)
    screen_width = min(x, max_screen_x)
    map_name = "test"
    displayed_map = [[], [], [], [], [], []]
    copyable = [[], [], [], [], [], []]
    for i in range(y):
        displayed_map[0].append([])
    for i in displayed_map[0]:
        for j in range(x):
            i.append([textures.map_blocks["empty"], textures.map_blocks["empty"], textures.map_blocks["empty"], False])
    for i in range(y):
        copyable[0].append([])
    for i in copyable[0]:
        for j in range(x):
            i.append(["empty", "empty", "empty", False])
else:
    if convert_bool(input("import? ")):
        map_name = input("insert map name: ")
        displayed_map = maps.map_list[map_name]
        y = len(displayed_map[0])
        x = len(displayed_map[0][0])
        screen_height = min(y, max_screen_y)
        screen_width = min(x, max_screen_x)
        print(x, y)
        copyable = [[], [], [], [], [], []]
        for i in range(y):
            copyable[0].append([])
        for i in copyable[0]:
            for j in range(x):
                i.append([])

        for i in range(y):
            for j in range(x):
                for h in range(3):
                    if isinstance(displayed_map[0][i][j][h], list):
                        copyable[0][i][j].append([reverse_block[displayed_map[0][i][j][h][0]], displayed_map[0][i][j][h][1]])
                    else:
                        copyable[0][i][j].append(reverse_block[displayed_map[0][i][j][h]])
                copyable[0][i][j].append(displayed_map[0][i][j][3])

        copyable[1] = copy.deepcopy(displayed_map[1])

        for [(cords_x, cords_y), _, _] in displayed_map[1]:
            if cords_x == -1:
                cords_x = 0
            if cords_x == x:
                cords_x = x - 1
            if cords_y == -1:
                cords_y = 0
            if cords_y == y:
                cords_y = y - 1
            event_list.append((cords_x, cords_y))

        temp = []
        for [cords, texture, bottom] in displayed_map[3]:
            copyable[3].append([cords, "entity_"+reverse_entity[texture], bottom])
            temp.append([cords, reverse_entity[texture], bottom])
            event_list3.append((cords[0] // 64, cords[1] // 64))

        displayed_map[3] = temp

        copyable[2] = copy.deepcopy(displayed_map[2])
        for [cords, _, _] in displayed_map[2]:
            event_list2.append(cords)

        copyable[4] = copy.deepcopy(displayed_map[4])
        copyable[5] = copy.deepcopy(displayed_map[5])

    else:
        x = int(input("insert width: "))
        y = int(input("insert height: "))
        screen_height = min(y, max_screen_y)
        screen_width = min(x, max_screen_x)
        map_name = input("insert map name: ")
        displayed_map = [[], [], [], [], [], []]
        copyable = [[], [], [], [], [], []]
        for i in range(y):
            displayed_map[0].append([])
        for i in displayed_map[0]:
            for j in range(x):
                i.append([textures.map_blocks["empty"], textures.map_blocks["empty"], textures.map_blocks["empty"], False])
        for i in range(y):
            copyable[0].append([])
        for i in copyable[0]:
            for j in range(x):
                i.append(["empty", "empty", "empty", False])
        map_setting()

win = pygame.display.set_mode((64 * screen_width + 20, 64 * screen_height), 0, 32)

max_folder = 0
for i in list(block_list)[::-1]:
    if isinstance(i, int):
        max_folder = i
        break

folder_index = 0
block_index = 0
max_index = 0
current_folder = ""
current_block = ""


def set_block_index(folder, index):
    try:
        global block_index, current_block
        block_index = index
        current_block = list(block_list)[list(block_list).index(folder) + index + 1]
        print(current_block)
    except IndexError:
        print(folder, index)
        set_block_index(0, 0)


set_block_index(0, 0)
i = list(block_list).index(folder_index) + 1
try:
    while True:
        if isinstance(list(block_list)[i], int):
            break
        i += 1
except IndexError:
    pass
max_index = i - list(block_list).index(folder_index) - 2

hitbox_index = 0
current_hitbox = ""


def set_hitbox_index(index):
    global hitbox_index, current_hitbox
    hitbox_index = index
    current_hitbox = list(hitbox_list)[hitbox_index]
    print(current_hitbox)


set_hitbox_index(0)

mouseHeld = {
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: False
    }

camera_x = 0
camera_y = 0

run = True
mode = True
layer = 0
all_layers = True
show_lines = True
hitbox_var1 = 0
hitbox_var2 = 0
hitbox_var3 = 0
hitbox_var4 = 0
hitbox_var_selected = 1
hitbox_var_types = ["addition one (1)", "addition two (2)", "addition three (3)", "addition four (4)"]
hitbox_var_list = ["none", "left", "top-left", "top", "top-right", "right", "bottom-right", "bottom", "bottom-left"]
copied_hitbox = False
making_hitbox = False
mh_precision = True
temp_hitbox = [(), ()]
offset = (0, 0)
try:
    while run:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < 64*x:
            m_location_x = mouse_pos[0] // 64 + camera_x
            m_location_y = mouse_pos[1] // 64 + camera_y
            mouse_location = (m_location_x, m_location_y)
        else:
            mouse_location = 0
        camera_mouse_pos = (mouse_pos[0]+64*camera_x, mouse_pos[1]+64*camera_y)
        win.fill((0, 0, 0))

        for i in range(2):
            if layer == i or all_layers:
                render_map_blocks(displayed_map, i, camera_x*64, camera_y*64)
                # for w in range(screen_width):
                #     for h in range(screen_height):
                #         if isinstance(displayed_map[0][h + camera_y][w + camera_x][i], list):
                #             win.blit(displayed_map[0][h + camera_y][w + camera_x][i][0], (w * 64 + displayed_map[0][h + camera_y][w + camera_x][i][1][0], h * 64 + displayed_map[0][h + camera_y][w + camera_x][i][1][1]))
                #         else:
                #             win.blit(displayed_map[0][h + camera_y][w + camera_x][i], (w*64, h*64))

        for [pos, texture, bottom] in displayed_map[3]:
            try:
                win.blit(entities_list[texture], (pos[0] - 64*camera_x - entities_list[texture].get_width() // 2, pos[1] - 64*camera_y - entities_list[texture].get_height() // 2))
            except KeyError:
                print("key error - texture printing")
        # for [pos, texture] in displayed_map[3]:
        #     try:
        #         win.blit(texture, (pos[0] - 64*camera_x, pos[1] - 64*camera_y))
        #     except TypeError:
        #         print("type error - texture printing")

        if layer == 2 or all_layers:
            render_map_blocks(displayed_map, 2, camera_x*64, camera_y*64)
            # for w in range(screen_width):
            #     for h in range(screen_height):
            #         if isinstance(displayed_map[0][h + camera_y][w + camera_x][2], list):
            #             win.blit(displayed_map[0][h + camera_y][w + camera_x][2][0], (w * 64 + displayed_map[0][h + camera_y][w + camera_x][2][1][0], h * 64 + displayed_map[0][h + camera_y][w + camera_x][2][1][1]))
            #         else:
            #             win.blit(displayed_map[0][h + camera_y][w + camera_x][2], (w * 64, h * 64))

        for w in range(screen_width):
            for h in range(screen_height):
                if displayed_map[0][h + camera_y][w + camera_x][3]:
                    if displayed_map[0][h + camera_y][w + camera_x][3] is True:
                        temp_tuple = (0, 0, 64, 64)
                        pygame.draw.rect(win, (255, 0, 0), (w * 64 + temp_tuple[0], h * 64 + temp_tuple[1], temp_tuple[2]+1, temp_tuple[3]+1), 1)
                    else:
                        for temp_tuple in displayed_map[0][h + camera_y][w + camera_x][3]:
                            pygame.draw.rect(win, (255, 0, 0), (w * 64 + temp_tuple[0], h * 64 + temp_tuple[1], temp_tuple[2]+1, temp_tuple[3]+1), 1)

        for hb in displayed_map[5]:
            pygame.draw.rect(win, (255, 0, 0), (hb[0]-64*camera_x, hb[1]-64*camera_y, hb[2], hb[3]), 1)

        if show_lines:
            for i in range(0, 64*screen_width+1, 64):
                pygame.draw.line(win, (255, 255, 255), (i, 0), (i, 64*screen_height))
            for i in range(0, 64 * screen_height + 1, 64):
                pygame.draw.line(win, (255, 255, 255), (0, i), (64*screen_width, i))

        for w in range(screen_width):
            for h in range(screen_height):
                if displayed_map[0][h + camera_y][w + camera_x][3]:
                    if displayed_map[0][h + camera_y][w + camera_x][3] is True:
                        temp_tuple = (0, 0, 64, 64)
                        pygame.draw.line(win, (255, 0, 0), (w * 64 + temp_tuple[0], h * 64 + temp_tuple[1]), (w * 64 + temp_tuple[0] + temp_tuple[2], h * 64 + temp_tuple[1] + temp_tuple[3]))
                        pygame.draw.line(win, (255, 0, 0), (w * 64 + temp_tuple[0], h * 64 + temp_tuple[1] + temp_tuple[3]), (w * 64 + temp_tuple[0] + temp_tuple[2], h * 64 + temp_tuple[1]))
                    else:
                        for temp_tuple in displayed_map[0][h + camera_y][w + camera_x][3]:
                            pygame.draw.line(win, (255, 0, 0), (w * 64 + temp_tuple[0], h * 64 + temp_tuple[1]), (w * 64 + temp_tuple[0] + temp_tuple[2], h * 64 + temp_tuple[1] + temp_tuple[3]))
                            pygame.draw.line(win, (255, 0, 0), (w * 64 + temp_tuple[0], h * 64 + temp_tuple[1] + temp_tuple[3]), (w * 64 + temp_tuple[0] + temp_tuple[2], h * 64 + temp_tuple[1]))

        for hb in displayed_map[5]:
            pygame.draw.line(win, (255, 0, 0), (hb[0]-64*camera_x, hb[1]-64*camera_y), (hb[0]-64*camera_x + hb[2], hb[1]-64*camera_y + hb[3]))
            pygame.draw.line(win, (255, 0, 0), (hb[0]-64*camera_x, hb[1]-64*camera_y + hb[3]), (hb[0]-64*camera_x + hb[2], hb[1]-64*camera_y))

        for s in event_list:
            pygame.draw.circle(win, (255, 255, 0), ((s[0]-camera_x)*64+32, (s[1]-camera_y)*64+32), 32, 1)

        for s in event_list2:
            pygame.draw.circle(win, (255, 0, 255), ((s[0]-camera_x) * 64 + 32, (s[1]-camera_y) * 64 + 32), 28, 1)

        for s in event_list3:
            pygame.draw.circle(win, (0, 255, 255), ((s[0]-camera_x) * 64 + 32, (s[1]-camera_y) * 64 + 32), 24, 1)

        if making_hitbox:
            if temp_hitbox[0]:
                pygame.draw.circle(win, (255*mh_precision, 255*mh_precision, 255*mh_precision), (temp_hitbox[0][0]-camera_x*64, temp_hitbox[0][1]-camera_y*64), 2*mh_precision)
            if temp_hitbox[1]:
                pygame.draw.circle(win, (255*mh_precision, 255*mh_precision, 255*mh_precision), (temp_hitbox[1][0]-camera_x*64, temp_hitbox[1][1]-camera_y*64), 2*mh_precision)
                if temp_hitbox[0]:
                    if temp_hitbox[0][0] > temp_hitbox[1][0]:
                        if temp_hitbox[0][1] > temp_hitbox[1][1]:
                            hb = (temp_hitbox[1][0], temp_hitbox[1][1], temp_hitbox[0][0] - temp_hitbox[1][0],
                                         temp_hitbox[0][1] - temp_hitbox[1][1])
                        else:
                            hb = (temp_hitbox[1][0], temp_hitbox[0][1], temp_hitbox[0][0] - temp_hitbox[1][0],
                                         temp_hitbox[1][1] - temp_hitbox[0][1])
                    else:
                        if temp_hitbox[0][1] > temp_hitbox[1][1]:
                            hb = (temp_hitbox[0][0], temp_hitbox[1][1], temp_hitbox[1][0] - temp_hitbox[0][0],
                                         temp_hitbox[0][1] - temp_hitbox[1][1])
                        else:
                            hb = (temp_hitbox[0][0], temp_hitbox[0][1], temp_hitbox[1][0] - temp_hitbox[0][0],
                                         temp_hitbox[1][1] - temp_hitbox[0][1])
                    pygame.draw.rect(win, (255, 0, 0), (hb[0]-64*camera_x, hb[1]-64*camera_y, hb[2], hb[3]), 1)

        pygame.draw.rect(win, (0, 0, 0), (64 * screen_width + 1, 0, 20, 64 * screen_height))
        if not mode:
            pygame.draw.rect(win, (255, 0, 0), (64 * screen_width + 1, 0, 20, 64 * screen_height))
        if making_hitbox:
            pygame.draw.rect(win, (0, 255, 0), (64 * screen_width + 1, 0, 20, 64 * screen_height))

        pygame.draw.rect(win, (0, 0, 55 + (200 if layer == 2 else 0)), (64 * screen_width + 8, screen_height, 6, 20 * screen_height))
        pygame.draw.rect(win, (0, 0, 55 + (200 if layer == 1 else 0)), (64 * screen_width + 8, 22*screen_height, 6, 20 * screen_height))
        pygame.draw.rect(win, (0, 0, 55 + (200 if layer == 0 else 0)), (64 * screen_width + 8, 43*screen_height, 6, 20 * screen_height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if mouse_pos[0] < x * 64:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        pygame.draw.rect(win, (255, 255, 255), (64 * screen_width + 1, 0, 20, 64 * screen_height))
                        pygame.display.update()
                        offset = (int(input("offset x: ")), int(input("offset y: ")))
                    elif event.key == pygame.K_LEFT and camera_x > 0:
                        camera_x -= 1
                    elif event.key == pygame.K_RIGHT and camera_x < x - max_screen_x:
                        camera_x += 1
                    elif event.key == pygame.K_DOWN and camera_y < y - max_screen_y:
                        camera_y += 1
                    elif event.key == pygame.K_UP and camera_y > 0:
                        camera_y -= 1
                    elif event.key == pygame.K_r:
                        if making_hitbox:
                            if temp_hitbox[0][0] > temp_hitbox[1][0]:
                                if temp_hitbox[0][1] > temp_hitbox[1][1]:
                                    temp_rect = (temp_hitbox[1][0], temp_hitbox[1][1], temp_hitbox[0][0] - temp_hitbox[1][0], temp_hitbox[0][1] - temp_hitbox[1][1])
                                else:
                                    temp_rect = (temp_hitbox[1][0], temp_hitbox[0][1], temp_hitbox[0][0] - temp_hitbox[1][0], temp_hitbox[1][1] - temp_hitbox[0][1])
                            else:
                                if temp_hitbox[0][1] > temp_hitbox[1][1]:
                                    temp_rect = (temp_hitbox[0][0], temp_hitbox[1][1], temp_hitbox[1][0] - temp_hitbox[0][0], temp_hitbox[0][1] - temp_hitbox[1][1])
                                else:
                                    temp_rect = (temp_hitbox[0][0], temp_hitbox[0][1], temp_hitbox[1][0] - temp_hitbox[0][0], temp_hitbox[1][1] - temp_hitbox[0][1])
                            displayed_map[5].append(temp_rect)
                            copyable[5].append(temp_rect)
                        else:
                            temp_hitbox = [(0, 0), (0, 0)]
                        making_hitbox = not making_hitbox
                    elif event.key == pygame.K_t:
                        print("remove freestyle hitbox")
                        for i in range(len(displayed_map[5])):
                            print(str(i)+": "+str(displayed_map[5][i]))
                        temp_pop = int(input("pop index: "))
                        displayed_map[5].pop(temp_pop)
                        copyable[5].pop(temp_pop)
                    elif event.key == pygame.K_p:
                        mh_precision = not mh_precision

                    elif event.key == pygame.K_x:
                        layer += 1
                        if layer == 3:
                            layer = 0

                    elif event.key == pygame.K_w:
                        copied_hitbox = False
                        hitbox_var_selected += 1
                        if hitbox_var_selected >= 5:
                            hitbox_var_selected = 1
                        print(hitbox_var_types[hitbox_var_selected-1])

                    elif event.key == pygame.K_q:
                        copied_hitbox = False
                        globals()["hitbox_var" + str(hitbox_var_selected)] += 1
                        if globals()["hitbox_var" + str(hitbox_var_selected)] >= 9:
                            globals()["hitbox_var" + str(hitbox_var_selected)] = 0
                        print("{} \\/ {} \\/ {} \\/ {}".format(hitbox_var_list[hitbox_var1], hitbox_var_list[hitbox_var2], hitbox_var_list[hitbox_var3], hitbox_var_list[hitbox_var4]))

                    elif event.key == pygame.K_e:
                        if mode and copyable[0][mouse_location[1]][mouse_location[0]][layer] != "empty":
                            if isinstance(copyable[0][mouse_location[1]][mouse_location[0]][layer], list):
                                i = list(block_list).index(copyable[0][mouse_location[1]][mouse_location[0]][layer][0]) - 1
                            else:
                                i = list(block_list).index(copyable[0][mouse_location[1]][mouse_location[0]][layer]) - 1

                            try:
                                while True:
                                    if isinstance(list(block_list)[i], int):
                                        break
                                    i -= 1
                            except IndexError:
                                pass
                            folder_index = list(block_list)[i]
                            current_folder = block_list[folder_index]
                            j = list(block_list).index(folder_index) + 1
                            try:
                                while True:
                                    if isinstance(list(block_list)[j], int):
                                        break
                                    j += 1
                            except IndexError:
                                pass
                            max_index = j - list(block_list).index(folder_index) - 2
                            if isinstance(copyable[0][mouse_location[1]][mouse_location[0]][layer], list):
                                set_block_index(folder_index, list(block_list).index(copyable[0][mouse_location[1]][mouse_location[0]][layer][0]) - i - 1)
                            else:
                                set_block_index(folder_index, list(block_list).index(copyable[0][mouse_location[1]][mouse_location[0]][layer]) - i - 1)


                        else:
                            if displayed_map[0][mouse_location[1]][mouse_location[0]][3] is not False:
                                copied_hitbox = copy.deepcopy(displayed_map[0][mouse_location[1]][mouse_location[0]][3])

                    elif event.key == pygame.K_l:
                        show_lines = not show_lines

                    elif event.key == pygame.K_z:
                        mode = not mode

                    elif event.key == pygame.K_s:
                        map_setting()

                    elif event.key == pygame.K_a:
                        print("mouse pos: " + str(mouse_pos), str(camera_mouse_pos))
                        print("mouse_location: " + str(mouse_location))
                        print("folder: " + str(folder_index), current_folder)
                        print("block: " + str(block_index), current_block)
                        print("camera: " + str((camera_x, camera_y)))
                        if copied_hitbox is False:
                            print("hitbox: " + str(hitbox_index), current_hitbox)
                            print("{} \\/ {} \\/ {} \\/ {}".format(hitbox_var_list[hitbox_var1], hitbox_var_list[hitbox_var2], hitbox_var_list[hitbox_var3], hitbox_var_list[hitbox_var4]), hitbox_var_types[hitbox_var_selected - 1])
                        else:
                            print(copied_hitbox)

                    elif event.key == pygame.K_v:
                        all_layers = not all_layers
                        if all_layers:
                            print("all layers")
                        else:
                            print("one layer")

                    elif event.key == pygame.K_b:
                        temp_list = copyable[4]
                        for i in range(len(copyable[4])):
                            if copyable[4][i] == "True":
                                temp_list[i] = True
                            if copyable[4][i] == "False":
                                temp_list[i] = False
                        print("{5} = [{0}, {1}, {2}, {3}, {4}, {6}]".format(str(copyable[0]).replace("'", ""), str(copyable[1]), str(copyable[2]), str(copyable[3]).replace("'", ""), str(temp_list), "m_"+map_name, str(copyable[5])))
                        win = pygame.display.set_mode((64 * x, 64 * y), 0, 32)
                        win.fill((0, 0, 0))
                        for i in range(2):
                            for w in range(x):
                                for h in range(y):
                                    if isinstance(displayed_map[0][h][w][i], list):
                                        win.blit(displayed_map[0][h][w][i][0], (w * 64 + displayed_map[0][h][w][i][1][0], h * 64 + displayed_map[0][h][w][i][1][1]))
                                    else:
                                        win.blit(displayed_map[0][h][w][i], (w * 64, h * 64))
                        rect = pygame.Rect(0, 0, 64*x, 64*y)
                        sub = win.subsurface(rect)
                        if save_image:
                            pygame.image.save(sub, "resources/maps/m_"+map_name+".png")
                        win = pygame.display.set_mode((64 * screen_width + 20, 64 * screen_height), 0, 32)

                    elif event.key == pygame.K_c:
                        try:
                            current_folder = block_list[folder_index+1]
                            folder_index += 1
                        except KeyError:
                            current_folder = block_list[0]
                            folder_index = 0
                        i = list(block_list).index(folder_index) + 1
                        try:
                            while True:
                                if isinstance(list(block_list)[i], int):
                                    break
                                i += 1
                        except IndexError:
                            pass
                        max_index = i - list(block_list).index(folder_index) - 2
                        print(current_folder)
                        set_block_index(folder_index, 0)

                    elif event.key == pygame.K_d:
                        try:
                            current_folder = block_list[folder_index-1]
                            folder_index -= 1
                        except KeyError:
                            current_folder = block_list[max_folder]
                            folder_index = max_folder
                        i = list(block_list).index(folder_index) + 1
                        try:
                            while True:
                                if isinstance(list(block_list)[i], int):
                                    break
                                i += 1
                        except IndexError:
                            pass
                        max_index = i - list(block_list).index(folder_index) - 2
                        print(current_folder)
                        set_block_index(folder_index, 0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        mouseHeld[event.button] = True

                    if event.button == 6:
                        if mouse_location not in event_list3:
                            pygame.draw.rect(win, (0, 255, 255), (64 * screen_width + 1, 0, 20, 64 * screen_height))
                            pygame.display.update()
                            temp_location = copy.deepcopy(camera_mouse_pos)
                            print(str(i) for (i, _) in entities_list.items())
                            temp_name = input("insert texture name: ")
                            dy = int(input("bottom: "))
                            x_val = temp_location[0]
                            y_val = temp_location[1]
                            event_list3.append((temp_location[0] // 64, temp_location[1] // 64))
                            displayed_map[3].append([(x_val, y_val), temp_name, dy])
                            copyable[3].append([(x_val, y_val), "entity_"+temp_name, dy])
                        else:
                            displayed_map[3].pop(event_list3.index(mouse_location))
                            copyable[3].pop(event_list3.index(mouse_location))
                            event_list3.pop(event_list3.index(mouse_location))

                    if event.button == 7:
                        if mouse_location not in event_list2:
                            pygame.draw.rect(win, (255, 0, 255), (64 * screen_width + 1, 0, 20, 64 * screen_height))
                            pygame.display.update()
                            temp_location = mouse_location
                            temp_name = input("what is the name of the textbox? ")
                            temp_bool = convert_bool(input("will it play forcibly?"))
                            event_list2.append(temp_location)
                            displayed_map[2].append([temp_location, temp_name, temp_bool])
                            copyable[2].append([temp_location, temp_name, temp_bool])
                        else:
                            displayed_map[2].pop(event_list2.index(mouse_location))
                            copyable[2].pop(event_list2.index(mouse_location))
                            event_list2.pop(event_list2.index(mouse_location))

                    if event.button == 2:
                        if mouse_location not in event_list:
                            pygame.draw.rect(win, (255, 255, 0), (64 * screen_width + 1, 0, 20, 64 * screen_height))
                            pygame.display.update()
                            temp2_location = mouse_location
                            event_list.append(temp2_location)
                            adjust = input(str(temp2_location) + " right, left, up, down, stay: ")

                            if adjust == "right":
                                temp_location = (temp2_location[0] + 1, temp2_location[1])
                            elif adjust == "left":
                                temp_location = (temp2_location[0] - 1, temp2_location[1])
                            elif adjust == "up":
                                temp_location = (temp2_location[0], temp2_location[1] - 1)
                            elif adjust == "down":
                                temp_location = (temp2_location[0], temp2_location[1] + 1)
                            else:
                                temp_location = (temp2_location[0], temp2_location[1])

                            print(temp_location)
                            temp_name = input("name of map: ")
                            pre_dx = input("add x value: ")
                            pre_dy = input("add y value: ")
                            try:
                                temp_togo_x = int(pre_dx)
                            except ValueError:
                                temp_togo_x = float(pre_dx)
                            try:
                                temp_togo_y = int(pre_dy)
                            except ValueError:
                                temp_togo_y = float(pre_dy)

                            displayed_map[1].append([temp_location, temp_name, (temp_togo_x, temp_togo_y)])
                            copyable[1].append([temp_location, temp_name, (temp_togo_x, temp_togo_y)])
                        else:
                            displayed_map[1].pop(event_list.index(mouse_location))
                            copyable[1].pop(event_list.index(mouse_location))
                            event_list.pop(event_list.index(mouse_location))

                    if event.button == 4:
                        if mode:
                            if block_index < max_index:
                                set_block_index(folder_index, block_index + 1)
                            else:
                                set_block_index(folder_index, 0)

                        else:
                            copied_hitbox = False
                            hitbox_var1 = 0
                            hitbox_var2 = 0
                            hitbox_var3 = 0
                            hitbox_var4 = 0
                            hitbox_var_selected = 1
                            try:
                                set_hitbox_index(hitbox_index + 1)
                            except IndexError:
                                set_hitbox_index(0)

                    if event.button == 5:
                        if mode:
                            if block_index == 0:
                                set_block_index(folder_index, max_index)
                            else:
                                set_block_index(folder_index, block_index - 1)

                        else:
                            copied_hitbox = False
                            hitbox_var1 = 0
                            hitbox_var2 = 0
                            hitbox_var3 = 0
                            hitbox_var4 = 0
                            hitbox_var_selected = 1
                            if hitbox_index == 0:
                                set_hitbox_index(len(hitbox_list) - 1)
                            else:
                                set_hitbox_index(hitbox_index - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    mouseHeld[event.button] = False

        if mouse_location != 0:
            if making_hitbox:
                if mouseHeld[1]:
                    temp_hitbox[0] = tuple(camera_mouse_pos)
                if mouseHeld[3]:
                    temp_hitbox[1] = tuple(camera_mouse_pos)
            else:
                if mouse_location[0] >= x:
                    mouse_location = (x-1, mouse_location[1])
                elif mouse_location[0] < 0:
                    mouse_location = (0, mouse_location[1])
                if mouse_location[1] >= y:
                    mouse_location = (mouse_location[0], y-1)
                elif mouse_location[1] < 0:
                    mouse_location = (mouse_location[0], 0)
                elif mode:
                    if mouseHeld[1]:
                        if offset == (0, 0):
                                displayed_map[0][mouse_location[1]][mouse_location[0]][layer] = block_list[current_block]
                                copyable[0][mouse_location[1]][mouse_location[0]][layer] = current_block
                        else:
                            displayed_map[0][mouse_location[1]][mouse_location[0]][layer] = [block_list[current_block], copy.deepcopy(offset)]
                            copyable[0][mouse_location[1]][mouse_location[0]][layer] = [current_block, copy.deepcopy(offset)]
                    if mouseHeld[3]:
                        displayed_map[0][mouse_location[1]][mouse_location[0]][layer] = block_list["empty"]
                        copyable[0][mouse_location[1]][mouse_location[0]][layer] = "empty"
                else:
                    if mouseHeld[1]:
                        if copied_hitbox is not False:
                            displayed_map[0][mouse_location[1]][mouse_location[0]][3] = copied_hitbox
                            copyable[0][mouse_location[1]][mouse_location[0]][3] = copied_hitbox
                        else:
                            temp_tuple = hitbox_list[current_hitbox]
                            finallist = [0, 0, 0, 0]
                            if temp_tuple is True:
                                displayed_map[0][mouse_location[1]][mouse_location[0]][3] = True
                                copyable[0][mouse_location[1]][mouse_location[0]][3] = True
                            else:
                                true_final_list = []
                                temp_list = [hitbox_var1, hitbox_var2, hitbox_var3, hitbox_var4]
                                for temp_hitbox_var in temp_list:
                                    if temp_hitbox_var == 0:
                                        continue
                                    elif temp_hitbox_var == 1:
                                        finallist[0] = 0
                                        finallist[1] = temp_tuple[1]
                                        finallist[2] = temp_tuple[0] + temp_tuple[2]
                                        finallist[3] = temp_tuple[3]
                                    elif temp_hitbox_var == 2:
                                        finallist[0] = 0
                                        finallist[1] = 0
                                        finallist[2] = temp_tuple[0] + temp_tuple[2]
                                        finallist[3] = temp_tuple[1] + temp_tuple[3]
                                    elif temp_hitbox_var == 3:
                                        finallist[0] = temp_tuple[0]
                                        finallist[1] = 0
                                        finallist[2] = temp_tuple[2]
                                        finallist[3] = temp_tuple[1] + temp_tuple[3]
                                    elif temp_hitbox_var == 4:
                                        finallist[0] = temp_tuple[0]
                                        finallist[1] = 0
                                        finallist[2] = 64 - temp_tuple[0]
                                        finallist[3] = temp_tuple[1] + temp_tuple[3]
                                    elif temp_hitbox_var == 5:
                                        finallist[0] = temp_tuple[0]
                                        finallist[1] = temp_tuple[1]
                                        finallist[2] = 64 - temp_tuple[0]
                                        finallist[3] = temp_tuple[3]
                                    elif temp_hitbox_var == 6:
                                        finallist[0] = temp_tuple[0]
                                        finallist[1] = temp_tuple[1]
                                        finallist[2] = 64 - temp_tuple[0]
                                        finallist[3] = 64 - temp_tuple[1]
                                    elif temp_hitbox_var == 7:
                                        finallist[0] = temp_tuple[0]
                                        finallist[1] = temp_tuple[1]
                                        finallist[2] = temp_tuple[2]
                                        finallist[3] = 64 - temp_tuple[1]
                                    elif temp_hitbox_var == 8:
                                        finallist[0] = 0
                                        finallist[1] = temp_tuple[1]
                                        finallist[2] = temp_tuple[0] + temp_tuple[2]
                                        finallist[3] = 64 - temp_tuple[1]

                                    true_final_list.append(tuple(finallist))

                                if not true_final_list:
                                    true_final_list.append(hitbox_list[current_hitbox])

                                displayed_map[0][mouse_location[1]][mouse_location[0]][3] = true_final_list
                                copyable[0][mouse_location[1]][mouse_location[0]][3] = true_final_list
                    if mouseHeld[3]:
                        displayed_map[0][mouse_location[1]][mouse_location[0]][3] = False
                        copyable[0][mouse_location[1]][mouse_location[0]][3] = False

        pygame.display.update()
        clock.tick(30)
except Exception as error:
    temp_list = copyable[4]
    for i in range(len(copyable[4])):
        if copyable[4][i] == "True":
            temp_list[i] = True
        if copyable[4][i] == "False":
            temp_list[i] = False
    print("{5} = [{0}, {1}, {2}, {3}, {4}, {6}]".format(str(copyable[0]).replace("'", ""), str(copyable[1]), str(copyable[2]), str(copyable[3]).replace("'", ""), str(temp_list), "m_" + map_name, str(copyable[5])))
    print(error)
    raise error

temp_list = copyable[4]
for i in range(len(copyable[4])):
    if copyable[4][i] == "True":
        temp_list[i] = True
    if copyable[4][i] == "False":
        temp_list[i] = False

win = pygame.display.set_mode((64 * x, 64 * y), 0, 32)
win.fill((0, 0, 0))
for i in range(2):
    for w in range(x):
        for h in range(y):
            if isinstance(displayed_map[0][h][w][i], list):
                win.blit(displayed_map[0][h][w][i][0], (w * 64 + displayed_map[0][h][w][i][1][0], h * 64 + displayed_map[0][h][w][i][1][1]))
            else:
                win.blit(displayed_map[0][h][w][i], (w * 64, h * 64))

rect = pygame.Rect(0, 0, 64*x, 64*y)
sub = win.subsurface(rect)
if save_image:
    pygame.image.save(sub, "resources/maps/m_"+map_name+".png")
print("{5} = [{0}, {1}, {2}, {3}, {4}, {6}]".format(str(copyable[0]).replace("'", ""), str(copyable[1]), str(copyable[2]), str(copyable[3]).replace("'", ""), str(temp_list), "m_"+map_name, str(copyable[5])))

pygame.quit()
quit()
