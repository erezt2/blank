#  **attack: [name, color, mana_cost, [attack_modifier, accuracy_modifier, healing_modifier,
#  [rand_atk_min, rand_atk_max], [rand_hp_min, rand_atk_max], [crit_chance, crit_multiplier]], target, # 0 - self, 1 - all enemies, 2 - random enemy
#  [name, effect_time, is_targeting_player, add_effect, exist_effect, remove_effect, remove_condition, color], sound_effect, attack_type, attack_delay, attack_animation]]
# only difference from player attack is that "weapon_type" doesnt exist
# 0 - default animation, -1 - default death animation, -2 - default hit animation
attacks = {
    "none": ["waiting...", (255, 255, 255), 0, [0, 0, 0, [1, 1], [0, 0], [0, 0]], 0, -1, "none", 0, 0, -1],
    "test": ["kicking ass", (255, 0, 0), 0, [1, 0, 0, [1, 1], [1, 1], [0, 0]], 0, -1, "none", 0, 0, "slash1"],
    "slash1": ["dagger slash", (150, 150, 150), 0, [0.9, 0.05, 0, [0.9, 1.1], [0, 0], [0.1, 1.25]], 0, -1, "slash1", 0, 0, "slash1"],
    "slash2": ["slash", (130, 130, 130), 0, [0.65, 0.08, 0, [0.9, 1.1], [0, 0], [0.15, 1.20]], 0, -1, "slash1", 0, 0, "slash1"],
    "stab1": ["dagger stab", (150, 150, 150), 0, [1.3, 0.1, 0, [1, 1.3], [0, 0], [0.1, 1.25]], 0, -1, "stab1", 0, 0, -1],
    "fireball1": ["minor fireball", (150, 50, 50), 2, [1.7, 0.05, 0, [0.9, 1.1], [0, 0], [0.1, 1.25]], 0, -1, "fireball1", 0, 0, "fireball1"],

    "jump1": ["jump attack", (150, 150, 150), 0, [0.55, 0.1, 0, [1, 1.1], [0, 0], [0.25, 1.25]], 0, -1, "effect1", 0, 0, -1],
    "heal1": ["small heal", (60, 160, 60), 5, [0, 0, 0.4, [0, 0], [1, 1.3], [0, 0]], 2, -1, "heal1", 0, 1, "heal1"],
    "heal2": ["area heal", (70, 190, 70), 4, [0, 0, 0.3, [0, 0], [1, 1.5], [0, 0]], 1, -1, "heal1", 0, 1, "heal1"],
    "magicRay1": ["magic ray", (200, 50, 230), 2, [0.85, 0.06, 0, [1, 1.1], [0, 0], [0.15, 1.25]], 0, -1, "magic2", 0, 0, "16-purpleRay"],
    "magicBlast1": ["magic blast", (140, 30, 170), 5, [2.2, 0.09, 0, [0.7, 1.4], [0, 0], [0.03, 2]], 0, -1, "magic1", 0, 1, "16-purpleBlast"],

    "atkBoost1": ["attack boost", (200, 70, 60), 8, [0, 0, 0, [0, 0], [0, 0], [0, 0]], 0, ["attack boost", 3, False, "atk_boost1", "none", "atk_boost1", (200, 70, 60)], "magic3", 0, 4, -1],
    "lightning1": ["lightning bolt", (252, 255, 0), 5, [3.65, 0, 0, [1, 1.1], [0, 0], [0.5, 1.15]], 0, -1, "magic5", 0, 4, "0-lightning1-an"],
    "tripleSlash1": ["triple slash", (200, 200, 200), 0, [2.65, 0.05, 0, [0.75, 1.25], [0, 0], [0.2, 1.3]], 0, -1, "slash1", 0, 0, "10-tripleSlash1"],
    "maceAttack1": ["mace attack", (100, 100, 100), 0, [2, 0.06, 0, [0.9, 1], [0, 0], [0.5, 1.25]], 0, -1, "slash1", 0, 0, "7-slash2"],
    "poisonAttack1": ["poison attack", (30, 120, 30), 2, [1.1, 0.07, 0, [0.9, 1], [0, 0], [0.5, 1.25]], 0, ["low poison", 2, True, "none", "poison1", "none", (10, 60, 10)], "slash1", 0, 1, "10-slash1"],

    "boneRestore": ["bone restore", (80, 255, 80), 0, [0, 0, 0, [0, 0], [0, 0], [0, 0]], 0, -1, "heal1", 0, 0, "heal1"],
    "slash3": ["slash", (130, 40, 40), 0, [2, 0.075, 0, [0.8, 1], [0, 0], [0.15, 1.15]], 0, -1, "slash1", 0, 0, -1],
    "slash4": ["big slash", (170, 40, 40), 7, [3.8, 0.1, 0, [0.8, 1], [0, 0], [0.15, 1.25]], 0, -1, "slash1", 0, 1, "18-smoke1-an"],
    "slash5": ["huge slash", (200, 40, 40), 7, [4.8, 0.1, 0, [0.8, 1], [0, 0], [0.15, 1.35]], 0, -1, "slash1", 0, 2, "14-slash1-an"],
    "doubleSlash1": ["slash", (130, 40, 40), 0, [2.65, 0.075, 0, [0.9, 1.1], [0, 0], [0.1, 1.35]], 0, -1, "slash1", 0, 1, -1],

    "fireball2": ["fire spell", (170, 30, 30), 0, [3.25, 0.05, 0, [0.9, 1.05], [0, 0], [0.25, 1.25]], 0, -1, "38-magic7", 0, 2, "20-fire2-an"],
    "cinders": ["CINDERS", (255, 0, 0), 0, [5.2, 0, 0, [1, 1], [0, 0], [0, 0]], 0, ["burn", 3, True, "none", "burn1", "none", (255, 0, 0)], "12-magic6", 0, 0, "32-fire1-an"],
    "strike1": ["strike", (140, 30, 30), 10, [3.4, 0.06, 0, [0.8, 1.1], [0, 0], [0.1, 1.3]], 0, -1, "blunt1", 0, 1, -1],
    "slash6": ["big slash", (170, 40, 40), 4, [4, 0.1, 0, [0.8, 1], [0, 0], [0.15, 1.25]], 0, -1, "slash1", 0, 1, "wind1-an"],
    "slash7": ["big slash", (70, 170, 70), 0, [2.2, 0.08, 0, [0.9, 1.1], [0, 0], [0.12, 1.35]], 0, -1, "slash1", 0, 0, "wind1-an"],

    "flurry": ["flurry", (80, 190, 80), 10, [3.6, 0.1, 0, [0.7, 1.3], [0, 0], [0.2, 1.2]], 0, -1, "slash1", 0, 0, "0-flurry1"],
    "tornado": ["tornado", (90, 230, 90), 18, [2.9, 0.04, 0, [0.95, 1.1], [0, 0], [0.2, 1.2]], 0, -1, "magic7", 0, 0, "wind2-an"],
    "bigFlurry": ["starward flurry", (100, 255, 100), 0, [6.4, 0, 0, [1, 1], [0, 0], [0, 0]], 0, ["slowness", 3, True, "slowness", "none", "slowness", (10, 70, 10)], "slash1", 0, 0, -1],
    "lightRay1": ["light ray", (200, 200, 200), 12, [6, 0.05, 0, [0.8, 1.1], [0, 0], [0.1, 1.35]], 0, -1, "magic5", 0, 2, "lightning2-an"],
    "addTurn": ["add turn", (255, 255, 255), 0, [0, 0, 0, [0, 0], [0, 0], [0, 0]], 0, -1, "none", 0, 0, -1],

    "heal3": ["big heal", (140, 255, 140), 14, [0, 0, 1, [0, 0], [0.98, 1.1], [0, 0]], 1, -1, "heal1", 0, 1, "heal1"],

}
# **name: [displayed_name, texture, [hp, mana, attack, defense, evasion, accuracy, level], loot_table=[*[item, chance, [*amount]]], [mix_exp, max_exp, min_coins, max_coins], attacks: {**name: [weight, animation]}]
enemies = {
    "goblin1": ["goblin", "goblin", [18, 3, 15, 14, 18, 13, 4], [["goblin hat", 0.08, [1]]], [6, 9, 2, 4], {"slash1": [2, 1], "stab1": [1, 2], "fireball1": [0.5, 3]}],
    "slime1": ["blue slime", "slime", [8, 10, 10, 8, 5, 10, 2], [["slime core earing", 0.1, [1]]], [3, 5, 1, 2], {"jump1": [1, 1], "heal1": [0.2, 0]}],
    "bat1": ["small bat", "bat", [6, 0, 5, 5, 10, 13, 1], [["bat eye", 0.25, [1]], ["bat eye", 0.35, [1]]], [1, 2, 1, 1], {"slash2": [1, 1]}],
    "skeleton1": ["mace skeleton", "mace_skeleton", [42, 5, 19, 25, 5, 19, 5], [["skeleton contract", 0.1, [1]]], [16, 19, 4, 6], {"maceAttack1": [2.5, 1], "poisonAttack1": [10, 2]}],
    "wizard1": ["evil wizard", "purple_wizard", [37, 25, 25, 20, 16, 22, 6], [["wizard staff", 0.1, [1]]], [15, 21, 5, 7], {"magicRay1": [2, 2], "magicBlast1": [1, 1], "heal2": [0.35, 1]}],

    "swordsman1": ["dark swordsman", "dark_swordsman", [55, 20, 33, 30, 22, 33, 8], [["swordsman cape", 0.1, [1]]], [20, 27, 10, 11], {"tripleSlash1": [2, 2], "atkBoost1": [3, 1], "lightning1": [0.8, 1]}],
    "berserker": ["berserker", "berserker", [96, 35, 58, 55, 40, 56, 15], [], [50, 56, 12, 18], {"fireball2": [1, 3], "doubleSlash1": [1.5, 2], "slash3": [2, 1], "heal1": [0.7, 5], "cinders": [0, 4]}],  #
    "imp1": ["low imp", "imp1", [70, 25, 38, 30, 40, 28, 11], [], [30, 40, 10, 16], {"slash3": [1, 1], "strike1": [0.5, 2]}],
    "imp2": ["imp", "imp2", [80, 30, 44, 34, 34, 36, 13], [], [35, 44, 12, 17], {"slash3": [1, 1], "slash4": [0.5, 2], "slash5": [0.25, 1]}],
    "imp3": ["high imp", "imp3", [90, 35, 50, 48, 28, 40, 14], [], [40, 48, 13, 18], {"slash3": [1, 1], "slash6": [0.5, 1], "lightRay1": [0.3, 1], "addTurn": [0, 0]}],  #

    "samurai_apple": ["apple", "apple", [100, 0, 0, 10, 0, 0, 5], [], [0, 0, 0, 0], {}],
    "ninja": ["ninja", "ninja", [202, 72, 85, 75, 94, 88, 26], [], [100, 130, 50, 60], {"slash7": [1.8, 1], "flurry": [0.6, 2], "tornado": [1.3, 3], "bigFlurry": [0, 4], "heal3": [0.75, 5]}],
}
# chance,
# id: [[*[weight, *names], song, ]
# id: [[*enemies], song, background, loot_table=[*[item, chance, [*amount]]]]
encounters = {
    "test": [["ninja"], "song2", "arena1", [], [0, 0, 0, 0]],

    "ma_forest1": [["wizard1", "skeleton1"], "battle2", "arena1", [], [6, 7, 5, 5]],
    "ma_forest2": [["skeleton1", "skeleton1"], "battle2", "arena1", [], [7, 8, 5, 6]],
    "ma_forest3": [["wizard1", "skeleton1", "skeleton1"], "battle2", "arena1", [], [10, 13, 5, 8]],
    "ma_forest4": [["wizard1"], "battle2", "arena1", [], [1, 1, 1, 1]],
    "ma_forest5": [["skeleton1"], "battle2", "arena1", [], [1, 1, 1, 1]],
    "ma_forest6": [["swordsman1"], "battle2", "arena1", [], [1, 1, 1, 1]],
    "ma_forest7": [["swordsman1", "wizard1", "skeleton1"], "battle2", "arena1", [], [1, 1, 1, 1]],

    "ma_hill1": [["bat1", "bat1"], "battle1", "arena1", [], [1, 1, 1, 1]],
    "ma_hill2": [["slime1", "bat1"], "battle1", "arena1", [], [1, 3, 1, 1]],
    "ma_hill3": [["slime1", "bat1", "bat1"], "battle1", "arena1", [], [3, 5, 1, 2]],
    "ma_hill4": [["bat1", "bat1", "bat1"], "battle1", "arena1", [], [2, 3, 1, 1]],
    "ma_hill5": [["bat1", "bat1", "bat1", "bat1", "bat1"], "battle1", "arena1", [], [5, 7, 3, 4]],
    "ma_hill6": [["bat1"], "battle1", "arena1", [], [0, 0, 0, 0]],

    "ma_river1": [["goblin1"], "battle3", "arena1", [], [0, 0, 0, 0]],
    "ma_river2": [["goblin1", "slime1"], "battle3", "arena1", [], [1, 2, 1, 3]],
    "ma_river3": [["goblin1", "goblin1"], "battle3", "arena1", [], [4, 4, 4, 5]],
    "ma_river4": [["goblin1", "slime1", "slime1"], "battle3", "arena1", [], [7, 9, 4, 5]],
    "ma_river5": [["goblin1", "goblin1", "goblin1"], "battle3", "arena1", [["goblin dagger", 0.4, [1]]], [10, 11, 8, 10]],

    "sp_entrance1": [["imp1"], "battle5", "arena2", [], [0, 0, 0, 0]],
    "sp_entrance2": [["imp1", "imp1"], "battle5", "arena2", [], [3, 6, 2, 6]],
    "sp_entrance3": [["imp1", "imp2"], "battle5", "arena2", [], [8, 8, 6, 9]],
    "sp_entrance4": [["imp2", "imp1", "imp1"], "battle5", "arena2", [], [14, 18, 8, 10]],
    "sp_entrance5": [["imp2", "imp2", "imp1"], "battle5", "arena2", [], [15, 22, 12, 15]],
    "sp_entrance6": [["imp3"], "battle5", "arena2", [], [0, 0, 0, 0]],
    "sp_entrance7": [["imp3", "imp2", "imp1"], "battle5", "arena2", [], [18, 25, 14, 17]],

    "ninja": [["ninja"], "song2", "arena2", [], [0, 0, 0, 0]],
    "berserker": [["berserker"], "battle4", "arena1", [], [0, 0, 0, 0]],
    "samurai_apple": [["samurai_apple"], "apple", "arena1", [], [1, 1, 1, 1]],
}

if True:
    _test_list = []
    for attack in attacks:
        if attack in _test_list:
            raise Exception("name duplication error")
        _test_list.append(attack)
    del attack, _test_list

