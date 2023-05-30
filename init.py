import pygame.draw
from classes import *
__author__ = "erez"


# game's main code
def main():
    if True:
        _line = 0
        _travel_count = -1
        _temp_mission_list = []

    Ins.settings = Settings()
    if os.path.exists("save/settings.txt"):
        _f = open("save/settings.txt", "rb")
        Ins.settings = pickle.load(_f)
    else:
        _f = open("save/settings.txt", "wb")
        pickle.dump(Ins.settings, _f)

    _f.close()
    if not os.path.exists("save/info.txt"):
        _f = open("save/info.txt", "wb")
        pickle.dump([[0, 0, 0, 0], ["start new game", "start new game", "start new game", "start new game"]], _f)
    _f.close()
    Ins.settings.save()

    sounds.play("menu")
    pygame.display.set_caption("menu")
    stats_list = []  # stats_list = Ins.stats.__dict__.keys()  # max per page - 32
    Screen.set_state("mainMenu")

    while Screen.run:
        if Game.delta < 1:
            Game.current_time = time.time()
            Game.delta += (Game.current_time - Game.last_time) * Game.ticks_per_second
            Game.last_time = float(Game.current_time)
        if time.time() - Game.time_start > 1:
            Game.time_start += 1
            #print(Game.frame)
            Game.frame = 0

        if Game.delta > 5:
            Game.delta = 5
        if Game.delta < 1:
            continue
        else:
            Game.delta -= 1
            Game.frames += 1
            Game.frame += 1
        ##################################################  global code
        Screen.mouse_pos = pygame.mouse.get_pos()
        key_list()
        Screen.win.fill((0, 0, 0))
        Animation.animated = False
        Particles.rendered = False
        sounds.handle()
        # if not keysDown["f"] and not keysHeld["g"]:
        #     continue
        ##################################################  loops - main menu
        if Screen.state("mainMenu"):
            if Menu.frame >= 4096:
                Menu.frame = 0
            Screen.win.blit(textures.menu_bg, (int(-Menu.frame / 2), -212 - int(40 * math.sin(PI*Menu.frame/512))))
            Screen.win.blit(textures.menu_bg, (2048 + int(-Menu.frame / 2), -212 - int(40 * math.sin(PI*Menu.frame/512))))
            surface1 = pygame.font.SysFont("Aharoni", min(int(Menu.frame1 / 3), 60), 4).render("blank", False, (255, 255, 255))
            Screen.win.blit(surface1, (500 - int(surface1.get_width() / 2) - 25 * Menu.open_index, 100))
            surface1 = pygame.font.SysFont("Aharoni", 20).render("created by erez", False, (255, 255, 255))
            Screen.win.blit(surface1, (2, 600 - int(surface1.get_height())))

            if Menu.frame1 > 100:
                surface1 = pygame.font.SysFont("Aharoni", min(int(Menu.frame1 / 2 - 50), 30)).render("start", False, (80, 255, 80) if Menu.choose == 0 else (255, 255, 255))
                Screen.win.blit(surface1, (500 - int(surface1.get_width() / 2) - 25 * Menu.open_index, 300))
                surface1 = pygame.font.SysFont("Aharoni", min(int(Menu.frame1 / 2 - 50), 30)).render("options", False, (80, 255, 80) if Menu.choose == 1 else (255, 255, 255))
                Screen.win.blit(surface1, (500 - int(surface1.get_width() / 2) - 25 * Menu.open_index, 350))
                surface1 = pygame.font.SysFont("Aharoni", min(int(Menu.frame1 / 2 - 50), 30)).render("quit", False, (80, 255, 80) if Menu.choose == 2 else (255, 255, 255))
                Screen.win.blit(surface1, (500 - int(surface1.get_width() / 2) - 25 * Menu.open_index, 400))

            if Menu.frame1 > 200:

                if Menu.opened:
                    if Menu.open_index < 6:
                        Menu.open_index += 1

                else:
                    if Menu.open_index >= 1:
                        Menu.open_index -= 1

                if Menu.open_index >= 1:
                    pygame.draw.rect(Screen.win, (0, 0, 0), (1000 - 50 * Menu.open_index, 0, 300, 600))

                if Menu.choose is not None and Menu.choose >= 3:
                    if Menu.is_start:  # start menu
                        if keysDown[Ins.settings.move_up]:
                            sounds.play_effect("effect6")
                            Menu.choose -= 1
                            if Menu.choose < 3:
                                Menu.choose = (7 if Menu.file_choose else 10)

                        if keysDown[Ins.settings.move_down]:
                            sounds.play_effect("effect6")
                            Menu.choose += 1
                            if Menu.choose > (7 if Menu.file_choose else 10):
                                Menu.choose = 3

                        surface1 = font.render("saves:", False, (255, 255, 255))
                        Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 5))
                        surface1 = font.render("<back", False, ((255, 80, 80) if Menu.file_choose else (80, 255, 80)) if Menu.choose == 3 else (255, 255, 255))
                        Screen.win.blit(surface1, (890 + 50 * (6 - Menu.open_index), 5))

                        for i in range(4):
                            pygame.draw.rect(Screen.win, ((255, 80, 80) if Menu.file_choose else (80, 255, 80)) if Menu.choose == i+4 else (255, 255, 255), (710 + 50 * (6 - Menu.open_index), 45 + 110 * i, 280, 100), 2)
                            surface1 = font.render(f"save slot {i + 1}", False, ((255, 80, 80) if Menu.file_choose else (80, 255, 80)) if Menu.choose == i + 4 else (255, 255, 255))
                            Screen.win.blit(surface1, (715 + 50 * (6 - Menu.open_index), 50 + 110 * i))
                            if Menu.file_exist[i]:
                                surface1 = font.render(f'{Menu.file_sec[i] // 3600}:{Menu.file_sec[i] // 60 % 60} hours' if Menu.file_sec[i] / 60 >= 60 else f'{Menu.file_sec[i] //60} mins', False, ((255, 80, 80) if Menu.file_choose else (80, 255, 80)) if Menu.choose == i + 4 else (255, 255, 255))
                                Screen.win.blit(surface1, (715 + 50 * (6 - Menu.open_index), 80 + 110 * i))
                            surface1 = font.render(Menu.file_loc[i], False, ((255, 80, 80) if Menu.file_choose else (80, 255, 80)) if Menu.choose == i + 4 else (255, 255, 255))
                            Screen.win.blit(surface1, (715 + 50 * (6 - Menu.open_index), 110 + 110 * i))

                        surface1 = font.render("delete profile", False, (80, 255, 80) if Menu.choose == 8 else (255, 255, 255))
                        Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 485))
                        surface1 = font.render("view tutorial", False, (80, 255, 80) if Menu.choose == 9 else (255, 255, 255))
                        Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 520))
                        surface1 = font.render("duplicate save", False, (80, 255, 80) if Menu.choose == 10 else (255, 255, 255))
                        Screen.win.blit(surface1, (710 + 50 * (6 - Menu.open_index), 555))

                        if keysDown[Ins.settings.interact]:
                            if Menu.choose == 3:
                                if Menu.file_choose:
                                    Menu.file_choose = False
                                else:
                                    Menu.opened = False
                                    Menu.choose = 0
                            elif 4 <= Menu.choose <= 7:
                                if Menu.file_choose:
                                    if Menu.delete_file:
                                        if Menu.file_exist[Menu.choose - 4]:
                                            os.remove(f"./save/world{Menu.choose-3}.txt")
                                            Menu.file_loc[Menu.choose-4] = "start new game"
                                            Menu.file_sec[Menu.choose-4] = 0
                                            f = open(f"save/info.txt", "wb")
                                            pickle.dump([Menu.file_sec, Menu.file_loc], f)
                                            f.close()
                                            Menu.file_exist[Menu.choose - 4] = False
                                    else:
                                        if Menu.file_exist[Menu.choose - 4]:
                                            c = 1
                                            while os.path.exists(f"./save_copies/world{Menu.choose-3}copy{c}.txt"):
                                                c += 1
                                            f = open(f"./save_copies/world{Menu.choose-3}copy{c}.txt", "wb")
                                            d = open(f"./save/world{Menu.choose-3}.txt", "rb")
                                            b = d.read()
                                            f.write(b)
                                            d.close()
                                            f.close()
                                    Menu.file_choose = False
                                    Menu.choose = 3
                                else:
                                    Menu.current_save_slot = Menu.choose - 3
                                    Menu.time = pygame.time.get_ticks()
                                    Menu.selected_world = Menu.choose - 3
                                    if Menu.file_exist[Menu.choose - 4]:
                                        load_save()
                                    else:
                                        f = open(f"save/world{Menu.choose-3}.txt", "wb")
                                        Ins.player, Ins.ap, Ins.fv, Ins.stats = Player(), AP(), FV(), Stats()
                                        pickle.dump([Ins.player, Ins.ap, Ins.fv, Ins.stats], f)
                                        f.close()
                                        Screen.select_map(Ins.ap.player_map)
                                    Screen.set_state("world")
                                    continue
                            elif Menu.choose == 8:
                                Menu.choose = 4
                                Menu.delete_file = True
                                Menu.file_choose = True
                            elif Menu.choose == 9:
                                sounds.play_effect("effect9")
                                Screen.tutorial_index = 0
                                Screen.tutorial_in_game = False
                                Screen.set_state("tutorial")
                                continue
                            elif Menu.choose == 10:
                                Menu.choose = 4
                                Menu.delete_file = False
                                Menu.file_choose = True

                    else:  # options
                        run_settings(False)

                    if keysDown["esc"]:
                        if Menu.file_choose:
                            Menu.file_choose = False
                            Menu.choose = 3
                        else:
                            Menu.opened = False
                            Menu.choose = 1 - int(Menu.is_start)

                else:
                    if keysDown[Ins.settings.move_up]:
                        if Menu.choose is None:
                            Menu.choose = 1
                        Menu.choose -= 1
                        if Menu.choose < 0:
                            Menu.choose = 2
                        sounds.play_effect("effect6")

                    if keysDown[Ins.settings.move_down]:
                        if Menu.choose is None:
                            Menu.choose = 2
                        Menu.choose += 1
                        if Menu.choose > 2:
                            Menu.choose = 0
                        sounds.play_effect("effect6")

                    if keysDown[Ins.settings.interact]:
                        sounds.play_effect("effect6")
                        if Menu.choose is None:
                            Menu.choose = 0
                        elif Menu.choose == 0:
                            Menu.opened = True
                            Menu.choose = 3
                            Menu.is_start = True
                            Menu.file_exist = [os.path.exists(f"./save/world{i+1}.txt") for i in range(4)]
                            f = open("./save/info.txt", "rb")
                            Menu.file_sec, Menu.file_loc = pickle.load(f)
                            f.close()
                        elif Menu.choose == 1:
                            Menu.opened = True
                            Menu.choose = 3
                            Menu.is_start = False
                            Temp.settings = Settings()
                            Temp.settings.copy_from(Ins.settings)
                        elif Menu.choose == 2:
                            Screen.run = False

            elif keysDown[Ins.settings.interact]:
                Menu.frame1 = 250

            Menu.frame += 2
            Menu.frame1 += 1
        # menu
        elif Screen.state("menu"):
            ##############################################  draw
            if Screen.menu_num == 1:
                Screen.items_in_roller = 0
                try:
                    for _item_number in range(5):
                        if Ins.player.inventory[Screen.inventory_roller * 5 + _item_number]:
                            pass
                        Screen.items_in_roller += 1
                except IndexError:
                    if Screen.in_menu_num > Screen.items_in_roller:
                        Screen.in_menu_num = Screen.items_in_roller
                if Screen.items_in_roller == 0:
                    Screen.inventory_roller -= 1
                    Screen.inventory_roller = max(0, Screen.inventory_roller)
                    Screen.in_menu_num = 5
            if True:
                pygame.draw.rect(Screen.win, (110, 110, 110), (10, 10, 1000, 788))
                pygame.draw.rect(Screen.win, (140, 140, 140), (20, 50, 980, 295))
                pygame.draw.rect(Screen.win, (140, 140, 140), (20, 385, 510, 207))
                pygame.draw.rect(Screen.win, (140, 140, 140), (545, 385, 455, 207))

                """pygame.draw.rect(Screen.win, (180, 180, 180), (25, 55, 970, 53))
                pygame.draw.rect(Screen.win, (180, 180, 180), (25, 113, 970, 53))
                pygame.draw.rect(Screen.win, (180, 180, 180), (25, 171, 970, 53))
                pygame.draw.rect(Screen.win, (180, 180, 180), (25, 229, 970, 53))
                pygame.draw.rect(Screen.win, (180, 180, 180), (25, 287, 970, 53))"""

                pygame.draw.rect(Screen.win, (180, 180, 180), (25, 390, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (25, 491, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (126, 390, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (126, 491, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (227, 390, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (328, 390, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (429, 390, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (227, 491, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (328, 491, 96, 96))
                pygame.draw.rect(Screen.win, (180, 180, 180), (429, 491, 96, 96))

                surface1 = font4.render("inventory: page {}".format(Screen.inventory_roller+1 if Screen.inventory_roller != -1 else 1), False, (80, 255, 80) if Screen.menu_num == 1 else (0, 0, 0))
                Screen.win.blit(surface1, (20, 10))
                surface1 = font4.render("equipment:", False, (80, 255, 80) if Screen.menu_num == 2 else (0, 0, 0))
                Screen.win.blit(surface1, (20, 345))
                surface1 = font4.render("stats:", False, (80, 255, 80) if Screen.menu_num == 3 else (0, 0, 0))
                Screen.win.blit(surface1, (545, 345))

                surface1 = font4.render("max hp: {}".format(Ins.player.max_hp), False, (80, 255, 80) if Screen.menu_num == 3 and Screen.in_menu_num == 1 else (0, 0, 0))
                Screen.win.blit(surface1, (550, 382))
                surface1 = font4.render("hp: {}".format(int(Ins.player.hp)), False, (0, 0, 0))
                Screen.win.blit(surface1, (795, 382))
                surface1 = font4.render("max mana: {}".format(Ins.player.max_mana), False, (80, 255, 80) if Screen.menu_num == 3 and Screen.in_menu_num == 3 else (0, 0, 0))
                Screen.win.blit(surface1, (550, 417))
                surface1 = font4.render("mana: {}".format(int(Ins.player.mana)), False, (0, 0, 0))
                Screen.win.blit(surface1, (795, 417))
                surface1 = font4.render("attack: {}".format(floated_int(Ins.player.attack)), False, (80, 255, 80) if Screen.menu_num == 3 and Screen.in_menu_num == 5 else (0, 0, 0))
                Screen.win.blit(surface1, (550, 452))
                surface1 = font4.render("defense: {}".format(floated_int(Ins.player.defense)), False, (80, 255, 80) if Screen.menu_num == 3 and Screen.in_menu_num == 6 else (0, 0, 0))
                Screen.win.blit(surface1, (795, 452))
                surface1 = font4.render("accuracy: {}".format(floated_int(Ins.player.accuracy)), False, (80, 255, 80) if Screen.menu_num == 3 and Screen.in_menu_num == 7 else (0, 0, 0))
                Screen.win.blit(surface1, (550, 487))
                surface1 = font4.render("evasion: {}".format(floated_int(Ins.player.evasion)), False, (80, 255, 80) if Screen.menu_num == 3 and Screen.in_menu_num == 8 else (0, 0, 0))
                Screen.win.blit(surface1, (795, 487))
                surface1 = font4.render("exp: {}".format(Ins.player.total_exp), False, (0, 0, 0))
                Screen.win.blit(surface1, (550, 522))
                surface1 = font4.render("level: {}".format(Ins.player.level), False, (0, 0, 0))
                Screen.win.blit(surface1, (795, 522))
                surface1 = font4.render("coins: {}".format(Ins.player.coins), False, (0, 0, 0))
                Screen.win.blit(surface1, (550, 557))
                surface1 = font4.render("LP: {}".format(Ins.player.level_points), False, (0, 0, 0))
                Screen.win.blit(surface1, (795, 557))

                surface1 = font4.render("scrolls: page {}".format(Screen.scroll_roller + 1), False, (80, 255, 80) if Screen.menu_num == 4 else (0, 0, 0))
                Screen.win.blit(surface1, (20, 592))
                pygame.draw.rect(Screen.win, (140, 140, 140), (20, 632, 308, 106))
                for num in range(3):
                    pygame.draw.rect(Screen.win, (80, 255, 80) if Screen.menu_num == 4 and Screen.in_menu_num == num + 1 else (180, 180, 180), (25 + num * 101, 637, 96, 96))
                try:
                    for scroll_index in range(3):
                        Screen.win.blit(textures.scroll_select if scroll_index + 1 == (-1 if Ins.player.scroll is None else (Ins.player.scroll - 3 * Screen.scroll_roller)) else (textures.scroll_equip if Requires.scrolls_req[Screen.scroll_roller * 3 + scroll_index + 1][0] else textures.scroll_unequip), (25 + 101 * scroll_index, 637))
                except KeyError:
                    pass

                surface1 = font4.render("scripts: page {}".format(Screen.script_roller + 1), False, (80, 255, 80) if Screen.menu_num == 5 else (0, 0, 0))
                Screen.win.blit(surface1, (338, 592))
                pygame.draw.rect(Screen.win, (140, 140, 140), (338, 632, 308, 106))
                for num in range(3):
                    pygame.draw.rect(Screen.win, (80, 255, 80) if Screen.menu_num == 5 and Screen.in_menu_num == num + 1 else (180, 180, 180), (343 + num * 101, 637, 96, 96))
                try:
                    for script_index in range(3):
                        Screen.win.blit((textures.script_select if script_index + 1 == (-1 if Ins.player.script is None else (Ins.player.script - 3 * Screen.script_roller)) else textures.script_equip) if Requires.scripts_req[Screen.script_roller * 3 + script_index + 1][0] else textures.script_unequip, (343 + 101 * script_index, 637))
                except KeyError:
                    pass

                surface1 = font4.render("miscellaneous:", False, (80, 255, 80) if Screen.menu_num == 6 else (0, 0, 0))
                Screen.win.blit(surface1, (656, 592))
                pygame.draw.rect(Screen.win, (140, 140, 140), (656, 632, 344, 106))
                surface1 = font5.render("tutorial", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 1 else (0, 0, 0))
                Screen.win.blit(surface1, (665, 635))
                surface1 = font5.render("journal", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 2 else (0, 0, 0))
                Screen.win.blit(surface1, (780, 635))
                surface1 = font5.render("travel", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 3 else (0, 0, 0))
                Screen.win.blit(surface1, (890, 635))
                surface1 = font5.render("console", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 4 else (0, 0, 0))
                Screen.win.blit(surface1, (665, 670))
                surface1 = font5.render("settings", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 5 else (0, 0, 0))
                Screen.win.blit(surface1, (780, 670))
                surface1 = font5.render("stats", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 6 else (0, 0, 0))
                Screen.win.blit(surface1, (895, 670))
                surface1 = font5.render("menu", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 7 else (0, 0, 0))
                Screen.win.blit(surface1, (665, 702))
                surface1 = font5.render("class", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 8 else (0, 0, 0))
                Screen.win.blit(surface1, (780, 702))
                surface1 = font5.render("quit", False, (80, 255, 80) if Screen.menu_num == 6 and Screen.in_menu_num == 9 else (0, 0, 0))
                Screen.win.blit(surface1, (890, 702))

                if Screen.menu_num == 2:
                    for num in range(5):
                        if Screen.in_menu_num == 2 * num + 1:
                            pygame.draw.rect(Screen.win, (80, 255, 80), (25 + num * 101, 390, 96, 96))
                        if Screen.in_menu_num == 2 * num + 2:
                            pygame.draw.rect(Screen.win, (80, 255, 80), (25 + num * 101, 491, 96, 96))

                Screen.win.blit(textures.accessory_unequip if Ins.player.accessory1 is None else textures.accessory_equip, (328, 491))
                Screen.win.blit(textures.accessory_unequip if Ins.player.accessory2 is None else textures.accessory_equip, (429, 491))
                Screen.win.blit(textures.bow_unequip if Ins.player.bow is None else textures.bow_equip, (126, 491))
                Screen.win.blit(textures.chestplate_unequip if Ins.player.chestplate is None else textures.chestplate_equip, (126, 390))
                Screen.win.blit(textures.helmet_unequip if Ins.player.helmet is None else textures.helmet_equip, (25, 390))
                Screen.win.blit(textures.leggings_unequip if Ins.player.leggings is None else textures.leggings_equip, (227, 390))
                Screen.win.blit(textures.relic_unequip if Ins.player.relic is None else textures.relic_equip, (429, 390))
                Screen.win.blit(textures.staff_unequip if Ins.player.staff is None else textures.staff_equip, (227, 491))
                Screen.win.blit(textures.sword_unequip if Ins.player.sword is None else textures.sword_equip, (25, 491))
                Screen.win.blit(textures.talisman_unequip if Ins.player.talisman is None else textures.talisman_equip, (328, 390))

                _counter = 0
                for [_item, _] in Ins.player.inventory[Screen.inventory_roller * 5:Screen.inventory_roller * 5 + 5]:
                    pygame.draw.rect(Screen.win, (35, 35, 165) if _item in Ins.player.battle_inventory else (180, 180, 180), (25, 55 + _counter, 970, 53))
                    _counter += 58
                if Screen.items_in_roller != 0 and Screen.menu_num == 1:
                    pygame.draw.rect(Screen.win, (70, 70, 250) if Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0]
                                                                   in Ins.player.battle_inventory else (80, 255, 80), (25, 58 * Screen.in_menu_num - 3, 970, 53))
                _counter = 0
                for [_item, _amount] in Ins.player.inventory[Screen.inventory_roller * 5:Screen.inventory_roller * 5 + 5]:
                    surface1 = font2.render("{} {} {}".format(_amount, (items[_item][1] if _amount > 1 else _item) + (":" if items[_item][0] else ""), items[_item][0]), False, (0, 0, 0))
                    Screen.win.blit(surface1, (30, 55 + _counter))
                    Screen.win.blit(textures.small_inventory_icons[items[_item][3]], (943, 58 + _counter))
                    _counter += 58
                Screen.inventory_roller_max = int(math.ceil(len(Ins.player.inventory) / 5) - 1)
            ##############################################
            if Screen.menu_num == 1:
                pygame.draw.rect(Screen.win, (80, 255, 80), (20, 50, 980, 295), 1)
                if Screen.items_in_roller != 0:
                    Screen.description_message = Screen.get_text_format(items[Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0]][2], 845, font3)

                if Screen.is_question:
                    if keysDown[Ins.settings.other_function]:
                        Screen.is_question = False
                        if Screen.temp_num == 1:
                            if Ins.player.level >= items[Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0]][7]:
                                if Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0] in Ins.player.battle_inventory:
                                    Ins.player.battle_inventory.pop(Ins.player.battle_inventory.index(Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0]))
                                else:
                                    if len(Ins.player.battle_inventory) >= 3:
                                        Ins.player.battle_inventory.pop(2)
                                    Ins.player.battle_inventory.append(Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0])
                            else:
                                sounds.play_effect("effect4")
                                Screen.is_displaying = True
                                Screen.displayed_msg = "You need to be level {} to use this item".format(items[Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0]][7])
                                continue
                        else:
                            sounds.play_effect("effect4")
                            Screen.is_displaying = True
                            Screen.displayed_msg = "You cant use this item in battle"
                            continue

                    if keysDown[Ins.settings.interact] or mouseDown[1]:
                        _temp_item_list = Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0]
                        Screen.is_question = False
                        if not Screen.question_option:
                            if Ins.player.level >= items[_temp_item_list][7]:
                                sounds.play_effect("effect6")
                                if Screen.temp_num == 1:
                                    Ins.player.add_hp(items[_temp_item_list][4])
                                    Ins.player.add_mana(items[_temp_item_list][5])
                                    Ins.player.add_exp(items[_temp_item_list][6])
                                    for _passive in items[_temp_item_list][8]:
                                        globals()["ap_" + _passive]()
                                if Screen.temp_num == 2:
                                    Ins.player.add_max_hp(items[_temp_item_list][4])
                                    Ins.player.add_max_mana(items[_temp_item_list][5])
                                    Ins.player.exp_boost += items[_temp_item_list][6]
                                    Ins.player.add_attack(items[_temp_item_list][8])
                                    Ins.player.add_defense(items[_temp_item_list][9])
                                    Ins.player.add_evasion(items[_temp_item_list][10])
                                    Ins.player.add_accuracy(items[_temp_item_list][11])
                                    Ins.player.passive_list.extend(items[_temp_item_list][12][1])
                                    for _passive in items[_temp_item_list][12][0]:
                                        globals()["ap_" + _passive]()
                                if Screen.temp_num in (num for num in range(3, 12)):
                                    _temp_removed_item = None
                                    if Screen.temp_num == 3:
                                        if Ins.player.helmet is not None:
                                            _temp_removed_item = Ins.player.helmet
                                            Ins.player.add_item(Ins.player.helmet)
                                        Ins.player.helmet = _temp_item_list
                                    if Screen.temp_num == 4:
                                        if Ins.player.chestplate is not None:
                                            _temp_removed_item = Ins.player.chestplate
                                            Ins.player.add_item(Ins.player.chestplate)
                                        Ins.player.chestplate = _temp_item_list
                                    if Screen.temp_num == 5:
                                        if Ins.player.leggings is not None:
                                            Ins.player.add_item(Ins.player.leggings)
                                            _temp_removed_item = Ins.player.leggings
                                        Ins.player.leggings = _temp_item_list
                                    if Screen.temp_num == 6:
                                        if Ins.player.accessory1 is not None and Ins.player.accessory2 is not None:
                                            _temp_removed_item = Ins.player.accessory1
                                            Ins.player.add_item(Ins.player.accessory1)
                                            Ins.player.accessory1 = _temp_item_list
                                        elif Ins.player.accessory1 is None:
                                            Ins.player.accessory1 = _temp_item_list
                                        elif Ins.player.accessory2 is None:
                                            Ins.player.accessory2 = _temp_item_list
                                    if Screen.temp_num == 7:
                                        if Ins.player.sword is not None:
                                            _temp_removed_item = Ins.player.sword
                                            Ins.player.add_item(Ins.player.sword)
                                        Ins.player.sword = _temp_item_list
                                    if Screen.temp_num == 8:
                                        if Ins.player.bow is not None:
                                            _temp_removed_item = Ins.player.bow
                                            Ins.player.add_item(Ins.player.bow)
                                        Ins.player.bow = _temp_item_list
                                    if Screen.temp_num == 9:
                                        if Ins.player.staff is not None:
                                            _temp_removed_item = Ins.player.staff
                                            Ins.player.add_item(Ins.player.staff)
                                        Ins.player.staff = _temp_item_list
                                    if Screen.temp_num == 10:
                                        if Ins.player.talisman is not None:
                                            _temp_removed_item = Ins.player.talisman
                                            Ins.player.add_item(Ins.player.talisman)
                                        Ins.player.talisman = _temp_item_list
                                    if Screen.temp_num == 11:
                                        if Ins.player.relic is not None:
                                            _temp_removed_item = Ins.player.relic
                                            Ins.player.add_item(Ins.player.relic)
                                        Ins.player.relic = _temp_item_list
                                    try:
                                        Ins.player.add_max_hp(-1 * items[_temp_removed_item][4])
                                        Ins.player.add_max_mana(-1 * items[_temp_removed_item][5])
                                        Ins.player.exp_boost -= items[_temp_removed_item][6]
                                        Ins.player.add_attack(-1 * items[_temp_removed_item][8])
                                        Ins.player.add_defense(-1 * items[_temp_removed_item][9])
                                        Ins.player.add_evasion(-1 * items[_temp_removed_item][10])
                                        Ins.player.add_accuracy(-1 * items[_temp_removed_item][11])
                                        Ins.player.remove_passive(items[_temp_removed_item][12][1])
                                        for _passive in items[_temp_removed_item][12][2]:
                                            globals()["rp_"+_passive]()
                                    except KeyError:
                                        pass
                                    Ins.player.add_max_hp(items[_temp_item_list][4])
                                    Ins.player.add_max_mana(items[_temp_item_list][5])
                                    Ins.player.exp_boost += items[_temp_item_list][6]
                                    Ins.player.add_attack(items[_temp_item_list][8])
                                    Ins.player.add_defense(items[_temp_item_list][9])
                                    Ins.player.add_evasion(items[_temp_item_list][10])
                                    Ins.player.add_accuracy(items[_temp_item_list][11])
                                    Ins.player.passive_list.extend(items[_temp_item_list][12][1])
                                    for _passive in items[_temp_item_list][12][0]:
                                        globals()["ap_" + _passive]()
                            else:
                                sounds.play_effect("effect4")
                                Screen.is_displaying = True
                                Screen.displayed_msg = "You need to be level {} to use this item".format(items[_temp_item_list][7])
                                continue
                            Ins.player.add_item(_temp_item_list, -1)
                            Requires.scr_update()

                elif (keysDown[Ins.settings.interact] or mouseDown[1]) and len(Ins.player.inventory) != 0 and not Screen.is_displaying:
                    Screen.temp_num = items[Ins.player.inventory[Screen.inventory_roller*5+Screen.in_menu_num-1][0]][3]
                    if Screen.temp_num == 0:
                        Screen.is_displaying = True
                        Screen.displayed_msg = "you can't use this item!"
                        sounds.play_effect("effect4")
                        continue
                    else:
                        Screen.question_option = 0
                        Screen.is_question = True
                        sounds.play_effect("effect7")
                    if Screen.temp_num == 1:
                        if Ins.player.inventory[Screen.inventory_roller * 5 + Screen.in_menu_num - 1][0] in Ins.player.battle_inventory:
                            Screen.question_text = "do you want to consume this item? \"{}\" - unequip from battle".format(Ins.settings.other_function)
                        else:
                            Screen.question_text = "do you want to consume this item? \"{}\" - equip to battle".format(Ins.settings.other_function)
                    elif Screen.temp_num == 2:
                        Screen.question_text = "do you want to consume this item?"
                    elif Screen.temp_num in (num for num in range(3, 12)):
                        Screen.question_text = "do you want to equip this item?"

                if Screen.is_question or Screen.is_displaying:
                    pass
                elif keysDown[Ins.settings.move_down] or mouseDown[5]:
                    if len(Ins.player.inventory) > 1:
                        sounds.play_effect("effect1")
                        Screen.description_page = 0
                    Screen.in_menu_num += 1
                    if Screen.in_menu_num >= Screen.items_in_roller + 1:
                        Screen.in_menu_num = 1
                        Screen.inventory_roller += 1
                        if Screen.inventory_roller > Screen.inventory_roller_max:
                            Screen.inventory_roller = 0
                elif keysDown[Ins.settings.move_up] or mouseDown[4]:
                    if len(Ins.player.inventory) > 1:
                        sounds.play_effect("effect1")
                        Screen.description_page = 0
                    Screen.in_menu_num -= 1
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num = 5
                        Screen.inventory_roller -= 1
                        if Screen.inventory_roller < 0:
                            Screen.inventory_roller = Screen.inventory_roller_max
                elif keysDown[Ins.settings.move_right]:
                    if len(Ins.player.inventory) > 1 and Screen.in_menu_num != 1 or len(Ins.player.inventory) > 5:
                        sounds.play_effect("effect1")
                        Screen.description_page = 0
                    Screen.in_menu_num = 1
                    Screen.inventory_roller += 1
                    if Screen.inventory_roller > Screen.inventory_roller_max:
                        Screen.inventory_roller = 0
                elif keysDown[Ins.settings.move_left]:
                    if len(Ins.player.inventory) > 1 and Screen.in_menu_num != Screen.items_in_roller or len(Ins.player.inventory) > 5:
                        sounds.play_effect("effect1")
                        Screen.description_page = 0
                    Screen.in_menu_num = 5
                    Screen.inventory_roller -= 1
                    if Screen.inventory_roller < 0:
                        Screen.inventory_roller = Screen.inventory_roller_max

            elif Screen.menu_num == 2:
                pygame.draw.rect(Screen.win, (80, 255, 80), (20, 385, 510, 207), 1)
                if Screen.is_displaying or Screen.is_question:
                    pass
                elif mouseDown[5]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num += 1
                    if Screen.in_menu_num >= 11:
                        Screen.in_menu_num = 1
                elif mouseDown[4]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num -= 1
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num = 10
                elif keysDown[Ins.settings.move_down]:
                    Screen.description_page = 0
                    sounds.play_effect("effect1")
                    if Screen.in_menu_num % 2 == 0:
                        Screen.in_menu_num -= 1
                    else:
                        Screen.in_menu_num += 1
                elif keysDown[Ins.settings.move_up]:
                    Screen.description_page = 0
                    sounds.play_effect("effect1")
                    if Screen.in_menu_num % 2 != 0:
                        Screen.in_menu_num += 1
                    else:
                        Screen.in_menu_num -= 1
                elif keysDown[Ins.settings.move_right]:
                    Screen.description_page = 0
                    sounds.play_effect("effect1")
                    Screen.in_menu_num += 2
                    if Screen.in_menu_num >= 11:
                        Screen.in_menu_num -= 10
                elif keysDown[Ins.settings.move_left]:
                    Screen.description_page = 0
                    sounds.play_effect("effect1")
                    Screen.in_menu_num -= 2
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num += 10

                selected_item = None
                if True:
                    if Screen.in_menu_num == 1:
                        selected_item = Ins.player.helmet
                    if Screen.in_menu_num == 2:
                        selected_item = Ins.player.sword
                    if Screen.in_menu_num == 3:
                        selected_item = Ins.player.chestplate
                    if Screen.in_menu_num == 4:
                        selected_item = Ins.player.bow
                    if Screen.in_menu_num == 5:
                        selected_item = Ins.player.leggings
                    if Screen.in_menu_num == 6:
                        selected_item = Ins.player.staff
                    if Screen.in_menu_num == 7:
                        selected_item = Ins.player.talisman
                    if Screen.in_menu_num == 8:
                        selected_item = Ins.player.accessory1
                    if Screen.in_menu_num == 9:
                        selected_item = Ins.player.relic
                    if Screen.in_menu_num == 10:
                        selected_item = Ins.player.accessory2

                if selected_item is not None:
                    Screen.description_message = Screen.get_text_format("{}{} {}\n{}".format(selected_item, ":" if items[selected_item][0] else "", items[selected_item][0], items[selected_item][2]), 845, font3)

                    if keysDown[Ins.settings.interact] or mouseDown[1]:
                        Ins.player.add_max_hp(-1*items[selected_item][4])
                        Ins.player.add_max_mana(-1*items[selected_item][5])
                        Ins.player.exp_boost -= items[selected_item][6]
                        Ins.player.add_attack(-1*items[selected_item][8])
                        Ins.player.add_defense(-1*items[selected_item][9])
                        Ins.player.add_evasion(-1*items[selected_item][10])
                        Ins.player.add_accuracy(-1*items[selected_item][11])
                        Ins.player.remove_passive(items[selected_item][12][1])
                        for _passive in items[selected_item][12][2]:
                            globals()["rp_" + _passive]()
                        if True:
                            if Screen.in_menu_num == 1:
                                Ins.player.add_item(Ins.player.helmet)
                                Ins.player.helmet = None
                            if Screen.in_menu_num == 2:
                                Ins.player.add_item(Ins.player.sword)
                                Ins.player.sword = None
                            if Screen.in_menu_num == 3:
                                Ins.player.add_item(Ins.player.chestplate)
                                Ins.player.chestplate = None
                            if Screen.in_menu_num == 4:
                                Ins.player.add_item(Ins.player.bow)
                                Ins.player.bow = None
                            if Screen.in_menu_num == 5:
                                Ins.player.add_item(Ins.player.leggings)
                                Ins.player.leggings = None
                            if Screen.in_menu_num == 6:
                                Ins.player.add_item(Ins.player.staff)
                                Ins.player.staff = None
                            if Screen.in_menu_num == 7:
                                Ins.player.add_item(Ins.player.talisman)
                                Ins.player.talisman = None
                            if Screen.in_menu_num == 8:
                                Ins.player.add_item(Ins.player.accessory1)
                                Ins.player.accessory1 = None
                            if Screen.in_menu_num == 9:
                                Ins.player.add_item(Ins.player.relic)
                                Ins.player.relic = None
                            if Screen.in_menu_num == 10:
                                Ins.player.add_item(Ins.player.accessory2)
                                Ins.player.accessory2 = None
                        Screen.menu_num = 1
                        Screen.in_menu_num = 1

            elif Screen.menu_num == 3:
                pygame.draw.rect(Screen.win, (80, 255, 80), (545, 385, 455, 207), 1)
                Screen.description_message = ["LP - level points: add 0.5 point to each battle stat, 1 for mana or 2 for hp for 1 LP"]
                if Screen.is_displaying or Screen.is_question:
                    pass
                elif keysDown[Ins.settings.move_left]:
                    sounds.play_effect("effect1")
                    if Screen.in_menu_num % 2 == 0:
                        Screen.in_menu_num -= 2
                    Screen.in_menu_num += 1
                elif keysDown[Ins.settings.move_right]:
                    sounds.play_effect("effect1")
                    if Screen.in_menu_num % 2 != 0:
                        Screen.in_menu_num += 2
                    Screen.in_menu_num -= 1
                elif keysDown[Ins.settings.move_down]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num += 2
                    if Screen.in_menu_num >= 9:
                        Screen.in_menu_num -= 8
                elif keysDown[Ins.settings.move_up]:
                    sounds.play_effect("effect1")
                    if Screen.in_menu_num == 6:
                        Screen.in_menu_num = 8
                    else:
                        Screen.in_menu_num -= 2
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num += 8
                if Screen.in_menu_num in (2, 4):
                    Screen.in_menu_num = 6

                if Screen.is_displaying or Screen.is_question:
                    pass
                elif mouseDown[4]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num += 1
                    if Screen.in_menu_num >= 9:
                        Screen.in_menu_num = 1
                    elif Screen.in_menu_num == 2:
                        Screen.in_menu_num = 3
                    elif Screen.in_menu_num == 4:
                        Screen.in_menu_num = 5
                elif mouseDown[5]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num -= 1
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num = 8
                    elif Screen.in_menu_num == 2:
                        Screen.in_menu_num = 1
                    elif Screen.in_menu_num == 4:
                        Screen.in_menu_num = 3

                if Screen.is_question:
                    if keysDown[Ins.settings.interact] or mouseDown[1]:
                        if not Screen.question_option:
                            if Ins.player.level_points > 0:
                                Ins.player.level_points -= 1
                                sounds.play_effect("effect6")
                                if Screen.in_menu_num == 1:
                                    Ins.player.add_max_hp(2)
                                    Ins.player.add_hp(2)
                                elif Screen.in_menu_num == 3:
                                    Ins.player.add_max_mana(1)
                                    Ins.player.add_mana(1)
                                elif Screen.in_menu_num == 5:
                                    Ins.player.add_attack(0.5)
                                elif Screen.in_menu_num == 6:
                                    Ins.player.add_defense(0.5)
                                elif Screen.in_menu_num == 7:
                                    Ins.player.add_accuracy(0.5)
                                elif Screen.in_menu_num == 8:
                                    Ins.player.add_evasion(0.5)
                                Requires.scr_update()
                            else:
                                Screen.is_displaying = True
                                sounds.play_effect("effect4")
                                Screen.displayed_msg = "You need more party points to use this"
                        else:
                            sounds.play_effect("effect6")
                        Screen.is_question = False
                        continue

                elif (keysDown[Ins.settings.interact] or mouseDown[1]) and not Screen.is_displaying:
                    Screen.question_option = 0
                    Screen.is_question = True
                    sounds.play_effect("effect7")
                    Screen.question_text = "do you want to use 1 LP to boost this stat?"

            elif Screen.menu_num == 4:
                pygame.draw.rect(Screen.win, (80, 255, 80), (20, 632, 308, 106), 1)
                if Screen.is_displaying:
                    pass

                elif keysDown[Ins.settings.move_right] or mouseDown[4]:
                    Screen.description_page = 0
                    sounds.play_effect("effect1")
                    Screen.in_menu_num += 1
                    try:
                        scrolls[Screen.scroll_roller * 3 + Screen.in_menu_num]
                    except KeyError:
                        Screen.scroll_roller = 0
                        Screen.in_menu_num = 1
                    if Screen.in_menu_num >= 4:
                        Screen.in_menu_num = 1
                        Screen.scroll_roller += 1
                        if Screen.scroll_roller > Screen.scroll_roller_max:
                            Screen.scroll_roller = 0
                elif keysDown[Ins.settings.move_left] or mouseDown[5]:
                    Screen.description_page = 0
                    sounds.play_effect("effect1")
                    Screen.in_menu_num -= 1
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num = 3
                        Screen.scroll_roller -= 1
                        if Screen.scroll_roller < 0:
                            Screen.scroll_roller = Screen.scroll_roller_max
                            Screen.in_menu_num = (len(scrolls) - 1) % 3

                elif keysDown[Ins.settings.interact] or mouseDown[1]:
                    Screen.is_displaying = True
                    if Screen.scroll_roller * 3 + Screen.in_menu_num == Ins.player.scroll:
                        Screen.displayed_msg = "you unequipped the scroll"
                        Ins.player.scroll = None
                        sounds.play_effect("effect6")
                    elif Requires.scrolls_req[Screen.scroll_roller * 3 + Screen.in_menu_num][0]:
                        Ins.player.scroll = Screen.scroll_roller * 3 + Screen.in_menu_num
                        Screen.displayed_msg = "you equipped: {}".format(scrolls[Screen.scroll_roller * 3 + Screen.in_menu_num][0])
                        sounds.play_effect("effect6")
                    else:
                        Screen.displayed_msg = Requires.scrolls_req[Screen.scroll_roller * 3 + Screen.in_menu_num][1]
                        sounds.play_effect("effect4")
                    continue

                Screen.description_message = Screen.get_text_format("{}: {}".format(scrolls[Screen.scroll_roller * 3 + Screen.in_menu_num][0], scrolls[Screen.scroll_roller * 3 + Screen.in_menu_num][1]), 845, font3)

            elif Screen.menu_num == 5:
                pygame.draw.rect(Screen.win, (80, 255, 80), (338, 632, 308, 106), 1)
                if Screen.is_displaying:
                    pass

                elif keysDown[Ins.settings.move_right] or mouseDown[4]:
                    Screen.description_page = 0
                    sounds.play_effect("effect1")
                    Screen.in_menu_num += 1
                    try:
                        scripts[Screen.script_roller * 3 + Screen.in_menu_num]
                    except KeyError:
                        Screen.script_roller = 0
                        Screen.in_menu_num = 1
                    if Screen.in_menu_num > 3:
                        Screen.in_menu_num = 1
                        Screen.script_roller += 1
                        if Screen.script_roller > Screen.script_roller_max:
                            Screen.script_roller = 0
                elif keysDown[Ins.settings.move_left] or mouseDown[5]:
                    Screen.description_page = 0
                    sounds.play_effect("effect1")
                    Screen.in_menu_num -= 1
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num = 3
                        Screen.script_roller -= 1
                        if Screen.script_roller < 0:
                            Screen.script_roller = Screen.script_roller_max
                            Screen.in_menu_num = (len(scripts) - 1) % 3

                elif keysDown[Ins.settings.interact] or mouseDown[1]:
                    Screen.is_displaying = True
                    if Screen.script_roller * 3 + Screen.in_menu_num == Ins.player.script:
                        Screen.displayed_msg = "you unequipped the script"
                        Ins.player.script = None
                        sounds.play_effect("effect6")
                    elif Requires.scripts_req[Screen.script_roller * 3 + Screen.in_menu_num][0]:
                        Ins.player.script = Screen.script_roller * 3 + Screen.in_menu_num
                        Screen.displayed_msg = "you equipped: {}".format(scripts[Screen.scroll_roller * 3 + Screen.in_menu_num][0])
                        sounds.play_effect("effect6")
                    else:
                        Screen.displayed_msg = Requires.scripts_req[Screen.script_roller * 3 + Screen.in_menu_num][1]
                        sounds.play_effect("effect4")
                    continue

                Screen.description_message = Screen.get_text_format("{}: {}".format(scripts[Screen.script_roller * 3 + Screen.in_menu_num][0], scripts[Screen.script_roller * 3 + Screen.in_menu_num][1]), 845, font3)

            elif Screen.menu_num == 6:
                if Screen.in_menu_num == 2:
                    Screen.description_message = ["keep track of the story and side quests"]
                elif Screen.in_menu_num == 3:
                    Screen.description_message = ["travel to destinations without walking"]
                elif Screen.in_menu_num == 7:
                    Screen.description_message = ["return to main menu"]
                else:
                    Screen.description_message = ""

                pygame.draw.rect(Screen.win, (80, 255, 80), (656, 632, 344, 106), 1)
                if Screen.is_question:
                    if keysDown[Ins.settings.interact] or mouseDown[1]:
                        if Screen.in_menu_num == 9:
                            if not Screen.question_option:
                                Screen.run = False
                            Screen.is_question = False
                            sounds.play_effect("effect6")

                        if Screen.in_menu_num == 7:
                            if not Screen.question_option:
                                return_to_menu()
                            Screen.is_question = False
                            sounds.play_effect("effect6")

                elif (keysDown[Ins.settings.interact] or mouseDown[1]) and not Screen.is_question and not Screen.is_displaying:
                    if Screen.in_menu_num == 9:
                        if keysDown[Ins.settings.interact] and not Screen.is_displaying:
                            Screen.question_option = 0
                            Screen.is_question = True
                            sounds.play_effect("effect7")
                            Screen.question_text = "are you sure you want to quit? unsaved progress will be lost"

                    elif Screen.in_menu_num == 3:
                        if Ins.ap.travel_enabled:
                            sounds.play_effect("effect9")
                            Screen.set_state("fastTravel")
                            Screen.travel_page = 0
                            Screen.selected_travel_map = 0
                            _travel_count = 0
                        else:
                            Screen.is_displaying = True
                            Screen.displayed_msg = "fast travel is currently disabled"
                            sounds.play_effect("effect6")

                        continue

                    elif Screen.in_menu_num == 4:
                        if Screen.debug:
                            sounds.play_effect("effect9")
                            Screen.set_state("debug")
                        else:
                            Screen.is_displaying = True
                            Screen.displayed_msg = "debug mode is required for this action!"
                            sounds.play_effect("effect6")
                        continue

                    elif Screen.in_menu_num == 6:
                        sounds.play_effect("effect9")
                        Screen.set_state("stats")
                        stats_list = list(Ins.stats.__dict__.keys())
                        continue

                    elif Screen.in_menu_num == 2:
                        _temp_mission_list = [i for i in mission_list if not (Ins.ap.mission_progress_list[i[0]] is False or (Ins.ap.mission_claimed[i[0]] and not Ins.settings.showClaimedMissions))]
                        if not _temp_mission_list:
                            Screen.is_displaying = True
                            Screen.displayed_msg = "no missions to show"
                            continue
                        sounds.play_effect("effect9")
                        Screen.set_state("journal")
                        Screen.mission_index = 0
                        Screen.mission_page = 0
                        continue

                    elif Screen.in_menu_num == 1:
                        sounds.play_effect("effect9")
                        Screen.tutorial_index = 0
                        Screen.tutorial_in_game = True
                        Screen.set_state("tutorial")
                        continue

                    elif Screen.in_menu_num == 7:
                        if keysDown[Ins.settings.interact] and not Screen.is_displaying:
                            Screen.question_option = 0
                            Screen.is_question = True
                            sounds.play_effect("effect7")
                            Screen.question_text = "are you sure you want to go to the menu? unsaved progress will be lost"

                    elif Screen.in_menu_num == 8:
                        Screen.description_message = Screen.get_text_format(player_classes[1][1], 745, font3)
                        Screen.description_page = 0
                        Screen.is_displaying = False
                        Screen.set_state("classes")
                        sounds.play_effect("effect12")
                        Screen.classDeg = 0
                        Screen.classIndex = 0
                        Requires.class_update()
                        Screen.classRotationTime = 0
                        continue

                    elif Screen.in_menu_num == 5:
                        Temp.settings = Settings()
                        Temp.settings.copy_from(Ins.settings)
                        sounds.play_effect("effect9")
                        Screen.set_state("settings")
                        Menu.choose = 3
                        Menu.open_index = 20
                        continue

                elif keysDown[Ins.settings.move_left]:
                    sounds.play_effect("effect1")
                    if Screen.in_menu_num % 3 != 1:
                        Screen.in_menu_num -= 1
                    else:
                        Screen.in_menu_num += 2
                elif keysDown[Ins.settings.move_right]:
                    sounds.play_effect("effect1")
                    if Screen.in_menu_num % 3 != 0:
                        Screen.in_menu_num += 1
                    else:
                        Screen.in_menu_num -= 2
                elif keysDown[Ins.settings.move_down]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num += 3
                    if Screen.in_menu_num > 9:
                        Screen.in_menu_num -= 9
                elif keysDown[Ins.settings.move_up]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num -= 3
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num += 9
                elif mouseDown[4]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num += 1
                    if Screen.in_menu_num >= 10:
                        Screen.in_menu_num = 1
                elif mouseDown[5]:
                    sounds.play_effect("effect1")
                    Screen.in_menu_num -= 1
                    if Screen.in_menu_num <= 0:
                        Screen.in_menu_num = 9
            ##############################################
            if Screen.is_displaying:
                if keysDown[Ins.settings.interact] or mouseDown[1]:
                    Screen.is_displaying = False
                pygame.draw.rect(Screen.win, (140, 140, 140), (300, 200, 420, 200))
                pygame.draw.rect(Screen.win, (0, 0, 0), (300, 200, 420, 200), 2)
                _temp_text = Screen.get_text_format(Screen.displayed_msg, 410, font4)
                screen_start1 = 300
                for _text in _temp_text:
                    surface1 = font4.render(_text, False, (0, 0, 0))
                    Screen.win.blit(surface1, (int(510 - surface1.get_rect().width / 2), int(screen_start1 - (len(_temp_text))*35/2)))
                    screen_start1 += 35

                if keysDown["esc"]:
                    Screen.is_displaying = False
                    continue

            if Screen.is_question:
                pygame.draw.rect(Screen.win, (140, 140, 140), (300, 200, 420, 200))
                pygame.draw.rect(Screen.win, (0, 0, 0), (300, 200, 420, 200), 2)
                _temp_text = Screen.get_text_format(Screen.question_text, 410, font4)
                screen_start1 = 205
                for _text in _temp_text:
                    surface1 = font4.render(_text, False, (0, 0, 0))
                    Screen.win.blit(surface1, (int(510 - surface1.get_rect().width / 2), screen_start1))
                    screen_start1 += 35
                pygame.draw.rect(Screen.win, (180, 180, 180), (345, 315, 140, 58))
                pygame.draw.rect(Screen.win, (180, 180, 180), (535, 315, 140, 58))
                surface1 = font2.render("Yes", False, (0, 0, 0))
                Screen.win.blit(surface1, (368, 320))
                surface1 = font2.render("No", False, (0, 0, 0))
                Screen.win.blit(surface1, (577, 320))
                if keysDown[Ins.settings.move_left] or keysDown[Ins.settings.move_right] or mouseDown[5] or mouseDown[4]:
                    Screen.question_option = not Screen.question_option
                    sounds.play_effect("effect1")
                pygame.draw.rect(Screen.win, (80, 255, 80), (345 + 190 * Screen.question_option, 315, 140, 58), 1)

                if keysDown["esc"]:
                    Screen.is_question = False
                    continue

            if Screen.description_message != "":
                try:
                    pygame.draw.rect(Screen.win, (100, 100, 100), (20, 748, 980, 40))
                    surface1 = font3.render(Screen.description_message[Screen.description_page], False, (0, 0, 0))
                    Screen.win.blit(surface1, (30, 748))
                    surface1 = font3.render("page: {} /{}".format(Screen.description_page + 1, len(Screen.description_message)), False, (0, 0, 0))
                    Screen.win.blit(surface1, (990 - surface1.get_rect().width, 748))
                    if keysDown[Ins.settings.other_function] and not Screen.is_question and not Screen.is_displaying:
                        Screen.description_page += 1
                        if Screen.description_page >= len(Screen.description_message):
                            Screen.description_page = 0
                except IndexError:
                    pass
            ##############################################
            if keysDown["esc"] or mouseDown[2]:
                sounds.play_effect("effect3")
                Screen.set_state("world")
                Screen.resize(64 * Screen.screen_width, 64 * Screen.screen_height)
                pygame.display.set_caption(Screen.map_name)
                continue
            if (keysDown["tab"] or mouseDown[3]) and not Screen.is_question and not Screen.is_displaying:
                Screen.description_message = ""
                Screen.description_page = 0
                sounds.play_effect("effect5")
                Screen.menu_num += 1
                Screen.in_menu_num = 1
                Screen.script_roller = 0
                if Screen.menu_num > 6:
                    Screen.menu_num = 1
        # shop
        elif Screen.state("shop"):
            if Ins.settings.showUnsellableItems:
                temp_inventory = list(Ins.player.inventory)
            else:
                temp_inventory = list(item for item in Ins.player.inventory if item_sell_value[item[0]] is not None)
            pygame.draw.rect(Screen.win, (80, 80, 80), (5, 5, 690, 430))
            pygame.draw.rect(Screen.win, (150, 150, 150), (10, 10, 680, 380), 2)
            surface1 = font4.render("value", False, (255, 255, 255))
            Screen.win.blit(surface1, (40, 15))
            surface1 = font4.render("item", False, (255, 255, 255))
            Screen.win.blit(surface1, (340, 15))
            surface1 = font4.render("stock", False, (255, 255, 255))
            Screen.win.blit(surface1, (595, 15))
            _items_in_page = -1
            if Screen.shopMode:
                try:
                    for _item in range(9):
                        if temp_inventory[9 * Screen.shopSellPage + _item]:
                            pass
                        _items_in_page += 1
                except IndexError:
                    pass
                if len(temp_inventory) == 0:
                    Screen.shopMode = False
                elif _items_in_page == -1:
                    Screen.shopSellPage -= 1

                _counter = 0
                for _item in temp_inventory[9 * Screen.shopSellPage:9 * Screen.shopSellPage + 9]:
                    if item_sell_value[_item[0]] is None:
                        pygame.draw.rect(Screen.win, (50, 50, 50), (15, 62 + _counter * 35, 670, 35))
                    surface1 = font4.render(str(item_sell_value[_item[0]]) if item_sell_value[_item[0]] is not None else "n/a", False, (80, 255, 80) if _counter == Screen.shopIndex else (255, 255, 255))
                    Screen.win.blit(surface1, (int(84 - surface1.get_rect().width / 2), 60 + _counter * 35))
                    surface1 = font4.render(_item[0], False, (80, 255, 80) if _counter == Screen.shopIndex else (255, 255, 255))
                    Screen.win.blit(surface1, (180, 60 + _counter * 35))
                    surface1 = font4.render(str(_item[1]), False, (80, 255, 80) if _counter == Screen.shopIndex else (255, 255, 255))
                    Screen.win.blit(surface1, (int(635 - surface1.get_rect().width / 2), 60 + _counter * 35))
                    _counter += 1

            else:
                _counter = 0
                for _item in Ins.ap.shops[Screen.shopId]:
                    if _item[2] == 0:
                        pygame.draw.rect(Screen.win, (50, 50, 50), (15, 62 + _counter * 35, 670, 35))
                    surface1 = font4.render(str(_item[1]), False, (80, 255, 80) if _counter == Screen.shopIndex else (255, 255, 255))
                    Screen.win.blit(surface1, (int(84 - surface1.get_rect().width / 2), 60 + _counter * 35))
                    surface1 = font4.render(_item[0], False, (80, 255, 80) if _counter == Screen.shopIndex else (255, 255, 255))
                    Screen.win.blit(surface1, (180, 60 + _counter * 35))
                    if _item[2] != -1:
                        surface1 = font4.render(str(_item[2]), False, (80, 255, 80) if _counter == Screen.shopIndex else (255, 255, 255))
                        Screen.win.blit(surface1, (int(635 - surface1.get_rect().width / 2), 60 + _counter * 35))
                    _counter += 1
            pygame.draw.line(Screen.win, (150, 150, 150), (155, 10), (155, 390), 2)
            pygame.draw.line(Screen.win, (150, 150, 150), (580, 10), (580, 390), 2)

            ##############################################
            if Screen.is_displaying:
                pass
            elif Screen.shopIsBuying:
                if Screen.shopMode:
                    pygame.draw.rect(Screen.win, (110, 110, 110), (200, 100, 300, 150))
                    pygame.draw.rect(Screen.win, (0, 0, 0), (200, 100, 300, 150), 2)
                    surface1 = font4.render("{}".format(temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0]), False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width / 2), 110))
                    surface1 = font4.render("amount: {}".format(str(Screen.shopAmount)), False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width / 2), 140))
                    surface1 = font4.render("profit: {}".format(str(Screen.shopAmount * item_sell_value[temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0]])), False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width / 2), 170))
                    surface1 = font5.render("coins: {}".format(Ins.player.coins), False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width / 2), 210))
                    if keysDown[Ins.settings.interact]:
                        Screen.shopIsBuying = False
                        if Ins.player.coins >= -1 * Screen.shopAmount * item_sell_value[temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0]]:
                            sounds.play_effect("effect11")
                            Ins.player.add_coins(Screen.shopAmount * item_sell_value[temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0]])
                            if Ins.player.item_amount(temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0]) - Screen.shopAmount == 0:
                                Ins.player.add_item(temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0], -Screen.shopAmount)
                                Screen.shopIndex = 0
                            else:
                                Ins.player.add_item(temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0], -Screen.shopAmount)
                        else:
                            sounds.play_effect("effect4")
                            Screen.is_displaying = True
                            Screen.displayed_msg = "you don't have enough coins"
                            continue
                    elif keysDown[Ins.settings.other_function] or keysDown["esc"]:
                        Screen.shopIsBuying = False
                        continue
                    elif keysDown[Ins.settings.move_left]:
                        Screen.shopAmount -= 1
                        if Screen.shopAmount <= 0:
                            Screen.shopAmount = 1
                        else:
                            sounds.play_effect("effect9")
                    elif keysDown[Ins.settings.move_right]:
                        Screen.shopAmount += 1
                        if Ins.player.item_amount(temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0]) < Screen.shopAmount:
                            Screen.shopAmount -= 1
                        else:
                            sounds.play_effect("effect9")
                else:
                    pygame.draw.rect(Screen.win, (110, 110, 110), (200, 100, 300, 150))
                    pygame.draw.rect(Screen.win, (0, 0, 0), (200, 100, 300, 150), 2)
                    surface1 = font4.render("item: {}".format(Ins.ap.shops[Screen.shopId][Screen.shopIndex][0]), False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width / 2), 110))
                    surface1 = font4.render("amount: {}".format(str(Screen.shopAmount)), False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width/2), 140))
                    surface1 = font4.render("price: {}".format(str(Screen.shopAmount * Ins.ap.shops[Screen.shopId][Screen.shopIndex][1])), False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width / 2), 170))
                    surface1 = font5.render("coins: {}".format(Ins.player.coins), False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width / 2), 210))
                    if keysDown[Ins.settings.interact]:
                        Screen.shopIsBuying = False
                        if Ins.player.coins >= Screen.shopAmount * Ins.ap.shops[Screen.shopId][Screen.shopIndex][1]:
                            sounds.play_effect("effect11")
                            Ins.player.add_coins(-Screen.shopAmount * Ins.ap.shops[Screen.shopId][Screen.shopIndex][1])
                            if Ins.ap.shops[Screen.shopId][Screen.shopIndex][2] != -1:
                                Ins.ap.shops[Screen.shopId][Screen.shopIndex][2] -= Screen.shopAmount
                            if Ins.ap.shops[Screen.shopId][Screen.shopIndex][0] != "":
                                Ins.player.add_item(Ins.ap.shops[Screen.shopId][Screen.shopIndex][0], Screen.shopAmount)
                            for cmd in Ins.ap.shops[Screen.shopId][Screen.shopIndex][3]:
                                globals()["sh_"+cmd[0]](*cmd[1:])
                        else:
                            sounds.play_effect("effect4")
                            Screen.is_displaying = True
                            Screen.displayed_msg = "you don't have enough coins"
                            continue
                    elif keysDown[Ins.settings.other_function] or keysDown["esc"]:
                        Screen.shopIsBuying = False
                        continue
                    elif keysDown[Ins.settings.move_left]:
                        Screen.shopAmount -= 1
                        if Screen.shopAmount <= 0:
                            Screen.shopAmount = 1
                        else:
                            sounds.play_effect("effect9")
                    elif keysDown[Ins.settings.move_right]:
                        Screen.shopAmount += 1
                        if Ins.ap.shops[Screen.shopId][Screen.shopIndex][2] < Screen.shopAmount and Ins.ap.shops[Screen.shopId][Screen.shopIndex][2] != -1:
                            Screen.shopAmount -= 1
                        else:
                            sounds.play_effect("effect9")
            elif keysDown["tab"]:
                if len(temp_inventory) > 0:
                    sounds.play_effect("effect5")
                    Screen.shopMode = not Screen.shopMode
                    Screen.shopIndex = 0
                    if Screen.shopMode:
                        pygame.display.set_caption("shop - sell")
                    else:
                        pygame.display.set_caption("shop - buy")
                else:
                    sounds.play_effect("effect4")
                    Screen.displayed_msg = "you don't have any items to sell!"
                    Screen.is_displaying = True
            elif keysDown[Ins.settings.interact]:
                if Screen.shopMode:
                    if item_sell_value[temp_inventory[9 * Screen.shopSellPage + Screen.shopIndex][0]] is not None:
                        sounds.play_effect("effect6")
                        Screen.shopIsBuying = True
                        Screen.shopAmount = 1
                    else:
                        sounds.play_effect("effect4")
                        Screen.is_displaying = True
                        Screen.displayed_msg = "you cant sell this item!"
                        continue
                else:
                    if Ins.ap.shops[Screen.shopId][Screen.shopIndex][2] != 0:
                        sounds.play_effect("effect6")
                        Screen.shopIsBuying = True
                        Screen.shopAmount = 1
                    else:
                        sounds.play_effect("effect4")
                        Screen.is_displaying = True
                        Screen.displayed_msg = "no items in stock"
                        continue
            elif keysDown[Ins.settings.move_down]:
                Screen.description_page = 0
                if Screen.shopMode:
                    sounds.play_effect("effect1")
                    Screen.shopIndex += 1
                    if Screen.shopIndex > _items_in_page:
                        Screen.shopIndex = 0
                else:
                    sounds.play_effect("effect1")
                    Screen.shopIndex += 1
                    if Screen.shopIndex >= len(Ins.ap.shops[Screen.shopId]):
                        Screen.shopIndex = 0
            elif keysDown[Ins.settings.move_up]:
                Screen.description_page = 0
                if Screen.shopMode:
                    sounds.play_effect("effect1")
                    Screen.shopIndex -= 1
                    if Screen.shopIndex < 0:
                        Screen.shopIndex = int(_items_in_page)
                else:
                    sounds.play_effect("effect1")
                    Screen.shopIndex -= 1
                    if Screen.shopIndex < 0:
                        Screen.shopIndex = len(Ins.ap.shops[Screen.shopId]) - 1
            elif keysDown[Ins.settings.move_right] and Screen.shopMode:
                Screen.shopSellPage += 1
                if math.ceil(len(temp_inventory) / 9) - 1 > Screen.shopSellPage:
                    Screen.shopSellPage -= 1
            elif keysDown[Ins.settings.move_left] and Screen.shopMode:
                Screen.shopSellPage -= 1
                if Screen.shopSellPage < 0:
                    Screen.shopSellPage = 0
            ##############################################
            if Screen.is_displaying:
                if keysDown[Ins.settings.interact]:
                    Screen.is_displaying = False
                pygame.draw.rect(Screen.win, (110, 110, 110), (200, 100, 300, 150))
                pygame.draw.rect(Screen.win, (0, 0, 0), (200, 100, 300, 150), 2)
                _temp_text = Screen.get_text_format(Screen.displayed_msg, 295, font4)
                screen_start1 = 175
                for _text in _temp_text:
                    surface1 = font4.render(_text, False, (255, 255, 255))
                    Screen.win.blit(surface1, (int(350 - surface1.get_rect().width / 2), int(screen_start1 - (len(_temp_text))*35/2)))
                    screen_start1 += 35

                if keysDown["esc"]:
                    Screen.is_displaying = False
                    continue

            try:
                if Screen.shopMode:
                    Screen.description_message = Screen.get_text_format(items[temp_inventory[Screen.shopIndex + Screen.shopSellPage * 9][0]][2], 620, font3)
                else:
                    Screen.description_message = Screen.get_text_format(items[Ins.ap.shops[Screen.shopId][Screen.shopIndex][0]][2], 620, font3)

                pygame.draw.rect(Screen.win, (90, 90, 90), (10, 395, 680, 35))
                surface1 = font3.render(Screen.description_message[Screen.description_page], False, (0, 0, 0))
                Screen.win.blit(surface1, (15, 395))
                surface1 = font3.render(
                    "{} /{}".format(Screen.description_page + 1, len(Screen.description_message)), False,
                    (0, 0, 0))
                Screen.win.blit(surface1, (685 - surface1.get_rect().width, 395))
                if keysDown[Ins.settings.other_function] and not Screen.is_question and not Screen.is_displaying:
                    Screen.description_page += 1
                    if Screen.description_page >= len(Screen.description_message):
                        Screen.description_page = 0
            except IndexError:
                pass

            if keysDown["esc"] and not Screen.is_displaying:
                sounds.play_effect("effect3")
                Screen.set_state("world")
                Screen.resize(64 * Screen.screen_width, 64 * Screen.screen_height)
                pygame.display.set_caption(Screen.map_name)
                continue
        # battle
        elif Screen.state("battle"):  # screen size - 300 , 300 , 600 , 400
            ##############################################
            # sScreen.win.blit(Battle.background, (-24, -16))
            Battle.current_battle_frame += 1
            Ins.player.add_mana(Ins.player.max_mana / 600)
            Battle.Hitbox.color = (0, 0, 0)
            if Battle.Sprite.mode == 0:
                Battle.Hitbox.color = (255, 255, 255)
            elif Battle.Sprite.mode == 1:
                Battle.Hitbox.color = (255, 255, 0)
            elif Battle.Sprite.mode == 2:
                Battle.Hitbox.color = (255, 0, 255)
            elif Battle.Sprite.mode == 3:
                Battle.Hitbox.color = (0, 0, 255)
            elif Battle.Sprite.mode == 4:
                Battle.Hitbox.color = (0, 255, 255)
            elif Battle.Sprite.mode == 5:
                Battle.Hitbox.color = (0, 255, 0)
            if True:
                _attack_list = ["", (0, 0, 0), 0, [0, 0, 0, [0, 0], [0, 0]], -1, -1, 0]
                if Battle.selected_menu == 0:
                    _attack_list = attacks[Battle.selected_weapon_attack]
                elif Battle.selected_menu == 1:
                    _attack_list = scripts[Ins.player.script][2][Battle.selected_script_attack]
                elif Battle.selected_menu == 2:
                    _attack_list = scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack]

                if Battle.selected_battle_menu == 0:
                    if len(_attack_list[4]) == 1:
                        pygame.draw.rect(Screen.win, (40, 40, 40), (305, 305, 590, 390))
                    else:
                        for _rect in _attack_list[4][1:]:
                            pygame.draw.rect(Screen.win, (40, 40, 40), (_rect[0] + 305, _rect[1] + 305, _rect[2], _rect[3]))

            if True:
                for _hitbox in Battle.Hitbox.hitbox_list:
                    _hitbox.render_ff()
                Battle.Projectile.player_rect = [(Battle.Sprite.x + 305, Battle.Sprite.y + 305), (Battle.Sprite.x + Battle.Sprite.length + 305, Battle.Sprite.y + 305), (Battle.Sprite.x + Battle.Sprite.length + 305, Battle.Sprite.y + Battle.Sprite.length + 305), (Battle.Sprite.x + 305, Battle.Sprite.y + Battle.Sprite.length + 305)]
                for _projectile in Battle.Projectile.projectile_list:
                    _projectile.render_ff()

                pygame.draw.rect(Screen.win, (0, 0, 0), (0, 0, 1200, 300))
                pygame.draw.rect(Screen.win, (0, 0, 0), (0, 300, 300, 500))
                pygame.draw.rect(Screen.win, (0, 0, 0), (900, 300, 300, 500))
                pygame.draw.rect(Screen.win, (0, 0, 0), (300, 700, 600, 100))

                for _effect in Battle.Effect.effect_list:
                    _effect.render_ff()

            if True:
                if Battle.selected_battle_menu == 0:
                    surface1 = font4.render("attacks:", False, (255, 255, 255))
                    Screen.win.blit(surface1, (915, 265))

                    surface1 = font4.render("normal attacks:", False, (80, 255, 80) if Battle.selected_menu == 0 else (255, 255, 255))
                    Screen.win.blit(surface1, (915, 310))
                    surface1 = font4.render("{}: {} ".format(attacks[Battle.selected_weapon_attack][2], attacks[Battle.selected_weapon_attack][0]), False, attacks[Battle.selected_weapon_attack][1])
                    Screen.win.blit(surface1, (915, 345))
                    surface1 = font4.render("script attacks:", False, (80, 255, 80) if Battle.selected_menu == 1 else (255, 255, 255))
                    Screen.win.blit(surface1, (915, 385))
                    surface1 = font4.render("{}: {} ".format(scripts[Ins.player.script][2][Battle.selected_script_attack][2], scripts[Ins.player.script][2][Battle.selected_script_attack][0]), False, scripts[Ins.player.script][2][Battle.selected_script_attack][1])
                    Screen.win.blit(surface1, (915, 420))
                    surface1 = font4.render("scroll attacks:", False, (80, 255, 80) if Battle.selected_menu == 2 else (255, 255, 255))
                    Screen.win.blit(surface1, (915, 460))
                    surface1 = font4.render("{}: {} ".format(scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack][2], scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack][0]), False, scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack][1])
                    Screen.win.blit(surface1, (915, 495))

                    # TODO: fix specific delay y offset

                    if Battle.selected_menu == 1:
                        pygame.draw.rect(Screen.win, (80, 255, 255),
                                         (915, 660, int(260 * Battle.attack_delay_list[scripts[Ins.player.script][2][Battle.selected_script_attack][0]]
                                                        / scripts[Ins.player.script][2][Battle.selected_script_attack][9] / Battle.turn_delay_battle), 25))
                    elif Battle.selected_menu == 2:
                        pygame.draw.rect(Screen.win, (80, 255, 255),
                                         (915, 660, int(260 * Battle.attack_delay_list[scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack][0]]
                                                        / scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack][9] / Battle.turn_delay_battle), 25))
                    if Battle.selected_menu in (1, 2):
                        surface1 = font4.render("attack delay:", False, (255, 255, 255))
                        Screen.win.blit(surface1, (915, 620))
                        pygame.draw.rect(Screen.win, (255, 255, 255), (915, 660, 260, 25), 2)
                elif Battle.selected_battle_menu == 1:
                    surface1 = font4.render("inventory:", False, (255, 255, 255))
                    Screen.win.blit(surface1, (915, 265))
                    _counter = 0
                    for _item in Ins.player.battle_inventory:
                        for [_item2, _amount] in Ins.player.inventory:
                            if _item == _item2:
                                surface1 = font4.render("{}: {} ".format(_amount, _item), False, (80, 255, 80) if Battle.selected_battle_item == _counter else (255, 255, 255))
                                Screen.win.blit(surface1, (915, 310 + 40 * _counter))
                                _counter += 1
                                break

                else:
                    surface1 = font4.render("class actions:", False, (255, 255, 255))
                    Screen.win.blit(surface1, (915, 265))

                    _counter = 0
                    for _class_attack in player_classes[Ins.player.playerClass][2]:
                        if globals()["cat_con_"+player_classes[Ins.player.playerClass][0].replace(" ", "_")](False, _counter):
                            if _counter == Battle.selected_battle_class:
                                _color = (80, 255, 80)
                            else:
                                _color = (255, 255, 255)
                        else:
                            if _counter == Battle.selected_battle_class:
                                _color = (120, 120, 120)
                            else:
                                _color = (80, 80, 80)

                        surface1 = font4.render(f"{_class_attack}", False, _color)
                        Screen.win.blit(surface1, (915, 310 + 40 * _counter))
                        _counter += 1

                Screen.win.blit(Battle.texture, (int(Battle.enemy_x - Battle.enemy_width / 2), int(Battle.enemy_y - Battle.enemy_height / 2)))
                pygame.draw.rect(Screen.win, Battle.Hitbox.color, (300, 300, 600, 400), 9)
                surface1 = font4.render("hp:", False, (255, 255, 255))
                Screen.win.blit(surface1, (20, 300))
                surface1 = font4.render("{} /{}".format(int(Ins.player.hp), int(Ins.player.max_hp)), False, (255, 255, 255))
                Screen.win.blit(surface1, (280 - surface1.get_rect().width, 300))
                pygame.draw.rect(Screen.win, (0, 70, 0) if Battle.Sprite.current_effect in (1, 3, 5) else ((30, 0, 0) if Battle.Sprite.current_effect in (2, 4, 6) else (70, 255, 70)), (20, 350, max(min(int(260 * Ins.player.hp / Ins.player.max_hp), 260), 0), 25))
                pygame.draw.rect(Screen.win, (255, 255, 255), (20, 350, 260, 25), 2)
                surface1 = font4.render("mana:", False, (255, 255, 255))
                Screen.win.blit(surface1, (20, 385))
                surface1 = font4.render("{} /{}".format(int(Ins.player.mana), int(Ins.player.max_mana)), False, (255, 255, 255))
                Screen.win.blit(surface1, (280 - surface1.get_rect().width, 385))
                pygame.draw.rect(Screen.win, (80, 80, 255), (20, 435, max(min(int(260 * Ins.player.mana / Ins.player.max_mana), 260), 0), 25))
                pygame.draw.rect(Screen.win, (255, 255, 255), (20, 435, 260, 25), 2)
                surface1 = font4.render("delay:", False, (255, 255, 255))
                Screen.win.blit(surface1, (915, 550))
                pygame.draw.rect(Screen.win, (255, 255, 80), (915, 590, int(260 * Battle.next_attack_delay / Battle.attack_delay), 25))
                pygame.draw.rect(Screen.win, (255, 255, 255), (915, 590, 260, 25), 2)

                direction1 = ""
                if Battle.Sprite.direction == 0:
                    direction1 = "down"
                elif Battle.Sprite.direction == 1:
                    direction1 = "left"
                elif Battle.Sprite.direction == 2:
                    direction1 = "up"
                elif Battle.Sprite.direction == 3:
                    direction1 = "right"
                surface1 = font4.render("direction: {}".format(direction1), False, (255, 255, 255))
                Screen.win.blit(surface1, (300, 715))
                surface1 = font4.render("speed: {}".format(Battle.Sprite.velocity), False, (255, 255, 255))
                Screen.win.blit(surface1, (300, 750))

                surface1 = font4.render("enemy effects:", False, (255, 255, 255))
                Screen.win.blit(surface1, (20, 20))
                surface1 = font4.render("player effects:", False, (255, 255, 255))
                Screen.win.blit(surface1, (20, 470))
                line1, line2 = 510, 60
                for _effect in Battle.Effect.effect_list:
                    if _effect.name != "":
                        if _effect.target_player:
                            surface1 = font4.render(_effect.name, False, _effect.color)
                            Screen.win.blit(surface1, (20, line1))
                            line1 += 35
                        else:
                            surface1 = font4.render(_effect.name, False, _effect.color)
                            Screen.win.blit(surface1, (20, line2))
                            line2 += 35

            pygame.draw.rect(Screen.win, (80, 255, 255), (320, 2, round((1 - Battle.current_battle_frame / Battle.max_battle_frames) * 560), 4))
            pygame.draw.rect(Screen.win, (80, 255, 80), (320, 8, round(Battle.enemy_hp / Battle.enemy_max_hp * 560), 4))
            pygame.draw.rect(Screen.win, (255, 255, 255), (319, 0, 2, 14))
            pygame.draw.rect(Screen.win, (255, 255, 255), (879, 0, 2, 14))

            if Battle.enemy_last_frame_hp != Battle.enemy_hp:
                animation("1", False, int(Battle.enemy_hp - Battle.enemy_last_frame_hp), 12)
            if Battle.player_last_frame_hp != Ins.player.hp:
                animation("1", True, int(Ins.player.hp - Battle.player_last_frame_hp), 12)
            for _attack in Battle.attack_delay_list:
                if Battle.attack_delay_list[_attack] > 0:
                    Battle.attack_delay_list[_attack] -= 1
            if console_active_list["show fps"] == 1:
                surface1 = font5.render(str(int(Game.frame*10)/10), False, (255, 255, 255))
                Screen.win.blit(surface1, (1160, -5))
            ##############################################  handle sprite
            Battle.enemy_last_frame_hp = Battle.enemy_hp
            Battle.player_last_frame_hp = Ins.player.hp
            for _passive in Ins.player.passive_list:
                globals()["fp_" + _passive]()
            if console_active_list == 1:
                try:
                    pygame.draw.line(Screen.win, (255, 0, 0), (600, 300), (int(600 + 40 * math.cos(Battle.Sprite.degree)), int(300 + 40 * math.sin(Battle.Sprite.degree))))
                except TypeError:
                    pygame.draw.circle(Screen.win, (255, 0, 0), (600, 300), 10, 1)
            Battle.Sprite.set_degree()
            if Battle.Sprite.mode in (0, 4, 5, 2):
                Battle.Sprite.move()
            elif Battle.Sprite.mode == 1:
                temp_velocity = int(Battle.Sprite.velocity)
                Battle.Sprite.velocity = 610
                Battle.Sprite.move()
                Battle.Sprite.velocity = int(temp_velocity)
            elif Battle.Sprite.mode == 3:
                Battle.Sprite.gravity()
                # if Battle.Sprite.velocity > Battle.Sprite.mode_2_velocity:
                #     Battle.Hitbox.hitbox_rect_list = []
                #     for _hitbox in Battle.Hitbox.hitbox_list:
                #         Battle.Hitbox.hitbox_rect_list.append(pygame.Rect(int(_hitbox.x), int(_hitbox.y), _hitbox.width, _hitbox.height))
                #     for _ in range(abs(Battle.Sprite.mode_2_velocity)):
                #         Battle.Sprite.gravity()
                #
                # if Battle.Sprite.force_move and Battle.Sprite.mode_2_velocity < Battle.Sprite.velocity:
                #     Battle.Sprite.mode_2_velocity = Battle.Sprite.velocity
                #
                # try:
                #     Battle.Sprite.temp_degree_bool = math.isclose(Battle.Sprite.degree % (2 * PI), ((Battle.Sprite.direction - 1) * PI / 2 - PI / 4) % (2 * PI)) or math.isclose(Battle.Sprite.degree % (2 * PI), ((Battle.Sprite.direction - 1) * PI / 2 + PI / 4) % (2 * PI))
                # except TypeError:
                #     Battle.Sprite.temp_degree_bool = False
                # if Battle.Sprite.mode_2_velocity < Battle.Sprite.velocity and any((Battle.Sprite.temp_degree_bool and Battle.Sprite.direction == _key[0] and not keysHeld[_key[1]]) for _key in ((0, Ins.settings.move_up), (1, Ins.settings.move_right), (2, Ins.settings.move_down), (3, Ins.settings.move_left))):
                #     Battle.Sprite.mode_2_velocity = Battle.Sprite.velocity
                # Battle.Sprite.move()
                # Battle.Sprite.force_move = False
                #
                # if Battle.Sprite.velocity <= Battle.Sprite.mode_2_velocity:
                #     Battle.Hitbox.hitbox_rect_list = []
                #     for _hitbox in Battle.Hitbox.hitbox_list:
                #         Battle.Hitbox.hitbox_rect_list.append(pygame.Rect(int(_hitbox.x), int(_hitbox.y), _hitbox.width, _hitbox.height))
                #     for _ in range(abs(Battle.Sprite.mode_2_velocity)):
                #         Battle.Sprite.gravity()
            Battle.Sprite.draw()
            if (Battle.current_battle_frame - Battle.Sprite.effect_frame) % 20 == 0 and Battle.Sprite.current_effect_length > 0 and Battle.Sprite.current_effect != 0:
                Battle.Sprite.effect_ff()
            ##############################################  delete
            for _hitbox in Battle.Hitbox.hitbox_list:
                hitbox_rect = pygame.Rect(int(_hitbox.x + 305), int(_hitbox.y + 305), _hitbox.width, _hitbox.height)
                if not hitbox_rect.colliderect(pygame.Rect(250, 250, 700, 500)):
                    _hitbox.__class__.hitbox_list.pop(_hitbox.__class__.hitbox_list.index(_hitbox))
            bound = Polygon([(250, 250), (950, 250), (950, 750), (250, 750)])
            for _projectile in Battle.Projectile.projectile_list:
                if not Polygon.intersects(Polygon(_projectile.hitbox), bound):
                    _projectile.deleted()
                    _projectile.__class__.projectile_list.remove(_projectile)
            Battle.read_frame()
            try:
                globals()["bf_ex_"+str(Screen.enemy_id)]()
            except KeyError:
                pass
            ##############################################
            if Battle.next_attack_delay > 0:
                Battle.next_attack_delay -= 1
            if not Turns.pause:
                if keysDown[Ins.settings.battle_switch_menu]:
                    Battle.selected_battle_menu = (Battle.selected_battle_menu + 1) % 3
                if Battle.selected_battle_menu == 0:
                    if keysDown[Ins.settings.battle_func1]:
                        if Battle.selected_menu == 0:
                            Battle.selected_weapon_attack += 1
                            if Battle.selected_weapon_attack == 1 and Ins.player.sword is None:
                                Battle.selected_weapon_attack += 2
                            if Battle.selected_weapon_attack == 3 and Ins.player.bow is None:
                                Battle.selected_weapon_attack += 2
                            if Battle.selected_weapon_attack == 5 and Ins.player.staff is None:
                                Battle.selected_weapon_attack += 2
                            if Battle.selected_weapon_attack >= 7:
                                Battle.selected_weapon_attack = 0
                        else:
                            Battle.selected_menu = 0
                    elif keysDown[Ins.settings.battle_func2]:
                        if Ins.player.script is not None:
                            if Battle.selected_menu == 1:
                                Battle.selected_script_attack += 1
                                if len(scripts[Ins.player.script][2]) <= Battle.selected_script_attack:
                                    Battle.selected_script_attack = 0
                            else:
                                Battle.selected_menu = 1
                    elif keysDown[Ins.settings.battle_func3]:
                        if Ins.player.scroll is not None:
                            if Battle.selected_menu == 2:
                                Battle.selected_scroll_attack += 1
                                if len(scrolls[Ins.player.scroll][2]) <= Battle.selected_scroll_attack:
                                    Battle.selected_scroll_attack = 0
                            else:
                                Battle.selected_menu = 2
                elif Battle.selected_battle_menu == 1:
                    _temp_len = len(Ins.player.battle_inventory)
                    if keysDown[Ins.settings.battle_func1] and _temp_len >= 1:
                        Battle.selected_battle_item = 0
                    if keysDown[Ins.settings.battle_func2] and _temp_len >= 2:
                        Battle.selected_battle_item = 1
                    if keysDown[Ins.settings.battle_func3] and _temp_len >= 3:
                        Battle.selected_battle_item = 2
                else:
                    _temp_len = len(player_classes[Ins.player.playerClass][2])
                    if keysDown[Ins.settings.battle_func1] and _temp_len >= 1:
                        Battle.selected_battle_class = 0
                    if keysDown[Ins.settings.battle_func2] and _temp_len >= 2:
                        Battle.selected_battle_class = 1
                    if keysDown[Ins.settings.battle_func3] and _temp_len >= 3:
                        Battle.selected_battle_class = 2

                if keysDown[Ins.settings.battle_confirm]:
                    if Battle.selected_battle_menu == 0:
                        _attack_list = ["", (0, 0, 0), 0, [0, 0, 0, [0, 0], [0, 0]], -1, -1, 0]

                        _delay_over = True
                        if Battle.selected_menu == 0:
                            _attack_list = attacks[Battle.selected_weapon_attack]
                        elif Battle.selected_menu == 1:
                            _attack_list = scripts[Ins.player.script][2][Battle.selected_script_attack]
                            _delay_over = Battle.attack_delay_list[_attack_list[0]] <= 0
                        elif Battle.selected_menu == 2:
                            _attack_list = scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack]
                            _delay_over = Battle.attack_delay_list[_attack_list[0]] <= 0

                        if len(_attack_list[4]) == 1:
                            _in_area = True
                        else:
                            _in_area = False
                            for _rect in _attack_list[4][1:]:
                                if pygame.Rect(_rect[0], _rect[1], _rect[2], _rect[3]).collidepoint(round(Battle.Sprite.x + Battle.Sprite.length / 2), round(Battle.Sprite.y + Battle.Sprite.length / 2)):
                                    _in_area = True
                                    break

                        _is_weapon = False
                        _weapon_boost = 0
                        if _attack_list[6] == 0:
                            _is_weapon = True
                        elif _attack_list[6] == 1 and Ins.player.sword is not None:
                            _is_weapon = True
                            _weapon_boost = items[Ins.player.sword][13]
                        elif _attack_list[6] == 2 and Ins.player.bow is not None:
                            _is_weapon = True
                            _weapon_boost = items[Ins.player.bow][13]
                        elif _attack_list[6] == 3 and Ins.player.staff is not None:
                            _is_weapon = True
                            _weapon_boost = items[Ins.player.staff][13]

                        if Ins.player.mana >= _attack_list[2] and _in_area and _is_weapon and _delay_over and Battle.next_attack_delay == 0:
                            if _attack_list[7] != "":
                                sounds.play_effect(_attack_list[7])
                            if console_active_list["no delay"] == 0:
                                Battle.next_attack_delay = Battle.attack_delay
                                if Battle.selected_menu == 1:
                                    Battle.attack_delay_list[_attack_list[0]] = Battle.turn_delay_battle * _attack_list[9]
                                elif Battle.selected_menu == 2:
                                    Battle.attack_delay_list[_attack_list[0]] = Battle.turn_delay_battle * _attack_list[9]

                            Ins.player.add_mana(-1 * _attack_list[2])
                            if random.random() * (Ins.player.accuracy + 1) / (Battle.enemy_list[4][3] + 1) >= _attack_list[3][1]:
                                _is_crit = random.random() <= player_crit_rate(_attack_list[3][5][0])
                                _temp_critical = _attack_list[3][5][1] if _is_crit else 1
                                if _is_crit:
                                    animation("fadeText", "crit", (255, 80, 80), 4, point=(random.randint(450, 700), 250), layer=1)
                                _temp_attack_uniform = random.uniform(_attack_list[3][3][0], _attack_list[3][3][1])
                                _temp_heal_uniform = random.uniform(_attack_list[3][4][0], _attack_list[3][4][1])
                                _temp_damage = _temp_attack_uniform * _temp_critical * (_weapon_boost + 1) \
                                                * lvl_amp_func(Ins.player.level, Battle.enemy_list[4][5], _attack_list[8]) * player_atk_amp(_attack_list, Battle)\
                                               * atk_amp_func(Ins.player.attack, Battle.enemy_list[4][2], _attack_list[8]) * _attack_list[3][0]

                                # elif _attack_list[8] == 1:
                                    # _temp_damage *= 1

                                if _temp_damage > 0:
                                    Battle.damage_enemy(max(round(_temp_damage), random.randint(1, int((Ins.player.level + 1) / 10) + 1)))
                                else:
                                    Battle.damage_enemy(round(_temp_damage))
                                _temp_heal = Ins.player.defense * _attack_list[3][2] * (Ins.player.level / 99 + 1) * _temp_heal_uniform
                                if _temp_heal > 0:
                                    Ins.player.add_hp(max(round(_temp_heal), random.randint(0, int(Ins.player.level / 5 + 1))))
                                else:
                                    Ins.player.add_hp(round(_temp_heal))
                                if _attack_list[5] != -1:
                                    Battle.Effect(*_attack_list[5], (_attack_list, _temp_attack_uniform, _temp_critical, _temp_heal_uniform))
                                    # damage, damage rand range, accuracy, heal, heal rand range
                            else:
                                animation("1", False, "miss", 12)
                        else:
                            sounds.play_effect("effect4")

                    elif Battle.selected_battle_menu == 1:
                        if len(Ins.player.battle_inventory) >= 1 and Battle.next_attack_delay <= 0:
                            if console_active_list["no delay"] == 0:
                                Battle.next_attack_delay = Battle.attack_delay
                            _temp_item_list = Ins.player.battle_inventory[Battle.selected_battle_item]
                            Ins.player.add_hp(items[_temp_item_list][4])
                            Ins.player.add_mana(items[_temp_item_list][5])
                            for _passive in items[_temp_item_list][8]:
                                globals()["ap_" + _passive]()
                            if Ins.player.add_item(_temp_item_list, -1) == 1:
                                if len(Ins.player.battle_inventory) <= Battle.selected_battle_item:
                                    Battle.selected_battle_item -= 1
                                    if Battle.selected_battle_item <= -1:
                                        Battle.selected_battle_item = 0
                        else:
                            sounds.play_effect("effect4")

                    else:
                        # TODO: add more stuff here (?)
                        if Battle.next_attack_delay <= 0 and globals()["cat_con_" + player_classes[Ins.player.playerClass][0].replace(" ", "_")](False,  Battle.selected_battle_class):

                            globals()["cat_act_" + player_classes[Ins.player.playerClass][0].replace(" ", "_")](False,
                                                                                                                Battle.selected_battle_class)
                            if console_active_list["no delay"] == 0:
                                Battle.next_attack_delay = Battle.attack_delay
                        else:
                            sounds.play_effect("effect4")
            ##############################################
            if Screen.debug:
                if mouseHeld[1]:
                    Battle.Sprite.x = Screen.mouse_pos[0] - 305 - Battle.Sprite.length / 2
                    Battle.Sprite.y = Screen.mouse_pos[1] - 305 - Battle.Sprite.length / 2
                    Battle.Sprite.mode_2_velocity = 0
            ##############################################
            if keysDown["esc"]:
                Turns.pause = not Turns.pause

            if Turns.pause:
                surface1 = pygame.Surface((Screen.window_width, Screen.window_height))
                surface1.set_alpha(int(110))
                surface1.fill((0, 0, 0))
                Screen.win.blit(surface1, (0, 0))

                Screen.blit_text("give up", (Screen.window_width // 2, Screen.window_height // 2), font, (80, 255, 80), (0.5, 0.5))

                if keysDown[Ins.settings.interact] or keysDown[Ins.settings.battle_confirm]:
                    Battle.Effect.list_reset()
                    sounds.play("death_song", loops=0)
                    Screen.set_state("death")
                    animation("2")
                    Screen.afterBattleScreenVar = 0
                    Screen.afterBattleFrame = 0

            if Ins.player.hp <= 0 or Battle.current_battle_frame >= Battle.max_battle_frames or Battle.enemy_hp <= 0:
                Battle.Effect.list_reset()
                Ins.player.mana = int(Ins.player.mana)
                Ins.player.hp = int(Ins.player.hp)
                kill_on_tie = None
                if Battle.current_battle_frame >= Battle.max_battle_frames:
                    try:
                        kill_on_tie = globals()["bf_ti_" + str(Screen.enemy_id)]()
                    except KeyError:
                        kill_on_tie = True

                if Battle.enemy_hp <= 0 or kill_on_tie is False:
                    _line = 0
                    sounds.play("winning_song", loops=0, register=False)
                    Ins.player.mana = int(Ins.player.mana)
                    Screen.set_state("winner")
                    Screen.afterBattleFrame = 0
                    Screen.afterBattleList = [random.randint(Battle.enemy_list[6][0], Battle.enemy_list[6][1]), random.randint(Battle.enemy_list[6][2], Battle.enemy_list[6][3])]
                    Screen.afterBattleList1 = []
                    temp_float = math.log10(Screen.afterBattleList[0])
                    Screen.afterBattleScreenVar = max(10 ** ((int(temp_float) if temp_float - int(temp_float) <= 0.3 else int(temp_float) + 1) - 2), 1)
                    Screen.afterBattleTemp = 0
                    for item_list in Battle.enemy_list[5]:
                        if item_list[1] >= random.random():
                            temp_choice = random.choice(item_list[2])
                            Ins.player.add_item(item_list[0], temp_choice)
                            for i in range(len(Screen.afterBattleList1)):
                                if Screen.afterBattleList1[i][0] == item_list[0]:
                                    Screen.afterBattleList1[i][1] += temp_choice
                                    break
                            else:
                                Screen.afterBattleList1.append([item_list[0], temp_choice])
                    try:
                        globals()["bf_wn_" + str(Screen.enemy_id)]()
                    except KeyError:
                        pass
                elif Ins.player.hp <= 0 or kill_on_tie is True:  # death
                    sounds.play("death_song", loops=0)
                    Screen.set_state("death")
                    animation("2")
                    Screen.afterBattleScreenVar = 0
                    Screen.afterBattleFrame = 0

                Battle.enemy_list = []
                Screen.enemy_id = -1
                battle_stopped(False)
                continue
        # death
        elif Screen.state("death"):
            Screen.win.fill((120, 0, 0))
            ##############################################
            Animation.render_ff()
            surface1 = font2.render("YOU DIED", False, (255, 255, 255))
            surface1.set_alpha(min(int(1.5 * Screen.afterBattleFrame), 255))
            Screen.win.blit(surface1, (int(300 - surface1.get_rect().width / 2), 120))
            surface1 = font4.render("load save", False, (120, 255, 120) if Screen.afterBattleScreenVar == 0 else (200, 200, 200))
            surface1.set_alpha(min(int(1.3 * Screen.afterBattleFrame), 255))
            Screen.win.blit(surface1, (int(300 - surface1.get_rect().width / 2), 220))
            surface1 = font4.render("main menu", False, (120, 255, 120) if Screen.afterBattleScreenVar == 1 else (200, 200, 200))
            surface1.set_alpha(min(int(1.25 * Screen.afterBattleFrame), 255))
            Screen.win.blit(surface1, (int(300 - surface1.get_rect().width / 2), 260))
            surface1 = font4.render("quit", False, (120, 255, 120) if Screen.afterBattleScreenVar == 2 else (200, 200, 200))
            surface1.set_alpha(min(int(1.2 * Screen.afterBattleFrame), 255))
            Screen.win.blit(surface1, (int(300 - surface1.get_rect().width / 2), 300))
            if keysDown[Ins.settings.interact]:
                if Screen.afterBattleFrame < 170:
                    Screen.afterBattleFrame = 210
                elif Screen.afterBattleScreenVar == 0:
                    Screen.set_state("world")
                    load_save()
                    continue
                elif Screen.afterBattleScreenVar == 1:
                    return_to_menu()
                else:
                    Screen.run = False
            elif keysDown[Ins.settings.move_down]:
                if Screen.afterBattleFrame < 170:
                    Screen.afterBattleFrame = 210
                else:
                    Screen.afterBattleScreenVar += 1
                    if Screen.afterBattleScreenVar >= 3:
                        Screen.afterBattleScreenVar = 0
            elif keysDown[Ins.settings.move_up]:
                if Screen.afterBattleFrame < 170:
                    Screen.afterBattleFrame = 210
                else:
                    Screen.afterBattleScreenVar -= 1
                    if Screen.afterBattleScreenVar < 0:
                        Screen.afterBattleScreenVar = 2
            ##############################################
            Screen.afterBattleFrame += 1
        # win
        elif Screen.state("winner"):
            Screen.win.fill((0, min(Screen.afterBattleFrame, 120), 0))
            ##############################################
            c1 = min(max(2 * Screen.afterBattleFrame - 240, 0), 255)
            c2 = max(Screen.afterBattleFrame - 120 - max(2 * Screen.afterBattleFrame - 240, 0),
                     min(80, Screen.afterBattleFrame - 120), 0)
            c3 = max(Screen.afterBattleFrame - max(2 * Screen.afterBattleFrame - 240, 0),
                     min(80, Screen.afterBattleFrame - 120), 0)
            c4 = min(Screen.afterBattleFrame, 255)

            surface1 = font2.render("VICTORY", False, (c1, c4, c1))
            Screen.win.blit(surface1, (int(300 - surface1.get_rect().width / 2), 60))
            surface1 = font4.render("level: {}".format(Ins.player.level), False, (c1, c4, c1))
            Screen.win.blit(surface1, (20, 120))
            pygame.draw.rect(Screen.win, (c2, c3, c2), (20, 160, 180, 35))
            pygame.draw.rect(Screen.win, (c1, c4, c1),
                             (20, 160, max(int(180 * Ins.player.exp / Ins.player.next_lvl_exp), 1), 35))
            pygame.draw.rect(Screen.win, (c2, c3, c2), (20, 160, 180, 35), 3)
            surface1 = font5.render("{}/ {} exp".format(Ins.player.exp, Ins.player.next_lvl_exp), False, (c1, c4, c1))
            Screen.win.blit(surface1, (20, 200))
            surface1 = font5.render("coins: {}".format(Ins.player.coins), False, (c1, c4, c1))
            Screen.win.blit(surface1, (20, 230))
            surface1 = font4.render("items:", False, (c1, c4, c1))
            Screen.win.blit(surface1, (430, 120))
            ##############################################
            if Screen.afterBattleFrame == 223 + Screen.afterBattleList[0] // Screen.afterBattleScreenVar:
                Screen.afterBattleTemp = 0
                _line = 0

            if keysDown[Ins.settings.interact]:
                if Screen.afterBattleFrame < 220:
                    Screen.afterBattleFrame = 220
                elif Screen.afterBattleFrame < 220 + Screen.afterBattleList[0] // Screen.afterBattleScreenVar:
                    sounds.play_effect("exp_gain")
                    Ins.player.add_exp(Screen.afterBattleList[0] - Screen.afterBattleTemp)
                    Screen.afterBattleTemp = int(Screen.afterBattleList[0])
                    Screen.afterBattleFrame = 220 + Screen.afterBattleList[0] // Screen.afterBattleScreenVar
                elif Screen.afterBattleFrame <= 234 + Screen.afterBattleList[0] // Screen.afterBattleScreenVar:
                    if Screen.afterBattleFrame <= 223 + Screen.afterBattleList[0] // Screen.afterBattleScreenVar:
                        Screen.afterBattleTemp = 0
                    _line = 0
                    Ins.player.add_coins(Screen.afterBattleList[0] - Screen.afterBattleTemp) #(14 + Screen.afterBattleFrame - 234 - Screen.afterBattleList[0] // Screen.afterBattleScreenVar) * (Screen.afterBattleList[0] // 15)
                    sounds.play_effect("effect10")
                    Screen.afterBattleFrame = 240 + Screen.afterBattleList[0] // Screen.afterBattleScreenVar
                elif Screen.afterBattleFrame <= Screen.afterBattleList[0] // Screen.afterBattleScreenVar + 253 + 15 * len(Screen.afterBattleList1):
                    Screen.afterBattleFrame = Screen.afterBattleList[0] // Screen.afterBattleScreenVar + 253 + 15 * len(Screen.afterBattleList1)
                else:
                    Screen.set_state("world")
                    sounds.play(Screen.map_song, True)
                    Screen.resize(64 * Screen.screen_width, 64 * Screen.screen_height)
                    pygame.display.set_caption(Screen.map_name)
                    if Ins.settings.allowAutoSaves:
                        save_progress()
            if Screen.afterBattleFrame >= Screen.afterBattleList[0] // Screen.afterBattleScreenVar + 250:
                if _line // 30 != len(Screen.afterBattleList1[:(Screen.afterBattleFrame - Screen.afterBattleList[0] // Screen.afterBattleScreenVar - 250) // 15]):
                    sounds.play_effect("effect13")
                _line = 0
                for item_list in Screen.afterBattleList1[:(Screen.afterBattleFrame - Screen.afterBattleList[0] // Screen.afterBattleScreenVar - 250) // 15]:
                    surface1 = font5.render("{} x{}".format(item_list[0], item_list[1]), False, (255, 255, 255))
                    Screen.win.blit(surface1, (570 - surface1.get_rect().width, 155 + _line))
                    _line += 30

            elif 239 >= Screen.afterBattleFrame - Screen.afterBattleList[0] // Screen.afterBattleScreenVar >= 225:
                Ins.player.add_coins(Screen.afterBattleList[1] // 15)
                Screen.afterBattleTemp += Screen.afterBattleList[1] // 15
            elif 240 + Screen.afterBattleList[0] // Screen.afterBattleScreenVar == Screen.afterBattleFrame:
                Ins.player.add_coins(Screen.afterBattleList[1] - Screen.afterBattleTemp)
                if Screen.afterBattleList[1] - Screen.afterBattleTemp < 0:
                    print("FUCKING NEGATIVE")
                sounds.play_effect("effect10")
            elif Screen.afterBattleFrame > 220:
                if Screen.afterBattleFrame < Screen.afterBattleList[0] // Screen.afterBattleScreenVar + 220:
                    sounds.play_effect("exp_gain")
                    Ins.player.add_exp(Screen.afterBattleScreenVar)
                    Screen.afterBattleTemp += Screen.afterBattleScreenVar
                elif Screen.afterBattleFrame == Screen.afterBattleList[0] // Screen.afterBattleScreenVar + 220:
                    sounds.play_effect("exp_gain")
                    Ins.player.add_exp(Screen.afterBattleList[0] - Screen.afterBattleTemp)
                    if Screen.afterBattleList[0] - Screen.afterBattleTemp < 0:
                        print("AAAAAAAAAAAAAAAAAA")
                    Screen.afterBattleTemp = int(Screen.afterBattleList[0])
                    # Ins.player.exp = max(0, Ins.player.exp)

            if Screen.afterBattleFrame >= Screen.afterBattleList[0] // Screen.afterBattleScreenVar + 250 + 15 * len(Screen.afterBattleList1):
                surface1 = font4.render("press {} to continue:".format(Ins.settings.interact), False, (255, 255, 255))
                Screen.win.blit(surface1, (int(300 - surface1.get_rect().width / 2), 365))
            Screen.afterBattleFrame += 1
        # fast travel
        elif Screen.state("fastTravel"):
            pygame.draw.rect(Screen.win, (110, 110, 110), (10, 10, 530, 400))
            try:
                for _travel in range(6):
                    pygame.draw.rect(Screen.win,
                                     # ((255, 60, 60) if Screen.selected_travel_map == _travel else (140, 40, 40)) if
                                     # travel_list[Screen.travel_page * 6 + _travel][0] == Screen.selected_map_str else (
                                        (((80, 255, 80) if Screen.selected_travel_map == _travel else (140, 140, 140)) if
                                         Ins.ap.travel_unlocked[travel_list[Screen.travel_page * 6 + _travel][0]] else (
                                             (100, 100, 100) if Screen.selected_travel_map == _travel else (50, 50, 50))),
                                     (15, 50 + 60 * _travel, 520, 50))
                    surface1 = font2.render(travel_list[Screen.travel_page * 6 + _travel][2], False, (0, 0, 0))
                    Screen.win.blit(surface1, (20, 50 + 60 * _travel))
                    _travel_count = _travel
            except IndexError:
                pass
            surface1 = font4.render("travel menu: page {}/ {}".format(Screen.travel_page + 1, Screen.travel_max), False, (0, 0, 0))
            Screen.win.blit(surface1, (15, 10))
            ##############################
            if Screen.is_question:
                if keysDown[Ins.settings.interact]:
                    Screen.is_question = False
                    if not Screen.question_option:
                        sounds.play_effect("effect8")
                        _temp_list = travel_list[Screen.travel_page * 6 + Screen.selected_travel_map]

                        Ins.player.x = int(_temp_list[1][0]) * 64 + 32 - Ins.player.width / 2
                        Ins.player.y = int(_temp_list[1][1]) * 64 + 32 - Ins.player.height / 2
                        Ins.player.position()
                        Screen.select_map(_temp_list[0])

                        Screen.set_state("world")
                        Screen.is_displaying = False
                        Screen.resize(64 * Screen.screen_width, 64 * Screen.screen_height)
                        pygame.display.set_caption(Screen.map_name)
                        if sounds.get_current_song() != Screen.map_song:
                            sounds.play(Screen.map_song, True)
                        if Ins.settings.allowAutoSaves:
                            save_progress()
                        continue
                    else:
                        sounds.play_effect("effect6")
            elif Screen.is_displaying:
                pass

            elif keysDown[Ins.settings.interact]:
                # if travel_list[Screen.travel_page * 6 + Screen.selected_travel_map][0] == Screen.selected_map_str:
                #     sounds.play_effect("effect4")
                #     Screen.displayed_msg = "you are already there!"
                #     Screen.is_displaying = True
                #     continue
                if Ins.ap.travel_unlocked[travel_list[Screen.travel_page * 6 + Screen.selected_travel_map][0]]:
                    sounds.play_effect("effect7")
                    Screen.question_option = 0
                    Screen.question_text = "fast travel to \"{}\"?".format(
                        travel_list[Screen.travel_page * 6 + Screen.selected_travel_map][2])
                    Screen.is_question = True
                else:
                    sounds.play_effect("effect4")
                    Screen.displayed_msg = "you cant fast travel there yet!"
                    Screen.is_displaying = True
                    continue

            elif keysDown[Ins.settings.move_down]:
                if Screen.selected_travel_map == _travel_count:
                    keysDown[Ins.settings.move_right] = True
                else:
                    sounds.play_effect("effect1")
                    Screen.selected_travel_map += 1
            elif keysDown[Ins.settings.move_up]:
                if Screen.selected_travel_map == 0:
                    keysDown[Ins.settings.move_left] = True
                else:
                    sounds.play_effect("effect1")
                    Screen.selected_travel_map -= 1

            if Screen.is_displaying or Screen.is_question or keysDown[Ins.settings.interact]:
                pass
            elif keysDown[Ins.settings.move_left]:
                if Screen.travel_page != 0:
                    sounds.play_effect("effect5")
                    Screen.travel_page -= 1
                    Screen.selected_travel_map = 0
                    if keysDown[Ins.settings.move_up]:
                        Screen.selected_travel_map = 5
            elif keysDown[Ins.settings.move_right]:
                if Screen.travel_page != Screen.travel_max - 1:
                    sounds.play_effect("effect5")
                    Screen.travel_page += 1
                    Screen.selected_travel_map = 0
            ##############################
            if Screen.is_question:
                pygame.draw.rect(Screen.win, (140, 140, 140), (65, 100, 420, 200))
                pygame.draw.rect(Screen.win, (0, 0, 0), (65, 100, 420, 200), 2)
                _temp_text = Screen.get_text_format(Screen.question_text, 410, font4)
                screen_start1 = 105
                for _text in _temp_text:
                    surface1 = font4.render(_text, False, (0, 0, 0))
                    Screen.win.blit(surface1, (int(275 - surface1.get_rect().width / 2), screen_start1))
                    screen_start1 += 35
                pygame.draw.rect(Screen.win, (180, 180, 180), (110, 215, 140, 58))
                pygame.draw.rect(Screen.win, (180, 180, 180), (300, 215, 140, 58))
                surface1 = font2.render("Yes", False, (0, 0, 0))
                Screen.win.blit(surface1, (133, 220))
                surface1 = font2.render("No", False, (0, 0, 0))
                Screen.win.blit(surface1, (342, 220))
                if keysDown[Ins.settings.move_left] or keysDown[Ins.settings.move_right]:
                    Screen.question_option = not Screen.question_option
                    sounds.play_effect("effect1")
                pygame.draw.rect(Screen.win, (80, 255, 80), (110 + 190 * Screen.question_option, 215, 140, 58), 1)

                if keysDown["esc"]:
                    Screen.is_question = False
                    continue
            if Screen.is_displaying:
                if keysDown[Ins.settings.interact]:
                    Screen.is_displaying = False
                pygame.draw.rect(Screen.win, (140, 140, 140), (65, 100, 420, 200))
                pygame.draw.rect(Screen.win, (0, 0, 0), (65, 100, 420, 200), 2)
                _temp_text = Screen.get_text_format(Screen.displayed_msg, 410, font4)
                screen_start1 = 200
                for _text in _temp_text:
                    surface1 = font4.render(_text, False, (0, 0, 0))
                    Screen.win.blit(surface1, (int(275 - surface1.get_rect().width / 2), int(screen_start1 - (len(_temp_text)) * 35 / 2)))
                    screen_start1 += 35

                if keysDown["esc"]:
                    Screen.is_displaying = False
                    continue
            if keysDown["esc"]:
                sounds.play_effect("effect9")
                Screen.set_state("menu")
                Screen.is_displaying = False
                Screen.is_question = False
                continue
        # console
        elif Screen.state("debug"):
            pygame.draw.rect(Screen.win, (110, 110, 110), (10, 10, 530, 110))
            surface1 = font4.render(console_list[Screen.console_index % len(console_list)], False, (80, 255, 80))
            Screen.win.blit(surface1, (15, 45))
            surface1 = font4.render(console_list[(Screen.console_index - 1) % len(console_list)], False, (0, 0, 0))
            Screen.win.blit(surface1, (15, 10))
            surface1 = font4.render(console_list[(Screen.console_index + 1) % len(console_list)], False, (0, 0, 0))
            Screen.win.blit(surface1, (15, 80))

            surface1 = font4.render(str(console_choice_list[console_list[Screen.console_index % len(console_list)]][console_active_list[console_list[Screen.console_index % len(console_list)]]]), False, (80, 250, 80))
            Screen.win.blit(surface1, (535 - surface1.get_rect().width, 45))
            surface1 = font4.render(str(console_choice_list[console_list[(Screen.console_index - 1) % len(console_list)]][console_active_list[console_list[(Screen.console_index - 1) % len(console_list)]]]), False, (0, 0, 0))
            Screen.win.blit(surface1, (535 - surface1.get_rect().width, 10))
            surface1 = font4.render(str(console_choice_list[console_list[(Screen.console_index + 1) % len(console_list)]][console_active_list[console_list[(Screen.console_index + 1) % len(console_list)]]]), False, (0, 0, 0))
            Screen.win.blit(surface1, (535 - surface1.get_rect().width, 80))
            ##############################
            if keysDown[Ins.settings.interact]:
                console_active_list[console_list[Screen.console_index % len(console_list)]] = 0
            elif keysDown[Ins.settings.other_function]:
                for _settings in console_list:
                    console_active_list[_settings] = 0
            elif keysDown[Ins.settings.move_right]:
                console_active_list[console_list[Screen.console_index % len(console_list)]] += 1
                if console_active_list[console_list[Screen.console_index % len(console_list)]] >= len(
                        console_choice_list[console_list[Screen.console_index % len(console_list)]]):
                    console_active_list[console_list[Screen.console_index % len(console_list)]] = 0
            elif keysDown[Ins.settings.move_left]:
                console_active_list[console_list[Screen.console_index % len(console_list)]] -= 1
                if console_active_list[console_list[Screen.console_index % len(console_list)]] < 0:
                    console_active_list[console_list[Screen.console_index % len(console_list)]] = len(
                        console_choice_list[console_list[Screen.console_index % len(console_list)]]) - 1
            elif keysDown[Ins.settings.move_down]:
                Screen.console_index += 1
            elif keysDown[Ins.settings.move_up]:
                Screen.console_index -= 1
            ##############################
            if keysDown["esc"]:
                sounds.play_effect("effect9")
                Screen.set_state("menu")
                continue
        # journal
        elif Screen.state("journal"):
            pygame.draw.rect(Screen.win, (110, 110, 110), (10, 10, 540, 300))
            _temp_page_count = 0

            for _i in range(5):
                broken = True
                for _j in range(2):
                    if len(_temp_mission_list) <= 2 * _i + _j + 10 * Screen.mission_page:
                        break
                    _temp_value = Ins.ap.mission_progress_list[_temp_mission_list[2 * _i + _j + 10 * Screen.mission_page][0]]
                    if 2 * _i + _j == Screen.mission_index:
                        pygame.draw.rect(Screen.win, (80, 255, 80), (30 + _i * 101, 15 + _j * 101, 96, 96))
                    _temp_texture = textures.mission_normal
                    if _temp_mission_list[2 * _i + _j + 10 * Screen.mission_page][1]:
                        _temp_texture = textures.mission_main
                    if isinstance(_temp_value, int) and _temp_value >= 1:
                        _temp_texture = textures.mission_progress
                    if _temp_value is True:
                        if Ins.ap.mission_claimed[_temp_mission_list[2 * _i + _j + 10 * Screen.mission_page][0]]:
                            _temp_texture = textures.mission_finished
                        else:
                            _temp_texture = textures.mission_claimable
                    Screen.win.blit(_temp_texture, (30 + _i * 101, 15 + _j * 101))
                    _temp_page_count += 1
                else:
                    broken = False

                if broken:
                    break

            if Screen.mission_page > 0:
                pygame.draw.lines(Screen.win, (255, 255, 255), False, ((25, 25), (14, 110), (25, 195)), 5)
            if len(_temp_mission_list) > 10 * (Screen.mission_page + 1):
                pygame.draw.lines(Screen.win, (255, 255, 255), False, ((533, 25), (544, 110), (533, 195)), 5)

            _temp_text_index = Ins.ap.mission_progress_list[
                _temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]]
            _temp_string = "completed"
            if not Ins.ap.mission_claimed[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]]:
                _temp_string = "interact to claim"
            if Ins.ap.mission_progress_list[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]] is not True:
                _temp_string = mission_stats_list[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]][0][_temp_text_index]
            _temp_string = Screen.get_text_format("{}: {}".format(_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0], _temp_string), 534, font3)
            _temp_reward = Screen.get_text_format("reward: {}".format(mission_stats_list[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]][1]), 534, font3)
            _temp_font = (font3, 30)
            if len(_temp_string) + len(_temp_reward) > 3:
                _temp_font = (font9, 24)
                _temp_string = Screen.get_text_format(" ".join(_temp_string), 534, font9)
                _temp_reward = Screen.get_text_format(" ".join(_temp_reward), 534, font9)

            i = 0
            for text in _temp_string + _temp_reward:
                Screen.blit_text(text, (15, 210 + i), _temp_font[0], (0, 0, 0))
                i += _temp_font[1]
            ##############################
            if Screen.is_displaying:
                pass
            elif keysDown[Ins.settings.interact]:
                Screen.is_displaying = True
                if Ins.ap.mission_progress_list[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]] is True:
                    if Ins.ap.mission_claimed[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]]:
                        sounds.play_effect("effect4")
                        Screen.displayed_msg = "you already claimed this reward!"
                    else:
                        # _temp_mission_list = [i for i in mission_list if not (Ins.ap.mission_progress_list[i[0]] is False or (Ins.ap.mission_claimed[i[0]] or Ins.settings.showClaimedMissions))]
                        Ins.ap.mission_claimed[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]] = True
                        Ins.player.add_exp(mission_stats_list[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]][2][0])
                        Ins.player.add_coins(mission_stats_list[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]][2][1])
                        for cmd in mission_stats_list[_temp_mission_list[Screen.mission_index + 10 * Screen.mission_page][0]][2][2]:
                            if isinstance(cmd, str):
                                globals()["mf_" + cmd]()
                            else:
                                globals()["mf_" + cmd[0]](*cmd[1:])
                        Screen.displayed_msg = "you claimed this mission's reward!"
                else:
                    sounds.play_effect("effect4")
                    Screen.displayed_msg = "you didn't complete this mission yet!"
                continue
            elif keysDown[Ins.settings.move_down] or keysDown[Ins.settings.move_up]:
                if Screen.mission_index % 2 == 0:
                    Screen.mission_index += 1
                    if Screen.mission_index >= _temp_page_count:
                        Screen.mission_index -= 1
                    else:
                        sounds.play_effect("effect5")
                else:
                    sounds.play_effect("effect5")
                    Screen.mission_index -= 1
            elif keysDown[Ins.settings.move_left]:
                Screen.mission_index -= 2
                if Screen.mission_index < 0:
                    if Screen.mission_page > 0:
                        sounds.play_effect("effect5")
                        Screen.mission_index += 10
                        Screen.mission_page -= 1
                    else:
                        Screen.mission_index += 2
                else:
                    sounds.play_effect("effect5")
            elif keysDown[Ins.settings.move_right]:
                Screen.mission_index += 2
                if Screen.mission_index >= _temp_page_count:
                    if Screen.mission_page < Screen.mission_max_page - 1:
                        sounds.play_effect("effect5")
                        Screen.mission_index -= 10
                        Screen.mission_page += 1
                    else:
                        Screen.mission_index -= 2
                else:
                    sounds.play_effect("effect5")
            ##############################
            if Screen.is_displaying:
                if keysDown[Ins.settings.interact]:
                    Screen.is_displaying = False
                pygame.draw.rect(Screen.win, (140, 140, 140), (110, 80, 340, 160))
                pygame.draw.rect(Screen.win, (0, 0, 0), (110, 80, 340, 160), 2)
                _temp_text = Screen.get_text_format(Screen.displayed_msg, 336, font4)
                screen_start1 = 160
                for _text in _temp_text:
                    surface1 = font4.render(_text, False, (0, 0, 0))
                    Screen.win.blit(surface1, (int(280 - surface1.get_rect().width / 2), int(screen_start1 - (len(_temp_text)) * 35 / 2)))
                    screen_start1 += 35

                if keysDown["esc"]:
                    Screen.is_displaying = False
                    continue
            if keysDown["esc"]:
                sounds.play_effect("effect9")
                Screen.set_state("menu")
                Screen.is_displaying = False
                Requires.scr_update()
                continue
        # stats
        elif Screen.state("stats"):
            pygame.draw.rect(Screen.win, (110, 110, 110), (5, 5, 690, 485))
            _line = 0
            try:
                for stat in range(len(stats_list)):
                    surface1 = font4.render(
                        stats_list[2 * stat].replace("_", " ") + ": " + str(getattr(Ins.stats, stats_list[2 * stat])), False,
                        (0, 0, 0))
                    Screen.win.blit(surface1, (10, 30 * _line))
                    surface1 = font4.render(
                        stats_list[2 * stat + 1].replace("_", " ") + ": " + str(getattr(Ins.stats, stats_list[2 * stat + 1])),
                        False, (0, 0, 0))
                    Screen.win.blit(surface1, (355, 30 * _line))
                    _line += 1
            except IndexError:
                pass

            if keysDown["esc"]:
                sounds.play_effect("effect9")
                Screen.set_state("menu")
                pygame.display.set_caption("menu")
                continue
        # settings
        elif Screen.state("settings"):
            pygame.draw.rect(Screen.win, (120, 120, 120), (5, 5, 290, 590))
            run_settings(True)

            if keysDown["esc"]:
                Screen.is_displaying = False
                Screen.set_state("menu")
                continue
        # classes
        elif Screen.state("classes"):
            pygame.draw.rect(Screen.win, (80, 80, 80), (5, 5, 890, 840))
            pygame.draw.line(Screen.win, (80, 255, 80), (525, 400), (int(765 - font5.render(player_classes[Screen.classIndex + 1][0], False, (255, 255, 255)).get_rect().width / 2), 400), 4)
            pygame.draw.line(Screen.win, (80, 255, 80), (int(745 - font5.render(player_classes[Screen.classIndex + 1][0], False, (255, 255, 255)).get_rect().width / 2), 420), (int(765 - font5.render(player_classes[Screen.classIndex + 1][0], False, (255, 255, 255)).get_rect().width / 2), 400), 4)
            pygame.draw.line(Screen.win, (80, 255, 80), (int(745 - font5.render(player_classes[Screen.classIndex + 1][0], False, (255, 255, 255)).get_rect().width / 2), 380), (int(765 - font5.render(player_classes[Screen.classIndex + 1][0], False, (255, 255, 255)).get_rect().width / 2), 400), 4)
            surface1 = font5.render("selected class: " + player_classes[Ins.player.playerClass][0], False, (255, 255, 255))
            Screen.win.blit(surface1, (10, 5))
            for classIndex in list(player_classes.keys())[1:]:
                surface1 = font5.render(player_classes[classIndex][0], False, (80, 255, 80) if Ins.player.playerClass == classIndex else ((255, 255, 255) if Requires.classes_req[classIndex][0] else (0, 0, 0)))
                Screen.win.blit(surface1, (int(450 + 350 * math.cos((classIndex - 1 - Screen.classIndex + Screen.classRotationTime / 10) * PI / ((len(player_classes) - 1) / 2)) - surface1.get_rect().width / 2), int(400 + 350 * math.sin((classIndex - 1 - Screen.classIndex + Screen.classRotationTime / 10) * PI / ((len(player_classes) - 1) / 2)) - surface1.get_rect().height / 2)))
            ##############################################
            if Screen.classRotationTime != 0:
                Screen.classRotationTime += Screen.classDeg
            elif keysDown[Ins.settings.interact] and not Screen.is_displaying:
                if Requires.classes_req[Screen.classIndex + 1][0]:
                    if Ins.player.playerClass is None:
                        Ins.player.playerClass = Screen.classIndex + 1
                        globals()["cja_" + player_classes[Ins.player.playerClass][0]]()
                    elif Ins.player.playerClass == Screen.classIndex + 1:
                        globals()["cjs_" + player_classes[Ins.player.playerClass][0]]()
                        Ins.player.playerClass = None
                    else:
                        globals()["cjs_" + player_classes[Ins.player.playerClass][0]]()
                        Ins.player.playerClass = Screen.classIndex + 1
                        globals()["cja_" + player_classes[Ins.player.playerClass][0]]()
                else:
                    sounds.play_effect("effect4")
                    Screen.is_displaying = True
                    Screen.displayed_msg = str(Requires.classes_req[Screen.classIndex + 1][1])
                    continue
            elif keysDown[Ins.settings.move_up]:
                Screen.classIndex -= 1
                Screen.classRotationTime = -10
                Screen.classDeg = 1
                sounds.play_effect("effect14")
                if Screen.classIndex < 0:
                    Screen.classIndex = len(player_classes) - 2

                Screen.description_message = Screen.get_text_format(player_classes[Screen.classIndex + 1][1], 745, font3)
                Screen.description_page = 0
            elif keysDown[Ins.settings.move_down]:
                Screen.classIndex += 1
                Screen.classRotationTime = 10
                Screen.classDeg = -1
                sounds.play_effect("effect14")
                if Screen.classIndex >= len(player_classes) - 1:
                    Screen.classIndex = 0

                Screen.description_message = Screen.get_text_format(player_classes[Screen.classIndex + 1][1], 745, font3)
                Screen.description_page = 0
            if keysDown["esc"]:
                sounds.play_effect("effect9")
                Screen.is_displaying = False
                Screen.set_state("menu")
                continue
            try:
                pygame.draw.rect(Screen.win, (100, 100, 100), (10, 800, 880, 40))
                surface1 = font3.render(Screen.description_message[Screen.description_page], False, (0, 0, 0))
                Screen.win.blit(surface1, (20, 800))
                surface1 = font3.render(
                    "page: {} /{}".format(Screen.description_page + 1, len(Screen.description_message)), False,
                    (0, 0, 0))
                Screen.win.blit(surface1, (870 - surface1.get_rect().width, 800))
                if keysDown[Ins.settings.other_function]:
                    Screen.description_page += 1
                    if Screen.description_page >= len(Screen.description_message):
                        Screen.description_page = 0
            except IndexError:
                pass
            if Screen.is_displaying:
                if keysDown[Ins.settings.interact]:
                    Screen.is_displaying = False
                pygame.draw.rect(Screen.win, (140, 140, 140), (240, 250, 420, 200))
                pygame.draw.rect(Screen.win, (0, 0, 0), (240, 250, 420, 200), 2)
                _temp_text = Screen.get_text_format(Screen.displayed_msg, 410, font4)
                screen_start1 = 350
                for _text in _temp_text:
                    surface1 = font4.render(_text, False, (0, 0, 0))
                    Screen.win.blit(surface1, (round(450 - surface1.get_rect().width / 2), round(screen_start1 - (len(_temp_text)) * 35 / 2)))
                    screen_start1 += 35

                if keysDown["esc"]:
                    Screen.is_displaying = False
                    continue
        # world
        elif Screen.state("world"):
            ##################################################  movement
            if keysDown[Ins.settings.sprint]:
                Ins.player.velocity = 1.5 * 360 / 60 * float(
                    console_choice_list["speed multiplier"][console_active_list["speed multiplier"]])
                Ins.player.sprinting = True
            if keysUp[Ins.settings.sprint]:
                Ins.player.velocity = 360 / 60
                Ins.player.sprinting = False
            if not Screen.current and not Screen.freeze_player:
                Ins.player.set_degree()
                Ins.player.move()
            else:
                Ins.player.degree = None
            Ins.player.position()
            ##################################################  background draw
            if not Screen.map_layer:
                for i in range(2):
                    render_map_blocks(Screen.selected_map, i, Screen.camera_x, Screen.camera_y)
            else:
                if Screen.selected_map[4][4]:
                    display_map()
                else:
                    Screen.win.blit(Screen.map_layer, (-round(Screen.camera_x), -round(Screen.camera_y)))
            if not Screen.freeze_player:
                try:
                    for [pos, goto, goto_pos] in Screen.selected_map[1]:
                        if pos in Ins.player.touching_blocks:
                            # Ins.player.x = goto_pos[0] * 64 + 32 - Ins.player.width / 2
                            # Ins.player.y = goto_pos[1] * 64 + 32 - Ins.player.height / 2
                            # Ins.player.position()
                            # Screen.select_map(goto)

                            animation("4", ["change_map", goto, goto_pos], ["unfreeze"])
                            error.error(error.Broken)
                except error.Broken:
                    Screen.freeze_player = True
            ##################################################  event 2
            for _passive in Ins.player.passive_list:
                globals()["fp_" + _passive]()
            ##################################################  entity draw

            ##################################################  draw above player
            render_map_blocks(Screen.selected_map, 2, Screen.camera_x, Screen.camera_y, True)
            if console_active_list["show fps"] == 1:
                surface1 = font5.render(str(int(Game.frame * 10) / 10), False, (0, 0, 0))
                Screen.win.blit(surface1, (5, -5))
            ##################################################  draw text
            if Screen.current_message_delay > 0 and not Screen.current:
                Screen.current_message_delay -= 1
            if not Screen.current and not Screen.freeze_player:
                for [pos, text, boolean] in Screen.selected_map[2]:
                    if pos in Ins.player.touching_blocks:
                        if Screen.current_message_delay <= 0:
                            surface2 = font3.render("press {} to interact".format(Ins.settings.interact), False, (255, 255, 255))
                            _temp_pos = (64 * Screen.screen_height - 100) if Ins.player.y + Screen.camera_y < 64 * Screen.screen_height - 150 else 55
                            pygame.draw.rect(Screen.win, (0, 0, 0), (int(64 * Screen.screen_width / 2 - surface2.get_rect().width / 2 - 15), _temp_pos, surface2.get_rect().width + 30, 45))
                            pygame.draw.rect(Screen.win, (255, 255, 255), (int(64 * Screen.screen_width / 2 - surface2.get_rect().width / 2 - 15), _temp_pos, surface2.get_rect().width + 30, 45), 1)
                            Screen.win.blit(surface2, (int(64 * Screen.screen_width / 2 - surface2.get_rect().width / 2), _temp_pos))
                        if keysDown[Ins.settings.interact] or boolean or mouseDown[1]:
                            keysDown[Ins.settings.interact] = True
                            Screen.current_message_delay = 20
                            Requires.text_update()

                            if Requires.text_overdo[text]:
                                if Requires.text_condition[text]:
                                    current_list = texts.text_list
                                else:
                                    current_list = texts.rejected_text_list
                            else:
                                current_list = texts.overdo_text_list
                            if current_list[text] == "none":
                                break
                            Screen.open_text(current_list[text], True)
                        break
            try:
                globals()["mp_ex_" + Screen.selected_map_str]()
            except KeyError:
                pass
            if Screen.current:
                Screen.show_text()
            if Screen.message_updated_active > 0:
                Screen.display_message()
            ##################################################  turns menu
            if Ins.player.random_encounter_variable >= Ins.player.random_encounter_next and Screen.selected_map[4][0] and console_active_list["random encounters"] == 0:
                _max_total = 0
                for _value in Screen.selected_map[4][2].values():
                    _max_total += _value
                _total = 0
                _rand_val = random.uniform(0, _max_total)
                for _key, _value in Screen.selected_map[4][2].items():
                    _total += _value
                    if _total >= _rand_val:
                        start_turns(_key)
                        break
                else:
                    error.error(error.TurnsError, 1)
            ##################################################  esc menu
            if keysDown["esc"] and not Screen.current and not Screen.freeze_player:
                Screen.message_updated_active = 0
                sounds.play_effect("effect3")
                Requires.scr_update()
                Screen.set_state("menu")
                Screen.menu_num = 1
                Screen.in_menu_num = 1
                Screen.inventory_roller_max = int(math.ceil(len(Ins.player.inventory) / 5) - 1)
                Screen.scroll_roller_max = (len(scrolls) - 1) // 3
                Screen.script_roller_max = (len(scripts) - 1) // 3
                Screen.inventory_roller = 0
                Screen.scroll_roller = 0
                Screen.script_roller = 0
                Screen.description_page = 0
                Screen.items_in_roller = 0
                Screen.is_question = False
                Screen.is_displaying = False
                Screen.displayed_msg = ""
                Screen.question_option = 0
                if Ins.ap.first["menuTab"]:
                    Ins.ap.first["menuTab"] = False
                    Screen.is_displaying = True
                    Screen.displayed_msg = "press tab to switch menus"
            ##################################################
            # if Screen.debug:
            #     if mouseHeld[1]:
            #         Ins.player.x = Screen.mouse_pos[0] - Ins.player.width / 2
            #         Ins.player.y = Screen.mouse_pos[1] - Ins.player.height / 2
        # cutscene
        elif Screen.state("cutscene"):
            try:
                for cmd in Screen.cutSceneFunc[Screen.cutSceneFrame]:
                    globals()["cs_" + cmd[0]](*cmd[1:])
            except KeyError:
                pass
            ##########################################
            for i in (0, 1):
                render_map_blocks(Screen.cutSceneMap, i, Screen.cutSceneCameraX, Screen.cutSceneCameraY)
            render_cutscene_frame(Screen.cutSceneList, Screen.cutSceneFrame, 1, Screen.cutSceneCameraX, Screen.cutSceneCameraY)
            render_map_blocks(Screen.cutSceneMap, 2, Screen.cutSceneCameraX, Screen.cutSceneCameraY)
            for j in (2, 3):
                render_cutscene_frame(Screen.cutSceneList, Screen.cutSceneFrame, j, Screen.cutSceneCameraX, Screen.cutSceneCameraY)

            if console_active_list["show fps"] == 1:
                surface1 = font5.render(str(int(Game.frame * 10) / 10), False, (0, 0, 0))
                Screen.win.blit(surface1, (5, -5))
            if Screen.cutSceneFrame >= Screen.cutSceneMaxFrame - 1 or Screen.cutSceneSkip >= 30:
                Screen.cutSceneSkip = 0
                if not Screen.cutSceneContinueSong:
                    sounds.play(Screen.map_song, True)

                Screen.resize(64*Screen.screen_width, 64*Screen.screen_height)
                pygame.display.set_caption(Screen.map_name)
                Screen.set_state("world")
            elif keysHeld["esc"]:
                pygame.draw.rect(Screen.win, (0, 0, 0), (10, 10, 70, 50))
                pygame.draw.rect(Screen.win, (255, 255, 255), (10, 10, 70, 50), 2)
                Screen.blit_text("skip", (24, 12), font7)
                pygame.draw.rect(Screen.win, (255, 255, 255), (15, 35, int(60 * Screen.cutSceneSkip / 30), 18))

                Screen.cutSceneSkip += 1
            else:
                Screen.cutSceneSkip = 0
            Screen.cutSceneFrame += 1
        # tutorial
        elif Screen.state("tutorial"):
            pygame.draw.rect(Screen.win, (110, 110, 110), (5, 5, 610, 320))
            for option in range(7):
                pygame.draw.rect(Screen.win, (80, 255, 80) if option == 3 else (80, 80, 80), (10, 10 + 45 * option, 600, 40))
                Screen.blit_text(textures.tutorial_list[(Screen.tutorial_index + option - 3) % len(textures.tutorial_list)], (15, 5 + 45 * option), font6, (0, 0, 0))
            ##############################
            _temp_tutorial_name = textures.tutorial_list[Screen.tutorial_index % len(textures.tutorial_list)]
            if keysDown[Ins.settings.interact]:
                sounds.play_effect("effect1")
                Screen.resize(textures.tutorial_dict[_temp_tutorial_name][0].get_rect().size)
                pygame.display.set_caption("{}: page 1/ {}".format(_temp_tutorial_name, len(textures.tutorial_dict[_temp_tutorial_name])))
                Screen.tutorial_page = 0
                Screen.set_state("tutorial_display")
            elif keysDown[Ins.settings.move_up]:
                sounds.play_effect("effect6")
                Screen.tutorial_index -= 1
            elif keysDown[Ins.settings.move_down]:
                sounds.play_effect("effect6")
                Screen.tutorial_index += 1

            if keysDown["esc"]:
                sounds.play_effect("effect9")
                Screen.is_displaying = False
                pygame.display.set_caption("menu")
                if Screen.tutorial_in_game:
                    Screen.set_state("menu")
                else:
                    Screen.set_state("mainMenu")
        # tutorial display
        elif Screen.state("tutorial_display"):
            _temp_tutorial_name = textures.tutorial_list[Screen.tutorial_index % len(textures.tutorial_list)]
            Screen.win.blit(textures.tutorial_dict[_temp_tutorial_name][Screen.tutorial_page], (0, 0))
            if (keysDown[Ins.settings.move_right] or keysDown[Ins.settings.interact]) and Screen.tutorial_page < len(textures.tutorial_dict[_temp_tutorial_name]) - 1:
                Screen.tutorial_page += 1
                sounds.play_effect("effect5")
                Screen.resize(textures.tutorial_dict[_temp_tutorial_name][Screen.tutorial_page].get_rect().size)
                pygame.display.set_caption(
                    "{}: page {}/ {}".format(_temp_tutorial_name, Screen.tutorial_page + 1, len(textures.tutorial_dict[_temp_tutorial_name])))
            elif keysDown[Ins.settings.interact] and Screen.tutorial_page == len(textures.tutorial_dict[_temp_tutorial_name]) - 1:
                sounds.play_effect("effect1")
                Screen.set_state("tutorial")
            elif (keysDown[Ins.settings.move_left] or keysDown[Ins.settings.other_function]) and Screen.tutorial_page > 0:
                Screen.tutorial_page -= 1
                sounds.play_effect("effect5")
                Screen.resize(textures.tutorial_dict[_temp_tutorial_name][Screen.tutorial_page].get_rect().size)
                pygame.display.set_caption("{}: page {}/ {}".format(_temp_tutorial_name, Screen.tutorial_page + 1, len(textures.tutorial_dict[_temp_tutorial_name])))
            if keysDown["esc"]:
                sounds.play_effect("effect1")
                Screen.set_state("tutorial")
        # turns
        elif Screen.state("turns"):
            Screen.win.blit(Turns.background, (0, 0))
            Screen.blit_text(f"hp: {max(int(Ins.player.hp), 0)}/{Ins.player.max_hp}", (12, 6), font7)

            pygame.draw.rect(Screen.win, (0, 0, 0), (8, 35, 230, 25))
            pygame.draw.rect(Screen.win, (80, 255, 80), (8, 35, int(230 * max(Ins.player.hp, 0) / Ins.player.max_hp), 25))
            pygame.draw.rect(Screen.win, (30, 30, 30), (8, 35, 230, 25), 3)

            Screen.blit_text(f"mana: {max(int(Ins.player.mana), 0)}/{Ins.player.max_mana}", (12, 62), font7)

            pygame.draw.rect(Screen.win, (0, 0, 0), (8, 90, 230, 25))
            pygame.draw.rect(Screen.win, (80, 80, 255), (8, 90, int(230 * max(Ins.player.mana, 0) / Ins.player.max_mana), 25))
            pygame.draw.rect(Screen.win, (30, 30, 30), (8, 90, 230, 25), 3)

            Animation.render_ff(-10)
            Turns.render_ff()
            Animation.render_ff(0)
            for enemy in Turns.Enemy.enemy_list:
                if enemy.is_turn:
                    enemy.render_ff()

            if len(Turns.alive_enemies) == 0:
                if len(list(filter(lambda x: x.is_alive, Turns.Enemy.enemy_list))) == 0:
                    if not Animation.name_exists("player_win"):
                        animation("0", 5, ["turns_battle_win"], None, name="player_win")

            i = 0
            for _effect in Battle.Effect.effect_list:
                if not _effect.target_player or _effect.name == "":
                    continue
                if _effect.max_frames == -1:
                    duration = "inf"
                else:
                    duration = str(_effect.max_frames - _effect.frames)
                Screen.blit_text(f"{_effect.name}: {duration}", (10, 118 + i), font7, _effect.color)
                i += 24

            if not Turns.enemy_turn:
                if Turns.picking_enemy == 4:  # wait for next turn
                    pass
                elif Turns.picking_enemy == 3:  # attack calculations
                    if not Animation.name_exists("attack"):
                        hp_list = get_hp_list()

                        _attack_list = list(Turns.player_selected_attack)
                        _weapon_boost = Turns.player_weapon_boost

                        #  Battle.attack_delay_list[_attack_list[0]] = _attack_list[8]

                        if _attack_list[7] != "":
                            if "-" not in _attack_list[7]:
                                sounds.play_effect(_attack_list[7])
                        if console_active_list["no delay"] == 0:
                            if Battle.selected_menu == 0:
                                Battle.attack_delay_list[_attack_list[0]] = _attack_list[9] + 1
                            elif Battle.selected_menu == 1:
                                Battle.attack_delay_list[_attack_list[0]] = _attack_list[9] + 1
                            elif Battle.selected_menu == 2:
                                Battle.attack_delay_list[_attack_list[0]] = _attack_list[9] + 1

                        Ins.player.add_mana(-1 * _attack_list[2])
                        _temp_attack_uniform = 0
                        _temp_critical = 0
                        healing_try = True
                        hit = False
                        player_effect = None
                        if _attack_list[5] != -1:
                            player_effect = _attack_list[5][2]
                        _target = Turns.alive_enemies if Turns.player_enemy_object is None else [Turns.player_enemy_object]
                        for enemy in _target:
                            temp_hp = int(enemy.hp)

                            if random.random() * (Ins.player.accuracy + 1) / (enemy.evasion + 1) >= _attack_list[3][1]:
                                hit = True
                                _is_crit = random.random() <= player_crit_rate(_attack_list[3][5][0])
                                _temp_critical = _attack_list[3][5][1] if _is_crit else 1
                                if _is_crit:
                                    animation("fadeText", "crit", (255, 80, 80), 4,
                                              point=(random.randint(enemy.x - 40, enemy.x + 40), random.randint(enemy.y - 40, enemy.y + 40)), layer=1)
                                _temp_attack_uniform = random.uniform(_attack_list[3][3][0], _attack_list[3][3][1])

                                _temp_damage = _temp_attack_uniform * _temp_critical \
                                               * lvl_amp_func(Ins.player.level, enemy.level, _attack_list[8]) * player_atk_amp(_attack_list, enemy)\
                                               * (_weapon_boost + 1) * atk_amp_func(Ins.player.attack, enemy.defense, _attack_list[8]) * _attack_list[3][0]
                                # elif _attack_list[8] == 1:
                                # _temp_damage *= 1
                                if _temp_damage > 0:
                                    final_damage = -1 * max(round(_temp_damage), random.randint(1, Ins.player.level // 10 + 1))
                                else:
                                    final_damage = -1 * round(_temp_damage)

                                enemy.add_hp(final_damage)
                                # if final_damage != 0:
                                #     animation("1", True, round(final_damage), 4, point=(enemy.x + random.randint(-40, 40), enemy.y + random.randint(-40, 40)), frozen=False, layer=1)

                                if healing_try:
                                    _temp_heal_uniform = random.uniform(_attack_list[3][4][0], _attack_list[3][4][1])
                                    _temp_heal = Ins.player.defense * _attack_list[3][2] * (Ins.player.level / 99 + 1) * _temp_heal_uniform
                                    if _temp_heal > 0:
                                        final_heal = max(round(_temp_heal), random.randint(0, int(Ins.player.level / 5 + 1)))
                                    else:
                                        final_heal = round(_temp_heal)
                                    Ins.player.add_hp(final_heal)
                                    # if round(final_heal) != 0:
                                        # animation("1", False, round(final_heal), 4, point=(237 + random.randint(-40, 40), 276 + random.randint(-40, 40)), frozen=False, layer=1)
                                    # if _attack_list[5] != -1:
                                        # Battle.Effect(*_attack_list[5], (_attack_list, _temp_attack_uniform, _temp_critical, _temp_heal_uniform, Turns.player_enemy_object))
                                        # damage, damage rand range, accuracy, heal, heal rand range

                                if player_effect is False:
                                    temp = Battle.Effect(*_attack_list[5], stored_data=[enemy])
                                    for _effect in enemy.effects:
                                        if _effect is temp:
                                            continue
                                        if _effect.name == temp.name:
                                            if temp.max_frames == -1 or _effect.max_frames == -1:
                                                _effect.max_frames = -1
                                            else:
                                                _effect.max_frames += temp.max_frames
                                            Battle.Effect.effect_list.remove(temp)
                                            break
                                    else:
                                        enemy.effects.append(temp)

                                if player_effect is True and healing_try:
                                    temp = Battle.Effect(*_attack_list[5], stored_data=_target)
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

                            else:
                                hit = False
                                animation("1", False, "miss", 4, point=(enemy.x + random.randint(-40, 40), enemy.y + random.randint(-40, 40)))

                            healing_try = False
                            try:
                                globals()["atk_fnc_p_" + _attack_list[0].replace(" ", "_")](enemy, hit)
                            except KeyError:
                                pass
                            try:
                                globals()["trn_hit_" + enemy.enemy_id](enemy, hit, temp_hp, _attack_list)
                            except KeyError:
                                pass

                        Turns.picking_enemy = 4
                        Animation.name_remove("attack_name")

                        animation("0", 15, ["start_turns"], None)
                        display_hp_list(hp_list)
                elif Turns.picking_enemy == 2:  # play animation
                    if Animation.name_object("player").info[0] == 0:
                        if Turns.player_enemy_object is False:
                            Turns.player_enemy_object = None
                        elif Turns.player_enemy_object is True:
                            Turns.player_enemy_object = random.choice(Turns.alive_enemies)

                        if Turns.player_selected_attack[10] != -1 and "-" not in Turns.player_selected_attack[10]:
                            if Turns.player_enemy_object is None:
                                temp = True
                                for enemy in Turns.alive_enemies:
                                    if temp:
                                        animation(f"aa-{Turns.player_selected_attack[10]}", (237, 276), name="attack", point=(enemy.x, enemy.y), reference=enemy)
                                        temp = False
                                    else:
                                        animation(f"aa-{Turns.player_selected_attack[10]}", (237, 276), point=(enemy.x, enemy.y), reference=enemy)
                            else:
                                animation(f"aa-{Turns.player_selected_attack[10]}", (237, 276), name="attack", point=(Turns.player_enemy_object.x, Turns.player_enemy_object.y), reference=Turns.player_enemy_object)

                        Turns.picking_enemy = 3
                elif Turns.picking_enemy == 1:  # enemy pick
                    if not isinstance(Turns.player_enemy_object, bool):
                        _temp = Turns.player_enemy_object
                        pygame.draw.rect(Screen.win, (255, 255, 255), (
                        _temp.x - _temp.w // 2 - 10, _temp.y - _temp.h // 2 - 10, _temp.w + 20, _temp.h + 20), 3)

                    if not Turns.pause:
                        if keysDown[Ins.settings.battle_confirm]:
                            Animation.name_object("player").info[0] = Turns.player_selected_attack[6] + 1
                            Animation.name_object("player").info[1] = 0
                            animation("3", Turns.player_selected_attack[0], Turns.player_selected_attack[1], name="attack_name")
                            Turns.picking_enemy = 2

                            if Turns.player_selected_attack[10] != -1 and "-" in Turns.player_selected_attack[10]:
                                temp_anm = Turns.player_selected_attack[10].split("-")

                                if Turns.player_enemy_object is None:
                                    temp = True
                                    for enemy in Turns.alive_enemies:
                                        if temp:
                                            animation("0", int(temp_anm[0]),
                                                      ["animation", [f"aa-{'-'.join(temp_anm[1:])}", (237, 276)],
                                                       {"name": "attack", "point": (enemy.x, enemy.y),
                                                        "reference": enemy}], None)
                                            temp = False
                                        else:
                                            animation("0", int(temp_anm[0]),
                                                      ["animation", [f"aa-{'-'.join(temp_anm[1:])}", (237, 276)],
                                                       {"point": (enemy.x, enemy.y), "reference": enemy}], None)
                                else:
                                    animation("0", int(temp_anm[0]),
                                              ["animation", [f"aa-{'-'.join(temp_anm[1:])}", (237, 276)],
                                               {"name": "attack", "point": (Turns.player_enemy_object.x, Turns.player_enemy_object.y), "reference": Turns.player_enemy_object}],
                                              None)

                            if "-" in Turns.player_selected_attack[7]:
                                temp = Turns.player_selected_attack[7].split("-")
                                animation("0", int(temp[0]), ["sound_effect", '-'.join(temp[1:])], None)

                        elif not isinstance(Turns.player_enemy_object, bool):
                            if keysDown[Ins.settings.move_right] or keysDown[Ins.settings.move_up]:
                                Turns.player_selected_enemy += 1
                                Turns.player_selected_enemy %= len(Turns.Enemy.enemy_list)
                                while Turns.Enemy.enemy_list[Turns.player_selected_enemy] not in Turns.alive_enemies:
                                    Turns.player_selected_enemy += 1
                                    Turns.player_selected_enemy %= len(Turns.Enemy.enemy_list)
                                Turns.player_enemy_object = Turns.Enemy.enemy_list[Turns.player_selected_enemy]
                            elif keysDown[Ins.settings.move_left] or keysDown[Ins.settings.move_down]:
                                Turns.player_selected_enemy -= 1
                                Turns.player_selected_enemy %= len(Turns.Enemy.enemy_list)
                                while Turns.Enemy.enemy_list[Turns.player_selected_enemy] not in Turns.alive_enemies:
                                    Turns.player_selected_enemy -= 1
                                    Turns.player_selected_enemy %= len(Turns.Enemy.enemy_list)
                                Turns.player_enemy_object = Turns.Enemy.enemy_list[Turns.player_selected_enemy]
                        if keysDown[Ins.settings.battle_switch_menu]:
                            Turns.picking_enemy = 0

                    Screen.blit_text(f"press {Ins.settings.battle_switch_menu} to go back",
                                     (3, Screen.window_height - 3), align=(0, 1))
                elif Turns.picking_enemy == 0:  # action pick
                    pygame.draw.rect(Screen.win, (0, 0, 0, 0), (5, Screen.window_height - 200, 300, 195))
                    if Battle.selected_battle_menu == 0:
                        Screen.blit_text("attacks:", (10, 380), font5)
                        Screen.blit_text("normal attacks:", (10, 406), font5)
                        txt = "{}: {}".format(attacks[Battle.selected_weapon_attack][0], attacks[Battle.selected_weapon_attack][2])
                        Screen.blit_text(txt, (10, 432), font5, (80, 255, 80) if Battle.selected_menu == 0 else (255, 255, 255))
                        Screen.blit_text("script attacks:", (10, 458), font5)
                        txt = "{}: {}".format(scripts[Ins.player.script][2][Battle.selected_script_attack][0], scripts[Ins.player.script][2][Battle.selected_script_attack][2])
                        Screen.blit_text(txt, (10, 484), font5, (80, 255, 80) if Battle.selected_menu == 1 else (255, 255, 255))
                        Screen.blit_text("scroll attacks:", (10, 510), font5)
                        txt = "{}: {}".format(scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack][0], scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack][2])
                        Screen.blit_text(txt, (10, 536), font5, (80, 255, 80) if Battle.selected_menu == 2 else (255, 255, 255))

                        # _attack_list = ["", (0, 0, 0), 0, [0, 0, 0, [0, 0], [0, 0]], -1, -1, 0]
                        # if Battle.selected_menu == 0:
                        #     _attack_list = attacks[Battle.selected_weapon_attack]
                        # elif Battle.selected_menu == 1:
                        #     _attack_list = scripts[Ins.player.script][2][Battle.selected_script_attack]
                        # elif Battle.selected_menu == 2:
                        #     _attack_list = scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack]
                    elif Battle.selected_battle_menu == 1:
                        Screen.blit_text("inventory:", (10, 380), font4)
                        _counter = 0
                        for _item in Ins.player.battle_inventory:
                            for [_item2, _amount] in Ins.player.inventory:
                                if _item == _item2:
                                    Screen.blit_text("{}: {} ".format(_item, _amount), (10, 415 + 30 * _counter), font5, (80, 255, 80) if Battle.selected_battle_item == _counter else (255, 255, 255))
                                    _counter += 1
                                    break

                    else:
                        surface1 = font4.render("class actions:", False, (255, 255, 255))
                        Screen.win.blit(surface1, (10, 380))

                        _counter = 0
                        for _class_attack in player_classes[Ins.player.playerClass][2]:
                            if globals()["cat_con_"+player_classes[Ins.player.playerClass][0].replace(" ", "_")](Turns, _counter):
                                if _counter == Battle.selected_battle_class:
                                    _color = (80, 255, 80)
                                else:
                                    _color = (255, 255, 255)
                            else:
                                if _counter == Battle.selected_battle_class:
                                    _color = (120, 120, 120)
                                else:
                                    _color = (80, 80, 80)

                            surface1 = font4.render(f"{_class_attack}", False, _color)
                            _counter += 1
                            Screen.win.blit(surface1, (10, 380 + 35 * _counter))

                    if not Turns.pause:
                        if keysDown[Ins.settings.battle_switch_menu]:
                            Battle.selected_battle_menu = (Battle.selected_battle_menu + 1) % 3

                        if Battle.selected_battle_menu == 0:
                            if keysDown[Ins.settings.battle_func1]:
                                if Battle.selected_menu == 0:
                                    Battle.selected_weapon_attack += 1
                                    if Battle.selected_weapon_attack == 1 and Ins.player.sword is None:
                                        Battle.selected_weapon_attack += 2
                                    if Battle.selected_weapon_attack == 3 and Ins.player.bow is None:
                                        Battle.selected_weapon_attack += 2
                                    if Battle.selected_weapon_attack == 5 and Ins.player.staff is None:
                                        Battle.selected_weapon_attack += 2
                                    if Battle.selected_weapon_attack >= 7:
                                        Battle.selected_weapon_attack = 0
                                else:
                                    Battle.selected_menu = 0
                            elif keysDown[Ins.settings.battle_func2]:
                                if Ins.player.script is not None:
                                    if Battle.selected_menu == 1:
                                        Battle.selected_script_attack += 1
                                        if len(scripts[Ins.player.script][2]) <= Battle.selected_script_attack:
                                            Battle.selected_script_attack = 0
                                    else:
                                        Battle.selected_menu = 1
                            elif keysDown[Ins.settings.battle_func3]:
                                if Ins.player.scroll is not None:
                                    if Battle.selected_menu == 2:
                                        Battle.selected_scroll_attack += 1
                                        if len(scrolls[Ins.player.scroll][2]) <= Battle.selected_scroll_attack:
                                            Battle.selected_scroll_attack = 0
                                    else:
                                        Battle.selected_menu = 2
                        elif Battle.selected_battle_menu == 1:
                            _temp_len = len(Ins.player.battle_inventory)
                            if keysDown[Ins.settings.battle_func1] and _temp_len >= 1:
                                Battle.selected_battle_item = 0
                            if keysDown[Ins.settings.battle_func2] and _temp_len >= 2:
                                Battle.selected_battle_item = 1
                            if keysDown[Ins.settings.battle_func3] and _temp_len >= 3:
                                Battle.selected_battle_item = 2
                        else:
                            _temp_len = len(player_classes[Ins.player.playerClass][2])
                            if keysDown[Ins.settings.battle_func1] and _temp_len >= 1:
                                Battle.selected_battle_class = 0
                            if keysDown[Ins.settings.battle_func2] and _temp_len >= 2:
                                Battle.selected_battle_class = 1
                            if keysDown[Ins.settings.battle_func3] and _temp_len >= 3:
                                Battle.selected_battle_class = 2

                        # TODO: make thing do stuff (battle damage idiot)
                        if keysDown[Ins.settings.battle_confirm]:
                            if Battle.selected_battle_menu == 0:
                                _attack_list = ["", (0, 0, 0), 0, [0, 0, 0, [0, 0], [0, 0]], -1, -1, 0]

                                _delay_over = True
                                if Battle.selected_menu == 0:
                                    _attack_list = attacks[Battle.selected_weapon_attack]
                                elif Battle.selected_menu == 1:
                                    _attack_list = scripts[Ins.player.script][2][Battle.selected_script_attack]
                                elif Battle.selected_menu == 2:
                                    _attack_list = scrolls[Ins.player.scroll][2][Battle.selected_scroll_attack]

                                if _attack_list[0] in Battle.attack_delay_list:
                                    _delay_over = Battle.attack_delay_list[_attack_list[0]] <= 0
                                else:
                                    Battle.attack_delay_list[_attack_list[0]] = 0
                                    _delay_over = True

                                _is_weapon = False
                                _weapon_boost = 0
                                if _attack_list[6] == 0:
                                    _is_weapon = True
                                elif _attack_list[6] == 1 and Ins.player.sword is not None:
                                    _is_weapon = True
                                    _weapon_boost = items[Ins.player.sword][13]
                                elif _attack_list[6] == 2 and Ins.player.bow is not None:
                                    _is_weapon = True
                                    _weapon_boost = items[Ins.player.bow][13]
                                elif _attack_list[6] == 3 and Ins.player.staff is not None:
                                    _is_weapon = True
                                    _weapon_boost = items[Ins.player.staff][13]

                                if Ins.player.mana >= _attack_list[2] and _is_weapon and _delay_over:
                                    Turns.player_weapon_boost = _weapon_boost
                                    Turns.player_selected_attack = list(_attack_list)
                                    Turns.picking_enemy = 1
                                    if _attack_list[4][0] == 1:
                                        Turns.player_enemy_object = False
                                    elif _attack_list[4][0] == 2:
                                        Turns.player_enemy_object = True
                                    else:
                                        while Turns.Enemy.enemy_list[Turns.player_selected_enemy] not in Turns.alive_enemies:
                                            Turns.player_selected_enemy -= 1
                                            Turns.player_selected_enemy %= len(Turns.Enemy.enemy_list)
                                        Turns.player_enemy_object = Turns.Enemy.enemy_list[Turns.player_selected_enemy]
                                else:
                                    sounds.play_effect("effect4")
                            elif Battle.selected_battle_menu == 1:
                                if len(Ins.player.battle_inventory) >= 1:
                                    _temp_item_list = Ins.player.battle_inventory[Battle.selected_battle_item]
                                    Ins.player.add_hp(items[_temp_item_list][4])
                                    Ins.player.add_mana(items[_temp_item_list][5])
                                    for _passive in items[_temp_item_list][8]:
                                        globals()["ap_" + _passive]()
                                    if Ins.player.add_item(_temp_item_list, -1) == 1:
                                        if len(Ins.player.battle_inventory) <= Battle.selected_battle_item:
                                            Battle.selected_battle_item -= 1
                                            if Battle.selected_battle_item <= -1:
                                                Battle.selected_battle_item = 0

                                    animation("0", 15, ["start_turns"], None)
                                    Turns.picking_enemy = 4
                                else:
                                    sounds.play_effect("effect4")
                            else:
                                # TODO: add more stuff here (?)
                                if globals()["cat_con_" + player_classes[Ins.player.playerClass][0].replace(" ", "_")](True, Battle.selected_battle_class):
                                    hp_list = get_hp_list()
                                    globals()["cat_act_" + player_classes[Ins.player.playerClass][0].replace(" ", "_")](True, Battle.selected_battle_class)
                                    display_hp_list(hp_list)
                                    #animation("0", 15, ["start_turns"], None)
                                    #Turns.picking_enemy = 4
                                else:
                                    sounds.play_effect("effect4")

            if keysDown["esc"]:
                Turns.pause = not Turns.pause

            Animation.render_ff()
            Particles.render_ff()
            if Turns.pause:
                surface1 = pygame.Surface((Screen.window_width, Screen.window_height))
                surface1.set_alpha(int(110))
                surface1.fill((0, 0, 0))
                Screen.win.blit(surface1, (0, 0))

                Screen.blit_text("give up", (Screen.window_width // 2, Screen.window_height // 2), font, (80, 255, 80), (0.5, 0.5))

                if keysDown[Ins.settings.interact] or keysDown[Ins.settings.battle_confirm]:
                    Battle.Effect.list_reset()
                    sounds.play("death_song", loops=0)
                    Screen.set_state("death")
                    animation("2")
                    Screen.afterBattleScreenVar = 0
                    Screen.afterBattleFrame = 0

            # if keysDown["i"]:
            #     Turns.proceed_turn()

            # for i in range(5):
            #     if keysDown["num"+str(i)]:
            #         Animation.name_object("player").info[0] = i
            #         Animation.name_object("player").info[1] = 0
        # quit program
        elif not Screen.run:
            break
        else:
            error.error(error.StateCode, 1)
        ##################################################  global code
        if Screen.debug:
            if keysDown["c"]:
                start_turns("berserker")
            if keysDown["z"]:
                print(Screen.mouse_pos)
            if keysDown["x"]:
                Battle.enemy_hp = 0
                for enemy in Turns.Enemy.enemy_list:
                    enemy.hp = 0
            if keysDown["0"]:
                print(Ins.player.x, Ins.player.y)
            if keysDown["m"]:
                Ins.player.add_item("bandage")
            if keysDown["k"]:
                Ins.player.add_exp(1)
                Ins.player.add_exp(Ins.player.exp)
            if keysDown["u"]:
                particles("circle", [7, 11], [200, 230, 80, 20, 20, 20], [Screen.mouse_pos[0], Screen.mouse_pos[1], 7], 40, 8, "all", 4, 2, gravity=0, beginning_func="rand_decay_fade", exist_func=[["friction", 0.8]])
            if keysDown["b"]:
                Ins.stats.monsters_killed += 1
            if keysDown["o"]:
                start_battle(2)
            if keysDown["p"]:
                start_turns("test")
            if keysDown["y"]:
                print(Battle.Sprite.x, Battle.Sprite.y)
            if keysDown["h"]:
                start_cut_scene("aa")
            if keysHeld["right"]:
                Battle.current_battle_frame = 1600

        Animation.render_ff()
        if not Particles.rendered:
            Particles.render_ff()
        ##################################################  update screen
        pygame.display.flip()


if __name__ == "__main__":
    main()

pygame.quit()
quit()
