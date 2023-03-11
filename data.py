import pygame

"""
fix saving while text boxes - nope
fix battle attacks condition hitboxes

change class attacks to normal attacks with functions (?) - nah
add boss fight attack hitboxes
announce crits -- done

balacnce LP and stats

next addition in queue:
change all | lines seperators to automatic -- done?
add item consume and class actions -- done?
fix sound problem when getting items from win -- done

finish jessica shop

replace all text blitters with function -- lmao fuck off im not doing that
finish fixing cutscene generator for camera movement and check for bugs -- done?

change game balace? -- lazy ass lazy bitch do that after finishing mainter
turns battle system -- LMAO fucking idiot
turns battle editor?? (inside other editor? (no)) 
import classes into generators (finished? yes)
fix width and window_width -- nah fam its good enough

class leveling (?) nope

better auto saves (?) nope

add depth (ex: chair will be above you when you walk behind it and below it when you are in front of it) (???) -- done
add infinite layer options for maps (???) -- nope

test new battle hitbox system -- done?
----notes:

very plausible for mission system to be bugged, keep an eye out
settings will include: music volume, keyboard keys, option to hide unsellable items in shops, more, toggle auto save
AUTO SAVES

view other games for addition ideas
----------
when finishing all of the above add a fuck ton of content you lazy fuck, 
if you think of having less than 5 hours of gameplay i swear to god you 
are gonna fucking get it deep inside your ass. you wont know from where it hit ya. -- sadly it won't :'(, i need to finish up by feb
add stats menu --- done, looks bad, maybe will be changed - nope
add screen for continuing the game -- maybe changed
add death screen - exit game return to last save ----- add saving options - added

add sex :)
"""
pygame.init()
if True:
    #  fonts
    if True:
        font = pygame.font.SysFont("Aharoni", 36)
        font2 = pygame.font.SysFont("Algerian", 48)
        font3 = pygame.font.SysFont("Agency FB", 30)
        font4 = pygame.font.SysFont("Cooper Black", 30)
        font5 = pygame.font.SysFont("Cooper Black", 26)
        font6 = pygame.font.SysFont("Cooper Black", 36)
        font7 = pygame.font.SysFont("Aharoni", 22)
        font8 = pygame.font.SysFont("Aharoni", 16)
        font9 = pygame.font.SysFont("Agency FB", 24)

    #  constants
    if True:
        PI = 3.141592653589793

#  hp, max hp, mana, max mana, attack, defense, level, accuracy, evasion
#  name: [desc, plural, stat_boost_desc, {0: cosmetic, 1: consumable - boost, 2: consumable - perm stat boost, 3: wearable - head, 4: wearable - chest, 5: wearable - legs, 6: wearable - accessory, 7: holdable - sword, 8: holdable - bow, 9: holdable - staff 10: talisman, 11: cursed relic},
#  4 -> ,hp1+, mana1+, exp/exp_boost1+, required_level1+, attack2+/passive=[equip function], defense2+, evasion2+, accuracy2+, passive3+=[equip function, equipped passive, unequip function], attack/defense_booster3,4,5,7,8,9]
# Attacker.attack / (Defender.defense + 1) * attack_modifier * crit_multiplier * (level/66 +0.75) * attack_random_multiplier * (0 if accuracy_modifier * (Attacker.accuracy + 1) / (Defender.evasion + 1) < random.random() else 1) * (weapon_boost + 1) if player is attacker else (1 - armor_defense)
# Attacker.defense * health.modifier * (level/99 + 1) * heal_random_multiplier
items = {
    "apple": ["", "apples", "restores 5 hp", 1, 5, 0, 0, 0, []],
    "goblin hat": ["", "goblin hats", "a hat that once belonged to a goblin, +4 hp, +1 attack, +2 defense and +2 evasion. level 3", 3, 4, 0, 0, 3, 1, 2, 2, 0, [[], [], []], 0],
    "goblin dagger": ["", "goblin daggers", "the dagger of a leader goblin. +4 attack +3 evasion level 5. +7% damage when used", 7, 0, 0, 0, 5, 4, 0, 3, 0, [[], [], []], 0.07],
    "bat eye": ["", "bat eyes", "the eye of a bat. said to have some nurturemental value. +2 hp, +4 mana. level 1", 1, 2, 4, 0, 1, []],
    "slime core earing": ["", "slime core earings", "an accessory thats made from the core of a slime, +6 hp +3 mana", 6, 6, 3, 0, 3, 0, 0, 0, 0, [[], [], []]],

    "skeleton contract": ["", "skeleton contracts", "the skeleton contracts used for summoning a skeleton, +4 attack, +3 accuracy, -4 defense. level 6", 11, 0, 0, 0, 6, 4, -4, 0, 3, [[], [], []]],
    "wizard staff": ["", "wizard staves", "a staff that is usually given to wizards by their master, +6 mana, +5 atk, +3 accuracy +15% magic damage. level 6", 9, 0, 6, 0, 6, 5, 0, 0, 3, [[], [], []], 0.15],
    "swordsman cape": ["", "swordsman capes", "the cape of a dark swordsman. it is made by high quality fabric and is enchanted\n+4 hp, +6 defense, +3 evasion, 15% defense factor. level 7", 4, 4, 0, 0, 7, 0, 6, 3, 0, [[], [], []], 0.15],
    "sigil of permission": ["lvl 1", "", "a badge of acceptance by the kingdom of mainter", 0],
    "iron plated leggings": ["", "iron plated leggings", "a normal pair of leggings made out of iron. +5 defense, +3 accuracy. level 2", 5, 0, 0, 0, 2, 0, 5, 0, 3, [[], [], []], 0.2],

    "bracelet of aid": ["", "bracelets of aid", "mana +5, accuracy +5. level 2", 6, 0, 4, 0, 2, 0, 0, 0, 3, [[], [], []]],
    "rusty sword": ["", "rusty swords", "a sword that hadn't been in use for years. +2 attack, +2 accuracy +3% attack bonus. level 1", 7, 0, 0, 0, 1, 2, 0, 0, 2, [[], [], []], 0.03],
    "iron bow": ["", "iron bows", "a mass produced iron bow that is usually given to soldiers. +3 atk +1 defense, +3 accuracy. level 3", 8, 0, 0, 0, 3, 3, 1, 0, 3, [[], [], []], 0.06],
    "holy badge": ["", "holy badges", "a talisman with unknown origins that was stored in the mainter treasury.\n +6 mana, +5 evasion, +10% exp gain, +25% mana regen (in encounters). level 7", 10, 0, 6, 0.1, 7, 0, 0, 5, 0, [[], ["mana_regen1"], []]],
    "wooden staff": ["", "wooden staves", "a staff of the lowest tier. +4 mana, +3 attack, +6% magic damage. level 2", 9, 0, 4, 0, 2, 3, 0, 0, 0, [[], [], []], 0.06],

    "bandage": ["", "bandages", "used on wounds to prevent blood from flowing out. restore 18 hp level 4", 1, 18, 0, 0, 4, []],
    "worn out sword": ["", "", "a sword so old it cant be used as a weapon. it have some history but who knows...", 0],
    "angled bow": ["", "angled bows", "a bow made by a special craftsman that has a alight edge to it to improve arrow speed.\n +6 evasion +7 damage, +4 mana, +10% bow damage level 8", 8, 0, 4, 0, 8, 7, 0, 6, 0, [[], [], []], 0.1],
    "steel layered chestplate": ["", "steel layered chestplates", "an amrmor made from armor with an outside layer of steel. +9 defense, +4 hp, 12% defense factor. level 8", 4, 4, 0, 0, 8, 0, 9, 0, 0, [[], [], []], 0.12],
    "maximized potion": ["", "maximized potions", "a potion made by a revered alchemist. restores 50% of missing hp and mana (up to 80/40) increases damage by 25% for 3 turns. level 10\nconsuming outside a battle does not give attack effect", 1, 0, 0, 0, 10, ["attack_boost1"]],

    "attack peanut": ["", "attack peanuts", "special peanuts grown on a far land. permanently increase +0.5 attack and a 1% damage boost. level 10", 2, 0, 0, 0, 10, 0.5, 0, 0, 0, [["one_percent_boost"], []]],
    "small mana potion": ["", "small mana potions", "a mana potion that can be produced by your average alchemist. restores 20 mana. level 8", 1, 0, 20, 0, 8, []],
    "dwarven sword": ["", "", "a sword made by dwarves. high quality. +10 attack, +10 hp, +5 defense. increases all damage by 10% and +18% damage when used. level 16", 7, 10, 0, 0, 16, 10, 5, 0, 0, [["ten_percent_boost"], [], ["ten_percent_boost"]], 0.18],
    "safety pin": ["", "safety pins", "given to important figures to keep them safe, but somehow it has found its way over here...\n+12 hp, +6 defense, +6 evasion. level 13", 6, 10, 0, 0, 13, 0, 6, 6, 0, [[], [], []]],
    "stylish pants": ["", "", "pants made by a famous designer with both style and protection in mind.\n+5 evasion, +5 accuracy, +5 defense, +5 mana, +10% exp gain, 20% defense factor. level 14", 5, 0, 5, 0.1, 14, 0, 5, 5, 5, [[], [], []], 0.2],

    "jeweled staff": ["", "", "a staff embedded with many jewels.\n+8 damage, +12 mana, +20% damage when used. level 15", 9, 0, 12, 0, 15, 8, 0, 0, 0, [[], [], []], 0.2],
    "demonic blood vial": ["", "", "a small bottle with a bit of demonic blood. +6 damage, -4 defense, +6 accuracy, -4 evasion, +4 mana. level 14", 11, 0, 4, 0, 14, 6, -4, -4, 6, [[], [], []]],
}

#  script / scroll id: [name, desc, [*attacks=[0name, 1color, 2mana_cost, 3[attack_modifier, accuracy_modifier, healing_modifier,
#  [rand_atk_min, rand_atk_max], [rand_hp_min, rand_atk_max], [crit_chance, crit_multiplier]], 4[turns_attack, battle_area=*[x_start, y_start, width, height]], # 0 - choose, 1 - all enemies, 2 - random enemy,
#  5effect=[name, effect_time, is_targeting_player, add_effect, exist_effect, remove_effect,, color], 6weapon_type, 7sound_effect, 8attack type, 9attack delay, 10attack_animation]]
#  as closer accuracy modifier is to 1 the more dodges there are (range = 0 to 1)
scrolls = {
    None: ["none-scroll", "none", [["none1", (50, 50, 50), 0]]],
    1: ["common scroll", "scroll used in the day to day lifestyle of general adults\ncontains: purify, heal\npurify: high damage for one foe. costs 12 mana, has a 2 turns cooldown\nheal: restore hp. has a 2 turns cooldown",
        [["purify", (200, 230, 80), 16, [1.2, 0.05, 0, [0.95, 1.05], [0, 0], [0.2, 1.35]], [0, [95, 290, 400, 100]], -1, 3, "magic4", 0, 2, "purify1"],
        ["heal", (120, 255, 120), 8, [0, 0, 0.5, [0, 0], [0.9, 1.2], [0, 0]], [1], -1, 3, "heal1", 0, 2, "heal1"]]],
    2: ["supporter scroll", "scroll used by priests to help their party in battle.\nstats boost: boost all stats by 15% and increase critical rate for 3 turns. 5 turns cooldown\n"
                            "area purify: purify all enemies. 3 turns cooldown\nstats debuff: reduce all stats by 15% for a single enemy for 4 turns. 5 turns cooldown\nregeneration: restore hp and gain a regeneration effect for 2 turns",
        [["stats boost", (230, 40, 40), 15, [0, 0, 0, [0, 0], [0, 0], [0, 0]], [1], ["stat boost", 3, True, "statBoost1", "none", "statBoost1", (230, 40, 40)], 3, "magic2", 0, 5, -1],
         ["stats debuff", (30, 30, 130), 15, [0, 0, 0, [0, 0], [0, 0], [0, 0]], [0], ["stat debuff", 3, False, "statDebuff1", "none", "statDebuff1", (30, 30, 130)], 3, "magic8", 0, 5, -1],
         ["area purify", (220, 250, 100), 25, [1, 0.05, 0, [0.95, 1.05], [0, 0], [0.2, 1.35]], [1, [145, 315, 300, 75]], -1, 3, "magic4", 0, 3, "purify1"],
         ["regeneration", (140, 255, 140), 20, [0, 0, 0.6, [0, 0], [0.9, 1.1], [0, 0]], [1], ["regeneration", 2, True, "none", "regeneration1", "regeneration1", (140, 255, 140)], 3, "heal1", 0, 3, "heal1"]]]
}

scripts = {
    None: ["none-script", "none", [["none2", (50, 50, 50), 0]]],
    1: ["common script", "script used in the day to day lifestyle of general adults\nblind sweep: attack a random enemy with a high chance to miss but deal a lot of damage and have a high crit value, 1 turn cooldown\nwide shot: shoot all enemies with low chance of missing 1 turn delay" +
        "\nsword charge: attack an enemy with all your might. 1 turn cooldown",
        [["blind sweep", (150, 150, 150), 5, [0.975, 0.45, 0, [0.8, 1.12], [0, 0], [0.3, 1.4]], [2, [0, 0, 75, 390], [0, 0, 590, 75], [515, 0, 75, 390]], -1, 1, "slash1", 0, 1, -1],
         ["wide shot", (190, 160, 160), 5, [0.6, 0.02, 0, [0.9, 1.1], [0, 0], [0.1, 1.3]], [1, [0, 190, 590, 200]], -1, 2, "arrow1", 0, 1, "arrow1"],
        ["sword charge", (160, 190, 160), 5, [0.85, 0.06, 0, [1, 1.05], [0, 0], [0.05, 1.5]], [0, [195, 0, 200, 390]], -1, 1, "stab1", 0, 1, -1]]],
    2: ["samurai teachings", "a scroll passed by samurais from one to another.\n"
                "ground slash: attack all enemies at once, 2 turns cooldown\nattack stance: deal 60% more damage next turn 2 turns cooldown\ndeath slash: deal big damage to a single enemy 3 turns cooldown\ndefense stance: reduce incoming damage by 30% for 3 turns, 4 turns cooldown",
        [["ground slash", (200, 200, 200), 15, [0.85, 0.08, 0, [0.9, 1.1], [0, 0], [0.2, 1.25]], [1, [0, 145, 590, 100], [220, 0, 150, 390]], -1, 1, "slash1", 0, 2, "slash1"],
         ["death slash", (230, 230, 230), 30, [1.6, 0.04, 0, [1, 1.05], [0, 0], [0.1, 1.35]], [0, [145, 0, 300, 75]], -1, 1, "slash1", 0, 3, "samuraiSlash"],
         ["attack stance", (200, 100, 100), 10, [0, 0, 0, [0, 0], [0, 0], [0, 0]], [1], ["attack stance", 1, True, "stance1", "none", "stance1", (200, 100, 100)], 0, "none", 0, 2, -1],
         ["defense stance", (50, 50, 200), 10, [0, 0, 0, [0, 0], [0, 0], [0, 0]], [1], ["defense stance", 3, True, "stance2", "none", "stance2", (50, 50, 200)], 0, "none", 0, 4, -1]]]
}

# ["", (0, 0, 0), 0, [0, 0, 0, [0, 0], [0, 0], [0, 1]], [0], -1, 0, "none", 0, 0, -1],
# 0 - hands, 1 - sword, 2 - bow, 3 - staff
attacks = [  # 400 -> 0.4
    ["fist attack", (150, 150, 150), 0, [0.4, 0, 0, [0.86, 1.1], [0, 0], [0.15, 1.25]], [0, [0, 0, 590, 390]], -1, 0, "effect1", 0, 0, -1],
    ["light sword attack", (150, 150, 150), 0, [0.4, 0.05, 0, [0.98, 1.02], [0, 0], [0.2, 1.2]], [1], -1, 1, "effect1", 0, 0, -1],
    ["heavy sword attack", (150, 150, 150), 0, [0.6, 0.1, 0, [0.95, 1.05], [0, 0], [0.2, 1.2]], [0, [0, 0, 590, 150]], -1, 1, "effect1", 0, 0, -1],
    ["light bow attack", (150, 150, 150), 0, [0.4, 0.05, 0, [0.7, 1.3], [0, 0], [0.15, 1.25]], [1], -1, 2, "effect1", 0, 0, -1],
    ["heavy bow attack", (150, 150, 150), 0, [0.65, 0.1, 0, [0.70, 1.3], [0, 0], [0.05, 1.55]], [0, [0, 240, 590, 150]], -1, 2, "effect1", 0, 0, -1],
    ["light staff attack", (150, 150, 150), 2, [0.45, 0.05, 0, [0.95, 1.05], [0, 0], [0.15, 1.25]], [1], -1, 3, "effect1", 0, 0, -1],
    ["heavy staff attack", (150, 150, 150), 4, [0.7, 0.1, 0, [0.90, 1.1], [0, 0], [0.15, 1.25]], [0, [145, 95, 300, 200]], -1, 3, "effect1", 0, 0, -1],
]

console_list = ["show hitbox", "infinite health", "infinite mana", "no delay", "no clip", "speed multiplier", "random encounters", "show direction", "show fps"]
console_choice_list = {
    "show hitbox": ["false", "true"],
    "infinite health": ["false", "true"],
    "infinite mana": ["false", "true"],
    "no delay": ["false", "true"],
    "no clip": ["false", "true"],
    "speed multiplier": [1, 2, 3, 5],
    "random encounters": ["on", "off"],
    "show direction": ["false", "true"],
    "show fps": ["false", "true"],
}
console_active_list = {
    "show hitbox": 0,
    "infinite health": 0,
    "infinite mana": 0,
    "no delay": 0,
    "no clip": 0,
    "speed multiplier": 0,
    "random encounters": 0,
    "show direction": 0,
    "show fps": 0,
}

# [map_name, entry_location, screen_name, unlock on entry]
travel_list = [
    ["ma_capital", (8, 12), "mainter capital", True],
    ["ma_river", (15, 10), "mainter river", False],
    ["sp_entrance", (14, 1), "spludit entrance", True]
]

# [mission_name, main mission]
mission_list = [["the exterminator", True], ["anniversary gift", False], ["sailing skeleton", True], ["berserker duel", False], ["a shop for the worthy", True], ["a lost priestess", False]]
# *mission_name: [[*mission_directions], reward description, reward=[exp, coins, [*commands]]]
mission_stats_list = {
    "the exterminator": [["exit your house", "talk to the guard at the entrance of the hill at the west of the capital", "reach level 3", "go to the royal palace (north) and get the sigil of permission", "exterminate the evil swordsman in the forest (once)", "report back to the castle"], "80 exp, 40 coins and an unknown talisman", [80, 40, ["the_exterminator"]]],
    "anniversary gift": [["obtain a slime core earing and give it to danny"], "10 exp, 20 coins and a low tier scroll", [10, 20, ["anniversary_gift"]]],
    "sailing skeleton": [["obtain a skeleton contract and give it to the sailor"], "30 exp, 15 coins and a travel option to the bottom of the river (given without claiming mission)", [30, 15, []]],
    "berserker duel": [["talk to the wounded orc at the mainter forest", "give the orc a bandage (can be bought from jessica who's outside the palace)", "talk to the berserker, show him his old sword, and defeat him"], "45 exp, 10 coins and the berserker class", [45, 10, ["berserker_duel"]]],
    "a shop for the worthy": [["talk to jessica outside the palace", "talk to jessica when your total monster kill count is 25", "talk to jessica when you gain 2 additional levels"], "30 exp, 25 coins and a new shop (given without claiming mission)", [30, 25, []]],
    "a lost priestess": [["give the priestess a small mana potion and 150 coins"], "30 exp, and a scroll (given without claiming)", [30, 0, []]]
}

# *name: price (None is unsellable)
item_sell_value = {"swordsman cape": 60, "wizard staff": 45, "skeleton contract": 40, "slime core earing": 20, "bat eye": 5, "goblin dagger": 35, "goblin hat": 15,
                   "sigil of permission": None, "iron plated leggings": 50, "apple": 4, "bracelet of aid": 15, "rusty sword": 10, "maximized potion": 100,
                   "iron bow": 30, "wooden staff": 15, "bandage": 10, "worn out sword": None, "holy badge": None, "angled bow": 100, "steel layered chestplate": 120,
                   "attack peanut": None, "small mana potion": 20, "dwarven sword": 700, "safety pin": 340, "stylish pants": 520, "jeweled staff": 650,
                   "demonic blood vial": 480}

# classes {*id: [name, desc, [*class_battle_actions=[name, desc]]]}
player_classes = {
    None: ["None", "", ["idle"]],
    1: ["berserker", "a class specialized in sword attacks with a tendency to sacrifice your own vitality in order to deal more damage." 
                     "+20% damage with swords. +10 atk, -5 defense, +5 mana. abilities: reckless - once per battle for 20 mana, increase damage dealt and received by 25% for 3 turns."
                     "\nsacrifice: mana required = max mana capacity. remove half of your remaining hp and a third of each enemy's remaining hp.", ["reckless: 20", "sacrifice: all"]],
    2: ["ninja", "a class specialized in dodging. increases damage proportionally to the ratio between your remaining hp and you enemies hp." 
                 "(the lower your enemies hp is the more damage you do).\ndodger: once per battle increase evasion by 300 percent. costs 20 mana\n"
                 "\nsharpen: increase attack and attack boost by a small amount, no mana cost", ["dodger: 20", "sharpen: 0"]],

}

# screen states {*state: [size, caption]}
screen_states = {
    "world": [None, None],
    "turns": [(896, 576), None],
    "cutscene": [None, None],
    "tutorial": [(620, 330), "tutorial"],
    "tutorial_display": [None, None],
    "mainMenu": [(1000, 600), "main menu"],
    "menu": [(1020, 808), "menu"],
    "shop": [(700, 440), "shop - buy"],
    "death": [(600, 400), "you died loser"],
    "winner": [(600, 400), "win screen"],
    "battle": [(1200, 800), None],
    "fastTravel": [(550, 420), "fast travel"],
    "debug": [(550, 130), "console"],
    "journal": [(560, 320), "journal"],
    "stats": [(700, 495), "stats"],
    "settings": [(300, 600), "settings"],
    "classes": [(900, 850), "class selection"],
}

# click lists
if True:
    keysList = {
        "a": pygame.K_a,
        "b": pygame.K_b,
        "c": pygame.K_c,
        "d": pygame.K_d,
        "e": pygame.K_e,
        "f": pygame.K_f,
        "g": pygame.K_g,
        "h": pygame.K_h,
        "i": pygame.K_i,
        "j": pygame.K_j,
        "k": pygame.K_k,
        "l": pygame.K_l,
        "m": pygame.K_m,
        "n": pygame.K_n,
        "o": pygame.K_o,
        "p": pygame.K_p,
        "q": pygame.K_q,
        "r": pygame.K_r,
        "s": pygame.K_s,
        "t": pygame.K_t,
        "u": pygame.K_u,
        "v": pygame.K_v,
        "w": pygame.K_w,
        "x": pygame.K_x,
        "y": pygame.K_y,
        "z": pygame.K_z,
        "space": pygame.K_SPACE,
        "1": pygame.K_1,
        "2": pygame.K_2,
        "3": pygame.K_3,
        "4": pygame.K_4,
        "5": pygame.K_5,
        "6": pygame.K_6,
        "7": pygame.K_7,
        "8": pygame.K_8,
        "9": pygame.K_9,
        "0": pygame.K_0,
        "num0": pygame.K_KP0,
        "num1": pygame.K_KP1,
        "num2": pygame.K_KP2,
        "num3": pygame.K_KP3,
        "num4": pygame.K_KP4,
        "num5": pygame.K_KP5,
        "num6": pygame.K_KP6,
        "num7": pygame.K_KP7,
        "num8": pygame.K_KP8,
        "num9": pygame.K_KP9,
        "numDel": pygame.K_KP_PERIOD,
        "up": pygame.K_UP,
        "right": pygame.K_RIGHT,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "shift": pygame.K_LSHIFT,
        "ctrl": pygame.K_LCTRL,
        "esc": pygame.K_ESCAPE,
        "tab": pygame.K_TAB,
        "+": pygame.K_KP_PLUS,
        "-": pygame.K_KP_MINUS,
        ":": pygame.K_SEMICOLON,
        "del": pygame.K_DELETE,
        "\'": pygame.K_QUOTE,
        ".": pygame.K_PERIOD,
        ",": pygame.K_COMMA,
        "?": pygame.K_SLASH,
        "_": pygame.K_MINUS,
        "NP_enter": pygame.K_KP_ENTER,
        "enter": pygame.K_RETURN,
        "\b": pygame.K_BACKSPACE,
    }
    mouseDown = {key+1: False for key in range(7)}
    keysDown = {key: False for key in keysList}
    mouseHeld = {key+1: False for key in range(7)}
    keysHeld = {key: False for key in keysList}
    mouseUp = {key+1: False for key in range(7)}
    keysUp = {key: False for key in keysList}

# info checker
if True:
    _test_list = []
    for _id in scrolls:
        for attack in scrolls[_id][2]:
            if attack[0] in _test_list:
                raise Exception("name duplication error")
            _test_list.append(attack[0])
    for _id in scripts:
        for attack in scripts[_id][2]:
            if attack[0] in _test_list:
                raise Exception("name duplication error")
            _test_list.append(attack[0])
    for attack in attacks:
        if attack[0] in _test_list:
            raise Exception("name duplication error")
        _test_list.append(attack[0])

    for item in items:
        if item not in item_sell_value:
            print(item)
            raise Exception("item without sell value")
