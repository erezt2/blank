import copy

import pygame, random, math, textures, sounds, battle, error, time
from shapely.geometry import Polygon
from classes import Battle, Game
from data import keysList, mouseDown, keysDown, mouseHeld, keysHeld, mouseUp, keysUp

"""
manual:
front thumb button - create new projectile
rear thumb button - create new hitbox
middle click - create new command
n - create random
while creating:
  numpad - switch to a different mode
  right/ left click - use current mode
  middle click - show created product
  s - save current creation
  q - queue current creation
  esc - stop creating
  space - deploy creation

s - deploy saved creation
p - pop frame
i - show main list
o - show active list
r - edit stats
y - set frame to string
q - reset/ show queue
g - add set of frame to current frame
f - play battle
0 - set frame to 0
"""

pygame.init()
PI = 3.14159265359

# class Battle:
#     class Projectile:
#         projectile_list = []
#         player_rect = None
#
#         def __init__(self, x, y, width, height, degree, velocity, projectile_stats, image="", max_time=-1, attack_modifier=1, accuracy_modifier=0.05, random_multiplier=(0.98, 1.02), effects=("none", "none", "none", "none"), color=(255, 255, 255), spinning=(0.0, 0.0, 0.0, 0.0, 0.0), radian_offset=False):
#             self.x = x
#             self.y = y
#             self.width = width
#             self.height = height
#             self.degree = degree
#             self.velocity = velocity
#             self.projectile_type = projectile_stats[0]  # 0: normal, 1: unvanishing
#             self.projectile_effect = projectile_stats[1]  # 0: normal, 1: poison, 2: wither, 3: poison affected by attack, 4: wither affected by attack, 5: shield piercing poison, 6: shield piercing wither
#             self.projectile_application = projectile_stats[2]  # 0: normal, 1: hurts if moving, 2: hurts if not moving, 3: doesnt hurt
#             self.projectile_effect_damage = projectile_stats[3]
#             self.projectile_effect_length = projectile_stats[4]
#             self.projectile_damage_type = projectile_stats[5]  # 0: normal, 1: shield piercing, 2: uneffected by attack, 3: shield piercing uneffected by attack
#             self._created = effects[0]
#             self._existing = effects[1]
#             self._deleted = effects[2]
#             self._hit = effects[3]
#             self.attack_modifier = attack_modifier
#             self.accuracy_modifier = accuracy_modifier  # closer to 1 means more hits
#             self.random_multiplier = random_multiplier
#             self.hitbox = []
#             if image == "":
#                 self.image = ""
#                 self.color = color
#             else:
#                 self.image = textures.projectiles_list[image]
#                 self.hitbox_rotate = spinning[4]
#             self.__class__.projectile_list.append(self)
#             self.max_frames = max_time
#             self.frames = 0
#             self.rotation = spinning[0]
#             self.spinning_x_offset = spinning[1]
#             self.spinning_y_offset = spinning[2]
#             self.radian_offset = radian_offset
#             self.spinning_dot_rotation = spinning[3]
#             self.created()
#
#         def render_ff(self):
#             self.existing()
#             if Battle.running_battle:
#                 self.y += self.velocity * math.sin(self.degree)
#                 self.x += self.velocity * math.cos(self.degree)
#             temp_offset = (self.spinning_x_offset * math.cos(self.spinning_y_offset), self.spinning_x_offset * math.sin(self.spinning_y_offset)) if self.radian_offset else (self.spinning_x_offset, self.spinning_y_offset)
#             self.hitbox = []
#             rect_radius = math.sqrt(self.height ** 2 + self.width ** 2) / 2
#             try:
#                 rect_angle = math.atan(self.height / self.width)
#             except ZeroDivisionError:
#                 rect_angle = PI / 2
#             if self.image == "":
#                 if self.rotation % (2 * PI) == 0 and self.spinning_dot_rotation % (2 * PI) == 0:
#                     pygame.draw.rect(win, self.color, (int(self.x + temp_offset[0] - self.width / 2 + 305), int(self.y + temp_offset[1] - self.height / 2 + 305), self.width, self.height))
#                     self.hitbox = [(self.x + temp_offset[0] - self.width / 2 + 305, self.y + temp_offset[1] - self.height / 2 + 305), (self.x + temp_offset[0] + self.width / 2 + 305, self.y + temp_offset[1] - self.height / 2 + 305), (self.x + temp_offset[0] + self.width / 2 + 305, self.y + temp_offset[1] + self.height / 2 + 305), (self.x + temp_offset[0] - self.width / 2 + 305, self.y + temp_offset[1] + self.height / 2 + 305)]
#                 elif self.spinning_dot_rotation % (2 * PI) == 0:
#                     for dot in range(4):
#                         temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (
#                             PI if dot in (0, 3) else 0) + self.rotation
#                         self.hitbox.append((int(305 + temp_offset[0] + self.x + rect_radius * math.cos(temp_angle)),
#                                             int(305 + temp_offset[1] + self.y + rect_radius * math.sin(temp_angle))))
#                     pygame.draw.polygon(win, self.color, self.hitbox)
#                 else:
#                     for dot in range(4):
#                         temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (
#                             PI if dot in (0, 3) else 0) + self.rotation
#                         temp2_angle = math.atan2(rect_radius * math.sin(temp_angle) + temp_offset[1], rect_radius * math.cos(temp_angle) + temp_offset[0]) + self.spinning_dot_rotation
#                         temp2_radius = math.sqrt(rect_radius ** 2 + temp_offset[1] ** 2 + temp_offset[0] ** 2 + 2 * rect_radius * (temp_offset[0] * math.cos(temp_angle) + temp_offset[1] * math.sin(temp_angle)))
#                         self.hitbox.append((int(305 + self.x + math.cos(temp2_angle) * temp2_radius), int(305 + self.y + math.sin(temp2_angle) * temp2_radius)))
#                     pygame.draw.polygon(win, self.color, self.hitbox)
#             else:
#                 if self.rotation % (2 * PI) == 0 and self.spinning_dot_rotation % (2 * PI) == 0 and self.hitbox_rotate % (2 * PI) == 0:
#                     win.blit(self.image, (int(self.x + temp_offset[0] + 305 - self.image.get_rect().width / 2), int(self.y + temp_offset[1] + 305 - self.image.get_rect().height / 2)))
#                     self.hitbox = [(self.x + temp_offset[0] - self.width / 2 + 305, self.y + temp_offset[1] - self.height / 2 + 305), (self.x + temp_offset[0] + self.width / 2 + 305, self.y + temp_offset[1] - self.height / 2 + 305), (self.x + temp_offset[0] + self.width / 2 + 305, self.y + temp_offset[1] + self.height / 2 + 305), (self.x + temp_offset[0] - self.width / 2 + 305, self.y + temp_offset[1] + self.height / 2 + 305)]
#                 else:
#                     rotated_image = pygame.transform.rotate(self.image, -1 * (self.rotation + self.spinning_dot_rotation) / PI * 180)
#                     new_rect = rotated_image.get_rect(center=self.image.get_rect(center=(int(self.x + math.sqrt(temp_offset[0] ** 2 + temp_offset[1] ** 2) * math.cos(math.atan2(temp_offset[1], temp_offset[0]) + self.spinning_dot_rotation)), int(self.y + math.sqrt(temp_offset[0] ** 2 + temp_offset[1] ** 2) * math.sin(math.arctan2(temp_offset[1], temp_offset[0]) + self.spinning_dot_rotation)))).center)
#                     win.blit(rotated_image, (int(new_rect.topleft[0] + 305), int(new_rect.topleft[1] + 305)))
#                     for dot in range(4):
#                         temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (PI if dot in (0, 3) else 0) + self.rotation + self.hitbox_rotate
#                         temp2_angle = math.atan2(rect_radius * math.sin(temp_angle) + temp_offset[1], rect_radius * math.cos(temp_angle) + temp_offset[0]) + self.spinning_dot_rotation
#                         temp2_radius = math.sqrt(rect_radius ** 2 + temp_offset[1] ** 2 + temp_offset[0] ** 2 + 2 * rect_radius * (temp_offset[0] * math.cos(temp_angle) + temp_offset[1] * math.sin(temp_angle)))
#                         self.hitbox.append((int(305 + self.x + math.cos(temp2_angle) * temp2_radius), int(305 + self.y + math.sin(temp2_angle) * temp2_radius)))
#                     pygame.draw.polygon(win, (255, 255, 255), self.hitbox, 1)
#
#             if Battle.running_battle:
#                 if self.max_frames != -1 and self.frames >= self.max_frames - 1:
#                     self.deleted()
#                     self.__class__.projectile_list.pop(self.__class__.projectile_list.index(self))
#                 else:
#                     self.frames += 1
#
#         def created(self):
#             if self._created != "none" and Battle.running_battle:
#                 try:
#                     globals()["prc_" + self._created](self)
#                 except KeyError:
#                     pass
#
#         def existing(self):
#             if self._existing != "none" and Battle.running_battle:
#                 try:
#                     globals()["pre_" + self._existing](self)
#                 except KeyError:
#                     pass
#
#         def deleted(self):
#             if self._deleted != "none" and Battle.running_battle:
#                 try:
#                     globals()["prd_" + self._deleted](self)
#                 except KeyError:
#                     pass
#
#     class Hitbox:
#         hitbox_list = []
#         hitbox_rect_list = []
#         color = (255, 255, 255)
#
#         def __init__(self, x, y, width, height, degree, velocity, max_frames=-1, is_full=False, command=("none", "none"), color=None):
#             self.x = x
#             self.y = y
#             self.width = width
#             self.height = height
#             self.degree = degree
#             self.velocity = velocity
#             self.__class__.hitbox_list.append(self)
#             self.frames = 0
#             self.max_frames = max_frames
#             self.is_full = is_full
#             self._exist = command[0]
#             self._touching = command[1]
#             self.color = color
#
#         def render_ff(self):
#             if Battle.running_battle:
#                 self.existing()
#                 self.y += self.velocity * math.sin(self.degree)
#                 self.x += self.velocity * math.cos(self.degree)
#             if self.is_full:
#                 pygame.draw.rect(win, Battle.Hitbox.color if self.color is None else self.color, (int(305 + self.x), int(305 + self.y), self.width, self.height))
#             else:
#                 pygame.draw.rect(win, Battle.Hitbox.color if self.color is None else self.color, (int(305 + self.x), int(305 + self.y), self.width, self.height), 2)
#             if Battle.running_battle:
#                 if self.max_frames != -1 and self.frames >= self.max_frames - 1:
#                     self.__class__.hitbox_list.pop(self.__class__.hitbox_list.index(self))
#                 else:
#                     self.frames += 1
#
#         def existing(self):
#             if self._exist != "none" and Battle.running_battle:
#                 try:
#                     globals()["he_" + self._exist](self)
#                 except KeyError:
#                     pass
#
#     max_battle_frames = 2000
#     current_battle_frame = 0
#     running_battle = False
#     selected_battle = {}
#
#     @staticmethod
#     def dictionary_randomizer(dct, frame_list):
#         pick_repeatedly = list(dct.keys())[0]
#         reorder = list(dct.values())[0]
#         frames_iter = iter([])
#         if isinstance(frame_list, tuple):
#             repeat_count = frame_list[0]
#             frame_list = list(frame_list)[1:]
#             frames_iter = iter(frame_list)
#         else:
#             repeat_count = frame_list
#         dct = dict(list(dct.items())[1:])
#         dct1 = dict(dct)
#         max_total = 0
#         for key in dct1.keys():
#             max_total += key
#         for _ in range(repeat_count):
#             if reorder:
#                 max_total = 0
#                 for key in dct1.keys():
#                     max_total += key
#             rand_val = random.uniform(0, max_total)
#             total = 0
#             for key, value in dct1.items():
#                 total += key
#                 if rand_val <= total:
#                     if isinstance(value, list):
#                         if not pick_repeatedly and reorder:
#                             index = list(dct.keys()).index(key)
#                             for index1 in range(len(value)):
#                                 yield [frame_list[index][index1], value[index1]]
#                         else:
#                             temp_iter = next(frames_iter)
#                             for index in range(len(value)):
#                                 yield [temp_iter[index], value[index]]
#                     else:
#                         if isinstance(frame_list, list):
#                             if not pick_repeatedly and reorder:
#                                 index = list(dct.keys()).index(key)
#                                 yield [frame_list[index], value]
#                             else:
#                                 yield [next(frames_iter), value]
#                         else:
#                             yield value
#                     if pick_repeatedly or reorder:
#                         dct1.pop(key)
#                     break
#
#     @staticmethod
#     def init_battle(battle_dict):
#         Battle.selected_battle = dict()
#         for key, value in battle_dict.items():
#             if isinstance(key, int) or isinstance(key, str):
#                 Battle.add_to_frame(key, value)
#             elif isinstance(key, tuple):
#                 for frame in list(Battle.dictionary_randomizer(value, key)):
#                     if isinstance(frame[0], int):
#                         Battle.add_to_frame(frame[0], frame[1])
#                     elif isinstance(frame[0], tuple):
#                         for frame1 in frame[0]:
#                             Battle.add_to_frame(frame1, frame[1])
#
#     @staticmethod
#     def add_to_frame(key, value):
#         try:
#             if Battle.selected_battle[key]:
#                 pass
#         except KeyError:
#             Battle.selected_battle[key] = value
#         else:
#             if isinstance(Battle.selected_battle[key], tuple):
#                 if isinstance(value, tuple):
#                     Battle.selected_battle[key] = (*Battle.selected_battle[key], *value)
#                 else:
#                     Battle.selected_battle[key] = (*Battle.selected_battle[key], value)
#             else:
#                 if isinstance(value, tuple):
#                     Battle.selected_battle[key] = (Battle.selected_battle[key], *value)
#                 else:
#                     Battle.selected_battle[key] = (Battle.selected_battle[key], value)
#
#     @staticmethod
#     def read_frame(frame=None):
#         try:
#             if frame is None:
#                 frame = Battle.selected_battle[Battle.current_battle_frame]
#             else:
#                 frame = Battle.selected_battle[frame]
#         except KeyError:
#             return 0
#
#         if isinstance(frame, list):
#             try:
#                 globals()["bf_" + frame[0]](*frame[1:])
#             except KeyError:
#                 print("skipped command: "+frame[0])
#
#         elif isinstance(frame, tuple):
#             for frame1 in frame:
#                 Battle.read_frame(frame1)
#
#         elif isinstance(frame, dict):
#             for frame1 in Battle.dictionary_randomizer(list(frame.values())[0], list(frame.keys())[0]):
#                 Battle.read_frame(frame1)
#
#         elif isinstance(frame, set):
#             for frame1 in list(frame):
#                 Battle.read_frame(Battle.selected_battle[frame1])


def proceed_frame():
    Battle.current_battle_frame += 1
    for hitbox in Battle.Hitbox.hitbox_list:
        hitbox.render_ff()
    for projectile in Battle.Projectile.projectile_list:
        projectile.render_ff()
    for hitbox in Battle.Hitbox.hitbox_list:
        hitbox_rect = pygame.Rect(int(hitbox.x + 305), int(hitbox.y + 305), hitbox.width, hitbox.height)
        if not hitbox_rect.colliderect(pygame.Rect(250, 250, 700, 500)):
            hitbox.__class__.hitbox_list.pop(hitbox.__class__.hitbox_list.index(hitbox))
    for projectile in Battle.Projectile.projectile_list:
        if not Polygon.intersects(Polygon(projectile.hitbox), Polygon([(250, 250), (950, 250), (950, 750), (250, 750)])):
            projectile.deleted()
            projectile.__class__.projectile_list.remove(projectile)
    Battle.read_frame()


def main_add_to_frame(key, value):
    global main_battle_dict
    try:
        if main_battle_dict[key]:
            pass
    except KeyError:
        main_battle_dict[key] = value
    else:
        if isinstance(main_battle_dict[key], tuple):
            main_battle_dict[key] = (*main_battle_dict[key], value)
        else:
            main_battle_dict[key] = (main_battle_dict[key], value)


def convert_bool(string):
    return True if string.lower() in ("true", "yes") else False


if True:

    def bf_projectile(*args):
        Battle.Projectile(*args)


    def bf_hitbox(*args):
        Battle.Hitbox(*args)

main_battle_dict = {}
projectiles = []
hitboxes = []
commands = []
random_commands = []
random_commands2 = []
random_commands3 = []
queue = {}

## insert here

projectiles = [[295, 195, 90, 128, 0, 0, [0, 0, 0, 0.0, 0, 0], 'sponge2', -1, 2.2, 0.0, [1.0, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], [566, 264, 90, 128, 0, 0, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], [-49, 362, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False]]
hitboxes = [[-229, 59, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], [-228, 278, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None]]

##

current_addition_list = []
current_addition_mode = 0
current_addition_state = 0
state_1_list = ["x/y", "width/height", "degree/velocity", "x offset/y offset (normal)", "x offset/y offset (radians)", "rotation", "color", "image", "stats", "hitbox rotate"]
state_2_list = ["x/y", "width/height", "degree/velocity", "color", "stats"]
state_3_list = ["change command", "add argument", "string", "int", "float", "bool", "list", "edit list"]
state_4_list = ["change choice number", "multiple choice", "add argument", "edit argument", "edit chance"]
state_6_list = ["change choice number", "multiple choice", "add argument", "edit 1st degree argument", "edit 2st degree argument", "edit chance"]
state_3_list_index = 0
temp_main_list = [""]

b_level = 0
b_name = ""
b_song = ""
b_skip_start = 0
b_skip_end = 0
b_texture_name = ""
b_background = ""
b_hp = 0
b_attack = 0
b_defense = 0
b_evasion = 0
b_accuracy = 0
b_min_exp = 0
b_max_exp = 0
b_max_coins = 0
b_min_coins = 0
b_battle_id = 0

battle_temp_list = 0
if battle_temp_list != 0:
    main_battle_dict = battle_temp_list
    Battle.init_battle(main_battle_dict)
elif convert_bool(input("new: ")):
    try:
        b_level = int(input("foe's level: "))
    except ValueError:
        try:
            Battle.max_battle_frames = int(input("time: "))
        except ValueError:
            Battle.max_battle_frames = 2000
    else:
        b_name = input("foe's name: ")
        b_song = input("song name: ")
        b_skip_start = int(input("song_start_delay: "))
        b_skip_end = int(input("song_end_delay: "))
        b_texture_name = input("texture name: ")
        b_background = input("texture name: ")
        b_hp = int(input("foe's hp: "))
        b_attack = int(input("foe's attack: "))
        b_defense = int(input("foe's defense: "))
        b_evasion = int(input("foe's evasion: "))
        b_accuracy = int(input("foe's accuracy: "))
        b_min_exp = int(input("min exp: "))
        b_max_exp = int(input("max exp: "))
        b_min_coins = int(input("min coins: "))
        b_max_coins = int(input("max coins: "))
        b_battle_id = int(input("battle id: "))
        #Battle.max_battle_frames = int(sounds.get_song_len(b_song) * 30 - b_skip_start - b_skip_end)
        Battle.max_battle_frames = b_skip_end - b_skip_start
else:
    enemy_battle_id = int(input("battle id: "))
    main_battle_dict = battle.enemies_list[enemy_battle_id][0]
    b_battle_id = int(enemy_battle_id)
    b_level = battle.enemies_list[enemy_battle_id][5][5]
    b_name = battle.enemies_list[enemy_battle_id][1]
    b_song = battle.enemies_list[enemy_battle_id][2]
    b_skip_start = battle.enemies_list[enemy_battle_id][3][0]
    b_skip_end = battle.enemies_list[enemy_battle_id][3][1]
    b_texture_name = input("texture name: ")
    b_background = input("texture name: ")
    b_hp = battle.enemies_list[enemy_battle_id][5][0]
    b_attack = battle.enemies_list[enemy_battle_id][5][1]
    b_defense = battle.enemies_list[enemy_battle_id][5][2]
    b_evasion = battle.enemies_list[enemy_battle_id][5][3]
    b_accuracy = battle.enemies_list[enemy_battle_id][5][4]
    b_min_exp = battle.enemies_list[enemy_battle_id][7][0]
    b_max_exp = battle.enemies_list[enemy_battle_id][7][1]
    b_min_coins = battle.enemies_list[enemy_battle_id][7][2]
    b_max_coins = battle.enemies_list[enemy_battle_id][7][3]
    Battle.init_battle(main_battle_dict)
    #Battle.max_battle_frames = int(sounds.get_song_len(b_song) * 30 - b_skip_start - b_skip_end)
    Battle.max_battle_frames = b_skip_end - b_skip_start

clock = pygame.time.Clock()
win_width = 1200
win_height = 1000
win = pygame.display.set_mode((win_width, win_height))

temp_velocity = 0
rect_middle = [0, 0]

mouse_pos = (0, 0)
last_click = (0, 0)
run = True
Battle.running_battle = False
try:
    while run:
        if Game.delta < 1:
            Game.current_time = time.time()
            Game.delta += (Game.current_time - Game.last_time) * Game.ticks_per_second
            Game.last_time = float(Game.current_time)
        if time.time() - Game.time_start > 1:
            Game.time_start += 1
            # print(Game.frame)
            Game.frame = 0

        if Game.delta > 5:
            Game.delta = 5
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
                    for _key in keysList:
                        if event.key == keysList[_key]:
                            keysDown[_key] = True
                            keysHeld[_key] = True

                if event.type == pygame.KEYUP:
                    for _key in keysList:
                        if event.key == keysList[_key]:
                            keysUp[_key] = True
                            keysHeld[_key] = False
        if keysHeld["shift"]:
            mouse_pos = (pygame.mouse.get_pos()[0], mouse_pos[1])
        elif keysHeld["ctrl"]:
            mouse_pos = (mouse_pos[0], pygame.mouse.get_pos()[1])
        else:
            mouse_pos = pygame.mouse.get_pos()
        if mouseDown[1]:
            last_click = tuple(mouse_pos)
        ####################################################
        if mouseDown[1] and mouse_pos[1] >= win_height - 20 or keysDown["left"] or keysDown["up"] or keysDown["down"] or keysDown["right"] or mouseDown[4] or mouseDown[5]:
            if isinstance(Battle.current_battle_frame, str):
                Battle.init_battle(main_battle_dict)
                Battle.current_battle_frame = -1
                Battle.Hitbox.hitbox_list = []
                Battle.Projectile.projectile_list = []
                proceed_frame()
            Battle.running_battle = True
            temp_frame = int(Battle.max_battle_frames * mouse_pos[0] / win_width)
            if keysDown["left"]:
                temp_frame = Battle.current_battle_frame - 1
                if temp_frame < 0:
                    temp_frame = 0
            elif keysDown["up"]:
                temp_frame = Battle.current_battle_frame - 10
                if temp_frame < 0:
                    temp_frame = 0
            elif keysDown["right"]:
                temp_frame = Battle.current_battle_frame + 1
                if temp_frame >= Battle.max_battle_frames:
                    temp_frame = Battle.max_battle_frames - 1
            elif keysDown["down"]:
                temp_frame = Battle.current_battle_frame + 10
                if temp_frame >= Battle.max_battle_frames:
                    temp_frame = Battle.max_battle_frames - 1
            elif mouseDown[5]:
                temp_frame = Battle.current_battle_frame - 5
                if temp_frame < 0:
                    temp_frame = 0
            elif mouseDown[4]:
                temp_frame = Battle.current_battle_frame + 5
                if temp_frame >= Battle.max_battle_frames:
                    temp_frame = Battle.max_battle_frames - 5

            if temp_frame >= Battle.current_battle_frame:
                for i in range(temp_frame - Battle.current_battle_frame):
                    proceed_frame()
            else:
                Battle.init_battle(main_battle_dict)
                Battle.current_battle_frame = -1
                Battle.Hitbox.hitbox_list = []
                Battle.Projectile.projectile_list = []
                for i in range(temp_frame + 1):
                    proceed_frame()
            Battle.running_battle = False
            win.fill((0, 0, 0))

        if Battle.running_battle:
            Battle.read_frame()
        for _hitbox in Battle.Hitbox.hitbox_list:
            _hitbox.render_ff()
        for _projectile in Battle.Projectile.projectile_list:
            _projectile.render_ff()

        if keysDown["f"]:
            if isinstance(Battle.current_battle_frame, str):
                Battle.init_battle(main_battle_dict)
                Battle.current_battle_frame = -1
                Battle.Hitbox.hitbox_list = []
                Battle.Projectile.projectile_list = []
                proceed_frame()
            Battle.running_battle = not Battle.running_battle
            if Battle.running_battle:
                try:
                    sounds.play(b_song, False, delay_ms=(Battle.current_battle_frame + b_skip_start) / 27.3*1000, loops=1)
                except error.SoundError:
                    pass
            else:
                sounds.play("none")
        elif keysDown["0"]:
            Battle.init_battle(main_battle_dict)
            Battle.current_battle_frame = -1
            Battle.Hitbox.hitbox_list = []
            Battle.Projectile.projectile_list = []
            proceed_frame()
        if Battle.running_battle:
            Battle.current_battle_frame += 1
            if Battle.current_battle_frame >= Battle.max_battle_frames:
                Battle.current_battle_frame -= 1
                Battle.running_battle = False
                sounds.play("none")

        if current_addition_mode != 0:
            try:
                for i in range(10):
                    if keysDown["num" + str(i)]:
                        current_addition_state = i
                        if current_addition_mode == 1:
                            print(state_1_list[i])
                        elif current_addition_mode == 2:
                            print(state_2_list[i])
                        elif current_addition_mode == 3:
                            print(state_3_list[i])
                        elif current_addition_mode in (4, 5):
                            print(state_4_list[i])
                        elif current_addition_mode == 6:
                            print(state_6_list[i])
            except IndexError:
                print("invalid index")

            if current_addition_mode == 1:
                _temp_offset = (current_addition_list[14][1] * math.cos(current_addition_list[14][2]), current_addition_list[14][1] * math.sin(current_addition_list[14][2])) if current_addition_list[15] else (current_addition_list[14][1], current_addition_list[14][2])
                _temp_polygon = []
                _rect_radius = math.sqrt(current_addition_list[3] ** 2 + current_addition_list[2] ** 2) / 2
                try:
                    _rect_angle = math.atan(current_addition_list[3] / current_addition_list[2])
                except ZeroDivisionError:
                    _rect_angle = PI / 2
                if current_addition_list[7] == "":
                    for _dot in range(4):
                        _temp_angle = (1 if _dot % 2 == 0 else -1) * _rect_angle + (PI if _dot >= 2 else 0) + current_addition_list[14][0]
                        _temp_polygon.append((int(305 + current_addition_list[0] + math.cos(math.atan2(_rect_radius * math.sin(_temp_angle) + _temp_offset[1], _rect_radius * math.cos(_temp_angle) + _temp_offset[0]) + current_addition_list[14][3]) * math.sqrt(_rect_radius ** 2 + _temp_offset[1] ** 2 + _temp_offset[0] ** 2 + 2 * _rect_radius * (_temp_offset[0] * math.cos(_temp_angle) + _temp_offset[1] * math.sin(_temp_angle)))),
                                                int(305 + current_addition_list[1] + math.sin(math.atan2(_rect_radius * math.sin(_temp_angle) + _temp_offset[1], _rect_radius * math.cos(_temp_angle) + _temp_offset[0]) + current_addition_list[14][3]) * math.sqrt(_rect_radius ** 2 + _temp_offset[1] ** 2 + _temp_offset[0] ** 2 + 2 * _rect_radius * (_temp_offset[0] * math.cos(_temp_angle) + _temp_offset[1] * math.sin(_temp_angle))))))
                    pygame.draw.polygon(win, current_addition_list[13], _temp_polygon)
                    rect_middle = [(_temp_polygon[0][0] + _temp_polygon[2][0]) / 2, (_temp_polygon[0][1] + _temp_polygon[2][1]) / 2]
                else:
                    _temp_image = textures.projectiles_list[current_addition_list[7]].convert_alpha()
                    _rotated_image = pygame.transform.rotate(_temp_image, -1 * (current_addition_list[14][0] + current_addition_list[14][3]) / PI * 180)
                    _new_rect = _rotated_image.get_rect(center=_temp_image.get_rect(center=(int(current_addition_list[0]+math.sqrt(_temp_offset[0]**2+_temp_offset[1]**2)*math.cos(math.atan2(_temp_offset[1], _temp_offset[0])+current_addition_list[14][3])), int(current_addition_list[1]+math.sqrt(_temp_offset[1]**2+_temp_offset[0]**2)*math.sin(math.atan2(_temp_offset[1], _temp_offset[0])+current_addition_list[14][3])))).center)
                    win.blit(_rotated_image, (int(_new_rect.topleft[0] + 305), int(_new_rect.topleft[1] + 305)))
                    for _dot in range(4):
                        _temp_angle = (1 if _dot % 2 == 0 else -1) * _rect_angle + (PI if _dot >= 2 else 0) + current_addition_list[14][0] + current_addition_list[14][4]
                        _temp_polygon.append((int(305 + current_addition_list[0] + math.cos(math.atan2(_rect_radius*math.sin(_temp_angle)+_temp_offset[1], _rect_radius*math.cos(_temp_angle)+_temp_offset[0])+current_addition_list[14][3])*math.sqrt(_rect_radius**2+_temp_offset[1]**2+_temp_offset[0]**2+2*_rect_radius*(_temp_offset[0]*math.cos(_temp_angle)+_temp_offset[1]*math.sin(_temp_angle)))),
                                                int(305 + current_addition_list[1] + math.sin(math.atan2(_rect_radius*math.sin(_temp_angle)+_temp_offset[1], _rect_radius*math.cos(_temp_angle)+_temp_offset[0])+current_addition_list[14][3])*math.sqrt(_rect_radius**2+_temp_offset[1]**2+_temp_offset[0]**2+2*_rect_radius*(_temp_offset[0]*math.cos(_temp_angle)+_temp_offset[1]*math.sin(_temp_angle))))))
                    pygame.draw.polygon(win, (255, 255, 255), _temp_polygon, 2)
                pygame.draw.circle(win, (255, 0, 0), (int(current_addition_list[0] + 305), int(current_addition_list[1] + 305)), 2)
                pygame.draw.line(win, (200, 20, 20), (int(current_addition_list[0] + 305), int(current_addition_list[1] + 305)), (int(current_addition_list[0] + 305 + temp_velocity * math.cos(current_addition_list[4])), int(current_addition_list[1] + 305 + temp_velocity * math.sin(current_addition_list[4]))), 2)

                if mouseHeld[1] and mouse_pos[1] < win_height - 20:
                    if current_addition_state == 0:
                        current_addition_list[0] = mouse_pos[0] - 305
                        current_addition_list[1] = mouse_pos[1] - 305
                    elif current_addition_state == 1:
                        current_addition_list[2] = abs(current_addition_list[0] - mouse_pos[0] + 305) * 2
                        current_addition_list[3] = abs(current_addition_list[1] - mouse_pos[1] + 305) * 2
                        if keysHeld["z"]:
                            current_addition_list[2] = int(current_addition_list[3])
                    elif current_addition_state == 2:
                        if not keysHeld["v"]:
                            temp_velocity = int(math.sqrt((mouse_pos[0] - current_addition_list[0] - 305) ** 2 + (mouse_pos[1] - current_addition_list[1] - 305) ** 2))
                        if not keysHeld["c"]:
                            current_addition_list[4] = math.atan2(mouse_pos[1] - current_addition_list[1] - 305, mouse_pos[0] - current_addition_list[0] - 305)
                        if keysHeld["z"]:
                            current_addition_list[4] *= 4/PI
                            current_addition_list[4] = int(round(current_addition_list[4]))
                            current_addition_list[4] *= PI/4
                        if keysHeld["x"]:
                            temp_velocity /= 24
                            temp_velocity = int(round(temp_velocity))
                            temp_velocity *= 24
                        current_addition_list[5] = int(temp_velocity / 5)
                    elif current_addition_state == 3:
                        current_addition_list[15] = False
                        current_addition_list[14][1] = mouse_pos[0] - current_addition_list[0] - 305
                        current_addition_list[14][2] = mouse_pos[1] - current_addition_list[1] - 305
                    elif current_addition_state == 4:
                        current_addition_list[15] = True
                        if not keysHeld["x"]:
                            current_addition_list[14][1] = math.sqrt((mouse_pos[0] - current_addition_list[0] - 305) ** 2 + (mouse_pos[1] - current_addition_list[1] - 305) ** 2)
                        if not keysHeld["c"]:
                            current_addition_list[14][2] = math.atan2(mouse_pos[1] - current_addition_list[1] - 305, mouse_pos[0] - current_addition_list[0] - 305)
                        if keysHeld["z"]:
                            current_addition_list[14][2] *= 4/PI
                            current_addition_list[14][2] = int(round(current_addition_list[14][2]))
                            current_addition_list[14][2] *= PI/4
                    elif current_addition_state == 5:
                        if not keysHeld["x"]:
                            current_addition_list[14][0] = math.atan2(mouse_pos[1] - rect_middle[1], mouse_pos[0] - rect_middle[0])
                            if keysHeld["z"]:
                                current_addition_list[14][0] *= 4/PI
                                current_addition_list[14][0] = int(round(current_addition_list[14][0]))
                                current_addition_list[14][0] *= PI/4
                        else:
                            current_addition_list[14][3] = math.atan2(mouse_pos[1] - current_addition_list[1] - 305, mouse_pos[0] - current_addition_list[0] - 305)
                            if keysHeld["z"]:
                                current_addition_list[14][3] *= 4 / PI
                                current_addition_list[14][3] = int(round(current_addition_list[14][3]))
                                current_addition_list[14][3] *= PI / 4
                    elif current_addition_state == 6:
                        current_addition_list[13] = [int(input("red: ")), int(input("green: ")), int(input("blue: "))]
                    elif current_addition_state == 7:
                        current_addition_list[7] = input("texture: ")
                    elif current_addition_state == 8:
                        current_addition_list[6] = [int(input("type: ")), int(input("poison type: ")), int(input("application: ")), float(input("damage: ")), int(input("poison ticks: ")), int(input("attack calculation: "))]
                        current_addition_list[8] = int(input("max time: "))
                        current_addition_list[9] = float(input("attack modifier: "))
                        current_addition_list[10] = float(input("acurracy modifier: "))
                        current_addition_list[11] = [float(input("minimum random multiplier: ")), float(input("minimum random multiplier: "))]
                        current_addition_list[12] = [input("add effect: "), input("exist effect: "), input("remove effect: "), input("hit effect: ")]
                    elif current_addition_state == 9:
                        current_addition_list[14][4] = math.atan2(mouse_pos[1] - current_addition_list[1] - 305, mouse_pos[0] - current_addition_list[0] - 305)
                        if keysHeld["z"]:
                            current_addition_list[14][4] *= 4 / PI
                            current_addition_list[14][4] = int(round(current_addition_list[14][4]))
                            current_addition_list[14][4] *= PI / 4

                elif mouseDown[3]:
                    if current_addition_state in (3, 4):
                        current_addition_list[14][1] = 0
                        current_addition_list[14][2] = 0
                    elif current_addition_state == 2:
                        current_addition_list[4] = 0
                        current_addition_list[5] = 0
                        temp_velocity = 0
                    elif current_addition_state == 0:
                        current_addition_list[0] = 295
                        current_addition_list[1] = 195
                    elif current_addition_state == 5:
                        if not keysHeld["x"]:
                            current_addition_list[14][0] = 0
                        else:
                            current_addition_list[14][3] = 0
                    elif current_addition_state == 6:
                        current_addition_list[13] = [255, 255, 255]
                    elif current_addition_state == 7:
                        current_addition_list[7] = ""
                    elif current_addition_state == 8:
                        print(current_addition_list)
                    elif current_addition_state == 9:
                        current_addition_list[14][4] = 0

                elif mouseDown[2]:
                    print({i: current_addition_list[i] for i in range(len(current_addition_list))})
                    print("edit: ")
                    temp_edit = int(input("index: "))
                    if temp_edit in (0, 1, 2, 3, 5, 6, 8, 13):
                        temp_class = int
                    elif temp_edit in (7, 12):
                        temp_class = str
                    elif temp_edit in (4, 9, 10, 11, 14):
                        temp_class = float
                    else:
                        temp_class = convert_bool
                    if isinstance(current_addition_list[temp_edit], list):
                        for i in current_addition_list[temp_edit]:
                            current_addition_list[temp_edit][i] = temp_class(input("value: "))
                    else:
                        temp_input = input("value: ")
                        current_addition_list[temp_edit] = temp_class(temp_input)
                        if temp_edit == 5:
                            temp_velocity = int(temp_input) * 5

            elif current_addition_mode == 2:
                if current_addition_list[7]:
                    pygame.draw.rect(win, [255, 255, 255] if current_addition_list[9] is None else current_addition_list[9], (305 + current_addition_list[0], 305 + current_addition_list[1], current_addition_list[2], current_addition_list[3]))
                else:
                    pygame.draw.rect(win, [255, 255, 255] if current_addition_list[9] is None else current_addition_list[9], (305 + current_addition_list[0], 305 + current_addition_list[1], current_addition_list[2], current_addition_list[3]), 2)
                pygame.draw.circle(win, (255, 0, 0), (int(current_addition_list[0] + 305 + current_addition_list[2] / 2), int(current_addition_list[1] + 305 + current_addition_list[3] / 2)), 2)
                pygame.draw.line(win, (200, 20, 20), (int(current_addition_list[0] + 305 + current_addition_list[2] / 2), int(current_addition_list[1] + 305 + current_addition_list[3] / 2)), (int(current_addition_list[0] + 305 + temp_velocity * math.cos(current_addition_list[4]) + current_addition_list[2] / 2), int(current_addition_list[1] + 305 + temp_velocity * math.sin(current_addition_list[4]) + current_addition_list[3] / 2)), 2)

                if mouseHeld[1] and mouse_pos[1] < win_height - 20:
                    if current_addition_state == 0:
                        current_addition_list[0] = int(mouse_pos[0] - 305 - current_addition_list[2] / 2)
                        current_addition_list[1] = int(mouse_pos[1] - 305 - current_addition_list[3] / 2)
                    elif current_addition_state == 1:
                        temp_width = int(current_addition_list[2])
                        temp_height = int(current_addition_list[3])
                        current_addition_list[2] = abs(current_addition_list[0] + int(current_addition_list[2] / 2) - mouse_pos[0] + 305) * 2
                        current_addition_list[3] = abs(current_addition_list[1] + int(current_addition_list[3] / 2) - mouse_pos[1] + 305) * 2
                        current_addition_list[0] -= int((current_addition_list[2] - temp_width) / 2)
                        current_addition_list[1] -= int((current_addition_list[3] - temp_height) / 2)
                        if keysHeld["z"]:
                            current_addition_list[2] = int(current_addition_list[3])
                    elif current_addition_state == 2:
                        if not keysHeld["v"]:
                            temp_velocity = int(math.sqrt((mouse_pos[0] - current_addition_list[0] - 305 - current_addition_list[2] / 2) ** 2 + (mouse_pos[1] - current_addition_list[1] - 305 - current_addition_list[3] / 2) ** 2))
                        if not keysHeld["c"]:
                            current_addition_list[4] = math.atan2(mouse_pos[1] - current_addition_list[1] - 305 - current_addition_list[3] / 2, mouse_pos[0] - current_addition_list[0] - 305 - current_addition_list[2] / 2)
                        if keysHeld["z"]:
                            current_addition_list[4] *= 4/PI
                            current_addition_list[4] = int(round(current_addition_list[4]))
                            current_addition_list[4] *= PI/4
                        if keysHeld["x"]:
                            temp_velocity /= 24
                            temp_velocity = int(round(temp_velocity))
                            temp_velocity *= 24
                        current_addition_list[5] = int(temp_velocity / 5)
                    elif current_addition_state == 3:
                        current_addition_list[9] = [int(input("red: ")), int(input("green: ")), int(input("blue: "))]
                    elif current_addition_state == 4:
                        current_addition_list[6] = int(input("duration: "))
                        current_addition_list[7] = convert_bool(input("is full? "))
                        current_addition_list[8] = [input("exist effect: "), input("touch effect: ")]

                elif mouseDown[3]:
                    if current_addition_state == 0:
                        current_addition_list[0] = 295
                        current_addition_list[1] = 195
                    elif current_addition_state == 2:
                        current_addition_list[4] = 0
                        current_addition_list[5] = 0
                        temp_velocity = 0
                    elif current_addition_state == 3:
                        current_addition_list[9] = None
                    elif current_addition_state == 4:
                        current_addition_list[6] = -1
                        current_addition_list[7] = False
                        current_addition_list[8] = ["none", "none"]

                elif mouseDown[2]:
                    print({i: current_addition_list[i] for i in range(len(current_addition_list))})
                    print("edit: ")
                    temp_edit = int(input("index: "))
                    if temp_edit in (0, 1, 2, 3, 5, 6):
                        temp_input = input("value: ")
                        current_addition_list[temp_edit] = int(temp_input)
                        if temp_edit == 5:
                            temp_velocity = int(temp_input) * 5
                    elif temp_edit == 4:
                        current_addition_list[4] = float(input("value: "))
                    elif temp_edit == 7:
                        current_addition_list[7] = convert_bool(input("value: "))
                    elif temp_edit == 8:
                        current_addition_list[8] = [input("value: "), input("value: ")]
                    elif temp_edit == 9:
                        try:
                            current_addition_list[9] = [int(input("value: ")), int(input("value: ")), int(input("value: "))]
                        except ValueError:
                            current_addition_list[9] = None

            elif current_addition_mode == 3:
                if mouseDown[1] and mouse_pos[1] < win_height - 20:
                    if state_3_list_index == 0:
                        temp_main_list = current_addition_list
                        temp_main_number = 1
                    else:
                        temp_main_list = current_addition_list[state_3_list_index]
                        temp_main_number = 0
                    if current_addition_state == 0:
                        current_addition_list[0] = input("command name: ")
                    elif current_addition_state == 1:
                        temp_main_list.append("")
                        print("added arg")
                    elif current_addition_state == 2:
                        print({i: temp_main_list[i+temp_main_number] for i in range(len(temp_main_list)-temp_main_number)})
                        temp_input = int(input("index: "))
                        temp_main_list[temp_input+temp_main_number] = input("value: ")
                    elif current_addition_state == 3:
                        print({i: temp_main_list[i+temp_main_number] for i in range(len(temp_main_list)-temp_main_number)})
                        temp_input = int(input("index: "))
                        temp_main_list[temp_input+temp_main_number] = int(input("value: "))
                    elif current_addition_state == 4:
                        print({i: temp_main_list[i+temp_main_number] for i in range(len(temp_main_list)-temp_main_number)})
                        temp_input = int(input("index: "))
                        temp_main_list[temp_input+temp_main_number] = float(input("value: "))
                    elif current_addition_state == 5:
                        print({i: temp_main_list[i+temp_main_number] for i in range(len(temp_main_list)-temp_main_number)})
                        temp_input = int(input("index: "))
                        temp_main_list[temp_input+temp_main_number] = convert_bool(input("value: "))
                    elif current_addition_state == 6 and temp_main_number == 1:
                        print({i: current_addition_list[i+1] for i in range(len(current_addition_list)-1)})
                        temp_input = input("index: ")
                        current_addition_list[int(temp_input)+1] = [""]
                        state_3_list_index = int(temp_input) + 1
                    elif current_addition_state == 7:
                        print({i: current_addition_list[i] for i in range(len(current_addition_list) - 1) if isinstance(current_addition_list[i], list)})
                        state_3_list_index = int(input("index: "))

                elif mouseDown[3]:
                    if state_3_list_index == 0:
                        temp_main_list = current_addition_list
                    else:
                        temp_main_list = current_addition_list[state_3_list_index]
                    if current_addition_state == 0:
                        print(current_addition_list)
                    elif current_addition_state == 1:
                        if len(temp_main_list) >= 2:
                            temp_main_list.pop(-1)
                    else:
                        state_3_list_index = 0

            elif current_addition_mode == 4:
                if mouseDown[1] and mouse_pos[1] < win_height - 20:
                    if current_addition_state == 0:
                        current_addition_list[0] = int(input("number of rolls: "))
                    elif current_addition_state == 1:
                        current_addition_list[1][0] = not current_addition_list[1][0]
                        if current_addition_list[1] == [False, True]:
                            current_addition_list[1] = [False, False]
                        print(current_addition_list[1])
                    elif current_addition_state == 2:
                        temp_input = float(input("insert chance: "))
                        if temp_input in (1, 0) or any(temp_input == i[0] for i in current_addition_list[2:]):
                            print("cant use this chance")
                        else:
                            for i in queue:
                                print(i + ": " + str(queue[i]))
                            for i in list(j for j in main_battle_dict.keys() if isinstance(j, str)):
                                print("/" + i + ": " + str(main_battle_dict[i]))
                            temp_list = []
                            temp_input2 = input("insert key: ")
                            while temp_input2 != "":
                                temp_list.append(temp_input2)
                                temp_input2 = input("insert key: ")
                            temp_list2 = []
                            for i in temp_list:
                                if i[0] == "/":
                                    temp_list2.append({i[1:]})
                                else:
                                    temp_list2.append(queue[i])
                            current_addition_list.append([temp_input, tuple(temp_list2)])
                    elif current_addition_state == 3:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        temp_input = int(input("insert index: ")) + 2
                        for i in queue:
                            print(i + ": " + str(queue[i]))
                        for i in list(j for j in main_battle_dict.keys() if isinstance(j, str)):
                            print("/" + i + ": " + str(main_battle_dict[i]))
                        temp_input2 = input("insert command: ")
                        if temp_input2[0] == "/":
                            current_addition_list[temp_input][1] = (*current_addition_list[temp_input][1], {temp_input2[1:]})
                        else:
                            current_addition_list[temp_input][1] = (*current_addition_list[temp_input][1], queue[temp_input2])
                    elif current_addition_state == 4:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        temp_input = int(input("insert index: ")) + 2
                        temp_input2 = float(input("insert chance: "))
                        if temp_input2 in (1, 0) or any(temp_input2 == i[0] for i in current_addition_list[2:]):
                            print("cant use this chance")
                        else:
                            current_addition_list[temp_input][0] = float(temp_input2)

                elif mouseDown[3]:
                    if current_addition_state == 0:
                        print(current_addition_list[0])
                    elif current_addition_state == 1:
                        current_addition_list[1][1] = not current_addition_list[1][1]
                        if current_addition_list[1] == [False, True]:
                            current_addition_list[1] = [True, True]
                        print(current_addition_list[1])
                    elif current_addition_state == 2:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        current_addition_list.pop(int(input("pop index: "))+2)
                    elif current_addition_state == 3:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        temp_input = int(input("insert index: ")) + 2
                        for i in range(len(current_addition_list[temp_input][1])):
                            print(str(i) + ": " + str(current_addition_list[temp_input][1][i]))
                        temp_list = list(current_addition_list[temp_input][1])
                        temp_list.pop(int(input("pop index: ")))
                        current_addition_list[temp_input][1] = tuple(temp_list)
                    elif current_addition_state == 4:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2]))
                        temp_input = int(input("switch index 1: ")) + 2
                        temp_input2 = int(input("switch index 2: ")) + 2
                        current_addition_list[temp_input], current_addition_list[temp_input2] = current_addition_list[temp_input2], current_addition_list[temp_input]

                elif mouseDown[2]:
                    print(str(current_addition_list[0]), str(current_addition_list[1]))
                    for i in range(len(current_addition_list[2:])):
                        print(str(i) + ": " + str(current_addition_list[i + 2]))

            elif current_addition_mode == 5:
                if mouseDown[1] and mouse_pos[1] < win_height - 20:
                    if current_addition_state == 0:
                        temp_list = [int(input("number of rolls: "))]
                        try:
                            while True:
                                temp_list2 = [int(i) for i in input("execution frame: ").split(",")]
                                if len(temp_list2) == 1:
                                    temp_list.append(int(temp_list2[0]))
                                else:
                                    temp_list.append(tuple(temp_list2))
                        except ValueError:
                            current_addition_list[0] = tuple(temp_list)
                    elif current_addition_state == 1:
                        current_addition_list[1][0] = not current_addition_list[1][0]
                        print(current_addition_list[1])
                    elif current_addition_state == 2:
                        temp_input = float(input("insert chance: "))
                        if temp_input in (1, 0) or any(temp_input == i[0] for i in current_addition_list[2:]):
                            print("cant use this chance")
                        else:
                            for i in queue:
                                print(i + ": " + str(queue[i]))
                            for i in list(j for j in main_battle_dict.keys() if isinstance(j, str)):
                                print("/" + i + ": " + str(main_battle_dict[i]))
                            temp_list = []
                            temp_input2 = input("insert key: ")
                            while temp_input2 != "":
                                temp_list.append(temp_input2)
                                temp_input2 = input("insert key: ")
                            temp_list2 = []
                            for i in temp_list:
                                if i[0] == "/":
                                    temp_list2.append({i[1:]})
                                else:
                                    temp_list2.append(queue[i])
                            current_addition_list.append([temp_input, tuple(temp_list2)])
                    elif current_addition_state == 3:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        temp_input = int(input("insert index: ")) + 2
                        for i in range(len(current_addition_list[temp_input][1])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        try:
                            temp_input3 = int(input("insert index: "))
                        except ValueError:
                            temp_input3 = len(current_addition_list[temp_input][1])
                        for i in queue:
                            print(i + ": " + str(queue[i]))
                        for i in list(j for j in main_battle_dict.keys() if isinstance(j, str)):
                            print("/" + i + ": " + str(main_battle_dict[i]))
                        temp_input2 = input("insert command: ")
                        temp_list = list(current_addition_list[temp_input][1])
                        if temp_input2[0] == "/":
                            temp_list.insert(temp_input3, {temp_input2[1:]})
                        else:
                            temp_list.insert(temp_input3, queue[temp_input2])
                        current_addition_list[temp_input][1] = tuple(temp_list)
                    elif current_addition_state == 4:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        temp_input = int(input("insert index: ")) + 2
                        temp_input2 = float(input("insert chance: "))
                        if temp_input2 in (1, 0) or any(temp_input2 == i[0] for i in current_addition_list[2:]):
                            print("cant use this chance")
                        else:
                            current_addition_list[temp_input][0] = float(temp_input2)

                elif mouseDown[3]:
                    if current_addition_state == 0:
                        print(current_addition_list[0])
                    elif current_addition_state == 1:
                        current_addition_list[1][1] = not current_addition_list[1][1]
                        print(current_addition_list[1])
                    elif current_addition_state == 2:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        current_addition_list.pop(int(input("pop index: "))+2)
                    elif current_addition_state == 3:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i)+": "+str(current_addition_list[i+2]))
                        temp_input = int(input("insert index: ")) + 2
                        for i in range(len(current_addition_list[temp_input][1])):
                            print(str(i) + ": " + str(current_addition_list[temp_input][1][i]))
                        temp_list = list(current_addition_list[temp_input][1])
                        temp_list.pop(int(input("pop index: ")))
                        current_addition_list[temp_input][1] = tuple(temp_list)
                    elif current_addition_state == 4:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2]))
                        temp_input = int(input("switch index 1: ")) + 2
                        temp_input2 = int(input("switch index 2: ")) + 2
                        current_addition_list[temp_input], current_addition_list[temp_input2] = current_addition_list[temp_input2], current_addition_list[temp_input]

                elif mouseDown[2]:
                    print(str(current_addition_list[0]), str(current_addition_list[1]))
                    for i in range(len(current_addition_list[2:])):
                        print(str(i) + ": " + str(current_addition_list[i + 2]))

            elif current_addition_mode == 6:
                if mouseDown[1] and mouse_pos[1] < win_height - 20:
                    if current_addition_state == 0:
                        temp_list = [int(input("number of rolls: "))]
                        try:
                            while True:
                                print("new frame: ")
                                temp_list3 = [int(i) for i in input("execution frame: ").split(",")]
                                if len(temp_list3) == 1:
                                    temp_list2 = [int(temp_list3[0])]
                                else:
                                    temp_list2 = [tuple(temp_list3)]
                                try:
                                    while True:
                                        temp_list3 = [int(i) for i in input("execution frame: ").split(",")]
                                        if len(temp_list3) == 1:
                                            temp_list2.append(int(temp_list3[0]))
                                        else:
                                            temp_list2.append(tuple(temp_list3))
                                except ValueError:
                                    temp_list.append(tuple(temp_list2))
                        except ValueError:
                            current_addition_list[0] = tuple(temp_list)
                    elif current_addition_state == 1:
                        current_addition_list[1][0] = not current_addition_list[1][0]
                        print(current_addition_list[1])
                    elif current_addition_state == 2:
                        temp_input = float(input("insert chance: "))
                        if temp_input in (1, 0) or any(temp_input == i[0] for i in current_addition_list[2:]):
                            print("cant use this chance")
                        else:
                            for i in queue:
                                print(i + ": " + str(queue[i]))
                            for i in list(j for j in main_battle_dict.keys() if isinstance(j, str)):
                                print("/" + i + ": " + str(main_battle_dict[i]))
                            temp_list3 = []
                            temp_list = []
                            temp_input2 = input("insert key: ")
                            while temp_input2 != "":
                                temp_list.append(temp_input2)
                                temp_input2 = input("insert key: ")
                            temp_list2 = []
                            for i in temp_list:
                                if i[0] == "/":
                                    temp_list2.append({i[1:]})
                                else:
                                    temp_list2.append(queue[i])
                            while temp_list2:
                                print("new frame")
                                temp_list3.append(tuple(temp_list2))
                                temp_list = []
                                temp_input2 = input("insert key: ")
                                while temp_input2 != "":
                                    temp_list.append(temp_input2)
                                    temp_input2 = input("insert key: ")
                                temp_list2 = []
                                for i in temp_list:
                                    if i[0] == "/":
                                        temp_list2.append({i[1:]})
                                    else:
                                        temp_list2.append(queue[i])
                            current_addition_list.append([temp_input, list(temp_list3)])
                    elif current_addition_state == 3:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2][0]))
                            for j in range(len(current_addition_list[i + 2][1])):
                                print(current_addition_list[i + 2][1][j])
                        temp_input = int(input("insert index: ")) + 2
                        for i in range(len(current_addition_list[temp_input][1])):
                            print(str(i)+": "+str(current_addition_list[temp_input][1][i]))
                        try:
                            temp_input3 = int(input("insert index: "))
                        except ValueError:
                            temp_input3 = len(current_addition_list[temp_input][1])
                        for i in queue:
                            print(i + ": " + str(queue[i]))
                        for i in list(j for j in main_battle_dict.keys() if isinstance(j, str)):
                            print("/" + i + ": " + str(main_battle_dict[i]))
                        temp_list3 = list(current_addition_list[temp_input][1])
                        temp_list = []
                        temp_input2 = input("insert keys: ")
                        while temp_input2 != "":
                            temp_list.append(temp_input2)
                            temp_input2 = input("insert key: ")
                        temp_list2 = []
                        for i in temp_list:
                            if i[0] == "/":
                                temp_list2.append({i[1:]})
                            else:
                                temp_list2.append(queue[i])
                        temp_list3.insert(temp_input3, tuple(temp_list2))
                        current_addition_list[temp_input][1] = list(temp_list3)
                    elif current_addition_state == 4:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2][0]))
                            for j in range(len(current_addition_list[i + 2][1])):
                                print(current_addition_list[i + 2][1][j])
                        temp_input = int(input("insert index: ")) + 2
                        for i in range(len(current_addition_list[temp_input][1])):
                            print(str(i) + ": " + str(current_addition_list[temp_input][1][i]))
                        temp_input2 = int(input("insert index: "))
                        for i in range(len(current_addition_list[temp_input][1][temp_input2])):
                            print(str(i) + ": " + str(current_addition_list[temp_input][1][temp_input2][i]))
                        try:
                            temp_input4 = int(input("insert index: "))
                        except ValueError:
                            temp_input4 = len(current_addition_list[temp_input][1][temp_input2])
                        for i in queue:
                            print(i + ": " + str(queue[i]))
                        for i in list(j for j in main_battle_dict.keys() if isinstance(j, str)):
                            print("/" + i + ": " + str(main_battle_dict[i]))
                        temp_input3 = input("insert command: ")
                        temp_list = list(current_addition_list[temp_input][1][temp_input2])
                        if temp_input3[0] == "/":
                            temp_list.insert(temp_input4, {temp_input3[1:]})
                        else:
                            temp_list.insert(temp_input4, queue[temp_input3])
                        current_addition_list[temp_input][1][temp_input2] = tuple(temp_list)
                    elif current_addition_state == 5:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2][0]))
                            for j in range(len(current_addition_list[i + 2][1])):
                                print(current_addition_list[i + 2][1][j])
                        temp_input = int(input("insert index: ")) + 2
                        temp_input2 = float(input("insert chance: "))
                        if temp_input2 in (1, 0) or any(temp_input2 == i[0] for i in current_addition_list[2:]):
                            print("cant use this chance")
                        else:
                            current_addition_list[temp_input][0] = float(temp_input2)

                elif mouseDown[3]:
                    if current_addition_state == 0:
                        print(current_addition_list[0])
                    elif current_addition_state == 1:
                        current_addition_list[1][1] = not current_addition_list[1][1]
                        print(current_addition_list[1])
                    elif current_addition_state == 2:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2][0]))
                            for j in range(len(current_addition_list[i + 2][1])):
                                print(current_addition_list[i + 2][1][j])
                        current_addition_list.pop(int(input("pop index: "))+2)
                    elif current_addition_state == 3:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2][0]))
                            for j in range(len(current_addition_list[i + 2][1])):
                                print(current_addition_list[i + 2][1][j])
                        temp_input = int(input("insert index: ")) + 2
                        for i in range(len(current_addition_list[temp_input][1])):
                            print(str(i) + ": " + str(current_addition_list[temp_input][1][i]))
                        current_addition_list[temp_input][1].pop(int(input("pop index: ")))
                    elif current_addition_state == 4:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2][0]))
                            for j in range(len(current_addition_list[i + 2][1])):
                                print(current_addition_list[i + 2][1][j])
                        temp_input = int(input("insert index: ")) + 2
                        for i in range(len(current_addition_list[temp_input][1])):
                            print(str(i)+": "+str(current_addition_list[temp_input][1][i]))
                        temp_input2 = int(input("insert index: "))
                        for i in range(len(current_addition_list[temp_input][1][temp_input2])):
                            print(str(i)+": "+str(current_addition_list[temp_input][1][temp_input2][i]))
                        temp_input3 = int(input("pop index: "))
                        temp_list = list(current_addition_list[temp_input][1][temp_input2])
                        temp_list.pop(temp_input3)
                        current_addition_list[temp_input][1][temp_input2] = tuple(temp_list)
                    elif current_addition_state == 5:
                        for i in range(len(current_addition_list[2:])):
                            print(str(i) + ": " + str(current_addition_list[i + 2]))
                        temp_input = int(input("switch index 1: ")) + 2
                        temp_input2 = int(input("switch index 2: ")) + 2
                        current_addition_list[temp_input], current_addition_list[temp_input2] = current_addition_list[temp_input2], current_addition_list[temp_input]

                elif mouseDown[2]:
                    print(str(current_addition_list[0]), str(current_addition_list[1]))
                    for i in range(len(current_addition_list[2:])):
                        print(str(i) + ": " + str(current_addition_list[i + 2][0]))
                        for j in range(len(current_addition_list[i + 2][1])):
                            print(current_addition_list[i + 2][1][j])

            if keysDown["space"]:
                if current_addition_mode == 1:
                    Battle.Projectile(*current_addition_list)
                    main_add_to_frame(Battle.current_battle_frame, ["projectile", *current_addition_list])
                elif current_addition_mode == 2:
                    Battle.Hitbox(*current_addition_list)
                    main_add_to_frame(Battle.current_battle_frame, ["hitbox", *current_addition_list])
                elif current_addition_mode == 3:
                    main_add_to_frame(Battle.current_battle_frame, list(current_addition_list))
                elif current_addition_mode == 4:
                    Battle.read_frame({current_addition_list[0]: dict(current_addition_list[1:])})
                    main_add_to_frame(Battle.current_battle_frame, {current_addition_list[0]: dict(current_addition_list[1:])})
                elif current_addition_mode in (5, 6):
                    temp_frame = int(Battle.current_battle_frame)
                    Battle.running_battle = True
                    main_add_to_frame(current_addition_list[0], dict(current_addition_list[1:]))
                    Battle.init_battle(main_battle_dict)
                    Battle.current_battle_frame = -1
                    Battle.Hitbox.hitbox_list = []
                    Battle.Projectile.projectile_list = []
                    for i in range(temp_frame + 1):
                        proceed_frame()
                    Battle.running_battle = False

                current_addition_mode = 0

            elif keysDown["s"]:
                if current_addition_mode == 1:
                    projectiles.append(list(current_addition_list))
                elif current_addition_mode == 2:
                    hitboxes.append(list(current_addition_list))
                elif current_addition_mode == 3:
                    commands.append(list(current_addition_list))
                elif current_addition_mode == 4:
                    random_commands.append(list(current_addition_list))
                elif current_addition_mode == 5:
                    random_commands2.append(list(current_addition_list))
                elif current_addition_mode == 6:
                    random_commands3.append(list(current_addition_list))
                print("saved!")

            elif keysDown["q"]:
                print(list(queue.keys()))
                if current_addition_mode == 1:
                    queue[input("name: ")] = ["projectile", *current_addition_list]
                elif current_addition_mode == 2:
                    queue[input("name: ")] = ["hitbox", *current_addition_list]
                elif current_addition_mode == 3:
                    queue[input("name: ")] = list(current_addition_list)
                elif current_addition_mode == 4:
                    queue[input("name: ")] = {current_addition_list[0]: dict(current_addition_list[1:])}
                print("queued!")

            elif keysDown["esc"]:
                current_addition_mode = 0

        elif mouseDown[7]:
            print("projectile")
            current_addition_mode = 1
            current_addition_list = [295, 195, 20, 20, 0, 0, [0, 0, 0, 0, 0, 0], "", -1, 1, 0.05, [0.98, 1.02], ["none", "none", "none", "none"], [255, 255, 255], [0, 0, 0, 0, 0], False]
            temp_velocity = 0
            current_addition_state = 0
            rect_middle = [295, 195]

        elif mouseDown[6]:
            print("hitbox")
            current_addition_mode = 2
            current_addition_list = [295, 195, 80, 20, 0, 0, -1, False, ["none", "none"], None]
            current_addition_state = 0
            temp_velocity = 0

        elif mouseDown[2]:
            print("command")
            current_addition_mode = 3
            current_addition_list = [""]
            temp_main_list = [""]
            current_addition_state = 0
            rect_middle = [295, 195]

        elif keysDown["s"]:
            temp_input = int(input("addition mode: "))
            if temp_input == 1:
                for i in range(len(projectiles)):
                    print(str(i) + ": " + str(projectiles[i]))
                try:
                    current_addition_list = copy.deepcopy(projectiles[int(input("index: "))])
                    current_addition_mode = 1
                    temp_velocity = int(current_addition_list[5] * 5)
                    current_addition_state = 0
                    rect_middle = [295, 195]
                except KeyError:
                    pass
            elif temp_input == 2:
                for i in range(len(hitboxes)):
                    print(str(i) + ": " + str(hitboxes[i]))
                try:
                    current_addition_list = copy.deepcopy(hitboxes[int(input("index: "))])
                    current_addition_mode = 2
                    temp_velocity = int(current_addition_list[5] * 5)
                    current_addition_state = 0
                except KeyError:
                    pass
            elif temp_input == 3:
                for i in range(len(commands)):
                    print(str(i) + ": " + str(commands[i]))
                try:
                    current_addition_list = copy.deepcopy(commands[int(input("index: "))])
                    current_addition_mode = 3
                    current_addition_state = 0
                    state_3_list_index = 0
                except KeyError:
                    pass
            elif temp_input == 4:
                for i in range(len(random_commands)):
                    print(str(i) + ": " + str(random_commands[i]))
                try:
                    current_addition_list = copy.deepcopy(random_commands[int(input("index: "))])
                    current_addition_mode = 4
                except KeyError:
                    pass
            elif temp_input == 5:
                for i in range(len(random_commands2)):
                    print(str(i) + ": " + str(random_commands2[i]))
                try:
                    current_addition_list = copy.deepcopy(random_commands2[int(input("index: "))])
                    current_addition_mode = 5
                except KeyError:
                    pass
            elif temp_input == 6:
                for i in range(len(random_commands3)):
                    print(str(i) + ": " + str(random_commands3[i]))
                try:
                    current_addition_list = copy.deepcopy(random_commands3[int(input("index: "))])
                    current_addition_mode = 6
                except KeyError:
                    pass

        elif keysDown["p"]:
            print("pop frame: ")
            for i in main_battle_dict:
                print(str(i) + ": " + str(main_battle_dict[i]))
            try:
                temp_input = input("frame: ")
                if temp_input.lower() == "tuple":
                    temp_tuple_list = list(i for i in list(main_battle_dict) if isinstance(i, tuple))
                    for i in range(len(temp_tuple_list)):
                        print(str(i)+": "+str(temp_tuple_list[i]))
                    main_battle_dict.pop(temp_tuple_list[int(input("pop frame: "))])
                elif temp_input[0] == "/":
                    main_battle_dict.pop(temp_input[1:])
                else:
                    main_battle_dict.pop(int(temp_input))
            except KeyError:
                pass

        elif keysDown["i"]:
            for i in main_battle_dict:
                print(str(i) + ": " + str(main_battle_dict[i]))

        elif keysDown["o"]:
            for i in Battle.selected_battle:
                print(str(i) + ": " + str(Battle.selected_battle[i]))

        elif keysDown["r"]:
            b_name = input("foe's name ({}): ".format(b_name))
            b_song = input("song name ({}): ".format(b_song))
            b_skip_start = int(input("song_start_delay ({}): ".format(str(b_skip_start))))
            b_skip_end = int(input("song_end_delay ({}): ".format(str(b_skip_end))))
            b_texture_name = input("texture name ({}): ".format(str(b_texture_name)))
            b_background = input("background name ({}): ".format(str(b_background)))
            b_hp = int(input("foe's hp ({}): ".format(str(b_hp))))
            b_attack = int(input("foe's attack ({}): ".format(str(b_attack))))
            b_defense = int(input("foe's defense ({}): ".format(str(b_defense))))
            b_evasion = int(input("foe's evasion ({}): ".format(str(b_evasion))))
            b_accuracy = int(input("foe's accuracy ({}): ".format(str(b_accuracy))))
            b_level = int(input("foe's level ({}): ".format(str(b_level))))
            b_min_exp = int(input("min exp ({}): ".format(str(b_min_exp))))
            b_max_exp = int(input("max exp ({}): ".format(str(b_max_exp))))
            b_min_coins = int(input("min coins ({}): ".format(str(b_min_coins))))
            b_max_coins = int(input("max coins ({}): ".format(str(b_max_coins))))
            b_battle_id = int(input("battle id ({}): ".format(str(b_battle_id))))
            Battle.max_battle_frames = int(sounds.song_length[b_song] * 30 - b_skip_start - b_skip_end)

        elif keysDown["n"]:
            current_addition_state = 0
            if convert_bool(input("is interframe? ")):
                if convert_bool(input("singular event? ")):
                    current_addition_list = [(1, 0), [False, False]]
                    current_addition_mode = 5
                else:
                    current_addition_list = [(1, (0, 1)), [False, False]]
                    current_addition_mode = 6
            else:
                current_addition_list = [0, [False, False]]
                current_addition_mode = 4

        elif keysDown["y"]:
            Battle.current_battle_frame = input("set frame string: ")

        elif keysDown["q"]:
            if convert_bool(input("reset queue? ")):
                queue = {}
            else:
                for i in queue:
                    print(i + ": " + str(queue[i]))

        elif keysDown["g"]:
            for i in list(j for j in main_battle_dict.keys() if isinstance(j, int)):
                print(str(i) + ": " + str(main_battle_dict[i]))
            for i in list(j for j in main_battle_dict.keys() if isinstance(j, str)):
                print(i + ": " + str(main_battle_dict[i]))
            temp_set = set()
            try:
                while True:
                    temp_input = input("insert key: ")
                    if temp_input[0] == ".":
                        temp_input = int(temp_input[1:])
                    temp_set.add(temp_input)
            except IndexError:
                pass
            main_add_to_frame(Battle.current_battle_frame, temp_set)

        elif keysDown["l"]:
            print(Battle.selected_battle)

        win.blit(pygame.font.SysFont("Aharoni", 24).render(str(Battle.current_battle_frame), False, (255, 255, 255)), (5, win_height - 40))
        pygame.draw.rect(win, (255, 255, 255), (300, 300, 600, 400), 9)
        pygame.draw.rect(win, (60, 60, 60), (0, win_height - 20, win_width, 20))
        for h in range(1, 8):
            pygame.draw.line(win, (200, 200, 200), (int(h * win_width / 8), win_height - 20), (int(h * win_width / 8), win_height), 2)
        try:
            pygame.draw.line(win, (80, 80, 255), (int(Battle.current_battle_frame / (Battle.max_battle_frames - 1) * win_width), win_height - 20), (int(Battle.current_battle_frame / (Battle.max_battle_frames - 1) * win_width), win_height), 4)
        except TypeError:
            pygame.draw.rect(win, (150, 60, 60), (0, win_height - 20, win_width, 20))
        ####################################################
        pygame.draw.circle(win, (150, 150, 150), last_click, 2, 1)
        pygame.draw.circle(win, (150, 150, 150), mouse_pos, 2, 1)
        pygame.draw.rect(win, (150, 150, 150), (250, 250, 700, 500), 1)
        ####################################################
        pygame.display.update()
except Exception as error:
    print(main_battle_dict)
    print(f"""{projectiles = }
{hitboxes = }
{commands = }
{random_commands = }
{random_commands2 = }
{random_commands3 = }
{queue = }""")
    raise error
else:
    print(main_battle_dict)
    print("{}:".format(str(b_battle_id)), str(["var name here", b_name, b_song, [b_skip_start, b_skip_end], b_texture_name, [b_hp, b_attack, b_defense, b_evasion, b_accuracy, b_level], "loot table", [b_min_exp, b_max_exp, b_min_coins, b_max_coins], b_background]).replace('\'"', '').replace('"\'', ''))
    print(f"""{projectiles = }
{hitboxes = }
{commands = }
{random_commands = }
{random_commands2 = }
{random_commands3 = }
{queue = }""")