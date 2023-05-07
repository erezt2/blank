import copy
import random, math, pickle, os, time, importlib
import pygame
from shapely.geometry import Polygon
import maps, error, texts, textures, sounds, battle, cutscene, turns  # turns
from data import *


# a class used for pointer or encapsulation problems
class Temp:
    func = None
    is_defaulted_func = True
    func_args = []
    settings = None


def save_func(func=None, cap=-1):

    def inner_decorator(function):
        if func is None:
            _func = function.__name__
        elif isinstance(func, str):
            _func = func
        else:
            _func = func.__name__

        def wrapper(*args, **kwargs):
            if not Menu.reloading:
                if args:
                    Ins.ap.add_reload_func([_func, *args], cap)
                else:
                    Ins.ap.add_reload_func(_func, cap)
            return function(*args, **kwargs)
        return wrapper

    return inner_decorator


def remove_func(func=None, count=-1):
    def inner_decorator(function):
        if func is None:
            raise ValueError("remove func doesnt accept None as an argument (only string/function)")
        elif isinstance(func, str):
            _func = func
        else:
            _func = func.__name__

        def wrapper(*args, **kwargs):
            if not Menu.reloading:
                Ins.ap.remove_reload_func(_func, count)
            return function(*args, **kwargs)
        return wrapper
    return inner_decorator


def reset_data():
    items["sigil of permission"][0] = "lvl 1"


if True:
    def min_max(_min, value, _max):
        if value < _min:
            return _min
        if _max < value:
            return _max
        return value

    def floated_int(value):
        if int(value) == value:
            return int(value)
        return value


class Settings:
    def __init__(self):
        self.musicVolume = 40
        self.effectVolume = 40

        self.showUnsellableItems = False
        self.allowAutoSaves = True
        self.showClaimedMissions = False

        self.move_right = "d"
        self.move_down = "s"
        self.move_left = "a"
        self.move_up = "w"
        self.interact = "e"
        self.other_function = "q"
        self.sprint = "shift"

        self.battle_func1 = "1"
        self.battle_func2 = "2"
        self.battle_func3 = "3"
        self.battle_switch_menu = "q"
        self.battle_confirm = "e"

        self.screen_width = 13
        self.screen_height = 8

        self.particle_iterations = 1

    def copy_from(self, other):  # [attr for attr in dir(g) if not attr.startswith("__") and not callable(getattr(g, attr))]
        for attr in dir(self):
            if not attr.startswith("__") and not callable(getattr(self, attr)):
                setattr(self, attr, getattr(other, attr))

    def set_by_index(self, index, inp):
        if index == 0:
            self.move_right = inp
        elif index == 1:
            self.move_down = inp
        elif index == 2:
            self.move_left = inp
        elif index == 3:
            self.move_up = inp
        elif index == 4:
            self.interact = inp
        elif index == 5:
            self.other_function = inp
        elif index == 6:
            self.sprint = inp
        elif index == 7:
            self.battle_func1 = inp
        elif index == 8:
            self.battle_func2 = inp
        elif index == 9:
            self.battle_func3 = inp
        elif index == 10:
            self.battle_switch_menu = inp
        elif index == 11:
            self.battle_confirm = inp

    def save(self):
        sounds.set_effect_volume(self.effectVolume)
        sounds.set_music_volume(self.musicVolume)

        Screen.screen_height = self.screen_height
        Screen.screen_width = self.screen_width

    # def copy_to_keys(self):
    #     keys.move_right = self.move_right
    #     keys.move_down = self.move_down
    #     keys.move_left = self.move_left
    #     keys.move_up = self.move_up
    #     keys.interact = self.interact
    #     keys.other_function = self.other_function
    #     keys.sprint = self.sprint
    #
    #     keys.battle_func1 = self.battle_func1
    #     keys.battle_func2 = self.battle_func2
    #     keys.battle_func3 = self.battle_func3
    #     keys.battle_switch_menu = self.battle_switch_menu
    #     keys.battle_confirm = self.battle_confirm
    #
    #     self.__class__.showUnsellableItems = self.tempShowUnsellableItems
    #     self.__class__.allowAutoSaves = self.tempAllowAutoSaves
    #     self.__class__.showClaimedMissions = self.tempShowClaimedMissions
    #
    #     Screen.screen_height = self.screen_height
    #     Screen.screen_width = self.screen_width
    #
    #     sounds.set_effect_volume(self.effectVolume)
    #     sounds.set_music_volume(self.musicVolume)
    #
    # def copy_to_settings(self):
    #     self.musicVolume = sounds.music_volume
    #     self.effectVolume = sounds.effect_volume
    #
    #     # self.tempShowUnsellableItems = self.__class__.showUnsellableItems
    #     # self.tempAllowAutoSaves = self.__class__.allowAutoSaves
    #     # self.tempShowClaimedMissions = self.__class__.showClaimedMissions
    #
    #     self.screen_height = Screen.screen_height
    #     self.screen_width = Screen.screen_width
    #
    #     self.move_right = keys.move_right
    #     self.move_down = keys.move_down
    #     self.move_left = keys.move_left
    #     self.move_up = keys.move_up
    #     self.interact = keys.interact
    #     self.other_function = keys.other_function
    #     self.sprint = keys.sprint
    #
    #     self.battle_func1 = keys.battle_func1
    #     self.battle_func2 = keys.battle_func2
    #     self.battle_func3 = keys.battle_func3
    #     self.battle_switch_menu = keys.battle_switch_menu
    #     self.battle_confirm = keys.battle_confirm

    def reset(self):  # a copy of __init__
        self.copy_from(Settings())
        # return
        #
        # self.move_right = "d"
        # self.move_down = "s"
        # self.move_left = "a"
        # self.move_up = "w"
        # self.interact = "e"
        # self.other_function = "q"
        # self.sprint = "shift"
        # self.battle_func1 = "num1"
        # self.battle_func2 = "num2"
        # self.battle_func3 = "num3"
        # self.battle_switch_menu = "numDel"
        # self.battle_confirm = "num0"
        # self.effectVolume = 80
        # self.musicVolume = 50
        # self.allowAutoSaves = True
        # self.showUnsellableItems = False
        # self.screen_width = 10
        # self.screen_height = 7


class Menu:
    frame1 = 0
    frame = 0
    choose = None

    selected_world = None

    opened = False
    open_index = 0
    is_start = True

    file_choose = False
    delete_file = True

    file_exist = [False, False, False, False]
    file_sec = [0, 0, 0, 0]
    file_loc = ["", "", "", ""]
    current_save_slot = None
    time = 0

    reloading = False


class Game:
    frame = 0
    frames = 0
    clock = pygame.time.Clock()
    last_time = time.time()
    current_time = time.time()
    ticks_per_second = 30
    delta = 0
    time_start = time.time()


class Player:
    def __init__(self):
        self.max_hp = 20
        self.hp = 20
        self.max_mana = 10
        self.mana = 10
        self.attack = 10
        self.defense = 10
        self.evasion = 10
        self.accuracy = 10
        self.passive_list = []
        self.coins = 0

        self.exp = 0
        self.total_exp = 0
        self.level = 0
        self.next_lvl_exp = 5  # etnl = Ins.player.next_lvl_exp - Ins.player.exp
        self.exp_boost = 0
        self.level_points = 3
        self.atk_boost = 0
        self.def_boost = 0
        self.crit_rate_const = 0

        self.sword = None  # None
        self.bow = None  # None
        self.staff = None  # None
        self.helmet = None
        self.chestplate = None
        self.leggings = None
        self.accessory1 = None
        self.accessory2 = None
        self.talisman = None
        self.relic = None

        self.scroll = None
        self.script = None
        self.playerClass = None
        self.battle_inventory = []  # max len == 3

        self.width = 27  # 27
        self.height = 48  # 48
        self.hitbox_height = 16
        self.hitbox_width = 23
        self.degree = 0
        self.velocity = 360 / 60
        self.x = 1
        self.y = 1
        self.center_block = ()
        self.touching_blocks = set()
        self.touching_hitbox_blocks = set()
        self.inventory = []
        self.rect = pygame.Rect(self.x, self.y + self.height - self.hitbox_height, self.width, self.hitbox_height)

        self.animation_lib = "right"
        self.animation_num = 0
        self.animation_delay = 0
        self.sprinting = False

        self.random_encounter_variable = 0.0
        self.random_encounter_next = 320

    if True:
        def add_hp(self, amount):
            self.hp += amount
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            if console_active_list["infinite health"] == 1:
                self.hp = self.max_hp

        def add_max_hp(self, amount):
            self.max_hp += amount
            if self.hp > self.max_hp:
                self.hp = self.max_hp

        def add_mana(self, amount):
            self.mana += amount
            if self.mana > self.max_mana:
                self.mana = self.max_mana
            if console_active_list["infinite mana"] == 1:
                self.mana = self.max_mana

        def add_max_mana(self, amount):
            self.max_mana += amount
            if self.mana > self.max_mana:
                self.mana = self.max_mana

        def add_attack(self, amount):
            self.attack += amount

        def add_defense(self, amount):
            self.defense += amount

        def add_evasion(self, amount):
            self.evasion += amount

        def add_accuracy(self, amount):
            self.accuracy += amount

        def add_exp(self, amount):
            self.total_exp += round(amount * (self.exp_boost + 1))
            if self.total_exp > 99999999:
                self.total_exp = 99999999
            self.exp += round(amount * (self.exp_boost + 1))
            if self.level >= 99:
                self.next_lvl_exp = 1 + self.exp
            if self.exp >= self.next_lvl_exp:
                sounds.play_effect("effect2")
            while self.exp >= self.next_lvl_exp:
                self.exp -= self.next_lvl_exp
                # self.exp = max(0, self.exp)
                self.level += 1
                self.next_lvl_exp = int(1.075 * self.next_lvl_exp + 8)
                increase_level(self.level)

        def remove_passive(self, passives):
            for passive in passives:
                if passive in self.passive_list:
                    self.passive_list.pop(self.passive_list.index(passive))

        def add_coins(self, coins):
            if coins > 0:
                Ins.stats.total_coins += round(coins)
            self.coins += round(coins)

    def set_degree(self):

        if mouseHeld[3]:
            self.degree = None

            distance = (Screen.mouse_pos[1] + Screen.camera_y - self.y - self.height / 2)**2 + (Screen.mouse_pos[0] + Screen.camera_x - self.x - self.width / 2)**2

            if distance > 20:
                self.degree = math.atan2(Screen.mouse_pos[1] + Screen.camera_y - self.y - self.height / 2, Screen.mouse_pos[0] + Screen.camera_x - self.x - self.width / 2)
            else:
                return

            if distance >= 20000:
                Ins.player.velocity = 1.5 * 360 / 60 * float(console_choice_list["speed multiplier"][console_active_list["speed multiplier"]])
                Ins.player.sprinting = True
            elif not keysHeld[Ins.settings.sprint]:
                Ins.player.velocity = 360 / 60
                Ins.player.sprinting = False
        else:
            self.degree = math.atan2(keysHeld[Ins.settings.move_down] - keysHeld[Ins.settings.move_up], keysHeld[Ins.settings.move_right] - keysHeld[Ins.settings.move_left])

        if not self.degree and (keysHeld[Ins.settings.move_down] != keysHeld[Ins.settings.move_up] or keysHeld[Ins.settings.move_left] or not keysHeld[Ins.settings.move_right]) and not mouseHeld[3]:
            self.degree = None
        else:
            if -2*PI / 3 <= self.degree <= -PI/3:
                self.animation_lib = "up"
            elif PI / 3 <= self.degree <= 2*PI/3:
                self.animation_lib = "down"
            elif -PI / 3 <= self.degree <= PI/3:
                self.animation_lib = "right"
            else:
                self.animation_lib = "left"

    def move(self):
        if self.degree is None:
            pass
        else:
            if console_active_list["random encounters"] == 0:
                self.random_encounter_variable += 1.0 if not self.sprinting else 2.0
            self.y += self.velocity * math.sin(self.degree)

            if console_active_list["no clip"] == 0:
                self.position()
                temp_hitbox_list = []
                for temp_hitbox in Screen.selected_map[5]:
                    temp_hitbox_list.append(pygame.Rect(temp_hitbox))
                for block in self.touching_hitbox_blocks:
                    temp_hitbox = Screen.selected_map[0][block[1]][block[0]][3]
                    if temp_hitbox is True:
                        temp_hitbox_list.append(pygame.Rect(block[0] * 64, block[1] * 64, 64, 64))
                    elif temp_hitbox is not False:
                        for temp_hitbox2 in temp_hitbox:
                            temp_hitbox_list.append(pygame.Rect(temp_hitbox2[0] + block[0] * 64, temp_hitbox2[1] + block[1] * 64, temp_hitbox2[2], temp_hitbox2[3]))

                temp_rect = self.rect.union(pygame.Rect(self.rect.move(0, -self.velocity * math.sin(self.degree))))
                temp_hitbox_list2 = [-1]
                if self.degree > 0:  # moves down
                    for temp_hitbox in temp_hitbox_list:
                        if temp_hitbox.colliderect(temp_rect):
                            temp_hitbox_list2.append(self.rect.bottom - temp_hitbox.top)
                    self.y -= max(temp_hitbox_list2) + 1
                else:  # moves up
                    for temp_hitbox in temp_hitbox_list:
                        if temp_hitbox.colliderect(temp_rect):
                            temp_hitbox_list2.append(temp_hitbox.bottom - self.rect.top)
                    self.y += max(temp_hitbox_list2) + 1

                    # temp_hitbox_list2 = []
                    # for temp_hitbox in temp_hitbox_list:
                    #     if self.rect.colliderect(temp_hitbox):
                    #         temp_hitbox_list2.append(self.rect.clip(temp_hitbox))
                    #
                    # if len(temp_hitbox_list2) > 0:
                    #     temp_hitbox = temp_hitbox_list2[0].unionall(temp_hitbox_list2[1:])
                    #     self.y -= max(temp_hitbox.height, 1) * (1 if self.degree > 0 else -1)

            if self.y < 0:
                self.y = -1
            if self.y + self.height > Screen.height:
                self.y = Screen.height - self.height + 1

            self.x += self.velocity * math.cos(self.degree)

            if console_active_list["no clip"] == 0:
                self.position()
                temp_hitbox_list = []
                for temp_hitbox in Screen.selected_map[5]:
                    temp_hitbox_list.append(pygame.Rect(temp_hitbox))
                for block in self.touching_hitbox_blocks:
                    temp_hitbox = Screen.selected_map[0][block[1]][block[0]][3]
                    if temp_hitbox is True:
                        temp_hitbox_list.append(pygame.Rect(block[0] * 64, block[1] * 64, 64, 64))
                    elif temp_hitbox is not False:
                        for temp_hitbox2 in temp_hitbox:
                            temp_hitbox_list.append(
                                pygame.Rect(temp_hitbox2[0] + block[0] * 64, temp_hitbox2[1] + block[1] * 64,
                                            temp_hitbox2[2], temp_hitbox2[3]))

                temp_rect = self.rect.union(pygame.Rect(self.rect.move(-self.velocity * math.cos(self.degree), 0)))
                temp_hitbox_list2 = [-1]
                if abs(self.degree) < PI/2:  # moves right
                    for temp_hitbox in temp_hitbox_list:
                        if temp_hitbox.colliderect(temp_rect):
                            temp_hitbox_list2.append(self.rect.right - temp_hitbox.left)
                    self.x -= max(temp_hitbox_list2) + 1
                else:  # moves left
                    for temp_hitbox in temp_hitbox_list:
                        if temp_hitbox.colliderect(temp_rect):
                            temp_hitbox_list2.append(temp_hitbox.right - self.rect.left)
                    self.x += max(temp_hitbox_list2) + 1

                    # temp_hitbox_list2 = []
                    # for temp_hitbox in temp_hitbox_list:
                    #     if self.rect.colliderect(temp_hitbox):
                    #         temp_hitbox_list2.append(self.rect.clip(temp_hitbox))
                    #
                    # if len(temp_hitbox_list2) > 0:
                    #     temp_hitbox = temp_hitbox_list2[0].unionall(temp_hitbox_list2[1:])
                    #     self.x -= max(temp_hitbox.width, 1) * (1 if  else -1)

            if self.x < 0:
                self.x = -1
            if self.x + self.width > Screen.width:
                self.x = Screen.width - self.width + 1

            Screen.update_camera()

    def position(self):
        line = (self.x + self.width / 2) // 64
        row = (self.y + self.height - self.hitbox_height / 2) // 64
        self.center_block = (int(line), int(row))
        self.touching_hitbox_blocks = set()
        for i in [(self.x + (self.width - self.hitbox_width) / 2, self.y + self.height - self.hitbox_height), (self.x + (self.width + self.hitbox_width) / 2, self.y + self.height - self.hitbox_height), (self.x + (self.width - self.hitbox_width) / 2, self.y + self.height), (self.x + (self.width + self.hitbox_width) / 2, self.y + self.height)]:
            line = min(max(i[0] // 64, 0), Screen.width // 64 - 1)
            row = min(max(i[1] // 64, 0), Screen.height // 64 - 1)
            self.touching_hitbox_blocks.add((int(line), int(row)))
        self.rect = pygame.Rect(int(self.x + (self.width - self.hitbox_width) / 2), int(self.y) + self.height - self.hitbox_height, self.hitbox_width, self.hitbox_height)
        self.touching_blocks = set()
        for i in [(self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height)]:
            line = i[0] // 64
            row = i[1] // 64
            self.touching_blocks.add((int(line), int(row)))

    def draw(self):
        if self.degree is None:
            self.animation_num = 0
        Screen.win.blit(textures.player[self.animation_lib][self.animation_num][0], (int(self.x + textures.player[self.animation_lib][self.animation_num][1][0] - Screen.camera_x), int(self.y + textures.player[self.animation_lib][self.animation_num][1][1] - Screen.camera_y)))
        if console_active_list["show hitbox"] == 1:
            pygame.draw.rect(Screen.win, (255, 255, 255), self.rect, 1)
        if self.animation_delay >= 3:
            self.animation_num += 1
            self.animation_delay = 0
        else:
            if self.sprinting:
                self.animation_delay += 2
            else:
                self.animation_delay += 1
        if self.animation_num >= 9:
            self.animation_num = 1

    def add_item(self, item, amount=1):  # returns: 0 - item added normaly. 1 - item list removed. 2 - new item list added

        for slot in self.inventory:
            [name, number] = slot
            if item == name:
                number += amount
                self.inventory[self.inventory.index(slot)] = [name, number]
                if number == 0:
                    self.inventory.pop(self.inventory.index([name, number]))
                    if item in self.battle_inventory:
                        self.battle_inventory.remove(item)
                    return 1
                elif number < 0:
                    error.error(error.InventoryError, 2)
                return 0

        if item not in items:
            error.error(error.InventoryError, 4)
        if amount >= 0:
            self.inventory.append([item, amount])
            return 2
        else:
            error.error(error.InventoryError, 1)

    def item_amount(self, item):
        for [name, number] in self.inventory:
            if item == name:
                if number <= 0:
                    error.error(error.InventoryError, 3)
                return number
        return 0


class Screen:
    if True:
        debug = False

        run = True
        runState = ""
        window_width = 0
        window_height = 0
        freeze_player = False

        selected_travel_map = 0
        travel_page = 0
        travel_max = int(math.ceil(len(travel_list) / 6))

        console_index = 0

        mission_index = 0
        mission_page = 0
        mission_max_page = int(math.ceil(len(mission_list) / 10))

        tutorial_in_game = False
        tutorial_index = 0
        tutorial_page = 0

        message_updated_msg = ""
        message_updated_active = 0
        message_updated_time = 60

        map_layer = textures.none
        selected_map = maps.m_map0
        selected_map_str = "map0"
        map_switched_frame = False
        win = pygame.display.set_mode((1000, 600))
        clock = pygame.time.Clock()
        map_name = "lobby"
        map_song = "none"
        width = 64
        height = 64
        screen_width = 10
        screen_height = 7
        camera_x = 0
        camera_y = 0

        current = False
        current_list = []
        current_index = 0
        current_iter = iter([])
        current_name = ""
        current_text = ""
        current_lines = 0
        current_selected = 0
        current_message_delay = 0
        lines = 0

        menu_num = 0
        in_menu_num = 0
        inventory_roller = 0
        inventory_roller_max = 0
        items_in_roller = 0
        temp_num = 0
        scroll_roller = 0
        scroll_roller_max = 0
        script_roller = 0
        script_roller_max = (len(scrolls) - 1) // 3
        is_question = False
        is_displaying = False
        displayed_msg = ''
        question_option = 0
        question_text = ""
        description_message = ""
        description_page = 0

        enemy_id = -1
        max_battle_frames = 0
        current_battle_frame = -1

        cutSceneMap = maps.m_map0
        cutSceneList = dict()
        cutSceneMaxFrame = 0
        cutSceneFunc = {}
        cutSceneContinueSong = False
        cutSceneDelay = 0
        cutSceneFrame = 0
        cutSceneCameraX = 0
        cutSceneCameraY = 0
        cutSceneSkip = 0

        shopId = 0
        shopIndex = 0
        shopIsBuying = False
        shopAmount = 1
        shopMode = False
        shopSellPage = 0

        afterBattleScreenVar = 0
        afterBattleFrame = 0
        afterBattleList = []
        afterBattleList1 = []
        afterBattleTemp = 0

        classDeg = 0
        classIndex = 0
        classRotationTime = 0

        mouse_pos = (0, 0)
        dt = 0

    @classmethod
    def resize(cls, width, height=None):
        if isinstance(width, tuple) and height is None:
            cls.window_width, cls.window_height = width
            cls.win = pygame.display.set_mode(width)
        else:
            cls.window_width = width
            cls.window_height = height
            cls.win = pygame.display.set_mode((width, height))

    @classmethod
    def set_state(cls, state):
        cls.runState = state
        Animation.animation_saved = {i: Animation.animation_saved[i] for i in filter(lambda x: Animation.animation_saved[x].immune, Animation.animation_saved)}
        Animation.animation_list = list(filter(lambda x: x.immune, Animation.animation_list))
        Animation.animated = True
        Particles.particle_list.clear()
        if screen_states[state][0] is not None:
            Screen.resize(screen_states[state][0])
        if screen_states[state][1] is not None:
            pygame.display.set_caption(screen_states[state][1])

    @classmethod
    def state(cls, state):
        return state == cls.runState

    @classmethod
    def unlock_map_travel(cls, map_name, entering_map=False):
        if map_name in Ins.ap.travel_unlocked and Ins.ap.travel_unlocked[map_name] is False:
            if entering_map:
                for _map in travel_list:
                    if _map[0] == map_name:
                        if not _map[3]:
                            return
                        break
                else:
                    raise Exception("doesn't exist")
            Ins.ap.travel_unlocked[map_name] = True
            cls.message_updated_msg = "travel unlocked!"
            cls.message_updated_active = cls.message_updated_time

    @classmethod
    def update_camera(cls, init=False):
        if 64*cls.screen_height < cls.height:
            cls.camera_y = max(min(Ins.player.y + Ins.player.height / 2 - 32 * cls.screen_height, cls.height - 64 * cls.screen_height), 0)
        elif init:
            cls.camera_y = cls.height / 2 - 32 * cls.screen_height

        if 64*cls.screen_width < cls.width:
            cls.camera_x = max(min(Ins.player.x + Ins.player.width / 2 - 32 * cls.screen_width, cls.width - 64 * cls.screen_width), 0)
        elif init:
            cls.camera_x = cls.width / 2 - 32 * cls.screen_width

    @classmethod
    def select_map(cls, map_list):
        try:
            globals()["mp_ed_"+cls.selected_map_str]()
        except KeyError:
            pass

        cls.selected_map_str = map_list

        map_list = maps.map_list[map_list]

        cls.width = 64*len(map_list[0][0])
        cls.height = 64*len(map_list[0])

        cls.update_camera(True)

        if cls.selected_map[4][0] or map_list[4][0]:
            Ins.player.random_encounter_variable = 0
        cls.resize(64*cls.screen_width, 64*cls.screen_height)
        cls.selected_map = map_list

        cls.map_song = map_list[4][1]
        pygame.display.set_caption(map_list[4][3])
        cls.map_name = map_list[4][3]
        cls.map_layer = None
        Ins.ap.player_map = cls.selected_map_str
        try:
            if map_list[4][4]:
                cls.map_layer = []
                temp_val = 0
                while True:
                    cls.map_layer.append(pygame.image.load("resources/maps/"+str(temp_val)+"m_"+Screen.selected_map_str+".png"))
                    temp_val += 1
            else:
                cls.map_layer = pygame.image.load("resources/maps/m_"+Screen.selected_map_str+".png")
        except FileNotFoundError:
            pass

        try:
            globals()["mp_st_"+cls.selected_map_str]()
        except KeyError:
            pass

    @classmethod
    def get_text_format(cls, text, width=0, font_type=font):

        res = []
        for txt in text.split("\n"):
            temp_text = ""
            pre = ""
            for i in txt.split(" "):
                w = font_type.render(temp_text + pre + i, False, (255, 255, 255)).get_width()
                if width == 0 or w <= width:
                    temp_text += pre + i
                else:
                    res.append(temp_text)
                    temp_text = i
                pre = " "
            res.append(temp_text)

        # line = 0
        # for i in res:
        #     surface = font.render(i, False, (255, 255, 255))
        #     Screen.win.blit(surface, (pos[0], pos[1] + line))
        #     line += 32

        return res

    @classmethod
    def blit_text(cls, text, pos, text_font=font, color=(255, 255, 255), align=(0.0, 0.0), alpha=255):
        surface1 = text_font.render(text, False, color)
        w = surface1.get_width()
        h = surface1.get_height()
        if alpha < 255:
            surface1.set_alpha(round(alpha))
        Screen.win.blit(surface1, (round(pos[0] - align[0] * w), round(pos[1] - align[1] * h)))

    @classmethod
    def show_text(cls):
        try:
            if keysDown[Ins.settings.interact] or mouseDown[1]:
                if isinstance(cls.current_text, tuple):
                    for i in cls.current_text[cls.current_selected][1:]:
                        if isinstance(i, list):
                            globals()["f_" + i[0]](*i[1:])
                        else:
                            globals()["f_" + i]()

                cls.current_text = next(cls.current_iter)
                cls.current_index += 1

                if isinstance(cls.current_text, str):
                    cls.current_selected = 0

                elif isinstance(cls.current_text, tuple):
                    cls.current_selected = 1

                elif isinstance(cls.current_text, list):
                    for i in cls.current_text:
                        if isinstance(i, list):
                            globals()["f_" + i[0]](*i[1:])
                        else:
                            globals()["f_" + i]()
                    cls.show_text()

        except StopIteration:
            cls.current = False
            cls.current_selected = 0

        if isinstance(cls.current_text, str):
            temp_text = cls.get_text_format(cls.current_text, Screen.window_width - 70)
            temp_lines = len(temp_text)
            pygame.draw.rect(Screen.win, (0, 0, 0), (30, Screen.window_height - 30 - 40 * temp_lines - 10, Screen.window_width - 60, 40 * temp_lines + 10))
            pygame.draw.rect(Screen.win, (100, 100, 100), (30, Screen.window_height - 30 - 40 * temp_lines - 10, Screen.window_width - 60, 40 * temp_lines + 10), 2)
            i = Screen.window_height - 40 * len(temp_text) - 30

            surface = font.render(cls.current_name, False, (255, 255, 255))
            Screen.win.blit(surface, (35, i - 43))
            for j in temp_text:
                surface = font.render(j, False, (255, 255, 255))
                Screen.win.blit(surface, (40, i))
                i += 40

        elif isinstance(cls.current_text, tuple):
            if keysDown[Ins.settings.move_down] or mouseDown[5]:
                cls.current_selected += 1
                if cls.current_selected >= len(cls.current_text):
                    cls.current_selected = 1
            if keysDown[Ins.settings.move_up] or mouseDown[4]:
                cls.current_selected -= 1
                if cls.current_selected <= 0:
                    cls.current_selected = len(cls.current_text) - 1

            temp_text = list(map(lambda x: cls.get_text_format(x[0], Screen.window_width - 70), cls.current_text))
            temp_lines = sum(map(lambda x: len(x), temp_text))

            pygame.draw.rect(Screen.win, (0, 0, 0), (30, 30, Screen.window_width - 60, 40 * temp_lines + 10))
            pygame.draw.rect(Screen.win, (100, 100, 100), (30, 30, Screen.window_width - 60, 40 * temp_lines + 10), 2)

            i = 40
            temp_number = 0
            for txt in temp_text:
                temp_lines = len(txt)
                if temp_number != 0:
                    if temp_number == cls.current_selected:
                        pygame.draw.rect(Screen.win, (100, 255, 100), (35, i - 1, Screen.window_width - 70, 40 * temp_lines - 2))
                    pygame.draw.rect(Screen.win, (100, 100, 100), (35, i - 1, Screen.window_width - 70, 40 * temp_lines - 2), 1)
                for j in txt:
                    surface = font.render(j, False, (255, 255, 255))
                    Screen.win.blit(surface, (40, i))
                    i += 40
                temp_number += 1

            surface = font.render(cls.current_name, False, (255, 255, 255))
            Screen.win.blit(surface, (35, i + 7))

    @classmethod
    def display_message(cls):
        # top = 40 if (cls.current and cls.current_selected == 0) or (not cls.current and Ins.player.y > (cls.height / 2 - 24)) else (cls.window_height - 140)
        top = 40 if not cls.current_selected != 0 else cls.window_height - 140
        temp_x = 30*min(cls.message_updated_time-cls.message_updated_active, cls.message_updated_active, 10) - 305
        pygame.draw.rect(cls.win, (0, 0, 0), (temp_x, top, 305, 80))
        pygame.draw.rect(cls.win, (255, 255, 255), (temp_x, top, 305, 80), 2)
        surface = font4.render(cls.message_updated_msg, False, (255, 255, 255))
        cls.win.blit(surface, (int(temp_x + 150 - surface.get_rect().width / 2), top + 20))
        cls.message_updated_active -= 1

    @classmethod
    def insert_current(cls, *text_list):
        for i in text_list[::-1]:
            cls.current_list.insert(cls.current_index, i)

    @classmethod
    def append_current(cls, *text_list):
        for i in text_list:
            cls.current_list.append(i)

    @classmethod
    def open_text(cls, library, skip1=False):
        cls.current_text = texts.none
        cls.current_iter = iter(library[0])
        cls.current_name = next(cls.current_iter)
        try:
            while True:
                _temp_next = next(cls.current_iter)
                if isinstance(_temp_next, str):
                    globals()["f_"+_temp_next]()
                else:
                    globals()["f_"+_temp_next[0]](*_temp_next[1:])
        except StopIteration:
            pass
        cls.current = True
        cls.current_index = 0
        cls.current_list = list(library[1])
        cls.current_iter = iter(cls.current_list)
        if not skip1:
            cls.current_text = next(cls.current_iter)


class Battle:
    class Sprite:
        x = 0
        y = 0
        length = 44
        degree = 0
        velocity = 20
        is_moving = False

        mode = 0
        direction = 0

        mode_2_velocity = 1
        force_move = False
        temp_degree_bool = False
        temp_function_bool = False
        on_ground = False
        holding = False

        current_effect = 0
        current_effect_damage = 0
        current_effect_length = 0
        random_multiplier = (0.8, 1)
        effect_frame = 0

        @classmethod
        def set_degree(cls):
            if cls.mode == 1:
                temp_lib = keysDown
            else:
                temp_lib = keysHeld

            if cls.mode == 4:
                if keysDown[Ins.settings.move_right]:
                    cls.direction += 1
                    if cls.direction > 3:
                        cls.direction = 0
                    cls.degree = None
                if keysDown[Ins.settings.move_left]:
                    cls.direction -= 1
                    if cls.direction < 0:
                        cls.direction = 3
                    cls.degree = None

                cls.degree = math.atan2(temp_lib[Ins.settings.move_down] - temp_lib[Ins.settings.move_up], 0)
                if not cls.degree:
                    cls.degree = None
                else:
                    cls.degree += cls.direction * PI / 2

                return 0

            if cls.mode == 5 and (temp_lib[Ins.settings.move_down] == temp_lib[Ins.settings.move_up] == 1 or temp_lib[Ins.settings.move_left] == temp_lib[Ins.settings.move_right] == 1 or temp_lib[Ins.settings.move_left] == temp_lib[Ins.settings.move_right] == temp_lib[Ins.settings.move_down] == temp_lib[Ins.settings.move_up] == 0):
                return 0
            cls.degree = math.atan2(temp_lib[Ins.settings.move_down] - temp_lib[Ins.settings.move_up], temp_lib[Ins.settings.move_right] - temp_lib[Ins.settings.move_left])
            if cls.mode == 5:
                return 0
            if not cls.degree and (temp_lib[Ins.settings.move_down] != temp_lib[Ins.settings.move_up] or temp_lib[Ins.settings.move_left] or not temp_lib[Ins.settings.move_right]):
                cls.degree = None
            elif cls.mode != 3:
                cls.degree += cls.direction * PI / 2

            if console_active_list["show direction"] == 1:
                if cls.degree is None:
                    pygame.draw.circle(Screen.win, (80, 255, 80), (600, 300), 25, 1)
                else:
                    pygame.draw.line(Screen.win, (80, 255, 80), (600, 300), (round(600 + 50*math.cos(cls.degree)), round(300 + 50*math.sin(cls.degree))))
            # if cls.mode == 3:
            #     if cls.degree is None or not any([temp_lib[Ins.settings.move_right], temp_lib[Ins.settings.move_down], temp_lib[Ins.settings.move_left], temp_lib[Ins.settings.move_up]]):
            #         # cls.degree = (cls.direction - 1) * PI / 2
            #         # cls.force_move = True
            #         cls.on_ground = False
            #         pass
            #     else:
            #         if math.isclose(cls.degree % (PI * 2), (cls.direction * PI / 2) % (PI * 2)) or math.isclose(cls.degree % (PI * 2), (cls.direction * PI / 2 + PI / 4) % (PI * 2)):
            #             cls.degree = (cls.direction - 1) * PI / 2 + PI / 4
            #         elif math.isclose(cls.degree % (PI * 2), ((cls.direction - 2) * PI / 2) % (PI * 2)) or math.isclose(cls.degree % (PI * 2), ((cls.direction - 2) * PI / 2 - PI / 4) % (PI * 2)):
            #             cls.degree = (cls.direction - 1) * PI / 2 - PI / 4
            #         elif math.isclose(cls.degree % (PI * 2), ((cls.direction + 1) * PI / 2) % (PI * 2)):
            #             cls.degree = (cls.direction - 1) * PI / 2

            if console_active_list["show direction"] == 1:
                if cls.degree is None:
                    pygame.draw.circle(Screen.win, (255, 80, 80), (600, 300), 25, 1)
                else:
                    pygame.draw.line(Screen.win, (255, 80, 80), (600, 300), (round(600 + 50*math.cos(cls.degree)), round(300 + 50*math.sin(cls.degree))))

        @classmethod
        def gravity(cls):
            temp_hitbox_list = []
            for hitbox in Battle.Hitbox.hitbox_list:
                temp_hitbox_list.append(pygame.Rect(round(hitbox.x), round(hitbox.y), hitbox.width, hitbox.height))

            on_ground1 = False
            on_ground2 = False

            if keysUp[Ins.settings.move_up]:
                cls.holding = False

            # if cls.velocity == cls.mode_2_velocity:
            # cls.y += cls.mode_2_velocity * math.sin((cls.direction - 1) * PI / 2) / 16
            # cls.x += cls.mode_2_velocity * math.cos((cls.direction - 1) * PI / 2) / 16
            cls.is_moving = True
            temp_degree = (cls.direction + 1) * PI / 2
            #print(cls.on_ground)
            temp_rect2 = pygame.Rect(round(cls.x + 305), round(cls.y + 305), cls.length, cls.length)
            cls.y += cls.mode_2_velocity * math.sin(temp_degree)
            if keysHeld[Ins.settings.move_right]:
                cls.y += cls.velocity * math.sin(temp_degree - PI / 2)
            if keysHeld[Ins.settings.move_left]:
                cls.y += cls.velocity * math.sin(temp_degree + PI / 2)
            if keysHeld[Ins.settings.move_up] and cls.on_ground or cls.holding:
                cls.y += cls.velocity * math.sin(temp_degree + PI)
                cls.holding = True
            if keysHeld[Ins.settings.move_down]:
                cls.y += cls.velocity * math.sin(temp_degree)
            if console_active_list["no clip"] == 0:
                for _hitbox in Battle.Hitbox.hitbox_list:
                    _hitbox_rect = pygame.Rect(round(_hitbox.x + 305), round(_hitbox.y + 305), _hitbox.width,
                                               _hitbox.height)
                    if _hitbox_rect.colliderect(hp_get_battle_hitbox()):
                        if temp_rect2.centery < _hitbox_rect.centery:
                            cls.y = _hitbox.y - cls.length - 1
                        else:
                            cls.y = _hitbox.y + _hitbox.height + 1
                        cls.mode_2_velocity = 0
                        on_ground1 = True

                # temp_rect = pygame.Rect(round(cls.x), round(cls.y), cls.length, cls.length)
                # temp_rect = temp_rect.union(temp_rect2)
                # temp_hitbox_list2 = [-1]
                # if temp_degree > 0:  # moves down
                #     for temp_hitbox in temp_hitbox_list:
                #         if temp_hitbox.colliderect(temp_rect):
                #             temp_hitbox_list2.append(temp_rect.bottom - temp_hitbox.top)
                #             cls.is_moving = False
                #             on_ground1 = True
                #     cls.y -= max(temp_hitbox_list2) + 1
                # else:  # moves up
                #     for temp_hitbox in temp_hitbox_list:
                #         if temp_hitbox.colliderect(temp_rect):
                #             temp_hitbox_list2.append(temp_hitbox.bottom - temp_rect.top)
                #             cls.is_moving = False
                #             on_ground1 = True
                #     cls.y += max(temp_hitbox_list2) + 1

            temp_rect2 = pygame.Rect(round(cls.x + 305), round(cls.y + 305), cls.length, cls.length)
            cls.x += cls.mode_2_velocity * math.cos(temp_degree)
            if keysHeld[Ins.settings.move_right]:
                cls.x += cls.velocity * math.cos(temp_degree - PI / 2)
            if keysHeld[Ins.settings.move_left]:
                cls.x += cls.velocity * math.cos(temp_degree + PI / 2)
            if keysHeld[Ins.settings.move_up] and cls.on_ground or cls.holding:
                cls.x += cls.velocity * math.cos(temp_degree + PI)
                cls.holding = True
            if keysHeld[Ins.settings.move_down]:
                cls.x += cls.velocity * math.cos(temp_degree)

            if console_active_list["no clip"] == 0:
                for _hitbox in Battle.Hitbox.hitbox_list:
                    _hitbox_rect = pygame.Rect(round(_hitbox.x + 305), round(_hitbox.y + 305), _hitbox.width, _hitbox.height)
                    if _hitbox_rect.colliderect(hp_get_battle_hitbox()):
                        if temp_rect2.centerx > _hitbox_rect.centerx:
                            cls.x = _hitbox.x - cls.length - 1
                        else:
                            cls.x = _hitbox.x + _hitbox.width + 1
                        cls.mode_2_velocity = 0
                        on_ground2 = True

                # temp_rect = pygame.Rect(round(cls.x), round(cls.y), cls.length, cls.length)
                # temp_rect = temp_rect.union(temp_rect2)
                # temp_hitbox_list2 = [-1]
                # if abs(temp_degree) < PI / 2:  # moves right
                #     for temp_hitbox in temp_hitbox_list:
                #         if temp_hitbox.colliderect(temp_rect):
                #             temp_hitbox_list2.append(temp_rect.right - temp_hitbox.left)
                #             cls.is_moving = False
                #             on_ground2 = True
                #             cls.mode_2_velocity = 0
                #     cls.x -= max(temp_hitbox_list2) + 1
                # else:  # moves left
                #     for temp_hitbox in temp_hitbox_list:
                #         if temp_hitbox.colliderect(temp_rect):
                #             temp_hitbox_list2.append(temp_hitbox.right - temp_rect.left)
                #             cls.is_moving = False
                #             on_ground2 = True
                #             cls.mode_2_velocity = 0
                #     cls.x += max(temp_hitbox_list2) + 1

            cls.on_ground = False
            if on_ground2 or on_ground1:
                cls.on_ground = True

            if cls.y < 0:
                cls.y = 0
                cls.is_moving = False
                cls.on_ground = True
                cls.mode_2_velocity = 0
            if cls.y + cls.length > 390:
                cls.y = 390 - cls.length
                cls.is_moving = False
                cls.on_ground = True
                cls.mode_2_velocity = 0

            if cls.x < 0:
                cls.x = 0
                cls.is_moving = False
                cls.on_ground = True
                cls.mode_2_velocity = 0
            if cls.x + cls.length > 590:
                cls.x = 590 - cls.length
                cls.is_moving = False
                cls.on_ground = True
                cls.mode_2_velocity = 0

            cls.mode_2_velocity += 1
            # if cls.velocity == cls.mode_2_velocity:
            #     cls.y += math.sin((cls.direction - 1) * PI / 2) / 16
            #     cls.x += math.cos((cls.direction - 1) * PI / 2) / 16
            # cls.is_moving = True
            # temp_degree = (cls.direction + 1) * PI / 2
            # was_broken = False
            # cls.y += math.sin(temp_degree)
            # if not 0 <= cls.y <= 390 - cls.length:
            #     cls.mode_2_velocity = 0
            #     cls.y -= math.sin(temp_degree)
            #     cls.is_moving = False
            # sprite_rect = pygame.Rect(int(cls.x), int(cls.y), cls.length, cls.length)
            # for hitbox in Battle.Hitbox.hitbox_rect_list:
            #     if sprite_rect.colliderect(hitbox):
            #         if not was_broken:
            #             cls.mode_2_velocity = 0
            #             cls.y -= math.sin(temp_degree)
            #             cls.is_moving = False
            #             was_broken = True
            #
            # was_broken = False
            # cls.x += math.cos(temp_degree)
            # if not 0 <= cls.x <= 590 - cls.length:
            #     cls.mode_2_velocity = 0
            #     cls.x -= math.cos(temp_degree)
            #     cls.is_moving = False
            # sprite_rect = pygame.Rect(int(cls.x), int(cls.y), cls.length, cls.length)
            # for hitbox in Battle.Hitbox.hitbox_rect_list:
            #     if sprite_rect.colliderect(hitbox):
            #         if not was_broken:
            #             cls.mode_2_velocity = 0
            #             cls.x -= math.cos(temp_degree)
            #             cls.is_moving = False
            #             was_broken = True

        @classmethod
        def move(cls):
            if cls.mode in (0, 1, 3, 4, 5):
                if cls.mode == 1:
                    temp_lib = keysDown
                else:
                    temp_lib = keysHeld
                if cls.degree is not None and (any([temp_lib[Ins.settings.move_right], temp_lib[Ins.settings.move_down], temp_lib[Ins.settings.move_left], temp_lib[Ins.settings.move_up]]) or cls.force_move or cls.mode == 5):

                    temp_hitbox_list = []
                    for hitbox in Battle.Hitbox.hitbox_list:
                        temp_hitbox_list.append(pygame.Rect(round(hitbox.x), round(hitbox.y), hitbox.width, hitbox.height))

                    cls.y += cls.velocity * math.sin(cls.degree)

                    if console_active_list["no clip"] == 0:
                        temp_rect = pygame.Rect(round(cls.x), round(cls.y), cls.length, cls.length)
                        temp_rect = temp_rect.union(pygame.Rect(temp_rect.move(0, -cls.velocity * math.sin(cls.degree))))
                        temp_hitbox_list2 = [-1]
                        if cls.degree > 0:  # moves down
                            for temp_hitbox in temp_hitbox_list:
                                if temp_hitbox.colliderect(temp_rect):
                                    temp_hitbox_list2.append(temp_rect.bottom - temp_hitbox.top)
                                    cls.is_moving = False
                            cls.y -= max(temp_hitbox_list2) + 1
                        else:  # moves up
                            for temp_hitbox in temp_hitbox_list:
                                if temp_hitbox.colliderect(temp_rect):
                                    temp_hitbox_list2.append(temp_hitbox.bottom - temp_rect.top)
                                    cls.is_moving = False
                            cls.y += max(temp_hitbox_list2) + 1

                            # temp_hitbox_list2 = []
                            # for temp_hitbox in temp_hitbox_list:
                            #     if self.rect.colliderect(temp_hitbox):
                            #         temp_hitbox_list2.append(self.rect.clip(temp_hitbox))
                            #
                            # if len(temp_hitbox_list2) > 0:
                            #     temp_hitbox = temp_hitbox_list2[0].unionall(temp_hitbox_list2[1:])
                            #     self.y -= max(temp_hitbox.height, 1) * (1 if self.degree > 0 else -1)

                    if cls.y < 0:
                        cls.y = 0
                        cls.is_moving = False
                    if cls.y + cls.length > 390:
                        cls.y = 390 - cls.length
                        cls.is_moving = False

                    cls.x += cls.velocity * math.cos(cls.degree)

                    if console_active_list["no clip"] == 0:
                        temp_rect = pygame.Rect(round(cls.x), round(cls.y), cls.length, cls.length)
                        temp_rect = temp_rect.union(pygame.Rect(temp_rect.move(-cls.velocity * math.cos(cls.degree), 0)))
                        temp_hitbox_list2 = [-1]
                        if abs(cls.degree) < PI / 2:  # moves right
                            for temp_hitbox in temp_hitbox_list:
                                if temp_hitbox.colliderect(temp_rect):
                                    temp_hitbox_list2.append(temp_rect.right - temp_hitbox.left)
                                    cls.is_moving = False
                            cls.x -= max(temp_hitbox_list2) + 1
                        else:  # moves left
                            for temp_hitbox in temp_hitbox_list:
                                if temp_hitbox.colliderect(temp_rect):
                                    temp_hitbox_list2.append(temp_hitbox.right - temp_rect.left)
                                    cls.is_moving = False
                            cls.x += max(temp_hitbox_list2) + 1

                    if cls.x < 0:
                        cls.x = 0
                        cls.is_moving = False
                    if cls.x + cls.length > 590:
                        cls.x = 590 - cls.length
                        cls.is_moving = False

                else:
                    cls.is_moving = False

            elif cls.mode == 2:
                cls.is_moving = False
                if (cls.degree is not None and any([keysHeld[Ins.settings.move_right], keysHeld[Ins.settings.move_down], keysHeld[Ins.settings.move_left], keysHeld[Ins.settings.move_up]])) or cls.force_move:
                    if cls.degree % (2*PI) == 0:
                        Battle.Sprite.x = 502 - cls.length / 2
                        Battle.Sprite.y = 195 - cls.length / 2
                    elif cls.degree % (2*PI) == PI:
                        Battle.Sprite.x = 98 - cls.length / 2
                        Battle.Sprite.y = 195 - cls.length / 2
                    elif cls.degree % (2*PI) == PI / 2:
                        Battle.Sprite.x = 295 - cls.length / 2
                        Battle.Sprite.y = 335 - cls.length / 2
                    elif cls.degree % (2*PI) == 3 * PI / 2:
                        Battle.Sprite.x = 295 - cls.length / 2
                        Battle.Sprite.y = 65 - cls.length / 2
                    elif cls.degree % (2*PI) == PI / 4:
                        Battle.Sprite.x = 502 - cls.length / 2
                        Battle.Sprite.y = 335 - cls.length / 2
                    elif cls.degree % (2*PI) == 3 * PI / 4:
                        Battle.Sprite.x = 98 - cls.length / 2
                        Battle.Sprite.y = 335 - cls.length / 2
                    elif cls.degree % (2*PI) == 5 * PI / 4:
                        Battle.Sprite.x = 98 - cls.length / 2
                        Battle.Sprite.y = 65 - cls.length / 2
                    elif cls.degree % (2*PI) == 7 * PI / 4:
                        Battle.Sprite.x = 502 - cls.length / 2
                        Battle.Sprite.y = 65 - cls.length / 2
                else:
                    Battle.Sprite.x = 295 - cls.length / 2
                    Battle.Sprite.y = 195 - cls.length / 2

        @classmethod
        def draw(cls):
            if console_active_list["show hitbox"] == 1:
                pygame.draw.rect(Screen.win, (255, 255, 255), (round(cls.x + 305), round(cls.y + 305), cls.length, cls.length), 1)
            if cls.direction % 4 == 0:
                Screen.win.blit(textures.player_sprite_down, (round(cls.x + 305), round(cls.y + 305)))
            elif cls.direction % 4 == 1:
                Screen.win.blit(textures.player_sprite_left, (round(cls.x + 305), round(cls.y + 305)))
            elif cls.direction % 4 == 2:
                Screen.win.blit(textures.player_sprite_up, (round(cls.x + 305), round(cls.y + 305)))
            elif cls.direction % 4 == 3:
                Screen.win.blit(textures.player_sprite_right, (round(cls.x + 305), round(cls.y + 305)))
            else:
                rotated_image = pygame.transform.rotate(textures.player_sprite_down, -90 * cls.direction)
                new_rect = rotated_image.get_rect(center=textures.player_sprite_down.get_rect(topleft=(round(cls.x), round(cls.y))).center)
                Screen.win.blit(rotated_image, (round(new_rect.topleft[0] + 305), round(new_rect.topleft[1] + 305)))

                Screen.win.blit(pygame.transform.rotate(textures.player_sprite_down, -cls.direction * 90), (round(cls.x + 305 + 22 * (abs(0.5 - cls.direction % 1) - 0.5)), round(cls.y + 305 + 22 * (abs(0.5 - cls.direction % 1) - 0.5))))

        @classmethod
        def effect(cls, effect_type, effect_damage, effect_length, random_multiplier):
            if cls.current_effect > effect_type:
                return 0
            elif cls.current_effect_damage > effect_damage:
                return 0
            elif cls.current_effect_length > effect_length:
                return 0

            if cls.current_effect == 0:
                cls.effect_frame = Battle.current_battle_frame
            cls.current_effect = effect_type
            cls.current_effect_damage = effect_damage
            cls.random_multiplier = random_multiplier
            cls.current_effect_length = effect_length

        @classmethod
        def effect_ff(cls):
            cls.current_effect_length -= 1
            if cls.current_effect in (1, 2):
                Ins.player.add_hp(-1 * cls.current_effect_damage * (Battle.enemy_list[4][5] / 66 + 0.75) * random.uniform(cls.random_multiplier[0], cls.random_multiplier[1]) / (Ins.player.defense + 1))
            if cls.current_effect in (3, 4):
                Ins.player.add_hp(-1 * cls.current_effect_damage * (Battle.enemy_list[4][5] / 66 + 0.75) * random.uniform(cls.random_multiplier[0], cls.random_multiplier[1]) / (Ins.player.defense + 1) * Battle.enemy_list[4][1])
            if cls.current_effect in (5, 6):
                Ins.player.add_hp(-1 * cls.current_effect_damage * (Battle.enemy_list[4][5] / 66 + 0.75) * random.uniform(cls.random_multiplier[0], cls.random_multiplier[1]))
            if Ins.player.hp <= 0 and cls.current_effect in (1, 3, 5):
                Ins.player.hp = 1
            if cls.current_effect_length <= 0:
                cls.current_effect = 0
                cls.effect_damage = 0

    class Hitbox:
        hitbox_list = []
        hitbox_rect_list = []
        color = (255, 255, 255)

        def __init__(self, x, y, width, height, degree, velocity, max_frames=-1, is_full=False, command=("none", "none"), color=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.degree = degree
            self.velocity = velocity
            self.__class__.hitbox_list.append(self)
            self.frames = 0
            self.max_frames = max_frames
            self.is_full = is_full
            self._exist = command[0]
            self._touching = command[1]
            self.color = color

        def render_ff(self):
            temp_touching = False
            self.existing()
            if Battle.running_battle:
                self.y += self.velocity * math.sin(self.degree)
                _hitbox_rect = pygame.Rect(round(self.x + 305), round(self.y + 305), self.width, self.height)
                if _hitbox_rect.colliderect(hp_get_battle_hitbox()):
                    temp_touching = True
                    _hitbox_rect_top = pygame.Rect(round(self.x + 305), round(self.y + 305), self.width, self.height // 2)
                    if _hitbox_rect_top.colliderect(hp_get_battle_hitbox()):
                        Battle.Sprite.y = self.y - Battle.Sprite.length - 1
                    else:
                        Battle.Sprite.y = self.y + self.height + 1

                    if Battle.Sprite.y < 0:
                        Battle.Sprite.y = 0
                    if Battle.Sprite.y + Battle.Sprite.length > 390:
                        Battle.Sprite.y = 390 - Battle.Sprite.length

                self.x += self.velocity * math.cos(self.degree)

                _hitbox_rect = pygame.Rect(round(self.x + 305), round(self.y + 305), self.width, self.height)
                if _hitbox_rect.colliderect(hp_get_battle_hitbox()):
                    temp_touching = True
                    _hitbox_rect_top = pygame.Rect(round(self.x + 305), round(self.y + 305), self.width // 2, self.height)
                    if _hitbox_rect_top.colliderect(hp_get_battle_hitbox()):
                        Battle.Sprite.x = self.x - Battle.Sprite.length - 1

                    else:
                        Battle.Sprite.x = self.x + self.width + 1

                    if Battle.Sprite.x < 0:
                        Battle.Sprite.x = 0
                    if Battle.Sprite.x + Battle.Sprite.length > 590:
                        Battle.Sprite.x = 590 - Battle.Sprite.length


                # _hitbox_rect = pygame.Rect(round(self.x + 305), round(self.y + 305), self.width, self.height)
                # if _hitbox_rect.colliderect(pygame.Rect(round(Battle.Sprite.x + 305), round(Battle.Sprite.y + 305), Battle.Sprite.length, Battle.Sprite.length)):
                #     temp_touching = True
                #     if abs(self.degree) < PI / 2:
                #         Battle.Sprite.x = _hitbox_rect.right + 306
                #     else:
                #         Battle.Sprite.x = _hitbox_rect.left - Battle.Sprite.length + 304
                #
                #     if Battle.Sprite.x < 0:
                #         Battle.Sprite.x = 0
                #     if Battle.Sprite.x + Battle.Sprite.length > 590:
                #         Battle.Sprite.x = 590 - Battle.Sprite.length

                if temp_touching:
                    self.touching()
            if self.is_full:
                pygame.draw.rect(Screen.win, Battle.Hitbox.color if self.color is None else self.color, (round(305 + self.x), round(305 + self.y), self.width, self.height))
            else:
                pygame.draw.rect(Screen.win, Battle.Hitbox.color if self.color is None else self.color, (round(305 + self.x), round(305 + self.y), self.width, self.height), 2)
            if Battle.running_battle:
                if self.max_frames != -1 and self.frames >= self.max_frames - 1:
                    self.__class__.hitbox_list.pop(self.__class__.hitbox_list.index(self))
                else:
                    self.frames += 1

        def existing(self):
            if self._exist != "none":
                return globals()["he_"+self._exist](self)

        def touching(self):
            if self._touching != "none":
                return globals()["ht_"+self._touching](self)

    class Projectile:
        projectile_list = []
        player_rect = None

        def __init__(self, x, y, width, height, degree, velocity, projectile_stats, image="", max_time=-1, attack_modifier=1, accuracy_modifier=0.05,
                     random_multiplier=(0.98, 1.02), effects=("none", "none", "none", "none"), color=(255, 255, 255), spinning=(0.0, 0.0, 0.0, 0.0, 0.0), radian_offset=False):
            self.x = x  # 4 basic rect parameters
            self.y = y
            self.width = width
            self.height = height
            self.degree = degree  # movement info
            self.velocity = velocity
            # damage info
            self.projectile_type = projectile_stats[0]  # 0: normal, 1: unvanishing
            self.projectile_effect = projectile_stats[1]  # 0: normal, 1: poison, 2: wither, 3: poison affected by attack, 4: wither affected by attack, 5: shield piercing poison, 6: shield piercing wither
            self.projectile_application = projectile_stats[2]  # 0: normal, 1: hurts if moving, 2: hurts if not moving, 3: doesnt hurt
            self.projectile_effect_damage = projectile_stats[3]
            self.projectile_effect_length = projectile_stats[4]
            self.projectile_damage_type = projectile_stats[5]  # 0: normal, 1: shield piercing

            self.attack_modifier = attack_modifier
            self.accuracy_modifier = accuracy_modifier  # closer to 1 means more hits
            self.random_multiplier = random_multiplier
            # behavior info
            self._created = effects[0]
            self._existing = effects[1]
            self._deleted = effects[2]
            self._hit = effects[3]

            # rendering and position info
            self.hitbox = []
            if image == "":
                self.image = ""  # no texture (rect)
                self.color = color  # color
                self.rect_width = spinning[4]
            else:
                self.image = textures.projectiles_list[image].convert_alpha()  # texture
                self.hitbox_rotate = spinning[4]  # rotate hitbox (texture doesnt always align with hitbox)
            self.__class__.projectile_list.append(self)
            self.max_frames = max_time  # life span
            self.frames = 0
            self.rotation = spinning[0]  # angle from middle
            self.spinning_x_offset = spinning[1]  # offset x and y
            self.spinning_y_offset = spinning[2]
            self.radian_offset = radian_offset  # (radian or cartesian)
            self.spinning_dot_rotation = spinning[3]  # rotation angle from pos with offset relative to x,y

            self.created()  # run first func

        def render_ff(self):
            if Battle.running_battle:
                self.y += self.velocity * math.sin(self.degree)
                self.x += self.velocity * math.cos(self.degree)

            temp_offset = (self.spinning_x_offset * math.cos(self.spinning_y_offset), self.spinning_x_offset * math.sin(self.spinning_y_offset)) if self.radian_offset else (self.spinning_x_offset, self.spinning_y_offset)
            # self.hitbox = []
            # rect_radius = math.sqrt(self.height ** 2 + self.width ** 2) / 2
            # try:
            #     rect_angle = math.atan(self.height / self.width)
            # except ZeroDivisionError:
            #     rect_angle = PI / 2
            if self.image == "":
                # if self.rotation % (2*PI) == 0 and self.spinning_dot_rotation % (2*PI) == 0:
                #     pygame.draw.rect(Screen.win, self.color, (int(self.x + temp_offset[0] - self.width / 2 + 305), int(self.y + temp_offset[1] - self.height / 2 + 305), self.width, self.height))
                #     self.hitbox = [(int(self.x + temp_offset[0] - self.width / 2 + 305), int(self.y + temp_offset[1] - self.height / 2 + 305)), (int(self.x + temp_offset[0] + self.width / 2 + 305), int(self.y + temp_offset[1] - self.height / 2 + 305)), (int(self.x + temp_offset[0] + self.width / 2 + 305), int(self.y + temp_offset[1] + self.height / 2 + 305)), (int(self.x + temp_offset[0] - self.width / 2 + 305), int(self.y + temp_offset[1] + self.height / 2 + 305))]
                # elif self.spinning_dot_rotation % (2*PI) == 0:
                #     for dot in range(4):
                #         temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (PI if dot in (0, 3) else 0) + self.rotation
                #         self.hitbox.append((int(305 + temp_offset[0] + self.x + rect_radius * math.cos(temp_angle)), int(305 + temp_offset[1] + self.y + rect_radius * math.sin(temp_angle))))
                #     pygame.draw.polygon(Screen.win, self.color, self.hitbox)
                # else:
                #     for dot in range(4):
                #         temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (PI if dot in (0, 3) else 0) + self.rotation
                #         temp2_angle = math.atan2(rect_radius*math.sin(temp_angle)+temp_offset[1], rect_radius*math.cos(temp_angle)+temp_offset[0])+self.spinning_dot_rotation
                #         temp2_radius = math.sqrt(rect_radius**2+temp_offset[1]**2+temp_offset[0]**2+2*rect_radius*(temp_offset[0]*math.cos(temp_angle)+temp_offset[1]*math.sin(temp_angle)))
                #         self.hitbox.append((int(305 + self.x + math.cos(temp2_angle)*temp2_radius), int(305 + self.y + math.sin(temp2_angle)*temp2_radius)))
                #     pygame.draw.polygon(Screen.win, self.color, self.hitbox)
                self.hitbox = blit_rotated_rect(self.x + 305, self.y + 305, self.width, self.height, self.color, self.rect_width, self.rotation, temp_offset, self.spinning_dot_rotation)
            else:
                # if self.rotation % (2 * PI) == 0 and self.spinning_dot_rotation % (2*PI) == 0 and self.hitbox_rotate % (2 * PI) == 0:
                #     Screen.win.blit(self.image, (int(self.x + temp_offset[0] + 305 - self.image.get_rect().width / 2), int(self.y + temp_offset[1] + 305 - self.image.get_rect().height / 2)))
                #     self.hitbox = [(int(self.x + temp_offset[0] - self.width / 2 + 305), int(self.y + temp_offset[1] - self.height / 2 + 305)), (int(self.x + temp_offset[0] + self.width / 2 + 305), int(self.y + temp_offset[1] - self.height / 2 + 305)), (int(self.x + temp_offset[0] + self.width / 2 + 305), int(self.y + temp_offset[1] + self.height / 2 + 305)), (int(self.x + temp_offset[0] - self.width / 2 + 305), int(self.y + temp_offset[1] + self.height / 2 + 305))]
                # else:
                #     rotated_image = pygame.transform.rotate(self.image, -1 * (self.rotation + self.spinning_dot_rotation) / PI * 180)
                #     new_rect = rotated_image.get_rect(center=self.image.get_rect(center=(int(self.x+math.sqrt(temp_offset[0]**2+temp_offset[1]**2)*math.cos(math.atan2(temp_offset[1], temp_offset[0])+self.spinning_dot_rotation)), int(self.y+math.sqrt(temp_offset[0]**2+temp_offset[1]**2)*math.sin(math.atan2(temp_offset[1], temp_offset[0])+self.spinning_dot_rotation)))).center)
                #     Screen.win.blit(rotated_image, (int(new_rect.topleft[0] + 305), int(new_rect.topleft[1] + 305)))
                #     for dot in range(4):
                #         temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (PI if dot in (0, 3) else 0) + self.rotation + self.hitbox_rotate
                #         temp2_angle = math.atan2(rect_radius*math.sin(temp_angle)+temp_offset[1], rect_radius*math.cos(temp_angle)+temp_offset[0])+self.spinning_dot_rotation
                #         temp2_radius = math.sqrt(rect_radius**2+temp_offset[1]**2+temp_offset[0]**2+2*rect_radius*(temp_offset[0]*math.cos(temp_angle)+temp_offset[1]*math.sin(temp_angle)))
                #         self.hitbox.append((int(305 + self.x + math.cos(temp2_angle)*temp2_radius), int(305 + self.y + math.sin(temp2_angle)*temp2_radius)))
                # if console_active_list["show hitbox"] == 1:
                #     pygame.draw.polygon(Screen.win, (255, 255, 255), self.hitbox, 1)
                self.hitbox = blit_rotated_texture(self.image, self.x + 305, self.y + 305, self.width, self.height, self.rotation, temp_offset, self.spinning_dot_rotation, self.hitbox_rotate)

            if (not Battle.Sprite.is_moving and self.projectile_application == 1) or (Battle.Sprite.is_moving and self.projectile_application == 2) or self.projectile_application == 3:
                pass
            elif Polygon.intersects(Polygon(self.hitbox), Polygon(Battle.Projectile.player_rect)):
                if random.random() * (Battle.enemy_list[4][4] + 1) / (Ins.player.evasion + 1) >= self.accuracy_modifier:
                    if self.hit() in (True, None):
                        Battle.Sprite.effect(self.projectile_effect, self.projectile_effect_damage, self.projectile_effect_length, self.random_multiplier)
                        temp_armor_boost = ((1.1 if Ins.player.helmet is None else 1 - items[Ins.player.helmet][13]) *
                                            (1.1 if Ins.player.chestplate is None else 1 - items[Ins.player.chestplate][13]) *
                                            (1.1 if Ins.player.leggings is None else 1 - items[Ins.player.leggings][13]))**(1/3)
                        temp_damage = self.attack_modifier * (1.25 if random.random() <= 0.15 else 1) * lvl_amp_func(Battle.enemy_list[4][5], Ins.player.level, self.projectile_damage_type) * player_def_amp() \
                                      * random.uniform(self.random_multiplier[0], self.random_multiplier[1]) * atk_amp_func(Battle.enemy_list[4][1], Ins.player.defense, self.projectile_damage_type) * temp_armor_boost

                        Ins.player.add_hp(round(-1 * temp_damage))

                        if self.projectile_type == 0:
                            self.deleted()
                            self.__class__.projectile_list.remove(self)
                            return 0
                else:
                    animation("1", True, "miss", 12)

            if Battle.running_battle:
                if self.existing() or (self.max_frames != -1 and self.frames >= self.max_frames - 1):
                    self.deleted()
                    self.__class__.projectile_list.remove(self)
                else:
                    self.frames += 1

        def created(self):
            if self._created != "none" and Battle.running_battle:
                return globals()["prc_"+self._created](self)

        def existing(self):
            if self._existing != "none" and Battle.running_battle:
                return globals()["pre_"+self._existing](self)

        def deleted(self):
            if self._deleted != "none" and Battle.running_battle:
                return globals()["prd_"+self._deleted](self)

        def hit(self):
            if self._hit != "none":
                return globals()["prh_"+self._hit](self)

    class Effect:
        effect_list = []

        def __init__(self, name="", effect_time=-1, target_player=True, add_effect="none", exist_effect="none", remove_effect="none", color=(255, 255, 255), stored_data=()):
            self.frames = 0
            self.name = name
            self.max_frames = effect_time
            self.add_effect = add_effect
            self.exist_effect = exist_effect
            self.remove_effect = remove_effect
            self.target_player = target_player
            self.__class__.effect_list.append(self)
            self.prefix = ("p_" if target_player else "e_")
            self.color = color
            self.data = stored_data
            self.self_data = []
            self.created()

        def render_ff(self):

            if (self.max_frames != -1 and self.frames >= (1 if Battle.state_turns else Battle.effect_duration_battle) * self.max_frames) or self.existing():
                self.__class__.effect_list.remove(self)
                self.deleted()
                return True

            self.frames += 1
            return False

        def created(self):
            if self.add_effect != "none":
                if Battle.state_turns:
                    return globals()["t_ec_"+self.prefix+self.add_effect](self)
                else:
                    return globals()["b_ec_" + self.prefix + self.add_effect](self)

        def existing(self):
            if self.exist_effect != "none":
                if Battle.state_turns:
                    return globals()["t_ee_"+self.prefix+self.exist_effect](self)
                else:
                    return globals()["b_ee_" + self.prefix + self.exist_effect](self)

        def deleted(self):
            if self.remove_effect != "none":
                if Battle.state_turns:
                    return globals()["t_ed_"+self.prefix+self.remove_effect](self)
                else:
                    return globals()["b_ed_" + self.prefix + self.remove_effect](self)

        @classmethod
        def list_reset(cls):
            for _effect in cls.effect_list:
                _effect.deleted()
            cls.effect_list.clear()

        @classmethod
        def name_exists(cls, name):
            for _effect in cls.effect_list:
                if _effect.name == name:
                    return True
            return False

    running_battle = True

    ### used only in editor
    max_battle_frames = 2000
    current_battle_frame = 0
    ###

    state_turns = True

    next_attack_delay = 0

    player_last_frame_hp = 0
    enemy_last_frame_hp = 0

    selected_script_attack = 0
    selected_scroll_attack = 0
    selected_weapon_attack = 0
    selected_menu = 0
    selected_battle_menu = 0
    selected_battle_item = 0
    selected_battle_class = 0

    battle_variables = {}

    enemy_hp = 0
    enemy_max_hp = 0
    enemy_height = 0
    enemy_width = 0
    enemy_x = 600
    enemy_y = 150
    enemy_list = []
    texture = None
    background = None

    selected_battle = dict()
    attack_delay_list = dict()

    turn_delay_battle = 90
    effect_duration_battle = 90
    attack_delay = 45

    #  prefix bf
    # functions_list = {
    #     "Projectile": Projectile,
    #     "Hitbox": Hitbox,
    #     "Effect": Effect,
    #     "set_mode": bf_set_mode,
    #     "set_direction": bf_set_direction,
    #     "add_direction": bf_add_direction,
    # }

    @classmethod
    def damage_enemy(cls, damage):
        cls.enemy_hp -= damage
        if cls.enemy_hp > cls.enemy_max_hp:
            cls.enemy_hp = cls.enemy_max_hp

    @staticmethod
    def dictionary_randomizer(dct, frame_list):
        pick_repeatedly = list(dct.keys())[0]
        reorder = list(dct.values())[0]
        frames_iter = iter([])
        if isinstance(frame_list, tuple):
            repeat_count = frame_list[0]
            frame_list = list(frame_list)[1:]
            frames_iter = iter(frame_list)
        else:
            repeat_count = frame_list
        dct = dict(list(dct.items())[1:])
        dct1 = dict(dct)
        max_total = 0
        for key in dct1.keys():
            max_total += key
        for _ in range(repeat_count):
            if reorder:
                max_total = 0
                for key in dct1.keys():
                    max_total += key
            rand_val = random.uniform(0, max_total)
            total = 0
            for key, value in dct1.items():
                total += key
                if rand_val <= total:
                    if isinstance(value, list):
                        if not pick_repeatedly and reorder:
                            index = list(dct.keys()).index(key)
                            for index1 in range(len(value)):
                                yield [frame_list[index][index1], value[index1]]
                        else:
                            temp_iter = next(frames_iter)
                            for index in range(len(value)):
                                yield [temp_iter[index], value[index]]
                    else:
                        if isinstance(frame_list, list):
                            if not pick_repeatedly and reorder:
                                index = list(dct.keys()).index(key)
                                yield [frame_list[index], value]
                            else:
                                yield [next(frames_iter), value]
                        else:
                            yield value
                        if pick_repeatedly or reorder:
                            dct1.pop(key)
                        break

    @staticmethod
    def init_battle(battle_dict):
        Battle.selected_battle = dict()
        for key, value in battle_dict.items():
            if isinstance(key, int) or isinstance(key, str):
                Battle.add_to_frame(key, value)
            elif isinstance(key, tuple):
                for frame in list(Battle.dictionary_randomizer(value, key)):
                    if isinstance(frame[0], int):
                        Battle.add_to_frame(frame[0], frame[1])
                    elif isinstance(frame[0], tuple):
                        for frame1 in frame[0]:
                            Battle.add_to_frame(frame1, frame[1])

    @staticmethod
    def add_to_frame(key, value):
        try:
            if Battle.selected_battle[key]:
                pass
        except KeyError:
            Battle.selected_battle[key] = value
        else:
            if isinstance(Battle.selected_battle[key], tuple):
                if isinstance(value, tuple):
                    Battle.selected_battle[key] = (*Battle.selected_battle[key], *value)
                else:
                    Battle.selected_battle[key] = (*Battle.selected_battle[key], value)
            else:
                if isinstance(value, tuple):
                    Battle.selected_battle[key] = (Battle.selected_battle[key], *value)
                else:
                    Battle.selected_battle[key] = (Battle.selected_battle[key], value)

    @staticmethod
    def read_frame(frame=None):
        try:
            if frame is None:
                frame = Battle.selected_battle[Battle.current_battle_frame]
            elif isinstance(frame, int):
                frame = Battle.selected_battle[frame]
        except KeyError:
            return 0

        if isinstance(frame, list):
            globals()["bf_"+frame[0]](*frame[1:])

        elif isinstance(frame, tuple):
            for frame1 in frame:
                Battle.read_frame(frame1)

        elif isinstance(frame, dict):
            for frame1 in Battle.dictionary_randomizer(list(frame.values())[0], list(frame.keys())[0]):
                Battle.read_frame(frame1)

        elif isinstance(frame, set):
            for frame1 in list(frame):
                Battle.read_frame(Battle.selected_battle[frame1])


class Turns:
    class Enemy:
        enemy_list = []

        def __init__(self, enemy_id):
            turns_list = turns.enemies[enemy_id]
            self.enemy_id = enemy_id
            self.name = turns_list[0]
            self.max_hp = turns_list[2][0]
            self.hp = self.max_hp  # random.randint(round(self.max_hp * 0.85), self.max_hp)
            self.max_mana = turns_list[2][1]
            self.mana = self.max_mana  # random.randint(round(self.max_mana*0.75), self.max_mana)
            self.attack = turns_list[2][2]
            self.defense = turns_list[2][3]
            self.evasion = turns_list[2][4]
            self.accuracy = turns_list[2][5]
            self.level = turns_list[2][6]
            self.loot_table = turns_list[3]
            self.exp = random.randint(turns_list[4][0], turns_list[4][1])
            self.coins = random.randint(turns_list[4][2], turns_list[4][3])
            self.attack_weight = turns_list[5]
            self.info = {}

            self.atk_boost = 0
            self.effects = []

            self.texture = textures.battle_enemies[turns_list[1]]
            self.animation_index = 0
            self.default_animation_index = 0

            self.next_attacks = []
            self.next_attack = None
            self.attack_delay = {i: 0 for i in self.attack_weight}
            self.id = len(self.__class__.enemy_list)
            self.x, self.y = (0, 0)

            if "size" in self.texture:
                self.w, self.h = self.texture["size"]
            else:
                self.w = self.texture[0][0][0].get_width()
                self.h = self.texture[0][0][0].get_height()

            # 0 - starting animation
            # -1 - death animation
            # -2 - hit animation
            _temp = max(self.texture[0].keys())
            self.frame = random.randrange(0, _temp)
            while _temp > 0:
                _temp -= 1
                try:
                    self.texture[0][_temp]
                except KeyError:
                    pass
                else:
                    break
            self.displayed_frame = _temp

            self.is_turn = False
            self.is_alive = True

            self.__class__.enemy_list.append(self)
            self.info = []

        if True:
            def add_hp(self, amount):
                self.hp += amount
                if self.hp > self.max_hp:
                    self.hp = self.max_hp

            def add_mana(self, amount):
                self.mana += amount
                if self.mana > self.max_mana:
                    self.mana = self.max_mana

        def render_ff(self):
            texture = self.texture[self.animation_index]
            try:
                if isinstance(texture[self.frame], bool):
                    if self not in Turns.alive_enemies:
                        self.is_alive = False
                        return
                    self.frame = 0
                    self.displayed_frame = 0
                    if texture[self.frame]:
                        self.animation(self.default_animation_index)
                        texture = self.texture[self.animation_index]
                else:
                    self.displayed_frame = self.frame
            except KeyError:
                pass

            stop = None
            try:
                if self.is_turn:
                    stop = globals()["trn_anm_" + self.enemy_id](self, self.animation_index, self.frame)
            except KeyError:
                pass

            if self.is_turn and Turns.turn_phase == 1 and not Animation.name_exists("attack_delay") and \
                    (self.animation_index == self.default_animation_index or stop):
                if turns.attacks[self.next_attack][9] != -1 and not turns.attacks[self.next_attack][9].split("-")[0].isnumeric():
                    animation(f"aa-{turns.attacks[self.next_attack][9]}", (self.x, self.y), name="attack", point=(237, 276))
                # self.animation(self.default_animation_index)
                Turns.turn_phase = 2

            if self.is_turn:
                if Turns.in_between_delay <= 0:
                    if Turns.turn_phase == 0:
                        self.initiate_attack()
                        Turns.turn_phase = 1
                    elif Turns.turn_phase == 2:
                        if not Animation.name_exists("attack"):
                            self.execute_attack()
                            Turns.turn_phase = 3
                            Turns.in_between_delay = 30
                    elif Turns.turn_phase == 3:
                        Animation.name_remove("attack_name")
                        self.is_turn = False
                        animation("0", 15, ["start_turns"], None)
                else:
                    Turns.in_between_delay -= 1

            pygame.draw.rect(Screen.win, (20, 20, 20), (self.x - self.w // 2, self.y - self.h // 2 - 20, self.w, 15))
            pygame.draw.rect(Screen.win, (80, 255, 80), (self.x - self.w // 2, self.y - self.h // 2 - 20, max(int(self.w * self.hp / self.max_hp), 0), 15))
            pygame.draw.rect(Screen.win, (255, 255, 255), (self.x - self.w // 2, self.y - self.h // 2 - 20, self.w, 15), 2)

            temp = texture[self.displayed_frame]
            Screen.win.blit(texture[self.displayed_frame][0], (temp[1][0] + self.x - temp[0].get_width() // 2, temp[1][1] + self.y - temp[0].get_height() // 2))
            Screen.blit_text(self.name, (self.x - self.w // 2, self.y - self.h // 2 - 36), font8)
            self.frame += 1

            i = 0
            for _effect in self.effects:
                if _effect.name == "":
                    continue
                if _effect.max_frames == -1:
                    duration = "inf"
                else:
                    duration = str(_effect.max_frames - _effect.frames)
                Screen.blit_text(f"{_effect.name}: {duration}", (self.x - self.w // 2, self.y + self.h // 2 + 4 + i), font7, _effect.color)
                i += 23

        def animation(self, index):
            if index != self.animation_index:
                self.animation_index = index
                self.frame = 0
                self.displayed_frame = 0

        def do_turn(self):
            for i in self.attack_delay:
                if self.attack_delay[i] > 0:
                    self.attack_delay[i] -= 1
            Turns.in_between_delay = 20
            self.add_mana(self.max_mana / 10)
            self.is_turn = True
            try:
                globals()["trn_ex_" + self.enemy_id](self)
            except KeyError:
                pass

        def initiate_attack(self):
            temp_attack = ""
            if self.next_attacks:
                temp_attack = self.next_attacks.pop(0)
            else:
                temp_list = [i for i in self.attack_weight if self.attack_delay[i] == 0 and turns.attacks[i][2] <= self.mana and self.attack_weight[i][0] > 0]
                if len(temp_list) == 0:
                    temp_attack = "none"
                else:
                    temp_sum = sum(self.attack_weight[i][0] for i in temp_list)
                    temp_rand = random.random() * temp_sum
                    c = 0

                    for i in temp_list:
                        c += self.attack_weight[i][0]
                        if c > temp_rand:
                            temp_attack = i
                            break

            try:
                self.next_attack = globals()["trn_atk_res_"+self.enemy_id](self, temp_attack)
            except KeyError:
                self.next_attack = temp_attack
            try:
                if self.attack_weight[self.next_attack][1] != -1:
                    self.animation(self.attack_weight[self.next_attack][1])
                else:
                    animation("0", 10, None, None, name="attack_delay")
            except KeyError:
                pass
            animation("3", turns.attacks[self.next_attack][0], turns.attacks[self.next_attack][1], name="attack_name")
            if turns.attacks[self.next_attack][9] != -1 and "-" in turns.attacks[self.next_attack][9]:
                temp = turns.attacks[self.next_attack][9].split("-")
                if temp[0].isnumeric():
                    animation("0", int(temp[0]), ["animation", [f"aa-{'-'.join(temp[1:])}", (self.x, self.y)], {"name": "attack", "point": (237, 276)}], None)
            if "-" in turns.attacks[self.next_attack][6]:
                temp = turns.attacks[self.next_attack][6].split("-")
                animation("0", int(temp[0]), ["sound_effect", '-'.join(temp[1:])], None)

        def execute_attack(self):
            temp_attack = self.next_attack
            temp_hp = int(Ins.player.hp)

            self.attack_delay[temp_attack] = turns.attacks[temp_attack][8] + 1
            temp_attack = turns.attacks[temp_attack]

            if "-" not in temp_attack[6]:
                sounds.play_effect(temp_attack[6])
            self.add_mana(-1 * temp_attack[2])

            _target = []
            if temp_attack[4] == 0:
                _target = [self]
            elif temp_attack[4] == 1:
                _target = list(Turns.alive_enemies)
            elif temp_attack[4] == 2:
                _target = [random.choice(Turns.alive_enemies)]

            hp_list = get_hp_list()

            if random.random() * (self.evasion + 1) / (Ins.player.evasion + 1) >= temp_attack[3][1]:
                _is_crit = random.random() <= temp_attack[3][5][0]
                _temp_critical = temp_attack[3][5][1] if _is_crit else 1
                if _is_crit:
                    animation("fadeText", "crit", (255, 80, 80), 4,
                              point=(random.randint(197, 277), random.randint(206, 346)), layer=1)
                _temp_attack_uniform = random.uniform(temp_attack[3][3][0], temp_attack[3][3][1])

                temp_armor_boost = ((1.1 if Ins.player.helmet is None else 1 - items[Ins.player.helmet][13]) *
                                    (1.1 if Ins.player.chestplate is None else 1 - items[Ins.player.chestplate][13]) *
                                    (1.1 if Ins.player.leggings is None else 1 - items[Ins.player.leggings][13])) ** (1 / 3)
                temp_damage = _temp_attack_uniform * _temp_critical*temp_armor_boost \
                             * lvl_amp_func(self.level, Ins.player.level, temp_attack[7]) * player_def_amp()\
                              * atk_amp_func(self.attack, Ins.player.defense, temp_attack[7]) * temp_attack[3][0] * (self.atk_boost + 1)

                Ins.player.add_hp(round(-1 * temp_damage))

                for i in range(3):
                    if Animation.name_exists(f"atk{i+1}"):
                        Animation.name_remove(f"atk{i+1}")

                _temp_heal = self.defense * temp_attack[3][2] * (self.level / 99 + 1)
                _temp_heal_uniform = random.uniform(temp_attack[3][4][0], temp_attack[3][4][1])

                player_effect = None
                if temp_attack[5] != -1:
                    player_effect = temp_attack[5][2]

                for enemy in _target:
                    _temp_heal_uniform = random.uniform(temp_attack[3][4][0], temp_attack[3][4][1])
                    enemy.add_hp(round(_temp_heal * _temp_heal_uniform))
                    # if round(_temp_heal * _temp_heal_uniform) != 0:
                    #     animation("1", False, round(_temp_heal * _temp_heal_uniform), 4, point=(enemy.x + random.randint(-40, 40), enemy.y + random.randint(-40, 40)), frozen=False, layer=1)

                    if player_effect is False:
                        temp = Battle.Effect(*temp_attack[5], stored_data=[enemy])
                        for _effect in enemy.effects:
                            if _effect.name == temp.name:
                                if temp.max_frames == -1 or _effect.max_frames == -1:
                                    _effect.max_frames = -1
                                else:
                                    _effect.max_frames += temp.max_frames
                                Battle.Effect.effect_list.remove(temp)
                                break
                        else:
                            enemy.effects.append(temp)

                if player_effect is True:
                    temp = Battle.Effect(*temp_attack[5], stored_data=_target)
                    for _effect in Battle.Effect.effect_list:
                        if not _effect.target_player or _effect is temp:
                            continue
                        if _effect.name == temp.name:
                            if temp.max_frames == -1 or _effect.max_frames == -1:
                                _effect.max_frames = -1
                            else:
                                _effect.max_frames += temp.max_frames
                            Battle.Effect.effect_list.remove(temp)
                            break

                # if _temp_heal != 0:
                #     animation(1, False, _temp_heal, 4, point=(self.x + random.randint(-40, 40), self.y + random.randint(-40, 40)), frozen=False, name="atk1", layer=1)

                # if round(temp_damage) != 0:
                #     animation("1", True, round(-temp_damage), 4, point=(random.randint(197, 277), random.randint(206, 346)), frozen=False, layer=1)

                hit = True
            else:
                animation("1", True, "miss", 4, point=(random.randint(197, 277), random.randint(206, 346)), frozen=False, layer=1)  # animation miss
                hit = False
            try:
                globals()["atk_fnc_e_" + self.next_attack.replace(" ", "_")](self, hit, _target)
            except KeyError:
                pass
            try:
                globals()["trn_atk_" + self.enemy_id](self, hit, temp_hp)
            except KeyError:
                pass
            self.next_attack = None
            # attacks
            display_hp_list(hp_list)

    @classmethod
    def render_ff(cls):
        for enemy in Turns.Enemy.enemy_list:
            if not enemy.is_turn and enemy.is_alive:
                enemy.render_ff()

        _line = Screen.window_width - 60
        Screen.win.blit(textures.misc_textures["now"], (_line, 60))
        Screen.win.blit(textures.misc_textures["next"], (_line - 55, 60))
        for obj in (cls.turn_order + cls.turn_order_next):
            if obj is None:
                Screen.win.blit(textures.player_sprite_down, (_line + 2, 7))
            else:
                Screen.win.blit(obj.texture["profile"], (_line, 5))
                if Turns.picking_enemy == 1 and obj is cls.player_enemy_object:
                    pygame.draw.line(Screen.win, (255, 255, 255), (_line, 58), (_line + 50, 58), 3)
            _line -= 55

    @classmethod
    def proceed_turn(cls):
        if cls.turn_order[0] is None:
            for _effect in Battle.Effect.effect_list:
                if _effect.target_player:
                    _effect.render_ff()
        else:
            enemy = cls.turn_order[0]
            for _effect in enemy.effects:
                if _effect.render_ff():
                    enemy.effects.remove(_effect)

        for enemy in Turns.Enemy.enemy_list:
            if enemy in cls.alive_enemies and enemy.hp <= 0:
                if -1 in enemy.texture:
                    enemy.animation(-1)
                else:
                    enemy.is_alive = False
                while enemy in Turns.turn_order_next:
                    Turns.turn_order_next.remove(enemy)
                Turns.alive_enemies.remove(enemy)
                if enemy in Turns.turn_order:
                    Turns.turn_order.remove(enemy)
                try:
                    globals()["trn_dth_"+enemy.enemy_id](enemy)
                except KeyError:
                    pass

        if Ins.player.hp <= 0:
            Animation.name_object("player").info[0] = -2
            Animation.name_object("player").info[1] = 0
            animation("0", 50, ["turns_battle_death"], None)
            battle_stopped(True)
            return

        if len(Turns.alive_enemies) == 0:
            Ins.stats.turns_battles_won += 1
            battle_stopped(True)
            return

        else:
            del cls.turn_order[0]
            cls.turn_phase = 0
            Temp.pending_reset = False

            if len(cls.turn_order) == 0:
                cls.turn_order = list(cls.turn_order_next)
                random.shuffle(cls.turn_order_next)
                cls.turn_count += 1
            if cls.turn_order[0] is not None:
                cls.turn_order[0].do_turn()
                cls.enemy_turn = True
            else:
                cls.picking_enemy = 0
                Battle.selected_battle_menu = 0
                cls.enemy_turn = False
                Ins.player.add_mana(Ins.player.max_mana / 20)

                for i in Battle.attack_delay_list:
                    if Battle.attack_delay_list[i] > 0:
                        Battle.attack_delay_list[i] -= 1

                for _passive in Ins.player.passive_list:
                    globals()["fp_" + _passive]()
            try:
                globals()["trnb_ex_"+str(cls.turns_id)]()
            except KeyError:
                pass

    pause = False

    turn_count = 0
    selected_menu = 0
    turns_id = ""
    enemy_turn = True
    player_selected_attack = []
    player_selected_enemy = 0
    picking_enemy = 0
    player_enemy_object = None
    player_weapon_boost = 0

    in_between_delay = 0
    turn_phase = 0
    turns_list = []

    background = None
    positions_list = [[(680, 299)],
                      [(660, 163), (660, 472)],
                      [(608, 317), (760, 193), (772, 466)],
                      [(562, 202), (570, 420), (762, 406), (775, 187)],
                      [(481, 313), (622, 190), (788, 194), (786, 446), (628, 433)]]
    pending_actions = {}

    turn_order = []
    turn_order_next = []
    alive_enemies = []


class Animation:
    animation_list = []
    animation_saved = {}
    animated = False

    def __init__(self, animation_index, position, info, name, immune, layer, frozen, reference, duration):
        if name != "":
            if name in self.__class__.animation_saved:
                print(f"error: {name}")
                error.error(error.AnimationError, 1)
            self.__class__.animation_saved[name] = self
        self.name = name
        if position is None:
            self.x = None
            self.y = None
        else:
            self.x = position[0]
            self.y = position[1]
        self.frame = 0
        self.index = animation_index
        self.info = info
        # index - animation - info
        # 0 - timer - (time, end_func, existing_func)
        # 1 - display dmg - (damage, text, decay)
        # 2 - death screen - [*blood_drop]
        # 3 - display attack - (text, color)
        # 4 - fade to black
        # player - display player in turns
        self.layer = layer
        self.immune = immune
        self.frozen = frozen
        self.duration = duration
        for i in range(len(self.__class__.animation_list)):
            if self.__class__.animation_list[i].layer > self.layer:
                self.__class__.animation_list.insert(i, self)
                break
        else:
            self.__class__.animation_list.append(self)
        self.ref = reference

    def set_layer(self, layer):
        self.__class__.animation_list.remove(self)
        self.layer = layer
        for i in range(len(self.__class__.animation_list)):
            if self.__class__.animation_list[i].layer > self.layer:
                self.__class__.animation_list.insert(i, self)
                break
        else:
            self.__class__.animation_list.append(self)

    @classmethod
    def render_ff(cls, layer=True):
        if layer is False:
            return
        if cls.animated is True:
            return
        if layer is not True and cls.animated is not False and cls.animated >= layer:
            return

        for an in list(cls.animation_list):
            if cls.animated is not False and an.layer <= cls.animated:
                continue
            if layer is not True and an.layer > layer:
                break
            if an.frozen:
                continue
            if (an.duration != -1 and an.frame >= an.duration) or an.animate():
                if an in cls.animation_list:
                    cls.object_remove(an)
            else:
                an.frame += 1

        cls.animated = layer

    @classmethod
    def name_exists(cls, name):
        return name in cls.animation_saved

    @classmethod
    def name_object(cls, name):
        try:
            return cls.animation_saved[name]
        except KeyError:
            return None

    @classmethod
    def name_remove(cls, name):
        cls.animation_list.remove(cls.animation_saved.pop(name))

    @classmethod
    def object_remove(cls, obj):
        if obj.name == "":
            cls.animation_list.pop(cls.animation_list.index(obj))
        else:
            cls.name_remove(obj.name)

    def reset_name(self):
        self.__class__.animation_saved.pop(self.name)
        self.name = ""

    def animate(self):
        if self.index == "0":
            if self.info[2] is not None:
                globals()["anm_" + self.info[2][0]](*self.info[2][1:])
            if self.frame >= self.info[0]:
                if self.info[1] is not None:
                    globals()["anm_" + self.info[1][0]](*self.info[1][1:])
                return True
        elif self.index == "1":
            color = (80, 255, 80) if self.info[0] > 0 else ((120, 120, 120) if self.info[0] == 0 else (255, 80, 80))
            Screen.blit_text(str(self.info[1]), (self.x, self.y), font4, color, (0.5, 0), 255 - self.info[2] * self.frame)
            self.y -= 1
            if 255 - self.info[2] * self.frame <= 0:
                return True
        elif self.index == "fadeText":
            Screen.blit_text(str(self.info[0]), (self.x, self.y), font4, self.info[1], (0.5, 0), 255 - self.info[2] * self.frame)
            if 255 - self.info[2] * self.frame <= 0:
                return True
        elif self.index == "2":
            for bloodDrop in self.info:
                pygame.draw.rect(Screen.win, (80 - bloodDrop[0], 0, 0), (bloodDrop[1], 0, bloodDrop[2], min(int(self.frame / bloodDrop[3] - bloodDrop[4]), bloodDrop[5])))
        elif self.index == "3":
            surface2 = font3.render(self.info[0], False, self.info[1])
            if len(self.info) == 3:
                pos = self.info[2]
            else:
                pos = 55
            pygame.draw.rect(Screen.win, (0, 0, 0), (int(Screen.window_width / 2 - surface2.get_rect().width / 2 - 15), pos, surface2.get_rect().width + 30, 45))
            pygame.draw.rect(Screen.win, (255, 255, 255), (int(Screen.window_width / 2 - surface2.get_rect().width / 2 - 15), pos, surface2.get_rect().width + 30, 45), 1)
            Screen.win.blit(surface2, (int(Screen.window_width / 2 - surface2.get_rect().width / 2), pos))
        elif self.index == "4":
            surface1 = pygame.Surface((Screen.window_width, Screen.window_height))
            surface1.set_alpha(int(-255*(min(self.frame / 15, 1, 7/3 - self.frame / 15)-1)**2+255))
            surface1.fill((0, 0, 0))
            Screen.win.blit(surface1, (0, 0))
            if self.frame == 18 and self.info[0] is not None:
                if isinstance(self.info[0][0], list):
                    for cmd in self.info[0]:
                        globals()["anm_" + cmd[0]](*cmd[1:])
                else:
                    globals()["anm_"+self.info[0][0]](*self.info[0][1:])
            if self.frame >= 35:
                if self.info[1] is not None:
                    if isinstance(self.info[1][0], list):
                        for cmd in self.info[1]:
                            globals()["anm_" + cmd[0]](*cmd[1:])
                    else:
                        globals()["anm_"+self.info[1][0]](*self.info[1][1:])
                return True
        elif self.index == "animation":
            texture = textures.battle_animations[self.info[0]]
            if "align" not in texture:
                al = 0.5
            else:
                al = texture["align"]
            if "align_self" not in texture:
                als = 0.5
            else:
                als = texture["align_self"]
            if "cut" in texture:
                if self.name != "" and texture["cut"] <= self.frame:
                    self.reset_name()

            if self.ref is None:
                h = 100
            else:
                h = self.ref.height

            if self.frame in texture:
                self.info[1] = texture[self.frame]
                if self.info[1] is True:
                    return True
            Screen.win.blit(self.info[1][0], (self.info[1][1][0] + self.x - self.info[1][0].get_width() // 2,
                                              round(self.info[1][1][1] + self.y + h * (al - 0.5) - self.info[1][0].get_height() * als)))
        elif self.index == "player":
            sizes = [(50, 100, 0), (120, 100, 0), (200, 200, 10), (120, 100, 0), (200, 200, 29)]
            texture = textures.battle_enemies["player"][self.info[0]]
            try:
                if isinstance(texture[self.info[1]], bool):
                    self.info[1] = 0
                    self.info[2] = 0
                    if texture[self.info[1]]:
                        self.info[0] = 0
                        texture = textures.battle_enemies["player"][self.info[0]]
                else:
                    self.info[2] = self.info[1]
            except KeyError:
                pass
            Screen.win.blit(texture[self.info[2]][0], (texture[self.info[2]][1][0] + self.x - sizes[self.info[0]][0] // 2 + sizes[self.info[0]][2], texture[self.info[2]][1][1] + self.y - sizes[self.info[0]][1] // 2))
            self.info[1] += 1
        elif self.index == "aa-1":
            pygame.draw.line(Screen.win, (255, 255, 255), self.info[0], (self.x, self.y), 15 - self.frame)
            if self.frame >= 15:
                return True
        elif self.index == "aa-samuraiSlash":
            if self.frame >= 23:
                surface1 = pygame.Surface((Screen.window_width, Screen.window_height))
                surface1.set_alpha(int(255 - (self.frame - 23) * 60))
                surface1.fill((255, 255, 255))
                Screen.win.blit(surface1, (0, 0))
            elif self.frame >= 20:
                for i in range(20):
                    blit_rotated_rect(self.x + self.info[i][1], self.y + self.info[i][2], 1, 1500, (255, 255, 255), 0.0, self.info[i][0])
            else:
                for i in range(int(self.frame ** 3 / 1300)):
                    blit_rotated_rect(self.x + self.info[i][1], self.y + self.info[i][2], 1, 1500, (255, 255, 255), 0.0, self.info[i][0])

            if self.frame >= 26:
                return True
        elif self.index == "aa-slash1":
            if self.info[1] == 0:
                _sin = math.sin(self.info[0])
                _cos = math.cos(self.info[0])
                len1 = min_max(0, 80*self.frame, 300) - 300 // 2
                len2 = min_max(0, 80*self.frame - 310, 300) - 300 // 2
                if self.frame != 0 and len1 == len2:
                    self.info[1] = 1
                    return False
                pygame.draw.line(Screen.win, (255, 255, 255), (self.x + _cos * len1, self.y + _sin * len1),
                                    (self.x + _cos * len2, self.y + _sin * len2), 2)
            else:
                self.info[1] += 1
                if self.info[1] >= 7:
                    return True
        elif self.index == "aa-fireball1":
            pos = (round(self.info[0][0] + (self.x - self.info[0][0]) * self.frame / 15),
                   round(self.info[0][1] + (self.y - self.info[0][1]) * self.frame / 15))
            pygame.draw.circle(Screen.win, (255, 120, 20), pos, 20)
            if self.frame >= 15:
                return True
        elif self.index == "aa-heal1":
            if not Particles.tag_exists("heal"):
                return True
        elif self.index == "aa-purpleRay":
            pygame.draw.line(Screen.win, (200, 50, 230), (self.info[0][0]-83, self.info[0][1]-16), (self.x, self.y), 15 - self.frame)
            if self.frame >= 15:
                return True
        elif self.index == "aa-purpleBlast":
            pos = (round(self.info[0][0] - 63 + (self.x - self.info[0][0] + 63) * self.frame / 15),
                   round(self.info[0][1] - 26 + (self.y - self.info[0][1] + 26) * self.frame / 15))
            pygame.draw.circle(Screen.win, (140, 30, 170), pos, 20)
            if self.frame >= 15:
                return True
        elif self.index == "aa-tripleSlash1":
            if self.frame % 10 == 0:
                animation("aa-slash1", (self.x, self.y), point=(237, 276))
            if self.frame >= 29:
                return True
        elif self.index == "aa-slash2":
            if self.frame % 12 == 0:
                animation("aa-slash1", (self.x, self.y), point=(237, 276))
            if self.frame >= 23:
                return True
        elif self.index == "aad-arrow1":
            _pos = (8 - self.frame) * 60
            pygame.draw.line(Screen.win, (255, 255, 255), (self.x - _pos - 15, self.y - _pos - 15),
                             (self.x - _pos, self.y - _pos), 2)
            if self.frame >= 8:
                return True
        elif self.index == "aa-purify1":
            if self.frame == 0:
                self.set_layer(-100)
            width = self.frame * 4
            surface1 = pygame.Surface((width, 800))
            surface1.set_alpha((15 - self.frame) * 17)
            surface1.fill((200, 230, 80))
            Screen.win.blit(surface1, (self.x - width // 2, self.y + self.ref.h // 2 - 800))
            if self.frame >= 15:
                return True
        elif self.index == "flash":
            alpha = 255 - (255 / self.info[1]) * max(self.frame - self.info[2], 0)
            if alpha <= 0:
                return True
            surface1 = pygame.Surface((Screen.window_width, Screen.window_height))
            surface1.set_alpha(int(alpha))
            surface1.fill(self.info[0])
            Screen.win.blit(surface1, (0, 0))
        elif self.index == "aa-flurry1":
            if self.frame % 3 != 0:
                animation("slash1All", (self.x, self.y), point=(237, 276))
            if self.frame >= 10:
                return True
        #####################
        return False


class Requires:
    scrolls_req = None
    scripts_req = None
    text_condition = None
    text_overdo = None
    classes_req = None

    @classmethod
    def text_update(cls):
        cls.text_condition = {
            **{i: True for i in texts.text_list},
            ####
            "ma_ca_guard1": Ins.player.item_amount("sigil of permission") >= 1,
            "save_progress": True,
            "ma_ca_guard2": Ins.player.level >= 3,
            "ma_man1": Ins.player.item_amount("slime core earing") >= 1,
            "ma_sailor": Ins.player.item_amount("skeleton contract") >= 1,
            "ma_orc": Ins.player.item_amount("bandage") >= 1,
            "ma_berserker": Ins.player.item_amount("worn out sword") >= 1,
            "ma_woman1": Ins.fv.ma_jessica >= 3,
            "ma_port_boat": hp_get_sigil_lvl() >= 2,
            "ma_priestess": Ins.player.coins >= 150 and Ins.player.item_amount("small mana potion") >= 1,
        }
        cls.text_overdo = {
            **{i: True for i in texts.text_list},
            ###
            "shop1": Ins.fv.shop1_overdo,
            "ma_ca_guard1": Ins.fv.ma_pass_forest,
            "ma_ca_guard3": Ins.fv.guard3_overdo,
            "ma_ca_guard2": Ins.fv.guard2_overdo,
            "ma_pa_guard": not Ins.fv.script1,
            "ma_man1": Ins.fv.ma_man_overdo,
            "ma_orc": Ins.fv.ma_orc_overdo,
            "ma_samurai": not Ins.fv.apple,
            "sp_ninja": not Ins.fv.ninja,
        }

    @classmethod
    def scr_update(cls):
        cls.scrolls_req = {
            1: [Ins.fv.scroll1, "you can get this scroll from danny in mainter"],
            2: [Ins.fv.priestess, "talk to the priestess in the forest"]
        }
        cls.scripts_req = {
            1: [Ins.fv.script1, "you can get this script from the royal palace of mainter"],
            2: [Ins.fv.apple, "kill a samurai's apple in one hit"],
        }

    @classmethod
    def class_update(cls):
        cls.classes_req = {
            1: [Ins.fv.berserker, "berserker quest not finished"],
            2: [Ins.fv.ninja, "win against the ninja"]
        }


class Particles:
    particle_list = []
    particles = {
        "triangle": ((1, 0), (1, 2 * PI / 3), (1, 4 * PI / 3)),
        "square": ((1, 0), (1, PI / 2), (1, PI), (1, 3 * PI / 2)),
        "pentagon": ((1, 0), (1, 2 * PI / 5), (1, 4 * PI / 5), (1, 6 * PI / 5), (1, 8 * PI / 5)),
        "star": ((1, 0), (1/3, PI / 5), (1, 2 * PI / 5), (1/3, 3 * PI / 5), (1, 4 * PI / 5), (1/3, 5 * PI / 5), (1, 6 * PI / 5), (1/3, 7 * PI / 5), (1, 8 * PI / 5), (1/3, 9 * PI / 5)),
        "arrow": ((1, 0), (0.7211, 0.9828), (1/2, 0.6435), (0.7681, 2.7403), (0.7681, -2.7403), (1/2, -0.6435), (0.7211, -0.9828)),
        "plus": ((1, PI/10), (1, -PI/10), (0.437, -PI/4), (1, -4*PI/10), (1, -6*PI/10), (0.437, -3*PI/4), (1, -9*PI/10), (1, 9*PI/10), (0.437, 3*PI/4), (1, 6*PI/10), (1, 4*PI/10), (0.407, PI/4)),
    }
    directions = {
        "up": [-3*PI/4, -PI/4],
        "strict_up": [-5*PI/8, -3*PI/8],
        "right": [-PI / 4, PI / 4],
        "strict_right": [-PI / 8, PI / 8],
        "left": [3 * PI / 4, 5 * PI / 4],
        "strict_left": [7 * PI / 8, 9 * PI / 8],
        "down": [PI / 4, 3 * PI / 4],
        "strict_down": [3 * PI / 8, 5 * PI / 8],
        "all": [-PI, PI],
    }
    rendered = False
    tag_list = {}

    def __init__(self, _type, size, _color, point, angle, velocity, full, gravity, gravity_angle, begin_func, exist_func, death_func, rotation_start, rotation_speed, alpha, tags):
        self.rotate = rotation_start
        self.rotate_speed = rotation_speed
        self.exist_func = copy.deepcopy(exist_func)
        self.death_func = copy.deepcopy(death_func)
        self.size = size
        self.type = _type
        self.x, self.y = point
        self.full = full
        self.alpha = alpha

        # self.angle = angle
        # self.velocity = 64 * velocity
        # self.gravity = 64 * gravity
        # self.gravity_angle = gravity_angle

        self.frame = -1
        self.color = _color
        self.velocity = [64 * velocity * math.cos(angle), 64 * velocity * math.sin(angle)]
        self.gravity = [64 * gravity * math.cos(gravity_angle), 64 * gravity * math.sin(gravity_angle)]
        self.forces = []

        self.__class__.particle_list.append(self)
        if tags == "":
            pass
        elif isinstance(tags, list):
            for tag in tags:
                if tag in self.__class__.tag_list:
                    self.__class__.tag_list[tag] += 1
                else:
                    self.__class__.tag_list[tag] = 0
        else:
            if tags in self.__class__.tag_list:
                self.__class__.tag_list[tags] += 1
            else:
                self.__class__.tag_list[tags] = 0
            tags = [tags]
        self.tags = tags

        if begin_func != "none":
            if isinstance(begin_func, str):
                globals()["prt_bg_" + begin_func](self)
            elif isinstance(begin_func[0], str):
                globals()["prt_bg_" + begin_func[0]](self, *begin_func[1:])
            else:
                for fnc in begin_func:
                    globals()["prt_bg_" + fnc[0]](self, *fnc[1:])

    def render(self):

        self.forces.clear()

        temp_bool = False
        if self.exist_func != "none":
            if isinstance(self.exist_func, str):
                temp_bool = globals()["prt_ex_" + self.exist_func](self)
            elif isinstance(self.exist_func[0], str):
                temp_bool = globals()["prt_ex_" + self.exist_func[0]](self, *self.exist_func[1:])
            else:
                for fnc in self.exist_func:
                    temp_bool = globals()["prt_ex_" + fnc[0]](self, *fnc[1:]) or temp_bool

        if temp_bool or not -500 <= self.x <= Screen.window_width + 500 or not -500 <= self.y <= Screen.window_height + 500:
            if self.death_func != "none":
                if isinstance(self.death_func, str):
                    globals()["prt_dth_" + self.death_func](self)
                elif isinstance(self.death_func[0], str):
                    globals()["prt_dth_" + self.death_func[0]](self, *self.death_func[1:])
                else:
                    for fnc in self.death_func:
                        globals()["prt_dth_" + fnc[0]](self, *fnc[1:])
            self.remove()
            return

        for i in range(Ins.settings.particle_iterations):
            self.velocity[0] += self.gravity[0] / (30 * Ins.settings.particle_iterations)
            self.velocity[1] += self.gravity[1] / (30 * Ins.settings.particle_iterations)
            for force in self.forces:
                self.velocity[0] += force[0] / (30 * Ins.settings.particle_iterations)
                self.velocity[1] += force[1] / (30 * Ins.settings.particle_iterations)
            self.x += self.velocity[0] / (30 * Ins.settings.particle_iterations)
            self.y += self.velocity[1] / (30 * Ins.settings.particle_iterations)
        ###################
        surface1 = pygame.Surface((2*self.size + 4, 2*self.size + 4), pygame.SRCALPHA)
        if self.type == "circle":
            pygame.draw.circle(surface1, self.color, (round(self.size + 2), round(self.size + 2)), round(self.size), self.full)
        else:
            pygame.draw.polygon(surface1, self.color,
                                [[round(2 + self.size + self.size * rad[0] * math.cos(rad[1] + self.rotate)), round(2 + self.size + self.size * rad[0] * math.sin(rad[1] + self.rotate))]
                                 for rad in self.__class__.particles[self.type]], self.full)
        if round(self.alpha) < 255:
            surface1.set_alpha(round(self.alpha))
        Screen.win.blit(surface1, (self.x - self.size - 2, self.y - self.size - 2))
        ###################
        self.rotate += self.rotate_speed
        self.frame += 1

    def remove(self):
        self.__class__.particle_list.pop(self.__class__.particle_list.index(self))
        if self.tags == "":
            pass
        elif isinstance(self.tags, list):
            for tag in self.tags:
                self.__class__.tag_list[tag] -= 1
        else:
            self.__class__.tag_list[self.tags] -= 1

    @classmethod
    def tag_exists(cls, tag):
        return cls.tag_list[tag] > 0

    @classmethod
    def get_tag(cls, tag):
        return [part for part in cls.particle_list if tag in part.tags]

    @classmethod
    def render_ff(cls):
        cls.rendered = True
        for prt in cls.particle_list:
            prt.render()


# methods
if True:
    def display_map():
        # if Screen.selected_map_str == "map1":
        #    Screen.win.blit(Screen.map_layer[int(not Ins.fv.text1_v)], (-Screen.camera_x, -Screen.camera_y))
        # elif Screen.selected_map_str == "map3":
        #    Screen.win.blit(Screen.map_layer[int(not Ins.fv.text2_v)], (-Screen.camera_x, -Screen.camera_y))
        pass

    def load_save():
        importlib.reload(maps)
        reset_data()
        Menu.reloading = True
        _f = open(f"save/world{Menu.selected_world}.txt", "rb")
        temp = Ins.player, Ins.ap, Ins.fv, Ins.stats = pickle.load(_f)
        _f.close()

        t = Player(), AP(), FV(), Stats()
        for obj in range(4):
            for attr in vars(t[obj]):
                if attr not in vars(temp[obj]):
                    setattr(temp[obj], attr, getattr(t[obj], attr))

            remove = []
            for attr in vars(temp[obj]):
                if attr not in vars(t[obj]):
                    remove.append(attr)

            for attr in remove:
                delattr(temp[obj], attr)

        Ins.ap.update()

        for i in Ins.ap.run_on_reload:
            if isinstance(i, list):
                globals()[i[0]](*i[1:])
            else:
                globals()[i]()

        Requires.scr_update()
        Requires.class_update()
        Requires.text_update()
        Screen.select_map(Ins.ap.player_map)
        sounds.play(Screen.map_song)
        Menu.reloading = False

    def key_list():
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
                Screen.run = False
                Screen.runState = ""

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

    def proceed_mission(mission_str, stage=-1, skip=True):
        # -1: increase mission by one
        #
        current_stage = Ins.ap.mission_progress_list[mission_str]

        if current_stage is True or stage is False:
            return 0

        if stage == -1 and stage is not True:
            if current_stage is False:
                current_stage = 0
            else:
                Screen.message_updated_active = Screen.message_updated_time
                Screen.message_updated_msg = "journal updated!"
                current_stage += 1

        elif skip:
            if stage is True:
                Screen.message_updated_msg = "mission complete!"
                Screen.message_updated_active = Screen.message_updated_time
                current_stage = True

            elif current_stage is False:
                Screen.message_updated_msg = "journal updated!"
                Screen.message_updated_active = Screen.message_updated_time
                current_stage = stage

            elif stage == current_stage:
                if current_stage is False:
                    current_stage = 0

            elif stage > current_stage:
                Screen.message_updated_msg = "journal updated!"
                Screen.message_updated_active = Screen.message_updated_time
                current_stage = stage

        else:
            if current_stage is False and stage == 0:
                current_stage = 0
            else:
                if stage is True:
                    stage = len(mission_stats_list[mission_str][0])

                if stage == current_stage + 1:
                    current_stage += 1
                    Screen.message_updated_msg = "journal updated!"
                    Screen.message_updated_active = Screen.message_updated_time

        if current_stage >= len(mission_stats_list[mission_str][0]):
            current_stage = True
            Screen.message_updated_msg = "mission complete!"
            Screen.message_updated_active = Screen.message_updated_time

        Ins.ap.mission_progress_list[mission_str] = current_stage

    def start_cut_scene(cut_scene_str):
        cut_scene_list = cutscene.cut_scene_list[cut_scene_str]
        Screen.cutSceneMap = maps.map_list[cut_scene_list[1]]
        Screen.cutSceneList = cut_scene_list[0]
        Screen.cutSceneMaxFrame = cut_scene_list[2]
        Screen.cutSceneFunc = cut_scene_list[5]
        Screen.resize(64 * cut_scene_list[8][0], 64 * cut_scene_list[8][1])
        Screen.cutSceneFrame = 0

        if cut_scene_list[7] is None:
            Screen.cutSceneCameraX = float(Screen.camera_x)
            Screen.cutSceneCameraY = float(Screen.camera_y)
        else:
            Screen.cutSceneCameraX = cut_scene_list[7][0]
            Screen.cutSceneCameraY = cut_scene_list[7][1]

        if cut_scene_list[3] != sounds.get_current_song():
            sounds.play(cut_scene_list[3], loops=0)

        # sounds.last_played_no_delay()
        Screen.cutSceneContinueSong = cut_scene_list[6]

        pygame.display.set_caption(cut_scene_list[4])
        Screen.set_state("cutscene")

    def enter_shop(shop_id):
        Screen.shopId = shop_id
        Screen.shopIndex = 0
        Screen.set_state("shop")
        sounds.play_effect("effect10")
        Screen.shopIsBuying = False
        Screen.is_displaying = False
        Screen.displayed_msg = ""
        Screen.shopMode = False
        Screen.shopSellPage = 0
        Screen.description_page = 0
        _items_in_page = 0
        Screen.description_page = 0

    def run_settings(in_game):
        if keysDown[Ins.settings.move_up] and not keysHeld["tab"]:
            sounds.play_effect("effect6")
            if Menu.choose in (10, 16):
                Menu.choose -= 7
            elif Menu.choose in (3, 25):
                Menu.choose -= 2
            else:
                Menu.choose -= 1
            if Menu.choose < 3:
                Menu.choose += 23

        if keysDown[Ins.settings.move_down] and not keysHeld["tab"]:
            sounds.play_effect("effect6")
            if Menu.choose == 9:
                Menu.choose += 7
            elif Menu.choose == 24:
                Menu.choose += 2
            else:
                Menu.choose += 1
            if Menu.choose > 25:
                Menu.choose -= 23

        if not keysHeld["tab"] and (keysDown[Ins.settings.move_right] or keysDown[Ins.settings.move_left]):
            if 4 <= Menu.choose <= 9:
                Menu.choose += 6
                sounds.play_effect("effect6")
            elif 10 <= Menu.choose <= 15:
                sounds.play_effect("effect6")
                Menu.choose -= 6
            elif Menu.choose == 24:
                sounds.play_effect("effect6")
                Menu.choose += 1
            elif Menu.choose == 25:
                sounds.play_effect("effect6")
                Menu.choose -= 1

        surface1 = font.render("settings:", False, (255, 255, 255))
        Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 5))
        surface1 = font.render("<back", False, (80, 255, 80) if Menu.choose == 3 else (255, 255, 255))
        Screen.win.blit(surface1, (890 + 50 * (6 - Menu.open_index), 5))
        if True:
            surface1 = font7.render("right: " + Temp.settings.move_right, False, (80, 255, 80) if Menu.choose == 4 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 50))
            surface1 = font7.render("down: " + Temp.settings.move_down, False, (80, 255, 80) if Menu.choose == 5 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 80))
            surface1 = font7.render("left: " + Temp.settings.move_left, False, (80, 255, 80) if Menu.choose == 6 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 110))
            surface1 = font7.render("up: " + Temp.settings.move_up, False, (80, 255, 80) if Menu.choose == 7 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 140))
            surface1 = font7.render("interact: " + Temp.settings.interact, False, (80, 255, 80) if Menu.choose == 8 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 170))
            surface1 = font7.render("other: " + Temp.settings.other_function, False, (80, 255, 80) if Menu.choose == 9 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 200))
            surface1 = font7.render("sprint: " + Temp.settings.sprint, False, (80, 255, 80) if Menu.choose == 10 else (255, 255, 255))
            Screen.win.blit(surface1, (830 + 50 * (6 - Menu.open_index), 50))
            surface1 = font7.render("battle1: " + Temp.settings.battle_func1, False, (80, 255, 80) if Menu.choose == 11 else (255, 255, 255))
            Screen.win.blit(surface1, (830 + 50 * (6 - Menu.open_index), 80))
            surface1 = font7.render("battle2: " + Temp.settings.battle_func2, False, (80, 255, 80) if Menu.choose == 12 else (255, 255, 255))
            Screen.win.blit(surface1, (830 + 50 * (6 - Menu.open_index), 110))
            surface1 = font7.render("battle3: " + Temp.settings.battle_func3, False, (80, 255, 80) if Menu.choose == 13 else (255, 255, 255))
            Screen.win.blit(surface1, (830 + 50 * (6 - Menu.open_index), 140))
            surface1 = font7.render("battleS: " + Temp.settings.battle_switch_menu, False, (80, 255, 80) if Menu.choose == 14 else (255, 255, 255))
            Screen.win.blit(surface1, (830 + 50 * (6 - Menu.open_index), 170))
            surface1 = font7.render("battleC: " + Temp.settings.battle_confirm, False, (80, 255, 80) if Menu.choose == 15 else (255, 255, 255))
            Screen.win.blit(surface1, (830 + 50 * (6 - Menu.open_index), 200))
            surface1 = font8.render("hold tab and press a key to change", False, (30, 30, 30) if in_game else (110, 110, 110))
            Screen.win.blit(surface1, (716 + 50 * (6 - Menu.open_index), 226))

        if True:
            surface1 = font7.render("music volume: " + str(Temp.settings.musicVolume), False, (80, 255, 80) if Menu.choose == 16 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 245))
            surface1 = font7.render("sound effect volume: " + str(Temp.settings.effectVolume), False, (80, 255, 80) if Menu.choose == 17 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 270))
            surface1 = font7.render("auto saves: " + str(Temp.settings.allowAutoSaves), False, (80, 255, 80) if Menu.choose == 18 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 295))
            surface1 = font7.render("show unsellable: " + str(Temp.settings.showUnsellableItems), False, (80, 255, 80) if Menu.choose == 19 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 320))
            surface1 = font7.render("show claimed: " + str(Temp.settings.showClaimedMissions), False, (80, 255, 80) if Menu.choose == 20 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 345))

        if True:
            surface1 = font7.render("max screen width: " + str(Temp.settings.screen_width), False, (80, 255, 80) if Menu.choose == 21 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 370))
            surface1 = font7.render("max screen height: " + str(Temp.settings.screen_height), False, (80, 255, 80) if Menu.choose == 22 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 395))
            surface1 = font7.render("particles iterations: " + str(Temp.settings.particle_iterations), False, (80, 255, 80) if Menu.choose == 23 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 420))

        if True:
            surface1 = font.render("reset", False, (80, 255, 80) if Menu.choose == 24 else (255, 255, 255))
            Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 560))
            surface1 = font.render("save", False, (80, 255, 80) if Menu.choose == 25 else (255, 255, 255))
            Screen.win.blit(surface1, (910 + 50 * (6 - Menu.open_index), 560))

        if 4 <= Menu.choose <= 15:
            if keysHeld["tab"]:
                for key in keysDown:
                    if key == "tab":
                        continue
                    if keysDown[key]:
                        sounds.play_effect("effect7")
                        Temp.settings.set_by_index(Menu.choose - 4, key)
                        break

        elif Menu.choose == 16:
            if keysHeld[Ins.settings.move_right] and Temp.settings.musicVolume < 100:
                sounds.play_effect("effect9")
                Temp.settings.musicVolume += 2
            if keysHeld[Ins.settings.move_left] and Temp.settings.musicVolume > 0:
                sounds.play_effect("effect9")
                Temp.settings.musicVolume -= 2
        elif Menu.choose == 17:
            if keysHeld[Ins.settings.move_right] and Temp.settings.effectVolume < 100:
                sounds.play_effect("effect9")
                Temp.settings.effectVolume += 2
            if keysHeld[Ins.settings.move_left] and Temp.settings.effectVolume > 0:
                sounds.play_effect("effect9")
                Temp.settings.effectVolume -= 2
        elif Menu.choose == 21:
            if keysDown[Ins.settings.move_right] and Temp.settings.screen_width < 16:
                sounds.play_effect("effect9")
                Temp.settings.screen_width += 1
            if keysDown[Ins.settings.move_left] and Temp.settings.screen_width > 10:
                sounds.play_effect("effect9")
                Temp.settings.screen_width -= 1
        elif Menu.choose == 22:
            if keysDown[Ins.settings.move_right] and Temp.settings.screen_height < 10:
                sounds.play_effect("effect9")
                Temp.settings.screen_height += 1
            if keysDown[Ins.settings.move_left] and Temp.settings.screen_height > 6:
                sounds.play_effect("effect9")
                Temp.settings.screen_height -= 1
        elif Menu.choose == 23:
            if keysDown[Ins.settings.move_right] and Temp.settings.particle_iterations < 4:
                sounds.play_effect("effect9")
                Temp.settings.particle_iterations += 1
            if keysDown[Ins.settings.move_left] and Temp.settings.particle_iterations > 1:
                sounds.play_effect("effect9")
                Temp.settings.particle_iterations -= 1
        elif keysDown[Ins.settings.interact]:
            sounds.play_effect("effect6")
            if Menu.choose == 3:
                if in_game:
                    Screen.is_displaying = False
                    Screen.set_state("menu")
                else:
                    Menu.opened = False
                    Menu.choose = 1
            elif Menu.choose == 18:
                Temp.settings.allowAutoSaves = not Temp.settings.allowAutoSaves
            elif Menu.choose == 19:
                Temp.settings.showUnsellableItems = not Temp.settings.showUnsellableItems
            elif Menu.choose == 20:
                Temp.settings.showClaimedMissions = not Temp.settings.showClaimedMissions
            elif Menu.choose == 24:
                Temp.settings.reset()
            elif Menu.choose == 25:
                Ins.settings.copy_from(Temp.settings)
                Ins.settings.save()
                _f = open("save/settings.txt", "wb")
                pickle.dump(Ins.settings, _f)
                _f.close()
                if in_game:
                    Screen.is_displaying = False
                    Screen.set_state("menu")

                    Screen.update_camera(True)
                else:
                    Menu.opened = False
                    Menu.choose = 1

    def save_progress(announce=True):
        _f = open(f"save/world{Menu.current_save_slot}.txt", "wb")
        pickle.dump([Ins.player, Ins.ap, Ins.fv, Ins.stats], _f)
        _f.close()
        Menu.file_loc[Menu.current_save_slot - 1] = Screen.map_name
        Menu.file_sec[Menu.current_save_slot - 1] += int((pygame.time.get_ticks() - Menu.time) / 1000)
        Menu.time = pygame.time.get_ticks()
        _f = open(f"save/info.txt", "wb")
        pickle.dump([Menu.file_sec, Menu.file_loc], _f)
        _f.close()
        if announce:
            Screen.message_updated_msg = "progress saved!"
            Screen.message_updated_active = Screen.message_updated_time

    def return_to_menu():
        for song in sounds.song_delay:
            sounds.song_delay[song] = 0.0
        Screen.set_state("mainMenu")
        Menu.frame1 = 0
        Menu.frame = 0
        Menu.choose = None
        Menu.opened = False
        Menu.open_index = 0
        Menu.is_start = True
        Menu.file_choose = False
        Menu.delete_file = True
        Screen.is_question = False
        sounds.play("menu")
        importlib.reload(maps)
        reset_data()

    def redirect_text(text_string):
        Screen.open_text(texts.redirected_text[text_string], True)

    def start_battle(battle_id):
        Turns.pause = False
        Battle.state_turns = False
        Battle.attack_delay_list = {**{i[0]: 0 for i in scripts[Ins.player.script][2]},
                                    **{i[0]: 0 for i in scrolls[Ins.player.scroll][2]}}
        Screen.enemy_id = battle_id

        Battle.init_battle(battle.enemies_list[Screen.enemy_id][0])
        Battle.enemy_list = battle.enemies_list[Screen.enemy_id][1:]
        Battle.texture = textures.battle_bosses[Battle.enemy_list[3]]
        #Battle.background = textures.battle_enemies[Battle.enemy_list[3]]

        Battle.Sprite.direction = 0
        Battle.Sprite.mode = 0
        Battle.Sprite.velocity = 20
        Battle.Sprite.mode_2_velocity = 0.5
        Battle.Sprite.current_effect = 0

        Battle.selected_script_attack = 0
        Battle.selected_scroll_attack = 0
        Battle.selected_weapon_attack = 0
        Battle.selected_menu = 0
        Battle.selected_battle_menu = 0
        Battle.selected_battle_item = 0
        Battle.selected_battle_class = 0

        Battle.enemy_hp = Battle.enemy_list[4][0]
        Battle.enemy_max_hp = Battle.enemy_list[4][0]
        Battle.enemy_last_frame_hp = Battle.enemy_list[4][0]
        Battle.player_last_frame_hp = Ins.player.hp
        Battle.enemy_width = Battle.texture.get_width()
        Battle.enemy_height = Battle.texture.get_height()
        Battle.enemy_x = 600
        Battle.enemy_y = 150
        pygame.display.set_caption(Battle.enemy_list[0])
        sounds.play("none")

        Battle.Hitbox.hitbox_list.clear()
        Battle.Projectile.projectile_list.clear()

        Screen.set_state("battle")
        #Screen.max_battle_frames = int(
         #   sounds.song_length[Battle.enemy_list[1]] * 30 - Battle.enemy_list[2][0] - Battle.enemy_list[2][1])
        Battle.max_battle_frames = Battle.enemy_list[2][1] - Battle.enemy_list[2][0]
        Battle.current_battle_frame = -1
        Battle.Sprite.x = float(Ins.player.x - Screen.camera_x)
        Battle.Sprite.y = float(Ins.player.y - Screen.camera_y)

        for _frame in range(35):
            Battle.Sprite.x -= (Ins.player.x - Screen.camera_x - 600 + Battle.Sprite.length / 2) / 35
            Battle.Sprite.y -= (Ins.player.y - Screen.camera_y - 500 + Battle.Sprite.length / 2) / 35
            Screen.dt = 1000 / Screen.clock.tick(30)
            Screen.win.fill((0, 0, 0))
            key_list()
            pygame.draw.rect(Screen.win, (255, 255, 255), (300, 300, 600, 400), 10)
            Screen.win.blit(textures.player_pre_sprite, (round(Battle.Sprite.x), round(Battle.Sprite.y)))
            pygame.display.flip()

        reset_battle_variables()

        Battle.Sprite.x = 300 - Battle.Sprite.length / 2
        Battle.Sprite.y = 200 - Battle.Sprite.length / 2
        sounds.play(Battle.enemy_list[1], False, False, Battle.enemy_list[2][0] / 30 * 1000, 0)

        try:
            globals()["bf_bg_" + str(Screen.enemy_id)]()
        except KeyError:
            pass

    def start_turns(turns_id):
        Turns.pause = False
        Battle.state_turns = True
        Turns.turns_list = turns.encounters[turns_id]

        Turns.Enemy.enemy_list.clear()
        for _enemy in Turns.turns_list[0]:
            Turns.Enemy(_enemy)

        for _enemy in Turns.Enemy.enemy_list:
            _enemy.x, _enemy.y = Turns.positions_list[len(Turns.Enemy.enemy_list) - 1][_enemy.id]
            try:
                globals()["trn_bg_"+_enemy.enemy_id](_enemy)
            except KeyError:
                pass

        Turns.background = textures.battle_background[Turns.turns_list[2]]
        Ins.player.random_encounter_variable = 0
        Ins.player.random_encounter_next = random.randint(160, 420)
        animation("4", ["turns", Turns.turns_list[1]], None, immune=True, layer=400)
        Screen.freeze_player = True
        Turns.enemy_turn = True
        #Turns.turn_index = -1

        Battle.selected_script_attack = 0
        Battle.selected_scroll_attack = 0
        Battle.selected_weapon_attack = 0
        Battle.selected_menu = 0
        Battle.selected_battle_menu = 0
        Battle.selected_battle_item = 0
        Battle.selected_battle_class = 0

        # Turns.player_delay = {}
        Battle.attack_delay_list = {}
        Turns.turn_count = 0
        Turns.player_selected_enemy = 0
        Turns.picking_enemy = 0
        Turns.turn_order_next = Turns.Enemy.enemy_list + [None]
        Turns.alive_enemies = list(Turns.Enemy.enemy_list)
        random.shuffle(Turns.turn_order_next)
        Turns.turn_order = [None] + list(Turns.turn_order_next)
        random.shuffle(Turns.turn_order_next)
        Turns.turns_id = turns_id
        reset_battle_variables()

        try:
            globals()["trnb_bg_"+str(turns_id)]()
        except KeyError:
            pass

    def atk_amp_func(atk, defense, atk_type=0):
        if defense <= 0:
            return 999999
        if atk_type == 1:
            return atk
        const = 15
        return const * atk / (const + defense)

    def lvl_amp_func(attacker, attacked, atk_type=0):
        level_diff = attacker - attacked
        return level_diff / (15 + abs(level_diff)) + 1

    def player_atk_amp(weapon):
        mul = 1
        if weapon == 1 and Ins.player.playerClass == 1:
            mul += 0.2
        mul += Ins.player.atk_boost
        return mul

    def player_def_amp():
        return 1 / (1 + Ins.player.def_boost)

    def player_crit_rate(crit_rate):
        return crit_rate ** (1 / (1 + Ins.player.crit_rate_const))

    def increase_level(level):
        Ins.player.max_hp += 3
        Ins.player.max_mana += level % 2 + 1
        Ins.player.attack += 1.5
        Ins.player.evasion += 1.5
        Ins.player.accuracy += 1.5
        Ins.player.defense += 1.5
        Ins.player.hp = Ins.player.max_hp
        Ins.player.mana = Ins.player.max_mana
        Ins.player.level_points += 1
        if level == 3:
            proceed_mission("the exterminator", 3, True)

    def reset_battle_variables():
        Battle.battle_variables = {
            "berserkerUsed": False,
            "ninjaUsed": False,
            "ninjaTimesUsed": 0,
        }

    def get_hp_list():
        return [Ins.player.hp] + [enemy.hp for enemy in Turns.Enemy.enemy_list]

    def battle_stopped(is_turns):
        if is_turns:
            Ins.player.add_attack(-2 * Battle.battle_variables["ninjaTimesUsed"])
            Ins.player.atk_boost -= 0.1 * Battle.battle_variables["ninjaTimesUsed"]
        else:
            Ins.player.add_attack(-1 * Battle.battle_variables["ninjaTimesUsed"])
            Ins.player.atk_boost -= 0.05 * Battle.battle_variables["ninjaTimesUsed"]


# rendering methods
if True:
    def blit_rotated_rect(x, y, w, h, color, width=0.0, rot=0.0, point=(0, 0), point_rot=0.0):

        rect_radius = math.sqrt(h ** 2 + w ** 2) / 2
        try:
            rect_angle = math.atan(h / w)
        except ZeroDivisionError:
            rect_angle = PI / 2
        hitbox = []

        if rot % (2 * PI) == 0 and point_rot % (2 * PI) == 0:
            pygame.draw.rect(Screen.win, color, (round(x + point[0] - w / 2), round(y + point[1] - h / 2), w, h), round(width))
            hitbox = [(round(x + point[0] - w / 2 + 305),
                            round(y + point[1] - h / 2)), (
                           round(x + point[0] + w / 2),
                           round(y + point[1] - h / 2)), (
                           round(x + point[0] + w / 2),
                           round(y + point[1] + h / 2)), (
                           round(x + point[0] - w / 2),
                           round(y + point[1] + h / 2))]
        elif point_rot % (2 * PI) == 0:
            for dot in range(4):
                temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (PI if dot in (0, 3) else 0) + rot
                hitbox.append((round(point[0] + x + rect_radius * math.cos(temp_angle)),
                                    round(point[1] + y + rect_radius * math.sin(temp_angle))))
            pygame.draw.polygon(Screen.win, color, hitbox, round(width))
        else:
            for dot in range(4):
                temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (PI if dot in (0, 3) else 0) + rot
                temp2_angle = math.atan2(rect_radius * math.sin(temp_angle) + point[1],
                                         rect_radius * math.cos(temp_angle) + point[0]) + point_rot
                temp2_radius = math.sqrt(
                    rect_radius ** 2 + point[1] ** 2 + point[0] ** 2 + 2 * rect_radius * (
                                point[0] * math.cos(temp_angle) + point[1] * math.sin(temp_angle)))
                hitbox.append((round(x + math.cos(temp2_angle) * temp2_radius),
                                    round(y + math.sin(temp2_angle) * temp2_radius)))
            pygame.draw.polygon(Screen.win, color, hitbox, round(width))

        return hitbox

    def blit_rotated_texture(image, x, y, w=None, h=None, rot=0.0, point=(0, 0), point_rot=0.0, hitbox_rot=0.0):  # hitbox rot usless for only blitting purposes
        if w is None:
            w = image.get_width()
        if h is None:
            h = image.get_height()
        rect_radius = math.sqrt(h ** 2 + w ** 2) / 2
        try:
            rect_angle = math.atan(h / w)
        except ZeroDivisionError:
            rect_angle = PI / 2
        hitbox = []

        if rot % (2 * PI) == 0 and point_rot % (2 * PI) == 0 and hitbox_rot % (2 * PI) == 0:
            Screen.win.blit(image, (round(x + point[0] - image.get_rect().width / 2), round(y + point[1] - image.get_rect().height / 2)))
            hitbox = [(round(x + point[0] - w / 2),
                            round(y + point[1] - h / 2)), (
                           round(x + point[0] + w / 2),
                           round(y + point[1] - h / 2)), (
                           round(x + point[0] + w / 2),
                           round(y + point[1] + h / 2)), (
                           round(x + point[0] - w / 2),
                           round(y + point[1] + h / 2))]
        else:
            rotated_image = pygame.transform.rotate(image, -1 * (rot + point_rot) / PI * 180)
            new_rect = rotated_image.get_rect(center=image.get_rect(center=(
                round(x + math.sqrt(point[0] ** 2 + point[1] ** 2) * math.cos(math.atan2(point[1], point[0]) + point_rot)),
                round(y + math.sqrt(point[0] ** 2 + point[1] ** 2) * math.sin(math.atan2(point[1], point[0]) + point_rot)))).center)
            Screen.win.blit(rotated_image, (round(new_rect.topleft[0]), round(new_rect.topleft[1])))
            for dot in range(4):
                temp_angle = (1 if dot % 2 == 0 else -1) * rect_angle + (PI if dot in (0, 3) else 0) + rot + hitbox_rot
                temp2_angle = math.atan2(rect_radius * math.sin(temp_angle) + point[1], rect_radius * math.cos(temp_angle) + point[0]) + point_rot
                temp2_radius = math.sqrt(
                    rect_radius ** 2 + point[1] ** 2 + point[0] ** 2 + 2 * rect_radius * (
                                point[0] * math.cos(temp_angle) + point[1] * math.sin(temp_angle)))
                hitbox.append((round(x + math.cos(temp2_angle) * temp2_radius),
                                    round(y + math.sin(temp2_angle) * temp2_radius)))
        if console_active_list["show hitbox"] == 1:
            pygame.draw.polygon(Screen.win, (255, 255, 255), hitbox, 1)

        return hitbox

    def draw_entities(texture_list, range_y_bot=None, range_y_top=None):
        for [pos, texture, bottom] in texture_list:
            if range_y_bot is not None and not (pos[1] + texture.get_height() / 2 - bottom >= range_y_bot):
                continue
            if range_y_top is not None and not (pos[1] + texture.get_height() / 2 - bottom < range_y_top):
                continue
            Screen.win.blit(texture, (round(pos[0] - Screen.camera_x - texture.get_width() / 2),
                                      round(pos[1] - Screen.camera_y - texture.get_height() / 2)))

    def render_map_blocks(map_list, layer, camera_x, camera_y, insert_player=False):
        player_y = 0
        if insert_player:
            player_y = Ins.player.y + Ins.player.height - Ins.player.hitbox_height
            draw_entities(Screen.selected_map[3], None, 0)
            if player_y < 0:
                Ins.player.draw()
        h = -1
        for h in range(len(map_list[0])):
            for w in range(len(map_list[0][0])):
                if not map_list[0][h][w][layer] == textures.map_blocks["empty"]:
                    if isinstance(map_list[0][h][w][layer], list):
                        Screen.win.blit(map_list[0][h][w][layer][0], (w * 64 - round(camera_x) + map_list[0][h][w][layer][1][0], h * 64 - round(camera_y) + map_list[0][h][w][layer][1][1]))
                    else:
                        Screen.win.blit(map_list[0][h][w][layer], (w * 64 - round(camera_x), h * 64 - round(camera_y)))
            if insert_player:
                if h * 64 <= player_y < (h + 1) * 64:
                    draw_entities(Screen.selected_map[3], h*64, player_y)
                    Ins.player.draw()
                    draw_entities(Screen.selected_map[3], player_y, (h+1)*64)
                else:
                    draw_entities(Screen.selected_map[3], h*64, (h + 1) * 64)

        if insert_player:
            if player_y >= (h+1)*64:
                Ins.player.draw()
            draw_entities(Screen.selected_map[3], (h + 1) * 64, None)

    def render_cutscene_frame(cutscene_list, frame, layer, camera_x, camera_y):
        for _key in list(i for i in cutscene_list[frame] if i[0] == layer):

            if isinstance(_key[1], str):
                Screen.win.blit(_key[3].render(_key[1], False, _key[4]), (_key[2][0] - camera_x, _key[2][1] - camera_y))
            elif isinstance(_key[1], tuple):
                blit_rotated_rect(_key[1][0] + _key[1][2] / 2 - camera_x, _key[1][1] + _key[1][3] / 2 - camera_y, _key[1][2], _key[1][3], tuple(_key[2]), _key[3], _key[4], (0, 0), 0)
            else:
                blit_rotated_texture(_key[1], _key[2][0] - camera_x, _key[2][1] - camera_y, None, None, _key[3])

    def display_hp_list(hp_list):
        for i in range(len(hp_list)):
            temp_hp = -hp_list[i]
            i -= 1
            if i == -1:
                temp_hp += Ins.player.hp
                temp_hp = round(temp_hp)
                if temp_hp != 0:
                    animation("1", True, temp_hp, 4,
                              point=(random.randint(197, 277), random.randint(206, 346)), frozen=False, layer=1)
            else:
                enemy = Turns.Enemy.enemy_list[i]
                temp_hp += enemy.hp
                temp_hp = round(temp_hp)
                if temp_hp < 0:
                    if -2 in enemy.texture:
                        enemy.animation(-2)
                if temp_hp != 0:
                    if -temp_hp > Ins.stats.max_damage:
                        Ins.stats.max_damage = -temp_hp
                    animation("1", False, temp_hp, 4,
                              point=(enemy.x + random.randint(-40, 40), enemy.y + random.randint(-40, 40)),
                              frozen=False, layer=1)

    def animation(animation_id, *args, **kwargs):
        if animation_id == -1:
            return
        else:
            animation_id = str(animation_id)
        if "name" in kwargs:
            name = kwargs["name"]
        else:
            name = ""
        if "point" in kwargs:
            point = kwargs["point"]
        else:
            point = None
        if "immune" in kwargs:
            immune = kwargs["immune"]
        else:
            immune = False
        if "layer" in kwargs:
            layer = kwargs["layer"]
        else:
            layer = 0
        if "frozen" in kwargs:
            frozen = kwargs["frozen"]
        else:
            frozen = False
        if "reference" in kwargs:
            ref = kwargs["reference"]
        else:
            ref = None
        if "duration" in kwargs:
            dur = kwargs["duration"]
        else:
            dur = -1

        info = []
        ################################
        if animation_id == "0":
            layer = float("inf")
            info = args
        elif animation_id == "1":
            # (is_player, damage, decay) -> (damage, text, decay)
            if point is not None:
                pass
            elif args[0]:
                point = (random.randint(40, 260), 270)
            else:
                point = (random.randint(450, 700), 250)

            info.append(args[1] if isinstance(args[1], int) else 0)
            if isinstance(args[1], int):
                info.append(("+" if args[1] > 0 else "") + str(args[1]))
            else:
                info.append(args[1])
            info.append(args[2])
        elif animation_id == "fadeText":
            info.append(args[0])
            info.append(args[1])
            info.append(args[2])
        elif animation_id == "2":
            info = []  # [color, x, width, speed, delay, max]
            for bloodDrop in range(10):
                info.append(
                    [random.randint(0, 20), random.randint(bloodDrop * 60 + 5, bloodDrop * 60 + 55),
                     random.choice([3, 4, 4, 5, 5, 5, 6, 6]), random.randint(2, 6), random.randint(0, 20),
                     random.randint(30, 100)])
        elif animation_id == "player":
            # () -> (animation_id, frame, displayed_frame)
            info = [0, 0, 0]
        elif animation_id == "aa-samuraiSlash":
            # () -> (*[angle, x_pos, y_pos])
            info = []
            for i in range(20):
                info.append([random.uniform(0, PI), random.randint(-50, 50), random.randint(-50, 50)])
        elif animation_id == "aa-slash1":
            info = [random.uniform(3*PI / 4 - 0.3, 3*PI / 4 + 0.3), 0]
        elif animation_id == "slash1All":
            info = [random.uniform(0, 2*PI), 0]
            animation_id = "aa-slash1"
        elif animation_id == "aa-heal1":
            particles("circle", 10, [80, 255, 80], [args[0][0], args[0][1]], 1, 0, 0, 0, gravity=0, exist_func=[["decay", -3], ["fade", 8]], full=4, tags="heal")
        elif animation_id == "aa-arrow1":
            _len = 3
            for i in range(10):
                animation("0", i // _len, ["animation", ["aad-arrow1"], {"point": [random.randint(474, 826), random.randint(117, 499)]}], None)
            return
        elif animation_id == "aa-purify1":
            layer = -20
        elif animation_id == "animation":
            info.append(args[0])
            info.append(None)
        elif animation_id.startswith("aa") and animation_id.endswith("an"):
            an = "-".join(animation_id.split("-")[1:-1])
            animation("animation", an, **kwargs)
            return
        else:
            # args -> info
            # 0 - (time, end_func=[func, *args], exist_func=[func, *args])
            # 3 - (text, color)
            # 4 - (mid_func=[func, *args], end_func=[func, *args])
            info = args

        # animate an attack animation targeted at point
        # frame determines where at the animation we are
        # returns true if animation is finished else false0
        Animation(animation_id, point, info, name, immune, layer, frozen, ref, dur)

    def particles(types, size, color, area, count, duration, direction, velocity, full=0,
                  gravity=9.78, gravity_angle=PI/2, beginning_func=None, exist_func=None, death_func=None,
                  rotation=None, rotation_speed=None, alpha=None, tags=None):
        # types:
        # str - one type
        # list[str] - iterate through list
        # list[list[str, int]] - random with weight
        # area:
        # list[3] - circle x, y, radius
        # list[4] - rect, x, y (middle), width, height
        # directions / velocity/ gravity:
        # str / float / float - taken from direction dict / set vel / gravity (/angle)
        # list[2] - randomizes angle / velocity / gravity (/angle)
        if exist_func is None:
            exist_func = "none"
        if beginning_func is None:
            beginning_func = "none"
        if death_func is None:
            death_func = "none"
        if rotation_speed is None:
            rotation_speed = 0.0
        if rotation is None:
            rotation = 0.0
        if tags is None:
            tags = ""
        if alpha is None:
            alpha = 255

        for i in range(count):
            _point = list(area[0:2])
            if len(area) == 4:
                _point[0] += random.randint(-area[2], area[2])
                _point[1] += random.randint(-area[3], area[3])
            elif len(area) == 3:
                angle = random.uniform(-PI, PI)
                distance = random.random() + random.random()
                if distance > 1:
                    distance = 2 - distance
                _point[0] += area[2] * distance * math.cos(angle)
                _point[1] += area[2] * distance * math.sin(angle)

            _type = ""
            if isinstance(types, str):
                _type = types
            elif isinstance(types[0], str):
                _type = types[i % len(types)]
            else:
                _roll = random.uniform(0, sum(j[1] for j in types))
                _sum = 0
                for item in types:
                    _sum += item[1]
                    if _sum > _roll:
                        _type = item[0]
                        break

            # angles
            angles_org = [direction, gravity_angle]
            angles = [0, 0]
            for var in range(len(angles)):
                if isinstance(angles_org[var], float) or isinstance(angles_org[var], int):
                    angles[var] = angles_org[var]
                elif isinstance(angles_org[var], str):
                    angles[var] = random.uniform(*Particles.directions[angles_org[var]])
                elif isinstance(angles_org[var][0], str):
                    _roll = random.uniform(0, sum(Particles.directions[j][1] - Particles.directions[j][0] for j in angles_org[var]))
                    _sum = 0
                    for item in angles_org[var]:
                        _sum += Particles.directions[item][1] - Particles.directions[item][0]
                        if _sum > _roll:
                            angles[var] = random.uniform(*Particles.directions[item])
                            break
                elif isinstance(angles_org[var][0], list):
                    _roll = random.uniform(0, sum(j[1] - j[0] for j in angles_org[var]))
                    _sum = 0
                    for item in angles_org[var]:
                        _sum += item[1] - item[0]
                        if _sum > _roll:
                            angles[var] = random.uniform(*item)
                            break
                else:
                    angles[var] = random.uniform(*angles_org[var])

            if rotation is True:
                rotation = [-PI, PI]
            elif rotation is False:
                rotation = 0.0

            # sections
            sections_org = [velocity, gravity, size, rotation, rotation_speed, alpha]
            sections = [0, 0, 0, 0, 0, 0]
            for var in range(len(sections_org)):
                if isinstance(sections_org[var], float) or isinstance(sections_org[var], int):
                    sections[var] = sections_org[var]
                elif isinstance(sections_org[var][0], list):
                    _roll = random.uniform(0, sum(j[1] - j[0] for j in sections_org[var]))
                    _sum = 0
                    for item in sections_org[var]:
                        _sum += item[1] - item[0]
                        if _sum > _roll:
                            sections[var] = random.uniform(*item)
                            break
                else:
                    sections[var] = random.uniform(*sections_org[var])

            if len(color) == 3:
                _color = color
            else:
                _color = [min_max(0, color[i] + random.randint(-color[i + 3], color[i + 3]), 255) for i in range(3)]

            if duration == 0:
                Particles(_type, sections[2], _color, _point, angles[0], sections[0], full, sections[1],
                          angles[1], beginning_func, exist_func, death_func, sections[3], sections[4], sections[5], tags)
            else:
                animation("0",  int(i / count * duration), ["particles", _type, sections[2], _color, _point, angles[0], sections[0], full, sections[1],
                            angles[1], beginning_func, exist_func, death_func, sections[3], sections[4], sections[5], tags], None)


# helper functions
if True:
    def hp_get_texture_pos_by_name(map_string, texture_name):
        i = 0
        for texture in maps.map_list[map_string][3]:
            if textures.entities[texture_name] == texture[1]:
                return i
            i += 1
        return None

    def hp_get_text_pos_by_name(map_string, text_name):
        i = 0
        for text in maps.map_list[map_string][2]:
            if text[1] == text_name:
                return i
            i += 1
        return None

    def hp_delete_text_pos_by_name(map_string, text_name):
        del maps.map_list[map_string][2][hp_get_text_pos_by_name(map_string, text_name)]

    def hp_delete_texture_pos_by_name(map_string, texture_name):
        del maps.map_list[map_string][3][hp_get_texture_pos_by_name(map_string, texture_name)]

    def hp_bleed_particles(self, size, direction):
        particles("circle", size, [150, 40, 40, 30, 15, 15], [self.x, self.y, 20, 40], 30, 0,
                  direction, 5, 0, 15,
                  exist_func=[["friction", 0.95], ["decay", 0.1, 10], ["bounce", 0.65]])

    def hp_save_first_forest6():
        hp_delete_text_pos_by_name("ma_forest", "ma_forest_man")
        hp_delete_texture_pos_by_name("ma_forest", "swordsman1")
        maps.m_ma_forest[4][2]["ma_forest5"] = 1.5
        maps.m_ma_forest[4][2]["ma_forest6"] = 0.75

    def hp_get_battle_hitbox():
        return pygame.Rect(round(Battle.Sprite.x + 305), round(Battle.Sprite.y + 305), Battle.Sprite.length, Battle.Sprite.length)

    @remove_func("hp_update_sigil_lvl")
    @save_func()
    def hp_update_sigil_lvl(lvl):
        items["sigil of permission"][0] = f"lvl {lvl}"

    def hp_get_sigil_lvl():
        return int(items["sigil of permission"][0].split()[1])


# function related
if True:
    #  stats variables
    class Stats:
        def __init__(self):
            self.monsters_killed = 0
            self.turns_battles_won = 0
            self.total_coins = 0
            self.max_damage = 0

    #  function variables
    class FV:
        def __init__(self):
            self.num = False

            self.ma_pass_forest = True
            self.shop1_overdo = True
            self.guard3_overdo = True
            self.guard2_overdo = True
            self.palace_overdo = True
            self.ma_man_overdo = True
            self.ma_orc_first = True
            self.ma_orc_overdo = True
            self.ma_jessica = 0
            self.ma_jessica_level = None

            self.script1 = False
            self.scroll1 = False

            self.ma_exterminator = False

            self.berserker = False
            self.priestess = False
            self.ninja = False
            self.apple = False

    #  all purpose variables
    class AP:
        def __init__(self):
            # shops

            self.player_map = "map0"
            self.run_on_reload = []

            self.first = {
                "menuTab": True
            }

            # [map_name, start_loc, is_unlocked, displayed name]
            # map_name: is_unlocked
            self.travel_unlocked = {i[0]: False for i in travel_list}

            # *mission_name: False: hidden, 0: didn't start, 1-n: in progress (stages), True: finished
            self.mission_progress_list = {
                **{i[0]: False for i in mission_list},
                "the exterminator": 0,
            }
            # self.mission_progress_list = {
            #     "apple to the lumber": False,
            #     "wizard's appointment": 0,
            # }
            self.mission_claimed = {i[0]: False for i in mission_list}

            # shop_id: [*[item, price, stock (-1 is inf), [*commands]]]
            self.shops = {
                0: [['iron plated leggings', 55, 1, []], ["apple", 6, -1, []], ["bracelet of aid", 30, 2, []], ["rusty sword", 20, 1, []], ["wooden staff", 25, 1, []]],
                1: [["bandage", 20, -1, []], ["small mana potion", 35, -1, []], ["angled bow", 130, 1, []], ["steel layered chestplate", 160, 1, []], ["maximized potion", 150, 3, []], ["attack peanut", 80, 5, []]],
                2: [["dwarven sword", 900, 1, []], ["safety pin", 550, 2, []], ["stylish pants", 700, 1, []], ["jeweled staff", 850, 1, []], ["demonic blood vial", 650, 1, []], ["attack peanut", 140, 5, []]]
            }

            self.travel_enabled = True

        def add_reload_func(self, name, cap):
            if cap == -1 or self.run_on_reload.count(name) < cap:
                self.run_on_reload.append(name)

        def remove_reload_func(self, name, count):
            c = 0
            for index in range(len(self.run_on_reload)):
                if isinstance(self.run_on_reload[index], list):
                    func = self.run_on_reload[index][0]
                else:
                    func = self.run_on_reload[index]

                if func == name:
                    del self.run_on_reload[index]
                    c += 1

                    if count != -1 and c >= count:
                        break

        def update(self):
            temp = AP()
            self.travel_unlocked = {**temp.travel_unlocked, **self.travel_unlocked}
            self.mission_progress_list = {**temp.mission_progress_list, **self.mission_progress_list}
            self.mission_claimed = {**temp.mission_claimed, **self.mission_claimed}
            self.shops = {**temp.shops, **self.shops}

    # text functions  -  *args
    if True:
        def f_none():
            pass

        def f_redirect(text_string):
            redirect_text(text_string)

        def f_proceed_mission(mission_str, stage=-1, skip=True):
            proceed_mission(mission_str, stage, skip)

        def f_start_cut_scene(cut_scene_str):
            start_cut_scene(cut_scene_str)

        def f_run_classes():
            Screen.description_message = Screen.get_text_format(player_classes[1][1], 655, font3)
            Screen.description_page = 0
            Screen.is_displaying = False
            Screen.set_state("classes")
            sounds.play_effect("effect12")
            Screen.classDeg = 0
            Screen.classIndex = 0
            Requires.class_update()
            Screen.classRotationTime = 0

        def f_enter_shop(shop_id):
            enter_shop(shop_id)

        def f_add_item(item, num):
            Ins.player.add_item(item, num)

        def f_name(name=""):  # resets name
            Screen.current_name = name

        def f_save_progress(announce=True):
            save_progress(announce)

        def f_start_battle(battle_id):
            start_battle(battle_id)

        def f_start_turns(turns_id):
            start_turns(turns_id)

        def f_insert_current(*text_list):
            Screen.insert_current(*text_list)

        def f_append_current(*text_list):
            Screen.append_current(*text_list)

        def f_fv_set_var(variable, value=False):
            exec(f"Ins.fv.{variable} = value")

        def f_screen_fade(arg1=None, arg2=None):
            animation(4, arg1, arg2)

        @save_func()
        def f_remove_hitbox(map_string, x, y):
            maps.map_list[map_string][0][y][x][3] = False

        def f_exec(cmd):
            exec(cmd)

        @save_func()
        def f_save_exec(cmd):
            exec(cmd)

        def f_change_map(goto, goto_pos):
            animation("4", ["change_map", goto, goto_pos], ["unfreeze"])

        def f_travel_enabled(enabled):
            Ins.ap.travel_enabled = enabled

        ### content related:
        @save_func()
        def f_ma_boat_remove():
            hp_delete_text_pos_by_name("ma_port", "ma_port_boat")
            hp_delete_texture_pos_by_name("ma_port", "boat")

        def f_inn_func():
            cost = (Ins.player.max_mana - Ins.player.mana) // 2
            if Ins.player.coins >= cost:
                Screen.append_current(([f"would you like to sleep here for the night to restore your mana? it'll cost you {cost} coins (you have {Ins.player.coins} coins)"],
                                       ["yes", ["sub_coins", cost], ["restore_player"], ["screen_fade"]], ["no"]))
            else:
                Screen.append_current(([f"would you like to sleep here for the night to restore your mana? it'll cost you {cost} coins"],
                                       ["no (insufficient coins)"]))

        def f_sub_coins(cost):
            Ins.player.add_coins(-cost)

        def f_restore_player():
            Ins.player.hp = Ins.player.max_hp
            Ins.player.mana = Ins.player.max_mana

        def f_add_1():
            Ins.fv.num = True

        def f_offset_x(off):
            Ins.player.x += off

        def f_offset_y(off):
            Ins.player.y += off

        def f_ma_story2():
            if Ins.player.level >= 3:
                f_save_exec("maps.m_ma_palace[2].pop(0)")
                Screen.append_current("but of course! serving the kind is the duty of the citizens. come to me to get items that will help you")
            else:
                Screen.append_current("you dare taking a commission of the king while being this weak! get stronger and return here at once!", [["offset_y", 64]])

        def f_ma_story2_items():
            Ins.player.add_item("sigil of permission")
            Ins.player.add_item("iron bow")
            Ins.fv.script1 = True
            proceed_mission("the exterminator")

        def f_ma_sailor():
            start_cut_scene("ma_boat1")
            Ins.player.x = 979
            Ins.player.y = 633
            Screen.update_camera()
            Screen.unlock_map_travel("ma_river")

        def f_ma_orc_text():
            if Ins.fv.ma_orc_first:
                Ins.fv.ma_orc_first = False
                proceed_mission("berserker duel", 1)
                Screen.insert_current((["hello..."], ["are you the one causing all the trouble?"]), (["no.. i'm just passing by... but i got wounded by some strange swordsman..."], ["where was he?"]),
                                         "he is to the south-east of here... he was very strong so i barely made my escape...")

        def f_ma_orc_bandage():
            Ins.fv.ma_orc_overdo = False
            Ins.player.add_item("bandage", -1)
            Ins.player.add_item("worn out sword", 1)
            Screen.append_current("thank you sir... take this... this sword belongs to the berserker...", "he said anyone that presents him with that sword will be trained by him...", "you can find him in the mainter river")
            proceed_mission("berserker duel", 2)

        def f_ma_pa_guard():
            if Ins.fv.ma_exterminator:
                Screen.append_current("wow! you actually solved the problem! don't worry, you will get a good reward!", "you will be awarded an artifact from the treasury, and your sigil of permission will be upgraded", [["proceed_mission", "the exterminator"]])
            else:
                Screen.append_current("go along! Im awaiting good results! we will give you the rest of the rewards after you succeed")

        def f_ma_priestess():
            Ins.player.add_coins(-150)
            Ins.player.add_item("small mana potion")
            Ins.fv.priestess = True
            Screen.append_current("thank you child. in return i will teach you the teaching of priests, may god help you in the future",
                                  ["screen_fade", "remove_priestess", ["proceed_mission", "a lost priestess", True]])

        def f_sp_ninja():
            Ins.fv.ninja = True

        @save_func(cap=1)
        def f_remove_berserker():
            hp_delete_texture_pos_by_name("ma_river", "berserker")
            hp_delete_text_pos_by_name("ma_river", "ma_berserker")

        @save_func(cap=1)
        def f_remove_priestess():
            hp_delete_texture_pos_by_name("ma_forest", "priestess")
            hp_delete_text_pos_by_name("ma_forest", "ma_priestess")

        def f_jessica_text():
            if Ins.fv.ma_jessica == 0:
                if Ins.stats.monsters_killed >= 30:
                    Screen.append_current("hello young boy! I would offer to sell you some items since you are somewhat experienced, but im not sure if you are worthy...",
                                          "please raise your level twice and then ill sell you my products!")
                    Ins.fv.ma_jessica_level = int(Ins.player.level)
                    Ins.fv.ma_jessica = 2
                    proceed_mission("a shop for the worthy", 2)
                else:
                    Screen.append_current("hello young boy! I would offer to sell you some items, but you are not very experienced in combat!",
                                          "please kill a total of 30 monsters before talking to me again")
                    Ins.fv.ma_jessica = 1
                    proceed_mission("a shop for the worthy", 1)
            elif Ins.fv.ma_jessica == 1:
                if Ins.stats.monsters_killed >= 30:
                    Screen.append_current("I see you killed some monsters! but thats only monsters, im still not sure if you are worthy...",
                                          "please raise your level twice and then ill sell you my products!")
                    Ins.fv.ma_jessica_level = int(Ins.player.level)
                    Ins.fv.ma_jessica = 2
                    proceed_mission("a shop for the worthy", 2)
                else:
                    Screen.append_current(f"you killed only {Ins.stats.monsters_killed} monsters! kill {30-Ins.stats.monsters_killed} before talking to me again.")
            elif Ins.fv.ma_jessica == 2:
                if Ins.player.level - Ins.fv.ma_jessica_level >= 2:
                    Screen.append_current("good job! Ill let you buy my products now!")
                    Ins.fv.ma_jessica = 3
                    proceed_mission("a shop for the worthy", True)
                else:
                    Screen.append_current("you still haven't raised your level boy! come again later")

        @save_func(cap=1)
        def f_ma_sailor_saved():
            maps.map_list["ma_river"][3][hp_get_texture_pos_by_name("ma_river", "boat")][0] = (981, 543)
            del maps.map_list["ma_river"][2][hp_get_text_pos_by_name("ma_river", "ma_sailor")]

        def f_quit():
            pygame.quit()
            quit()

        def f_ma_samurai1():
            Screen.append_current("okay, im letting you hit an apple once. if you deal more than 100 hit points you are accepted",
                                  (["but if you don't, im going to kill you"], ["ok", ["start_turns", "samurai_apple"]], ["are you crazy?", ["append_current", "okay your loss idiot"]]))

    # mission function  -  *args
    if True:
        # mf - mission
        def mf_the_exterminator():
            Ins.player.add_item("holy badge")
            hp_update_sigil_lvl(2)

        def mf_anniversary_gift():
            Ins.fv.scroll1 = True

        def mf_berserker_duel():
            Ins.fv.berserker = True

    #  passives  -  no args
    if True:
        # ap - add passive
        if True:
            def ap_attack_boost1():
                _hp = int((Ins.player.max_hp - Ins.player.hp) // 2)
                _mana = int((Ins.player.max_mana - Ins.player.mana) // 2)
                Ins.player.add_hp(min(80, _hp))
                Ins.player.add_mana(min(40, _mana))
                if Screen.state("turns") or Screen.state("battle"):
                    Battle.Effect("damage boost 1", 3, True, "atk_boost1", "none", "atk_boost1", color=(200, 40, 40))

            def ap_one_percent_boost():
                Ins.player.atk_boost += 0.01

            def ap_ten_percent_boost():
                Ins.player.atk_boost += 0.1

        # fp - function passive
        if True:
            def fp_mana_regen1():
                if Screen.state("turns") or Screen.state("battle"):
                    if not Battle.Effect.name_exists("mana regen tier 1"):
                        Battle.Effect("mana regen tier 1", -1, True, "none", "mana_regen1", color=(40, 40, 200))

        # rp - remove passive
        if True:
            def rp_ten_percent_boost():
                Ins.player.atk_boost -= 0.1

    #  hitbox  -  hitbox object
    if True:
        # he - hitbox existing
        if True:
            pass

        # ht - hitbox touching
        if True:
            pass

    #  projectile functions  -  projectile object
    if True:
        # prc - projectile created
        if True:
            pass

        # pre - projectile existing
        if True:
            def pre_bounce_mid(self):
                if self.x < 0 or self.x > 600:
                    self.degree = -self.degree + PI
                if self.y < 0 or self.y > 400:
                    self.degree *= -1
                self.degree %= 2 * PI

        # prd - projectile deleted
        if True:
            pass

        # prh - projectile hit
        if True:
            pass

    #  effect functions  -  effect object
    if True:  # addition of p after prefix means player is targeted, e means enemy is targeted (default is player), starts with b_
        # ec - effect created
        if True:
            def b_ec_p_reckless1(self):
                Ins.player.atk_boost += 0.25
                Ins.player.def_boost -= 0.2

            def b_ec_p_atk_boost1(self):
                Ins.player.atk_boost += 0.25

            def b_ec_p_stance1(self):
                Ins.player.atk_boost += 0.6

            def b_ec_p_stance2(self):
                Ins.player.def_boost += 1 / 3

            def b_ec_p_statBoost1(self):
                t_ec_p_statBoost1(self)

            def b_ec_e_statDebuff1(self):
                b = 0.15
                self.self_data = [int(Battle.enemy_list[4][1] * b), int(Battle.enemy_list[4][2] * b),
                                  int(Battle.enemy_list[4][3] * b), int(Battle.enemy_list[4][4] * b)]
                Battle.enemy_list[4][1] -= self.self_data[0]
                Battle.enemy_list[4][2] -= self.self_data[1]
                Battle.enemy_list[4][3] -= self.self_data[2]
                Battle.enemy_list[4][4] -= self.self_data[3]

            def b_ec_p_dodge1(self):
                t_ec_p_dodge1(self)

        # ee - effect existing
        if True:
            def b_ee_p_mana_regen1(self):
                Ins.player.add_mana(Ins.player.max_mana / 2400)

            def b_ee_p_text(self):
                Screen.win.blit(font.render(self.data[0], False, self.data[2]), self.data[1])

            def b_ee_e_move_enemy(self):
                if self.max_frames != 0:
                    Battle.enemy_x += (self.data[0][0] - self.data[1][0]) / self.max_frames
                    Battle.enemy_y += (self.data[0][1] - self.data[1][1]) / self.max_frames


            def b_ee_p_regeneration1(self):
                Ins.player.add_hp(2 * Ins.player.max_hp / (Battle.effect_duration_battle * 15))

        # ed - effect deleted
        if True:
            def b_ed_e_move_enemy(self):
                Battle.enemy_x = self.data[0][0]
                Battle.enemy_y = self.data[0][1]

            def b_ed_p_atk_boost1(self):
                Ins.player.atk_boost -= 0.25

            def b_ed_p_reckless1(self):
                Ins.player.atk_boost -= 0.25
                Ins.player.def_boost += 0.2

            def b_ed_p_stance1(self):
                Ins.player.atk_boost -= 0.6

            def b_ed_p_stance2(self):
                Ins.player.def_boost -= 1 / 3

            def b_ed_p_statBoost1(self):
                t_ed_p_statBoost1(self)

            def b_ed_e_statDebuff1(self):
                Battle.enemy_list[4][1] += self.self_data[0]
                Battle.enemy_list[4][2] += self.self_data[1]
                Battle.enemy_list[4][3] += self.self_data[2]
                Battle.enemy_list[4][4] += self.self_data[3]

            def b_ed_p_regeneration1(self):
                pass

            def b_ed_p_dodge1(self):
                t_ed_p_dodge1(self)

    #  cut scene function - *args
    if True:
        # cs - cut scene
        def cs_set_screen_size(size_str):
            temp = size_str.split(" ")
            Screen.resize(int(temp[0]) * 64, int(temp[1]) * 64)

        def cs_set_camera(camera_str):
            temp = camera_str.split(" ")
            Screen.cutSceneCameraX = int(temp[0])
            Screen.cutSceneCameraY = int(temp[1])

        def cs_change_map(map_str):
            Screen.cutSceneMap = maps.map_list[map_str]
            # Screen.resize(64 * len(Screen.cutSceneMap[0][0]), 64 * len(Screen.cutSceneMap[0]))

        def cs_change_song(song):
            sounds.play(song, False, False)

        def cs_change_win_name(name):
            pygame.display.set_caption(name)

        def cs_effect(effect):
            sounds.play_effect(effect)

    #  shop functions - *args
    if True:
        # sh - shop
        pass

    #  class functions
    if True:
        # cja - class job addition
        if True:
            def cja_berserker():
                Ins.player.attack += 10
                Ins.player.defense -= 5
                Ins.player.mana += 5

            def cja_ninja():
                Ins.player.attack += 5
                Ins.player.evasion += 10
                Ins.player.hp -= 10

        # cjs - class job subtraction
        if True:
            def cjs_berserker():
                Ins.player.attack -= 10
                Ins.player.defense += 5
                Ins.player.mana -= 5

            def cjs_ninja():
                Ins.player.attack -= 5
                Ins.player.evasion -= 10
                Ins.player.hp += 10

    # battle functions -  *args
    if True:  # bf - battle functions
        def bf_set_mode(mode_num):
            Battle.Sprite.mode = mode_num

        def bf_set_direction(direction_num):
            Battle.Sprite.direction = direction_num

        def bf_add_direction(positive=True):
            if positive:
                Battle.Sprite.direction += 1
                if Battle.Sprite.direction >= 4:
                    Battle.Sprite.direction = 0
            else:
                Battle.Sprite.direction -= 1
                if Battle.Sprite.direction < 0:
                    Battle.Sprite.direction = 3

        def bf_projectile(*args):
            Battle.Projectile(*args)

        def bf_hitbox(*args):
            Battle.Hitbox(*args)

        def bf_effect(*args):
            Battle.Effect(*args)

        def bf_text(text, duration, pos=(300, 0), color=(255, 255, 255)):
            Battle.Effect(effect_time=duration, exist_effect="text", stored_data=(text, pos, color))

        def bf_move_enemy(pos, duration=0):
            Battle.Effect(effect_time=duration, target_player=False, exist_effect="move_enemy", remove_effect="move_enemy", stored_data=(pos, (int(Battle.enemy_x), int(Battle.enemy_y))))

        def bf_remove_all_projectiles():
            Battle.Projectile.projectile_list.clear()

    # battle function
    if True:
        # bf_bg - battle beginning
        if True:
            pass

        # bf_ex - battle existing
        if True:
            pass

        # bf_wn - battle win
        if True:
            def bf_wn_1():
                Screen.open_text([["mr boat man"], ["we are almost there! i can see the land!", [["change_map", "sp_entrance", (14, 1)], "ma_boat_remove"]]])

        # bf_ti - battle tie
        if True:
            pass

    # turns functions - turn enemy object
    if True:
        #  trn_bg - turns battle beginning function
        if True:
            def trn_bg_slime1(self):
                self.info.append(self.y)

            def trn_bg_ninja(self):
                self.info.append((self.x, self.y))
                self.info.append(2)

            def trn_bg_skeleton1(self):
                self.info.append(True)

            def trn_bg_berserker(self):
                self.info.append(True)

        #  trn_ex - turns battle existing function
        if True:
            def trn_ex_skeleton1(self):
                if self.info[0] and self.hp < self.max_hp / 3:
                    if random.random() < 0.5:
                        self.next_attacks.append("boneRestore")
                        self.info[0] = False

            def trn_ex_berserker(self):
                if self.info[0] and self.hp < self.max_hp / 3:
                    if random.random() < 0.7:
                        self.next_attacks.append("heal1")
                        self.info[0] = False

            def trn_ex_ninja(self):
                if self.info[1] > 0 and self.hp < self.max_hp / 3:
                    if random.random() < 0.8:
                        self.next_attacks.append("heal3")
                        self.info[1] -= 1

            def trn_ex_imp3(self):
                if Turns.turn_count == 4:
                    self.next_attacks.append("addTurn")

        # trn_dth - turn battle death function
        if True:
            pass

        # trn_anm - turn battle animation functiom
        if True:  # -> true - animation ended, false animation not ended
            def trn_anm_slime1(self, index, frame):
                if index == 1:
                    self.y = self.info[0] - 60 * frame + 5 * frame ** 2
                    if 60 * frame - 5 * frame ** 2 >= 0:
                        return False
                    else:
                        self.y = int(self.info[0])
                        self.animation(0)
                        return True
                return False

            def trn_anm_berserker(self, index, frame):
                if self.next_attack == "cinders" and frame >= 32:
                    return True
                elif self.next_attack == "slash3" and frame >= 17:
                    return True

            def trn_anm_ninja(self, index, frame):
                if self.next_attack == "tornado" and frame >= 35:
                    return True
                elif self.next_attack == "bigFlurry" and frame == 1:
                    self.x = 237
                    self.y = 316
                return False

        # trn_hit - turns battle hit
        if True:
            def trn_hit_samurai_apple(self, hit, last_hp):
                if self.hp > 0:
                    Ins.player.hp = -1000

        # trn_atk - turn battle attack
        if True:
            def trn_atk_berserker(self, hit, last_hp):
                if Turns.turn_count == 6 or (Turns.turn_count >= 8 and Turns.turn_count % 7 == 0):
                    self.next_attacks.append("cinders")
                    animation("3", "something big is going to happen next turn...", (255, 255, 255), 100, duration=60, layer=400)

            def trn_atk_ninja(self, hit, last_hp):
                if self.next_attack == "bigFlurry":
                    self.x, self.y = self.info[0]
                if Turns.turn_count == 6 or (Turns.turn_count >= 8 and Turns.turn_count % 7 == 0):
                    self.next_attacks.append("bigFlurry")
                    animation("3", "something big is going to happen next turn...", (255, 255, 255), 100, duration=60, layer=400)
        # trn_atk_res - turns attack restraint
        if True:
            def trn_atk_res_berserker(self, atk):
                if atk == "heal1" and self.hp >= self.max_hp * 0.85:
                    return "doubleSlash1"
                return atk

            def trn_atk_res_ninja(self, atk):
                if atk == "heal3" and self.hp >= self.max_hp * 0.78:
                    return "tornado"
                return atk

    # turns effect functions  -  effect object
    if True:  # addition of p after prefix means player is targeted, e means enemy is targeted (default is player), starts with t_
        # ec - effect created
        if True:
            def t_ec_e_atk_boost1(self):
                self.data[0].atk_boost += 0.65

            def t_ec_p_atk_boost1(self):
                Ins.player.atk_boost += 0.25

            def t_ec_p_reckless1(self):
                Ins.player.atk_boost += 0.25
                Ins.player.def_boost -= 0.2

            def t_ec_p_stance1(self):
                Ins.player.atk_boost += 0.6

            def t_ec_p_stance2(self):
                Ins.player.def_boost += 1/3

            def t_ec_p_statBoost1(self):
                b = 0.15
                self.self_data = [int(Ins.player.attack * b), int(Ins.player.defense * b),
                                  int(Ins.player.evasion * b), int(Ins.player.accuracy * b)]
                Ins.player.attack += self.self_data[0]
                Ins.player.defense += self.self_data[1]
                Ins.player.evasion += self.self_data[2]
                Ins.player.accuracy += self.self_data[3]
                Ins.player.crit_rate_const += 0.3

            def t_ec_e_statDebuff1(self):
                b = 0.15
                self.self_data = [int(self.data[0].attack * b), int(self.data[0].defense * b),
                                  int(self.data[0].evasion * b), int(self.data[0].accuracy * b)]
                self.data[0].attack -= self.self_data[0]
                self.data[0].defense -= self.self_data[1]
                self.data[0].evasion -= self.self_data[2]
                self.data[0].accuracy -= self.self_data[3]

            def t_ec_p_slowness(self):
                Ins.player.accuracy -= 10
                Ins.player.evasion -= 10

            def t_ec_p_dodge1(self):
                self.self_data = int(Ins.player.evasion)
                Ins.player.evasion += 3 * self.self_data

        # ee - effect existing
        if True:
            def t_ee_p_mana_regen1(self):
                Ins.player.add_mana(Ins.player.max_mana / 80)

            def t_ee_p_poison1(self):
                Ins.player.add_hp(-3)

            def t_ee_p_burn1(self):
                Ins.player.add_hp(-8)

            def t_ee_p_regeneration1(self):
                if self.frames != 0:
                    Ins.player.add_hp(Ins.player.max_hp // 6)

        # ed - effect deleted
        if True:
            def t_ed_p_regeneration1(self):
                Ins.player.add_hp(Ins.player.max_hp // 6)

            def t_ed_e_atk_boost1(self):
                self.data[0].atk_boost -= 0.65

            def t_ed_p_atk_boost1(self):
                Ins.player.atk_boost -= 0.25

            def t_ed_p_reckless1(self):
                Ins.player.atk_boost -= 0.25
                Ins.player.def_boost += 0.2

            def t_ed_p_stance1(self):
                Ins.player.atk_boost -= 0.6

            def t_ed_p_stance2(self):
                Ins.player.def_boost -= 1 / 3

            def t_ed_p_statBoost1(self):
                Ins.player.attack -= self.self_data[0]
                Ins.player.defense -= self.self_data[1]
                Ins.player.evasion -= self.self_data[2]
                Ins.player.accuracy -= self.self_data[3]
                Ins.player.crit_rate_const -= 0.3

            def t_ed_e_statDebuff1(self):
                self.data[0].attack += self.self_data[0]
                self.data[0].defense += self.self_data[1]
                self.data[0].evasion += self.self_data[2]
                self.data[0].accuracy += self.self_data[3]

            def t_ed_p_slowness(self):
                Ins.player.accuracy += 10
                Ins.player.evasion += 10

            def t_ed_p_dodge1(self):
                Ins.player.evasion -= 3 * self.self_data

    # turns battle function
    if True:
        # trnb_bg - turn beginning func
        if True:
            pass

        # trnb_ex - turn existing
        if True:
            pass

        # trnb_wn - battle win
        if True:
            @save_func(hp_save_first_forest6, 1)
            def trnb_wn_ma_forest6():
                if not Ins.fv.ma_exterminator:
                    hp_save_first_forest6()
                    proceed_mission("the exterminator")
                    Ins.fv.ma_exterminator = True

            def trnb_wn_berserker():
                Screen.open_text([["berserker"], ["i have nothing more to teach you...", [["proceed_mission", "berserker duel", True], ["save_progress", False]]]])

            def trnb_wn_ninja():
                Screen.open_text([["ninja"], ["damn bro... you are strong... ill teach you how to ninja rn ok ok", [["sp_ninja"], ["save_progress"]]]])

            def trnb_wn_samurai_apple():
                Ins.fv.apple = True

    # animation functions
    if True:
        #  anm
        def anm_change_map(goto, goto_pos):
            Ins.player.x = goto_pos[0] * 64 + 32 - Ins.player.width / 2
            Ins.player.y = goto_pos[1] * 64 + 32 - Ins.player.height / 2
            Ins.player.position()
            Screen.select_map(goto)
            Screen.unlock_map_travel(Screen.selected_map_str, True)
            if Ins.settings.allowAutoSaves:
                save_progress()
            
        def anm_unfreeze():
            Screen.freeze_player = False
            if sounds.get_current_song() != Screen.map_song:
                sounds.play(Screen.map_song, True)

        def anm_turns(song):
            Screen.set_state("turns")
            sounds.play(song, False, False)
            Screen.freeze_player = False
            animation("0", 20, ["start_turns"], None)
            animation("player", name="player", point=(237, 276), layer=-1)

        def anm_start_turns():
            Turns.proceed_turn()

        def anm_particles(*args):
            Particles(*args)

        def anm_animation(*args):
            animation(*args[0], **args[1])

        def anm_proceed_mission(mission_str, stage=-1, skip=True):
            proceed_mission(mission_str, stage, skip)

        def anm_sound_effect(effect):
            sounds.play_effect(effect)
        ###

        @save_func(cap=1)
        def anm_ma_story1():
            maps.m_ma_capital[3].pop(3)
            proceed_mission("the exterminator", 1)

        @save_func()
        def anm_remove_hitbox(map_string, x, y):
            maps.map_list[map_string][0][y][x][3] = False

        def anm_fv_set_var(variable, value=False):
            exec(f"Ins.fv.{variable} = value")


        def anm_turns_battle_death():
            Battle.Effect.list_reset()
            sounds.play("death_song", loops=0)
            Screen.set_state("death")
            animation("2")
            Screen.afterBattleScreenVar = 0
            Screen.afterBattleFrame = 0


        def anm_turns_battle_win():
            Battle.Effect.list_reset()
            Ins.player.mana = int(Ins.player.mana)
            sounds.play("winning_song", loops=0, register=False)
            Screen.set_state("winner")
            Screen.afterBattleFrame = 0
            Screen.afterBattleList = [0, 0]

            for enemy in Turns.Enemy.enemy_list:
                Screen.afterBattleList[0] += enemy.exp
                Screen.afterBattleList[1] += enemy.coins
                Ins.stats.monsters_killed += 1
            Screen.afterBattleList[0] += random.randint(Turns.turns_list[4][0], Turns.turns_list[4][1])
            Screen.afterBattleList[1] += random.randint(Turns.turns_list[4][2], Turns.turns_list[4][3])
            Screen.afterBattleList1 = []
            temp_float = math.log10(Screen.afterBattleList[0])
            Screen.afterBattleScreenVar = max(
                10 ** ((int(temp_float) if temp_float - int(temp_float) <= 0.3 else int(temp_float) + 1) - 2), 1)
            Screen.afterBattleTemp = 0
            for enemy in Turns.Enemy.enemy_list:
                for item_list in enemy.loot_table:
                    if item_list[1] >= random.random():
                        temp_choice = random.choice(item_list[2])
                        Ins.player.add_item(item_list[0], temp_choice)
                        for i in range(len(Screen.afterBattleList1)):
                            if Screen.afterBattleList1[i][0] == item_list[0]:
                                Screen.afterBattleList1[i][1] += temp_choice
                                break
                        else:
                            Screen.afterBattleList1.append([item_list[0], temp_choice])

            for item_list in Turns.turns_list[3]:
                if item_list[1] >= random.random():
                    temp_choice = random.choice(item_list[2])
                    Ins.player.add_item(item_list[0], temp_choice)
                    for i in range(len(Screen.afterBattleList1)):
                        if Screen.afterBattleList1[i][0] == item_list[0]:
                            Screen.afterBattleList1[i][1] += temp_choice
                            break
                    else:
                        Screen.afterBattleList1.append([item_list[0], temp_choice])
            Turns.picking_enemy = 0

            try:
                globals()["trnb_wn_" + str(Turns.turns_id)]()
            except KeyError:
                pass

    # particle function - particle object
    if True:
        # prt_bg
        if True:
            def prt_bg_none(self):
                pass

            def prt_bg_rand_decay_fade(self):
                if random.random() < 0.5:
                    self.exist_func.append(["decay", 0.15, 3])

                else:
                    self.exist_func.append(["fade", 4])

        # prt_ex
        if True:
            def prt_ex_none(self):
                pass

            def prt_ex_bounce(self, m=1):
                if self.y < self.size:
                    self.velocity[1] *= -m
                    self.y = self.size + 1
                elif self.y > Screen.window_height - self.size:
                    self.velocity[1] *= -m
                    self.y = Screen.window_height - self.size - 1

                if self.x < self.size:
                    self.velocity[0] *= -m
                    self.x = self.size + 1
                elif self.x > Screen.window_width - self.size:
                    self.velocity[0] *= -m
                    self.x = Screen.window_width - self.size - 1

            def prt_ex_friction(self, f):
                self.forces.append([-f * self.velocity[0], -f * self.velocity[1]])

            def prt_ex_rotation_friction(self, f):
                self.rotate_speed *= f

            def prt_ex_decay(self, d, s=0):
                if self.frame >= s:
                    self.size -= d
                if self.size <= 0:
                    return True

            def prt_ex_inward_force(self, y, f=1):
                self.forces.append([0, (y - self.y) * f])

            def prt_ex_missile(self, f=1):
                self.rotate = math.atan2(-self.velocity[1], -self.velocity[0])
                self.forces.append([f * (237 - self.x), f * (276 - self.y)])

            def prt_ex_fade(self, a, s=0):
                if self.frame >= s:
                    self.alpha -= a
                if self.alpha <= 0:
                    return True

        # prt_dth
        if True:
            def prt_dth_none(self):
                pass

    # attack function, atk_fnc  -  enemy object, did hit, [target]
    if True:
        def atk_fnc_e_test(self, hit, target):
            ang = math.atan2(self.y - 276, self.x - 237)
            # print([3 * PI / 4 + ang, 5 * PI / 4 + ang])

            r = 2
            if r == 1:
                particles("circle", [5, 9], [135, 35, 35, 30, 15, 15], [237, 276, 20, 40], 50, 0, ["strict_up", "strict_down"], 5, 0, 15, exist_func=[["friction", 0.95], ["decay", 0.1, 10], ["bounce", 0.65]])
            elif r == 2:
                particles(["star", "triangle", "square"], [12, 14], [140, 140, 140, 40, 40, 40], [237, 276, 30], 50, 1, "all", [10, 16], 2, 0,
                          exist_func=[["friction", 5], ["decay", 0.2, 3], ["rotation_friction", 0.95]], rotation=True, rotation_speed=[[0.1, 0.25], [-0.25, -0.1]])
            elif r == 3:
                particles("square", 4, [255, 255, 255], [220, 276, 0, 40], 120, 0,
                          [3 * PI / 4 + ang, 5 * PI / 4 + ang], 7, 0, 0, exist_func=[["friction", 0.92], ["decay", 0.1, 10], ["inward_force", 276, 2.5], ["bounce"]], rotation=True)
            else:
                particles(["circle", "square"], 8, [255, 255, 255], [self.x, self.y, 30], 50, 0, "all", 5, 0, 0,
                          exist_func=[["missile", 1.5], ["friction", 2], ["decay", 0.1, 45]])

        def atk_fnc_e_slash1(self, hit, target):
            if hit:
                particles("circle", [3, 6], [150, 40, 40, 30, 15, 15], [237, 276, 20, 40], 50, 0,
                          ["strict_up", "strict_down"], 4, 0, 15,
                          exist_func=[["friction", 1], ["decay", 0.08, 10], ["bounce", 0.7]])

        def atk_fnc_e_stab1(self, hit, target):
            if hit:
                particles("circle", [4, 7], [160, 40, 40, 30, 15, 15], [237, 276, 20, 40], 50, 0,
                          "strict_left", 4, 0, 15,
                          exist_func=[["friction", 1], ["decay", 0.08, 10], ["bounce", 0.7]])

        def atk_fnc_e_heal1(self, hit, target):
            particles("plus", [10, 12], [40, 160, 40, 3, 10, 3], [target[0].x, target[0].y, 40, 15], 6, 12, -PI/2, 3, gravity=0, exist_func=[["friction", 1], ["fade", 5]])

        def atk_fnc_e_heal2(self, hit, target):
            for tar in target:
                particles("plus", [10, 12], [40, 160, 40, 3, 10, 3], [tar.x, tar.y, 40], 6, 12, "strict_up", 3, gravity=0, exist_func=[["friction", 1], ["fade", 3]])

        def atk_fnc_e_magicRay1(self, hit, target):
            particles(["star", "triangle", "square"], [10, 12], [200, 50, 230, 20, 20, 20], [237, 276, 30], 30, 1,
                      "all", [10, 16], 2, 0,
                      exist_func=[["friction", 5], ["decay", 0.2, 3], ["rotation_friction", 0.95]], rotation=True,
                      rotation_speed=[[0.1, 0.25], [-0.25, -0.1]])

        def atk_fnc_e_magicBlast1(self, hit, target):
            particles(["star", "triangle", "square"], [14, 17], [140, 30, 170, 20, 20, 20], [237, 276, 30], 65, 0,
                      "all", [10, 16], 2, 0,
                      exist_func=[["friction", 5], ["decay", 0.2, 3], ["rotation_friction", 0.95]], rotation=True,
                      rotation_speed=[[0.1, 0.25], [-0.25, -0.1]])

        def atk_fnc_e_boneRestore(self, hit, target):
            self.add_hp((self.max_hp - self.hp) / 2)
            particles("plus", [10, 12], [40, 160, 40, 3, 10, 3], [self.x, self.y, 40], 6, 12, "all", 3, gravity=0,
                      exist_func=[["friction", 1], ["fade", 3]])

            # types, size, color, area, count, duration, direction, velocity, full = 0,
            # gravity = 9.78, gravity_angle = PI / 2, beginning_func = None, exist_func = None, death_func = None,
            # rotation = None, rotation_speed = None, alpha = None, tags = None)

        def atk_fnc_e_atkBoost1(self, hit, target):
            particles("arrow", [10, 13], [220, 70, 10, 20, 20, 10], [self.x, self.y, 40, 10], 15, 5,
                      -PI/2, [7, 10], 0, 0,
                      exist_func=[["friction", 3.3], ["fade", 4, 6]], rotation=-PI/2)

        def atk_fnc_e_cinders(self, hit, target):
            animation("flash", (255, 0, 0), 4, 1)

        def atk_fnc_e_addTurn(self, hit, target):
            Turns.turn_order_next.append(self)


        def atk_fnc_e_heal3(self, hit, target):
            particles("plus", [10, 12], [40, 160, 40, 3, 10, 3], [self.x, self.y, 20], 24, 8, "all", 2, gravity=0,
                      exist_func=[["friction", 1]], beginning_func="rand_decay_fade")

        ### 237, 276
        def atk_fnc_p_fist_attack(self, hit):
            if hit:
                hp_bleed_particles(self, [4, 5], "strict_right")

        def atk_fnc_p_light_sword_attack(self, hit):
            if hit:
                hp_bleed_particles(self, [5, 6], ["strict_up", "strict_down"])

        def atk_fnc_p_heavy_sword_attack(self, hit):
            if hit:
                hp_bleed_particles(self, [6, 7], ["strict_up", "strict_down"])

        def atk_fnc_p_light_bow_attack(self, hit):
            if hit:
                hp_bleed_particles(self, [5, 6], "strict_right")

        def atk_fnc_p_heavy_bow_attack(self, hit):
            if hit:
                hp_bleed_particles(self, [6, 7], "strict_right")

        def atk_fnc_p_light_staff_attack(self, hit):
            if hit:
                hp_bleed_particles(self, [5, 6], ["strict_up", "strict_down"])

        def atk_fnc_p_heavy_staff_attack(self, hit):
            if hit:
                hp_bleed_particles(self, [6, 7], ["strict_up", "strict_down"])

        def atk_fnc_p_heal(self, hit):
            particles("plus", [10, 12], [40, 160, 40, 3, 10, 3], [237, 276, 40, 25], 12, 12, -PI/2, 2, gravity=0, exist_func=[["friction", 1], ["fade", 5]])

        def atk_fnc_p_purify(self, hit):
            if hit:
                particles("circle", [7, 11], [200, 230, 80, 20, 20, 20], [self.x, self.y, 7],
                          40, 8, "all", 4, 2, gravity=0, beginning_func="rand_decay_fade",
                          exist_func=[["friction", 0.8]])

        def atk_fnc_p_stats_boost(self, hit):
            particles("arrow", [9, 11], [220, 70, 10, 20, 20, 10], [237, 316, 40, 10], 15, 5,
                      -PI / 2, [9, 11], 0, 0,
                      exist_func=[["friction", 4], ["fade", 6, 6]], rotation=-PI / 2)

        def atk_fnc_p_stats_debuff(self, hit):
            particles("arrow", [8, 10], [10, 10, 180, 10, 10, 20], [self.x, self.y, self.w // 2, self.h // 2], 15, 5,
                      PI / 2, [7, 10], 0, 0,
                      exist_func=[["friction", 4], ["fade", 6, 6]], rotation=PI / 2)

        def atk_fnc_p_regeneration(self, hit):
            particles("plus", [10, 12], [40, 160, 40, 3, 10, 3], [237, 276, 40, 25], 12, 12, "all", 2, gravity=0, exist_func=[["friction", 1], ["fade", 5]])

        def atk_fnc_p_attack_stance(self, hit):
            particles("circle", [3, 4], [255, 80, 80], [237, 276 + 40, 30, 0], 80, 5, [[-0.1, 0.1], [PI-0.1, PI+0.1]], [0, 2], gravity=0, exist_func=[["friction", 1], ["fade", 5]])

        def atk_fnc_p_defense_stance(self, hit):
            particles("circle", [3, 4], [40, 40, 160], [237, 276 + 40, 30, 0], 80, 5, [[-0.1, 0.1], [PI-0.1, PI+0.1]], [0, 2], gravity=0, exist_func=[["friction", 1], ["fade", 5]])

    # class attacks  -
    if True:
        # cat_con - attack conditions
        if True:
            def cat_con_None(is_turns, index):
                if index == 0:
                    return True

            def cat_con_berserker(is_turns, index):
                if index == 0:
                    if Ins.player.mana >= 20 and not Battle.battle_variables["berserkerUsed"]:
                        return True
                elif index == 1:
                    if Ins.player.mana == Ins.player.max_mana:
                        return True

            def cat_con_ninja(is_turns, index):
                if index == 0:
                    if not Battle.battle_variables["ninjaUsed"] and Ins.player.mana >= 20:
                        return True
                elif index == 1:
                    return True

        # cat_act - attack action
        if True:
            def cat_act_berserker(is_turns, index):
                if index == 0:
                    Battle.Effect("reckless", 3, True, "reckless1", "none", "reckless1", (255, 255, 255))
                    Ins.player.add_mana(-20)
                    Battle.battle_variables["berserkerUsed"] = True
                    if is_turns:
                        particles("arrow", [9, 11], [220, 70, 10, 20, 20, 10], [237, 316, 40, 10], 15, 5,
                                  -PI / 2, [9, 11], 0, 0,
                                  exist_func=[["friction", 4], ["fade", 6, 6]], rotation=-PI / 2)
                        particles("arrow", [8, 10], [10, 10, 180, 10, 10, 20], [237, 236, 40, 10], 15, 5,
                                  PI / 2, [7, 10], 0, 0,
                                  exist_func=[["friction", 4], ["fade", 6, 6]], rotation=PI / 2)

                        animation("0", 15, ["start_turns"], None)
                elif index == 1:
                    Ins.player.mana = 0
                    Ins.player.add_hp(-Ins.player.hp // 2)
                    if is_turns:
                        particles("circle", [4, 7], [160, 40, 40, 30, 15, 15], [237, 276, 20, 40], 50, 0,
                                  "all", 4, 0, 15,
                                  exist_func=[["friction", 1], ["decay", 0.08, 10], ["bounce", 0.7]])
                        for enemy in Turns.alive_enemies:
                            enemy.add_hp(-enemy.hp // 3)
                            particles("circle", [4, 7], [160, 40, 40, 30, 15, 15], [enemy.x, enemy.y, 20, 40], 50, 0,
                                      "all", 4, 0, 15,
                                      exist_func=[["friction", 1], ["decay", 0.08, 10], ["bounce", 0.7]])
                        animation("0", 15, ["start_turns"], None)
                    else:
                        Battle.enemy_hp //= 3
                        Battle.enemy_hp *= 2

            def cat_act_ninja(is_turns, index):
                if index == 0:
                    Battle.Effect("dodge boost", 3, True, "dodge1", "none", "dodge1", (255, 255, 255))
                    Ins.player.add_mana(-20)
                    Battle.battle_variables["ninjaUsed"] = True
                    if is_turns:
                        particles("circle", [4, 8], [0, 150, 200, 0, 10, 15], [237, 276, 7],
                                  40, 8, "all", 4, 2, gravity=0, beginning_func="rand_decay_fade",
                                  exist_func=[["friction", 2]])
                        animation("0", 15, ["start_turns"], None)
                elif index == 1:
                    Battle.battle_variables["ninjaTimesUsed"] += 1
                    if is_turns:
                        particles("arrow", [9, 11], [220, 70, 10, 20, 20, 10], [237, 276, 40, 10], 15, 5,
                                  -PI / 2, [9, 11], 0, 0,
                                  exist_func=[["friction", 4], ["fade", 6, 6]], rotation=-PI / 2)
                        animation("0", 15, ["start_turns"], None)
                        Ins.player.add_attack(2)
                        Ins.player.atk_boost += 0.1
                    else:
                        Ins.player.add_attack(1)
                        Ins.player.atk_boost += 0.05

            def cat_act_None(is_turns, index):
                if index == 0:
                    if is_turns:
                        animation("0", 15, ["start_turns"], None)

    # map functions
    if True:
        # mp_st
        if True:
            pass

        # mp_ex
        if True:
            def mp_ex_ma_forest():
                surface1 = pygame.Surface((Screen.window_width, Screen.window_height))
                surface1.set_alpha(180)
                surface1.fill((0, 0, 0))
                Screen.win.blit(surface1, (0, 0))

        # mp_ed
        if True:
            pass


# global "pointers"
class Ins:
    fv = None
    stats = None
    ap = None
    player = None
    settings = None
