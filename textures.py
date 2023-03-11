import pygame, error, os, re

none = pygame.image.load("resources/none.png")

## entities
#  player
player_directory = "resources/entities/player/"
player_change1 = [(3, 0), (2, 0), (3, 0), (1, 0), (0, 0), (-2, 0), (0, 0), (1, 0), (2, 0)]
player_change2 = [(-2, 0), (-2, 0), (-2, 0), (-1, 0), (-2, 0), (-2, 0), (-2, 0), (-2, 0), (-2, 0)]
player_change3 = [(2, 0), (0, 0), (2, 0), (2, 0), (2, 0), (1, 0), (2, 0), (2, 0), (2, 0)]
player_change4 = [(-2, 0), (-2, 0), (-2, 0), (-2, 0), (-2, 0), (-2, 0), (-2, 0), (-1, 0), (-2, 0)]
player = {
    "right": [[pygame.image.load(player_directory + "right" + str(i+1) + ".png"), player_change1[i]] for i in range(9)],
    "down": [[pygame.image.load(player_directory + "down" + str(i+1) + ".png"), player_change2[i]] for i in range(9)],
    "left": [[pygame.image.load(player_directory + "left" + str(i+1) + ".png"), player_change3[i]] for i in range(9)],
    "up": [[pygame.image.load(player_directory + "up" + str(i+1) + ".png"), player_change4[i]] for i in range(9)],
}

player_sprite_down = pygame.image.load("resources/battle/sprite/sprite_down.png")
player_sprite_left = pygame.image.load("resources/battle/sprite/sprite_left.png")
player_sprite_up = pygame.image.load("resources/battle/sprite/sprite_up.png")
player_sprite_right = pygame.image.load("resources/battle/sprite/sprite_right.png")
player_pre_sprite = pygame.image.load("resources/entities/player/down1.png")


## other
#  inventory
accessory_unequip = pygame.image.load("resources/other/menu/accessory.png")
accessory_equip = pygame.image.load("resources/other/menu/accessory_equip.png")
bow_unequip = pygame.image.load("resources/other/menu/bow.png")
bow_equip = pygame.image.load("resources/other/menu/bow_equip.png")
chestplate_unequip = pygame.image.load("resources/other/menu/chestplate.png")
chestplate_equip = pygame.image.load("resources/other/menu/chestplate_equip.png")
helmet_unequip = pygame.image.load("resources/other/menu/helmet.png")
helmet_equip = pygame.image.load("resources/other/menu/helmet_equip.png")
leggings_unequip = pygame.image.load("resources/other/menu/leggings.png")
leggings_equip = pygame.image.load("resources/other/menu/leggings_equip.png")
relic_unequip = pygame.image.load("resources/other/menu/relic.png")
relic_equip = pygame.image.load("resources/other/menu/relic_equip.png")
staff_unequip = pygame.image.load("resources/other/menu/staff.png")
staff_equip = pygame.image.load("resources/other/menu/staff_equip.png")
sword_unequip = pygame.image.load("resources/other/menu/sword.png")
sword_equip = pygame.image.load("resources/other/menu/sword_equip.png")
talisman_unequip = pygame.image.load("resources/other/menu/talisman.png")
talisman_equip = pygame.image.load("resources/other/menu/talisman_equip.png")

small_inventory_icons = [
    pygame.image.load("resources/other/menu/small_cosmetic.png"),
    pygame.image.load("resources/other/menu/small_consume.png"),
    pygame.image.load("resources/other/menu/small_perm.png"),
    pygame.image.load("resources/other/menu/small_helmet.png"),
    pygame.image.load("resources/other/menu/small_chestplate.png"),
    pygame.image.load("resources/other/menu/small_leggings.png"),
    pygame.image.load("resources/other/menu/small_accessory.png"),
    pygame.image.load("resources/other/menu/small_sword.png"),
    pygame.image.load("resources/other/menu/small_bow.png"),
    pygame.image.load("resources/other/menu/small_staff.png"),
    pygame.image.load("resources/other/menu/small_talisman.png"),
    pygame.image.load("resources/other/menu/small_relic.png"),
]

#  scrolls and scripts
scroll_unequip = pygame.image.load("resources/other/menu/scroll.png")
scroll_equip = pygame.image.load("resources/other/menu/scroll_equip.png")
scroll_select = pygame.image.load("resources/other/menu/scroll_select.png")

script_unequip = pygame.image.load("resources/other/menu/script.png")
script_equip = pygame.image.load("resources/other/menu/script_equip.png")
script_select = pygame.image.load("resources/other/menu/script_select.png")

#  missions
mission_normal = pygame.image.load("resources/other/menu/mission_normal.png")
mission_main = pygame.image.load("resources/other/menu/mission_main.png")
mission_progress = pygame.image.load("resources/other/menu/mission_progress.png")
mission_finished = pygame.image.load("resources/other/menu/mission_finished.png")
mission_claimable = pygame.image.load("resources/other/menu/mission_claimable.png")


#  in battle

projectiles_list = {}
for file in os.listdir("resources\\battle\\projectiles"):
    projectiles_list[file[:file.find(".")]] = pygame.image.load(os.path.join("resources\\battle\\projectiles", file))

map_blocks = {"empty": none}
c = -1
for folder in os.listdir("resources\\blocks"):
    map_blocks[c] = folder
    path = os.path.join("resources\\blocks", folder)
    for file in os.listdir(path):
        if file[:file.find(".")] in map_blocks:
            error.error(error.CodeError, 1)
        map_blocks[file[:file.find(".")]] = pygame.image.load(os.path.join(path, file))
    c += 1

misc_textures = {}
for file in os.listdir("resources\\other\\misc"):
    misc_textures[file[:file.find(".")]] = pygame.image.load(os.path.join("resources\\other\\misc", file))

# battle
# file structure:
# enemy_name ->
#   *animation-group_animation-frame_offset-x_offset-y.png
# or *animation-group_last-frame_return-to-default
# or profile (50x50 pixels)


def get_wrapped_arg(string, position):
    return re.match(rf"^([^_.]+_){{{position}}}(?P<num>[^_.]+)", string).group("num")


def get_wrapped_num(string):
    return sum(1 for i in string if i == "_") + 1


def tuple_sum(*args):
    if len(set([len(i) for i in args if i is not None])) != 1:
        raise TypeError("length of tuples is different")
    res = list(args[0])
    for arg in args[1:]:
        if arg is None:
            continue
        for i in range(len(arg)):
            res[i] += arg[i]
    return res


def open_texture(string, flip_x=False, size=None):
    temp = pygame.image.load(string)
    if size is not None:
        size = (round(size * temp.get_width()), round(size * temp.get_height()))
        temp = pygame.transform.scale(temp, size)
    if flip_x:
        temp = pygame.transform.flip(temp, flip_x, False)
    return temp


def choose_num_type(value):
    if "." in value:
        return float(value)
    return int(value)


def get_from_dict(_dict, key):
    if _dict is None:
        return None
    if key in _dict:
        return _dict[key]
    return None


def multiply(*args):
    res = 1
    for num in args:
        if num is not None:
            res *= num
    return res


battle_bosses = {}
for file in os.listdir("resources\\battle\\bosses"):
    battle_bosses[file[:file.find(".")]] = pygame.image.load(os.path.join("resources\\battle\\bosses", file))

battle_enemies = {}
for files in os.listdir("resources\\battle\\enemies"):
    _temp_groups = []
    _temp_list = {}
    root = os.path.join("resources\\battle\\enemies", files)
    _temp_list["profile"] = pygame.image.load(os.path.join(root, "profile.png"))

    _f = open(os.path.join(root, "settings.txt"), "r")
    lines = _f.readlines()
    _f.close()
    tags = []

    for line in lines:
        line = line.replace("\n", "").split(" ")
        if len(line) == 0:
            pass
        elif len(line) == 1:
            tags.append(line[0])
        elif line[1] == "@":
            _temp_dict = {}
            i = 2
            while i < len(line):
                _temp_dict[int(line[i])] = choose_num_type(line[i + 1])
                i += 2
            _temp_list[line[0]] = _temp_dict
        elif len(line) == 2:
            _temp_list[line[0]] = choose_num_type(line[1])
        else:
            _temp_list[line[0]] = tuple(choose_num_type(arg) for arg in line[1:])
    _temp_list["tags"] = tags

    for file in filter(lambda x: "." not in x, os.listdir(root)):
        group_num = int(get_wrapped_arg(file, 0))
        _temp_list[group_num] = {}

        frame_jump = 0
        folder_pos = (0, 0)
        if get_wrapped_num(file) == 2:
            frame_jump = int(get_wrapped_arg(file, 1))
        elif get_wrapped_num(file) == 3:
            folder_pos = tuple(int(get_wrapped_arg(file, i+1)) for i in range(2))
        elif get_wrapped_num(file) == 4:
            folder_pos = tuple(int(get_wrapped_arg(file, i+2)) for i in range(2))
            frame_jump = int(get_wrapped_arg(file, 1))

        pic_dir = os.path.join(root, file)
        ordered = list(sorted(os.listdir(pic_dir), key=lambda x: get_wrapped_arg(x, 0)))
        current_frame = 0
        for picture in ordered:
            temp_frame_jump = 0
            temp_folder_pos = (0, 0)
            if get_wrapped_num(picture) == 2:
                temp_frame_jump = int(get_wrapped_arg(picture, 1))
            elif get_wrapped_num(picture) == 3:
                temp_folder_pos = tuple(int(get_wrapped_arg(picture, i + 1)) for i in range(2))
            elif get_wrapped_num(picture) == 4:
                temp_folder_pos = tuple(int(get_wrapped_arg(picture, i + 2)) for i in range(2))
                temp_frame_jump = int(get_wrapped_arg(picture, 1))
            _temp_list[group_num][current_frame] = [open_texture(os.path.join(pic_dir, picture), "flip" in _temp_list["tags"],
                                                    multiply(get_from_dict(_temp_list, "scale"), get_from_dict(get_from_dict(_temp_list, "scaleSub"), group_num))),
                                                    tuple_sum(folder_pos, temp_folder_pos, get_from_dict(_temp_list, "move"))]
            current_frame += frame_jump + temp_frame_jump
        _temp_list[group_num][current_frame] = True
        # if file.endswith('txt'):
        #     _temp_list[_temp_info[0]][_temp_info[1]] = bool(int(re.match(rf"^([^_\.]+_){{{2}}}(?P<num>[^_.]+)", file).group("num")))
        # else:
        #     pos = tuple(int(re.match(rf"^([^_\.]+_){{{i}}}(?P<num>[^_.]+)", file).group("num")) for i in range(2, 4))
        #     _temp_list[_temp_info[0]][_temp_info[1]] = [pygame.image.load(os.path.join(root, file)), pos]
    battle_enemies[files] = _temp_list

battle_animations = {}
for animation in os.listdir("resources\\battle\\animations"):
    _temp_groups = []
    _temp_list = {}
    root = os.path.join("resources\\battle\\animations", animation)

    _f = open(os.path.join(root, "settings.txt"), "r")
    lines = _f.readlines()
    _f.close()
    tags = []

    for line in lines:
        line = line.replace("\n", "").split(" ")
        if len(line) == 1:
            tags.append(line[0])
        elif len(line) == 2:
            _temp_list[line[0]] = choose_num_type(line[1])
        else:
            _temp_list[line[0]] = tuple(choose_num_type(arg) for arg in line[1:])
    _temp_list["tags"] = tags

    frame_jump = 0
    folder_pos = (0, 0)
    if get_wrapped_num(animation) == 2:
        frame_jump = int(get_wrapped_arg(animation, 1))
    elif get_wrapped_num(animation) == 3:
        folder_pos = tuple(int(get_wrapped_arg(animation, i + 1)) for i in range(2))
    elif get_wrapped_num(animation) == 4:
        folder_pos = tuple(int(get_wrapped_arg(animation, i + 2)) for i in range(2))
        frame_jump = int(get_wrapped_arg(animation, 1))

    ordered = list(sorted(filter(lambda x: x.endswith("png"), os.listdir(root)), key=lambda x: get_wrapped_arg(x, 0), reverse=("reverse" in _temp_list["tags"])))
    current_frame = 0
    for picture in ordered:
        temp_frame_jump = 0
        temp_folder_pos = (0, 0)
        if get_wrapped_num(picture) == 2:
            temp_frame_jump = int(get_wrapped_arg(picture, 1))
        elif get_wrapped_num(picture) == 3:
            temp_folder_pos = tuple(int(get_wrapped_arg(picture, i + 1)) for i in range(2))
        elif get_wrapped_num(picture) == 4:
            temp_folder_pos = tuple(int(get_wrapped_arg(picture, i + 2)) for i in range(2))
            temp_frame_jump = int(get_wrapped_arg(picture, 1))

        _temp_list[current_frame] = [
            open_texture(os.path.join(root, picture), "flip" in _temp_list["tags"],
                         get_from_dict(_temp_list, "scale")),
            tuple_sum(folder_pos, temp_folder_pos, get_from_dict(_temp_list, "move"))]
        current_frame += frame_jump + temp_frame_jump
    _temp_list[current_frame] = True

    battle_animations[get_wrapped_arg(animation, 0)] = _temp_list

battle_background = {"none": none}
for file in os.listdir("resources\\battle\\background"):
    battle_background[file[:file.find(".")]] = pygame.image.load(os.path.join("resources\\battle\\background", file))

#  cut scene / entities
entities = {
    "none": none,
}
for file in os.listdir("resources\\entities\\entities"):
    entities[file[:file.find(".")]] = pygame.image.load(os.path.join("resources\\entities/entities", file))

cutscene_entities = {
    "tree_pos1": pygame.image.load("resources/blocks/nature/tree1.png"),
    "player_left1": pygame.image.load("resources/entities/player/left1.png"),
    "player_right1": pygame.image.load("resources/entities/player/right1.png"),
}
for file in os.listdir("resources\\cutscene"):
    entities[file[:file.find(".")]] = pygame.image.load(os.path.join("resources\\cutscene", file))
# for i in entities:
#     if i in cutscene_entities:
#         error.error(error.CodeError, 1)

# main menu
menu_bg = pygame.image.load("resources/menu/bg.png")

tutorial_list = []
tutorial_dict = {}
for root, subs, files in os.walk("resources\\tutorial"):
    if root.endswith("tutorial"):
        continue
    _temp_list = []
    _temp = sorted(files)
    for file in _temp:
        _temp_list.append(pygame.image.load(os.path.join(root, file)))

    tutorial_list.append(root)
    tutorial_dict[root[root.rfind("_")+1:]] = _temp_list

tutorial_list.sort()
tutorial_list = [root[root.rfind("_")+1:] for root in tutorial_list]
