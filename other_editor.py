import pygame
from pygame.compat import as_bytes, as_unicode
from data import keysList, mouseDown, keysDown, mouseHeld, keysHeld, mouseUp, keysUp
"""
MANUAL:

menus:
    e - select
    q - next item

writer:
    letter - type letter
    enter - accept and next item
    backspace - delete index
    left - index one to the left
    right - index one to the right
    
    keypad enter - add argument
    del - remove argument
    up/ down - move between arguments
    
    ctrl + a - select all
    ctrl + v - paste
    while selected:
        ctrl + c - copy
        backspace / any letter - delete all
        left - sets index to start
        right - sets index to end
    
    bottom: items left in queue
    top: argument index
"""

font = pygame.font.SysFont("Cooper Black", 30)
font3 = pygame.font.SysFont("Cooper Black", 16)
font2 = pygame.font.SysFont("Agency FB", 30)
clock = pygame.time.Clock()

if True:
    typeBar = ""
    typeBar1 = ""
    typeBar2 = ""
    typeBarX = 5
    typeBarY = 5
    index = -1
    maxIndex = 0
    framesUP = 0
    UpBool = True
    is_all_selected = False
isTypeBar = False
content = ["text", "scroll/script", "items", "shop", "loot table"]
current_object = [None]
current_iter = iter(current_object)
current_next = next(current_iter)

up_down_content = [""]
up_down_index = 0
up_down_max_index = 0
allow_up_down = False
separate_and_convert = False

queue = []
queue_num = 0
first_input = True
inputs = []
final_inputs = []

mode = False
stage = 0
enter_count = 0

win_width = 300
win_height = 150
win = pygame.display.set_mode((300, 150))

letter_height = font.render("n", False, (0, 0, 0)).get_rect().height

in_game_map_x = 64 * 11
current_order = []

if True:  # types
    text_types = ["dialog", "question", "command", "finish"]

    scroll_types = ["new attack", "finish"]

    loot_table_types = shop_types = ["new item", "finish"]


def init_type_bar(x, y):
    global typeBar, typeBar1, typeBar2, typeBarX, typeBarY, index, maxIndex, framesUP, UpBool, is_all_selected
    typeBar = ""
    typeBar1 = ""
    typeBar2 = ""
    typeBarX = x
    typeBarY = y
    index = -1
    maxIndex = 0
    framesUP = 0
    UpBool = True
    is_all_selected = False


def current(obj):
    global current_object, current_iter, current_next
    current_object = obj
    current_iter = iter(obj)
    current_next = next(current_iter)


def win_size(width, height):
    global win, win_width, win_height
    win = pygame.display.set_mode((width, height))
    win_width = width
    win_height = height


current(content)
pygame.scrap.init()
run = True
while run:
    dt = 1000 / clock.tick(30)
    mouse_pos = pygame.mouse.get_pos()
    win.fill((255, 255, 255))
    if len(queue) != queue_num:
        if first_input:
            queue_num = len(queue)
            first_input = False
        else:
            queue.pop(0)

        if len(queue) != 0:
            init_type_bar(font.render(queue[0], False, (0, 0, 0)).get_rect().width + 40, win_height / 2 - letter_height / 2)
        else:
            final_inputs.append(inputs)
            inputs = []
            first_input = True
            win_size(300, 150)
            isTypeBar = False
            if mode == 0:
                current(text_types)
                stage = 1
            elif mode == 1:
                current(scroll_types)
                stage = 1
            elif mode == 3:
                current(shop_types)
                stage = 1
            elif mode == 4:
                current(loot_table_types)
                stage = 1

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
    if isTypeBar:
        for i in [k for k, v in keysDown.items() if v]:
            if keysHeld["enter"]:
                if allow_up_down:
                    if up_down_content == [""] and mode == 0:
                        pass
                    elif separate_and_convert:
                        temp = []
                        for text in up_down_content:
                            temp2 = text.split(",")
                            for text2 in range(len(temp2)):
                                if temp2[text2].startswith("."):
                                    temp2[text2] = int(temp2[text2].replace(".", ""))
                            temp.append(temp2)
                        inputs.append(temp)
                    else:
                        if mode == 0 and (current_next == "dialog" or (current_next == "question" and enter_count == 0)):
                            inputs.append("|".join(up_down_content))
                        else:
                            inputs.append(up_down_content)
                else:
                    # if typeBar1 + typeBar2 == "" and mode == 0:
                    #     pass
                    if separate_and_convert:
                        temp2 = (typeBar1 + typeBar2).split(",")
                        for text2 in range(len(temp2)):
                            if temp2[text2].startswith("."):
                                temp2[text2] = int(temp2[text2].replace(".", ""))
                        inputs.append(temp2)
                    else:
                        inputs.append(typeBar1 + typeBar2)

                enter_count += 1
                if mode == 0:
                    if stage == 0:
                        allow_up_down = True
                        separate_and_convert = True
                    if current_next == "question":
                        if enter_count == 1:
                            allow_up_down = True
                            separate_and_convert = False
                        if enter_count == 2:
                            allow_up_down = True
                            separate_and_convert = True
                            queue += ["commands: "] * (len(up_down_content) + 1)
                            queue_num = len(up_down_content) + 1
                elif mode == 1:
                    if enter_count == 1:
                        allow_up_down = False
                        separate_and_convert = True
                    elif enter_count == 2:
                        allow_up_down = False
                        separate_and_convert = False
                    elif enter_count == 14:
                        allow_up_down = True
                        separate_and_convert = True
                    elif enter_count == 15:
                        allow_up_down = False
                        separate_and_convert = False
                    elif enter_count == 19:
                        if typeBar != "none":
                            queue += ["effect time: ", "is targeting player? ", "add effect: ", "exist effect: ", "remove effect: ", "removing condition: ", "color: "]
                            queue_num = 8
                    elif enter_count == 25:
                        allow_up_down = False
                        separate_and_convert = True
                elif mode == 2:
                    if enter_count == 3:
                        allow_up_down = True
                    elif enter_count == 4:
                        allow_up_down = False
                    elif enter_count == 5:
                        if int(typeBar1 + typeBar2) == 0:
                            pass
                        elif int(typeBar1 + typeBar2) == 1:
                            queue += ["hp: ", "mana: ", "exp: ", "required level: ", "equip passive: "]
                            queue_num = 6
                        elif int(typeBar1 + typeBar2) == 2:
                            queue += ["max hp: ", "max mana: ", "exp multiplier: ", "required level: ", "attack bonus: ", "defense bonus: ", "evasion bonus: ", "accuracy bonus:", "equip passive: ", "equipped passive: "]
                            queue_num = 11
                        elif int(typeBar1 + typeBar2) in (3, 4, 5, 7, 8, 9):
                            queue += ["max hp: ", "max mana: ", "exp multiplier: ", "required level: ", "attack bonus: ", "defense bonus: ", "evasion bonus: ", "accuracy bonus:", "equip passive: ", "equipped passive: ", "unequip passive: ", "atk/def boost: "]
                            queue_num = 13
                        else:
                            queue += ["max hp: ", "max mana: ", "exp multiplier: ", "required level: ", "attack bonus: ", "defense bonus: ", "evasion bonus: ", "accuracy bonus:", "equip passive: ", "equipped passive: ", "unequip passive: "]
                            queue_num = 12
                    elif enter_count == 13:
                        allow_up_down = True
                    elif enter_count == 16:
                        allow_up_down = False
                elif mode == 3:
                    if enter_count == 3:
                        allow_up_down = True
                        separate_and_convert = True
                elif mode == 4:
                    if enter_count == 2:
                        allow_up_down = False
                        separate_and_convert = True
                print(inputs[-1])
                typeBar = ""
                typeBar1 = ""
                typeBar2 = ""
                index = -1
                maxIndex = 0
                queue_num -= 1
                up_down_content = [""]
                up_down_max_index = 0
                up_down_index = 0

            elif keysHeld["ctrl"]:
                if i == "a":
                    is_all_selected = True
                elif i == "c":
                    is_all_selected = False
                    pygame.scrap.put(pygame.SCRAP_TEXT, as_bytes(typeBar1+typeBar2))
                elif i == "v":
                    temp_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if temp_text:
                        if is_all_selected:
                            index = -1
                            typeBar2 = ""
                            typeBar1 = str(temp_text, "utf-8").replace("\0", "")
                            maxIndex = len(typeBar1)
                        else:
                            typeBar1 += str(temp_text, "utf-8").replace("\0", "")
                            maxIndex += len(str(temp_text, "utf-8").replace("\0", ""))
                    is_all_selected = False
                elif i == "left":
                    index = -maxIndex - 1
                    typeBar2 = typeBar1 + typeBar2
                    typeBar1 = ""
                    is_all_selected = False
                    framesUP = 15
                    UpBool = True
                elif i == "right":
                    index = -1
                    typeBar1 += typeBar2
                    typeBar2 = ""
                    is_all_selected = False
                    framesUP = 15
                    UpBool = True
            elif i == "left":
                index -= 1
                if -index > maxIndex + 1:
                    index += 1
                else:
                    typeBar2 = typeBar1[-1] + typeBar2
                    typeBar1 = typeBar1[:-1]
                is_all_selected = False
                framesUP = 15
                UpBool = True
            elif i == "right":
                index += 1
                if index > -1:
                    index -= 1
                else:
                    typeBar1 += typeBar2[0]
                    typeBar2 = typeBar2[1:]
                is_all_selected = False
                framesUP = 15
                UpBool = True
            elif i == "NP_enter":
                if allow_up_down:
                    up_down_content.insert(up_down_index + 1, "")
                    up_down_index += 1
                    up_down_max_index += 1
                    index = -1
                    typeBar1 = ""
                    typeBar2 = ""
            elif i == "del":
                if allow_up_down:
                    if up_down_max_index > 0:
                        up_down_content.pop(up_down_index)
                        up_down_index -= 1
                        up_down_max_index -= 1
                        index = -1
                        typeBar2 = ""
                        typeBar1 = up_down_content[up_down_index]
            elif i == "up":
                if allow_up_down:
                    if up_down_index > 0:
                        up_down_index -= 1
                        print("up")
                    index = -1
                    typeBar2 = ""
                    typeBar1 = up_down_content[up_down_index]
            elif i == "down":
                if allow_up_down:
                    if up_down_index < up_down_max_index:
                        up_down_index += 1
                        print("down")
                    index = -1
                    typeBar2 = ""
                    typeBar1 = up_down_content[up_down_index]

            elif i == "\b":
                typeBar1 = typeBar1[:-1]
                maxIndex -= 1
                if is_all_selected:
                    typeBar1 = ""
                    typeBar2 = ""
                    index = -1
                    maxIndex = 0
                    is_all_selected = False
            else:
                if is_all_selected:
                    typeBar1 = ""
                    typeBar2 = ""
                    index = -1
                    maxIndex = 0
                    is_all_selected = False
                typeBar1 += i
                maxIndex += 1
        typeBar = typeBar1 + typeBar2
        up_down_content[up_down_index] = typeBar
        surfaceUP = font2.render("^", False, (0, 0, 0))
        surface2 = font.render(typeBar1, False, (0, 0, 0))
        surface1 = font.render(typeBar, False, (0, 0, 0), None if not is_all_selected else (80, 80, 255))
        if UpBool:
            win.blit(surfaceUP, (int(typeBarX + surface2.get_rect().width - 5), int(typeBarY + 30)))
        if framesUP <= 0:
            UpBool = not UpBool
            framesUP = 15
        else:
            framesUP -= 1
        win.blit(surface1, (int(typeBarX), int(typeBarY)))

        surface1 = font3.render("{}/ {}".format(up_down_index+1, up_down_max_index+1), False, (0, 0, 0))
        win.blit(surface1, (5, 5))
        surface1 = font3.render("{}".format(len(queue)), False, (0, 0, 0))
        win.blit(surface1, (5, 80))

    if not isinstance(mode, bool):
        if mode == 0:
            if stage == 0:
                surface1 = font.render(queue[0], False, (0, 0, 0))
                win.blit(surface1, (20, int(win_height / 2 - surface1.get_rect().height / 2)))
                pygame.draw.rect(win, (0, 0, 0), (typeBarX - 10, -10, int((in_game_map_x - 50)*5/6), win_height + 20), 1)
            elif stage == 1:
                if keysDown["q"]:
                    try:
                        current_next = next(current_iter)
                    except StopIteration:
                        current(text_types)
                if keysDown["e"]:
                    enter_count = 0
                    win_size(800, 100)
                    isTypeBar = True
                    stage = 0
                    if current_next == "dialog":
                        queue = ["dialog: "]
                        allow_up_down = True
                        separate_and_convert = False

                    elif current_next == "question":
                        queue = ["question: ", "answers: "]
                        allow_up_down = True
                        separate_and_convert = False
                    elif current_next == "command":
                        queue = ["command: "]
                        allow_up_down = True
                        separate_and_convert = True
                    elif current_next == "finish":
                        break
                    current_order.append(current_next)
                surface1 = font.render(current_next, False, (0, 0, 0))
                win.blit(surface1, (int(win_width / 2 - surface1.get_rect().width / 2), int(win_height / 2 - surface1.get_rect().height / 2)))

        elif mode == 1:
            if stage == 0:
                surface1 = font.render(queue[0], False, (0, 0, 0))
                win.blit(surface1, (20, int(win_height / 2 - surface1.get_rect().height / 2)))
            elif stage == 1:
                if keysDown["q"]:
                    try:
                        current_next = next(current_iter)
                    except StopIteration:
                        current(scroll_types)
                if keysDown["e"]:
                    enter_count = 0
                    win_size(800, 100)
                    isTypeBar = True
                    stage = 0
                    if current_next == "new attack":
                        queue = ["name: ", "color: ", "mana cost: ", "attack multiplier: ", "accuracy multiplier: ",
                                 "healing multiplier: ", "rand atk min multiplier: ", "rand atk max multiplier: ",
                                 "rand heal min multiplier: ", "rand heal max multiplier: ", "critical chance: ",
                                 "critical multiplier", "weapon type: ", "sound effect: ", "hitbox: ", "attack type: ",
                                 "attack delay", "attack_animation", "effect name: "]
                    elif current_next == "finish":
                        break
                surface1 = font.render(current_next, False, (0, 0, 0))
                win.blit(surface1, (int(win_width / 2 - surface1.get_rect().width / 2), int(win_height / 2 - surface1.get_rect().height / 2)))

        elif mode == 2:
            try:
                surface1 = font.render(queue[0], False, (0, 0, 0))
            except IndexError:
                break
            win.blit(surface1, (20, int(win_height / 2 - surface1.get_rect().height / 2)))

        elif mode == 3:
            if stage == 0:
                surface1 = font.render(queue[0], False, (0, 0, 0))
                win.blit(surface1, (20, int(win_height / 2 - surface1.get_rect().height / 2)))
            elif stage == 1:
                if keysDown["q"]:
                    try:
                        current_next = next(current_iter)
                    except StopIteration:
                        current(shop_types)
                if keysDown["e"]:
                    enter_count = 0
                    win_size(800, 100)
                    isTypeBar = True
                    stage = 0
                    if current_next == "new item":
                        queue = ["item: ", "cost: ", "stock: ", "commands: "]
                        allow_up_down = False
                        separate_and_convert = False
                    elif current_next == "finish":
                        break
                surface1 = font.render(current_next, False, (0, 0, 0))
                win.blit(surface1, (int(win_width / 2 - surface1.get_rect().width / 2), int(win_height / 2 - surface1.get_rect().height / 2)))

        elif mode == 4:
            if stage == 0:
                surface1 = font.render(queue[0], False, (0, 0, 0))
                win.blit(surface1, (20, int(win_height / 2 - surface1.get_rect().height / 2)))
            elif stage == 1:
                if keysDown["q"]:
                    try:
                        current_next = next(current_iter)
                    except StopIteration:
                        current(loot_table_types)
                if keysDown["e"]:
                    enter_count = 0
                    win_size(800, 100)
                    isTypeBar = True
                    stage = 0
                    if current_next == "new item":
                        queue = ["item name: ", "drop chance: ", "amounts: "]
                        allow_up_down = False
                        separate_and_convert = False
                    elif current_next == "finish":
                        break
                surface1 = font.render(current_next, False, (0, 0, 0))
                win.blit(surface1, (int(win_width / 2 - surface1.get_rect().width / 2), int(win_height / 2 - surface1.get_rect().height / 2)))

    elif mode is False:
        if keysDown["q"]:
            try:
                current_next = next(current_iter)
            except StopIteration:
                current(content)
        if keysDown["e"]:
            mode = current_object.index(current_next)
            if mode == 0:
                win_size(800, 100)
                isTypeBar = True
                queue = ["name: ", "command: "]
            elif mode == 1:
                win_size(800, 100)
                isTypeBar = True
                queue = ["name: ", "desc: "]
            elif mode == 2:
                win_size(800, 100)
                isTypeBar = True
                queue = ["item name: ", "front desc: ", "plural name: ", "long desc: ", "item type: "]
            elif mode == 3:
                win_size(800, 100)
                isTypeBar = True
                queue = ["shop id: "]
            elif mode == 4:
                win_size(800, 100)
                isTypeBar = True
                queue = ["item name: ", "drop chance: ", "amounts: "]
        surface1 = font.render(current_next, False, (0, 0, 0))
        win.blit(surface1, (int(win_width / 2 - surface1.get_rect().width / 2), int(win_height / 2 - surface1.get_rect().height / 2)))

    pygame.display.update()

print(final_inputs)
if run:
    output = []
    if mode == 0:
        try:
            output = [[final_inputs[0][0], *final_inputs[0][1]], []]
        except IndexError:
            output = [[final_inputs[0][0]], []]
        for out in range(1, len(current_order)+1):
            if current_order[out - 1] in ("dialog", "command"):
                output[1].append(final_inputs[out][0])
            else:
                temp_output = [[final_inputs[out][0]]]
                for ans in range(len(final_inputs[out][1])):
                    try:
                        temp_output.append([final_inputs[out][1][ans], *final_inputs[out][ans + 2]])
                    except IndexError:
                        temp_output.append([final_inputs[out][1][ans]])
                output[1].append(tuple(temp_output))
        print(output)
    elif mode == 1:
        output = [final_inputs[0][0], "|".join(final_inputs[0][1]), []]
        for attack in final_inputs[1:]:
            temp_hitbox = -1
            if attack[14] not in ([['']], [["_1"]]):
                temp_hitbox = attack[14]
                for hitbox in range(len(temp_hitbox)):
                    for hitbox2 in range(len(temp_hitbox)):
                        temp_hitbox[hitbox][hitbox2] = int(temp_hitbox[hitbox][hitbox2])
            for color in range(len(attack[1])):
                attack[1][color] = int(attack[1][color])
            temp_effect = -1
            if attack[18] != "none":
                for color in range(len(attack[25])):
                    attack[25][color] = int(attack[25][color])
                temp_effect = [attack[18], attack[19], attack[20], attack[21], attack[22], attack[23], attack[24], tuple(attack[25])]
            temp_output = [attack[0], tuple(attack[1]), int(attack[2]), [float(attack[3]), float(attack[4]), float(attack[5]),
                            [float(attack[6]), float(attack[7])], [float(attack[8]), float(attack[9])], [float(attack[10]), float(attack[11])]],
                           temp_hitbox, temp_effect, int(attack[12]), attack[13], int(attack[15]), int(attack[16]), int(attack[17])]
            output[2].append(temp_output)
        print(output)
    elif mode == 2:
        output = [final_inputs[0][1], final_inputs[0][2], "|".join(final_inputs[0][3]), int(final_inputs[0][4])]
        if int(final_inputs[0][4]) == 0:
            pass
        elif int(final_inputs[0][4]) == 1:
            output += [int(final_inputs[0][5]), int(final_inputs[0][6]), int(final_inputs[0][7]), int(final_inputs[0][8]), final_inputs[0][9]]
        elif int(final_inputs[0][4]) == 2:
            output += [int(final_inputs[0][5]), int(final_inputs[0][6]), float(final_inputs[0][7]), int(final_inputs[0][8]), int(final_inputs[0][9]), int(final_inputs[0][10]), int(final_inputs[0][11]), int(final_inputs[0][12]), [final_inputs[0][13], final_inputs[0][14]]]
        elif int(final_inputs[0][4]) in (3, 4, 5, 7, 8, 9):
            output += [int(final_inputs[0][5]), int(final_inputs[0][6]), float(final_inputs[0][7]), int(final_inputs[0][8]), int(final_inputs[0][9]), int(final_inputs[0][10]), int(final_inputs[0][11]), int(final_inputs[0][12]), [final_inputs[0][13], final_inputs[0][14], final_inputs[0][15]], float(final_inputs[0][16])]
        else:
            output += [int(final_inputs[0][5]), int(final_inputs[0][6]), float(final_inputs[0][7]), int(final_inputs[0][8]), int(final_inputs[0][9]), int(final_inputs[0][10]), int(final_inputs[0][11]), int(final_inputs[0][12]), [final_inputs[0][13], final_inputs[0][14], final_inputs[0][15]]]
        print("'" + final_inputs[0][0] + "': " + str(output))
    elif mode == 3:
        for i in final_inputs[1:]:
            if i[3] == [[""]]:
                output.append([i[0], int(i[1]), int(i[2].replace("_", "-")), []])
            else:
                output.append([i[0], int(i[1]), int(i[2].replace("_", "-")), i[3]])
        print(final_inputs[0][0]+":", output)
    elif mode == 4:
        for i in final_inputs:
            output.append([i[0], float(i[1]), list(int(j) for j in i[2])])
        print(output)

pygame.quit()
quit()
