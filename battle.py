import textures
"""
when init:
"" tuple: {} dict = random with weight
 tuple - "total rolls|*frame choices"
 if a list is chosen, it will assign each frame by order to the selected list. if there is a list in the keys of the dict it is recommended to use only one roll

 dict = {
     removes_val_when_picked : force_pick_all
     *probability = actions
 }

  # False: False is used to get frames and assign lines to them

  # True: False is used to get some frames and assign lines to them, but each line can be assigned only once

  # True: True is used to get some frames and assign lines to them, but each line can be assigned only once and all the lines must be assigned

  # False: True is used to assign a fixed frame to each line and generate some lines

() tuple: line = runs the line for all the frames in the tuple
 tuple (*frames)

int: line = runs the line for the frame

str: line = used for saving frames
"""
"""
 dict = {
     removes_val_when_picked : number of rolls
     *probability = functions
 }

[] lists = functions
list = [function, *args]

() tuples = all
tuple = (run all commands inside)

{} sets = all
set = {read all frames in the set}
"""
"types to use - int, str, float, complex, dict, set, list, tuple, bool"

### battle dict
b_sponge = \
    {30: ['projectile', 34, 444, 100, 100, -1.0025094781323536, 19, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 60: ['projectile', 532, 448, 100, 100, -2.2119050956546027, 16, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 90: ['projectile', 649, 101, 100, 100, 2.784283970581693, 16, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 120: ['projectile', 289, -59, 100, 100, 1.3791478301082194, 13, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 150: ['projectile', 25, -62, 100, 100, 1.0503378773437473, 18, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 180: ['projectile', 67, 438, 100, 100, -0.7207402169734671, 19, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 210: (['projectile', 564, 441, 100, 100, -2.601173153319209, 19, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', 558, -48, 100, 100, 2.1015698239978033, 21, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False]), 240: (['projectile', 47, -57, 100, 100, 1.570796326795, 19, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', 207, 445, 98, 98, -1.570796326795, 24, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', 351, -60, 100, 100, 1.570796326795, 24, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', 537, 447, 100, 100, -1.570796326795, 24, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 1.7, 0.0, [0.95, 1.1], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False]), 270: ['projectile', 295, 195, 600, 14, 0, 0, [1, 0, 0, 0.0, 0, 0], '', 6, 0.0, 0.0, [0.0, 0.0], ['none', 'none', 'none', 'none'], [255, 0, 0], [0, 0, 0, 0, 0], False], 282: ['projectile', 295, 195, 600, 14, 0, 0, [1, 0, 0, 0.0, 0, 0], '', 6, 0.0, 0.0, [0.0, 0.0], ['none', 'none', 'none', 'none'], [255, 0, 0], [0, 0, 0, 0, 0], False], 294: ['projectile', 295, 195, 600, 14, 0, 0, [1, 0, 0, 0.0, 0, 0], '', 6, 0.0, 0.0, [0.0, 0.0], ['none', 'none', 'none', 'none'], [255, 0, 0], [0, 0, 0, 0, 0], False], 300: ['hitbox', -7, 182, 600, 24, 0, 0, 240, True, ['none', 'none'], None], 310: (['projectile', 208, 97, 90, 124, -0.24497866312686414, 1, [0, 0, 0, 0.0, 0, 0], 'sponge2', 120, 2.0, 0.0, [1.0, 1.2], ['none', 'none', 'none', 'none'], [255, 255, 255], [1.570796326795, 0, 0, 0.0, 0], False], ['projectile', 544, 131, 90, 126, -2.62244653934327, 1, [0, 0, 0, 0.0, 0, 0], 'sponge2', 120, 2.0, 0.0, [1.0, 1.2], ['none', 'none', 'none', 'none'], [255, 255, 255], [1.570796326795, 0, 0, 0.0, 0], False], ['projectile', -29, 342, 92, 126, 0.0, 12, [0, 0, 0, 0.0, 0, 0], 'sponge2', 120, 2.0, 0.0, [1.0, 1.2], ['none', 'none', 'none', 'none'], [255, 255, 255], [1.570796326795, 0, 0, 0.0, 0], False]), 330: ['projectile', 429, 76, 90, 126, 3.0309354324158977, 1, [0, 0, 0, 0.0, 0, 0], 'sponge2', 120, 2.0, 0.0, [1.0, 1.2], ['none', 'none', 'none', 'none'], [255, 255, 255], [1.570796326795, 0, 0, 0.0, 0], False], 340: ['projectile', 67, 93, 90, 126, 0, 0, [0, 0, 0, 0.0, 0, 0], 'sponge2', 120, 2.0, 0.0, [1.0, 1.2], ['none', 'none', 'none', 'none'], [255, 255, 255], [1.570796326795, 0, 0, 0.0, 0], False], 350: (['projectile', -30, 251, 92, 126, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge2', 120, 2.0, 0.0, [1.0, 1.2], ['none', 'none', 'none', 'none'], [255, 255, 255], [1.570796326795, 0, 0, 0.0, 0], False], ['projectile', 625, 252, 90, 126, 3.14159265359, 19, [0, 0, 0, 0.0, 0, 0], 'sponge2', 120, 2.0, 0.0, [1.0, 1.2], ['none', 'none', 'none', 'none'], [255, 255, 255], [1.570796326795, 0, 0, 0.0, 0], False]), 375: ['projectile', -46, 347, 90, 126, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge2', 120, 2.0, 0.0, [1.0, 1.2], ['none', 'none', 'none', 'none'], [255, 255, 255], [1.570796326795, 0, 0, 0.0, 0], False], 390: ['projectile', -51, 269, 90, 128, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge2', -1, 2.2, 0.0, [1.0, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 410: ['projectile', -26, 91, 90, 128, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge2', -1, 2.2, 0.0, [1.0, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 430: ['projectile', 13, 23, 90, 128, 1.2870022175865687, 10, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.8, 1.2], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 440: ['projectile', 566, 264, 90, 124, -3.0258334358689827, 8, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 540: ['projectile', 565, 35, 90, 128, 2.7038013499482467, 10, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 560: ['projectile', 27, 236, 90, 128, -1.4930313871921643, 15, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 660: ['projectile', 292, 31, 92, 126, 0.7349359893805925, 14, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 790: ['remove_all_projectiles'], 800: (['hitbox', -230, 76, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], ['set_mode', 4]), 820: ['hitbox', -228, 162, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], 840: ['hitbox', -229, 272, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], 860: ['hitbox', -231, 70, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], 880: ['hitbox', -231, 173, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], 900: ['hitbox', -228, 278, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], 920: ['hitbox', -229, 170, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], 940: ['hitbox', -229, 59, 220, 22, 0.0, 14, -1, False, ['none', 'none'], None], 830: ['projectile', -53, 35, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 850: ['projectile', -50, 221, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 870: ['projectile', -49, 129, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 890: ['projectile', -49, 362, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 910: (['projectile', -57, 236, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', -54, 44, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False]), 950: (['projectile', -49, 362, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', -50, 263, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', -53, 35, 94, 98, 0.0, 14, [0, 0, 0, 0.0, 0, 0], 'sponge1', -1, 2.5, 0.1, [0.8, 1.0], ['none', 'none', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False]), 1000: (['set_mode', 0], ['projectile', 16, 379, 90, 128, -1.2426764317795913, 9, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False]), 1005: ['projectile', 191, 376, 90, 128, -2.4132752725986095, 9, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 1010: ['projectile', 277, 371, 90, 124, -0.3430239404207034, 8, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], 1015: (['projectile', 386, 370, 92, 128, -2.0803885916038225, 7, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', 500, 367, 90, 124, -1.7033478590915707, 15, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False]), 1180: (['projectile', 354, 373, 90, 128, -2.8632929945846817, 4, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False], ['projectile', 44, 50, 90, 126, -2.6311043316730176, 5, [1, 0, 0, 0.0, 0, 0], 'sponge2', -1, 0.4, 0.0, [0.9, 1.1], ['none', 'bounce_mid', 'none', 'none'], [255, 255, 255], [0, 0, 0, 0, 0], False])}

### turns lists

# [name, texture, [hp, attack, defense, evasion, accuracy, lvl], attack_function, attacks={*weighted_attacks:, *named_attacks:}, loot_table=[*[item, chance, [*amount]]]]

#  enemy_id battle???: [list, [song_start_frames, song_end_frames], song_delay, texture, [hp, attack, defense, evasion, accuracy, lvl], loot_table=[*[item, chance, [*amount]]], [mix_exp, max_exp, min_coins, max_coins]]

#  enemy_id battle: [list, name, song, [song_start_frames, song_end_frames], texture, [hp, attack, defense, evasion, accuracy, lvl], loot_table=[*[item, chance, [*amount]]], [mix_exp, max_exp, min_coins, max_coins], background]

enemies_list = {
    1: [b_sponge, 'cursed spongebob', 'spongebob', [0, 1937], 'spongebob', [800, 40, 40, 20, 60, 15], [], [80, 100, 30, 40], 'f']
}

# Attacker.attack / (Defender.defense + 1) * attack_modifier * crit_multiplier * (level/66 +0.75) * attack_random_multiplier * (0 if accuracy_modifier * (Attacker.accuracy + 1) / (Defender.evasion + 1) < random.random() else 1) * (weapon_boost + 1) if player is attacker else (1 - armor_defense)
# Attacker.defense * health.modifier * (level/99 + 1) * heal_random_multiplier
# [name, color, mana_cost, [attack_modifier, accuracy_modifier, healing_modifier, [rand_atk_min, rand_atk_max], [rand_hp_min, rand_hp_max]], [*[x_start, y_start, width, height]], [name, effect_time, effect_player, add_effect, exist_effect, remove_effect, effect_remove, color, stored_data], weapon{0: none, 1: sword, 2: bow, 3: staff}]
