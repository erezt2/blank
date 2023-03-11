none = "none"
empty = " "

"""
text format:
[["name", *"commands"], [ *args=[type_list=[*commands], type_tuple=(["question"], *answers=["answer", "command if picked"]), type_string="displayed_text"] ]]
command = cmd_str or [cmd_str, *args] ( [cmd_str] is also acceptable )
"""

# class Texts:
if True:  # mainter
    # guard east
    ma_ca_guard1_rejected = [["city guard"], [
        "stop! this forest is infested with evil creatures. only the exterminator assigned by the king can proceed"]]

    ma_ca_guard1 = [["city guard"],
                    ["stop! thi... oh, you are the one the king assigned as an exterminator of this area? go through",
                     "just know that the monsters here are really tough. so be careful!",
                     [["fv_set_var", "ma_pass_forest"], ["remove_hitbox", "ma_capital", 34, 11], ["screen_fade", None, ["proceed_mission", "berserker duel", 0]]]]]

    ma_ca_guard1_overdo = [["city guard"], ["welcome back, come and go into the forest"]]

    # guard south
    ma_ca_guard2_rejected = [["city guard"], ["kid, you shouldn't really be here. the monsters here are a lot stronger than those at the hill, get back here when you are stronger"]]

    ma_ca_guard2 = [["city guard"], ["the monster here are tougher than the ones in the hill, so make sure you come back alive!", [["screen_fade"], ["fv_set_var", "guard2_overdo"], ["remove_hitbox", "ma_capital", 26, 29]]]]

    ma_ca_guard2_overdo = [["city guard"], ["the monster here are tougher than the ones in the hill, so make sure you come back alive!"]]
    # guard west
    ma_ca_guard3 = [["city guard"], [(["hello! are you here to train for the extermination job?"], ["yes"]),
                                     "although you only need to be level 3 to accept, i recommend you to be at a higher level when entering the forest",
                                     "after you hit level 3, you should go to the south of the town to gain more levels at the river",
                                     "before entering the hill, i recommend you allocate some points to atk and defense from the menu, because you currently have no chacne against these monsters",
                                     "sometimes you get bad luck and get a bad encounter, in which case, press 'esc' and then press 'give up' to save yourself time",
                                     [["screen_fade", ["remove_hitbox", "ma_capital", 0, 6], ["proceed_mission", "the exterminator", 2]], ["fv_set_var", "guard3_overdo"]]]]

    ma_ca_guard3_overdo = [["city guard"], [
        "although you only need to be level 3 to accept, i recommend you to be at a higher level when entering the forest",
        "after you hit level 3, you should go to the south of the town to gain more levels at the river, dont forget to allocate you LP to stats from the menu!"]]

    #
    ma_story1 = [["city guard"], [
        "hello mighty citizen! due to some unexpected circumstances in the mainter forest, we, the royal palace, are recruiting personal.",
        "you dont seem that strong, but alas! you can get stronger by going to the hill to the west of the town",
        "there are some low level monsters there you can kill to level up. good luck!",
        [["screen_fade", ["ma_story1"]], ["save_exec", "maps.m_ma_capital[2].pop(3)"]]]]

    ma_story2 = [["palace guard"], [(["stop! you are in the territory of the palace of the king! state you business!"],
                                              ["i'm here to apply to the position of the extermination of the forest", ["ma_story2"]],
                                     ["nevermind, ill get out", ["offset_y", 64]])]]

    ma_pa_guard = [["palace guard"], ["here! take these: first of all - a new script! you can equip this script and use its attacks in battle.", "and second - a bow! how could you use the script without one!",
                                      "sadly, we don't have a sword to give you, but you can buy one from johny. he's at the top right house near the hill.",
                                      "also take this sigil of permission to let the forest guard know you are allowed to be there.", ["ma_story2_items"]]]

    ma_pa_guard_overdo = [["palace guard"], [["ma_pa_guard"]]]

    ma_man1_rejected = [["danny"], [
        "hey, can you give me a slime core earing? me and my wife are having our anniversary but i forgot to get her a gift...",
        "ill make it worth your while, i have a leftover scroll, i can give it to you",
        [["proceed_mission", "anniversary gift", 0]]]]

    ma_man1 = [["danny"], [(["hey, can you give me a slime core earing? me and my wife are having our anniversary but i forgot to get her a gift..."],
                            ["yes", ["proceed_mission", "anniversary gift", True], ["fv_set_var", "ma_man_overdo"],
                             ["add_item", "slime core earing", -1]], ["no"])]]

    ma_man1_overdo = [["danny"], ["thanks"]]

    ma_sailor_rejected = [["sailor"], ["oi lad, r' ya tryin to pass the river?, fetch me som' skeleton contract from the big ol' forest and ill let you com' on board", [["proceed_mission", "sailing skeleton", 0]]]]

    ma_sailor = [["sailor"], ["oi lad, r' ya tryin to pass the river?, fetch me som' skeleton contract from the big ol' forest and ill let you com' on board",
                              (["(give the sailor skeleton contract?)"], ["yes", ["proceed_mission", "sailing skeleton", True], ["add_item", "skeleton contract", -1], ["ma_sailor_saved"], ["ma_sailor"]], ["no"])]]

    ma_forest_man = [["???"],
                     ["so you found me...", "but i won't go down without a fight!", [["start_turns", "ma_forest6"]]]]

    ma_orc_rejected = [["wounded orc"], [["ma_orc_text"], (["please... can you spare me some bandages? im very hurt..."], ["sorry i don't have any"])]]

    ma_orc = [["wounded orc"], [["ma_orc_text"], (["please... can you spare me some bandages? im very hurt..."], ["ok", "ma_orc_bandage"], ["sorry i don't have any"])]]

    ma_orc_overdo = [["passerby orc"], ["thanks bro"]]

    ma_berserker_rejected = [["berserker"], ["......"]]

    ma_berserker = [["berserker"], [(["......"], ["(show him the broken sword)"]), "my god... my first sword... i see fate has finally brought me my first disciple", "now let me teach you how to be a berserker!",
                                    [["remove_berserker"], ["start_turns", "berserker"]]]]

    ma_woman1_rejected = [["jessica"], [["jessica_text"]]]

    ma_woman1 = [["jessica"], [[["enter_shop", 1]]]]

    ma_port_boat_rejected = [["mr boat man"], ["son, this boat is military property. if you want to get on the ship with us to spludit get a lvl 2 sigil of permission"]]

    ma_port_boat = [["mr boat man"], ["oh! i see you have a lvl 2 sigil of permission. how uncommon to see someone of your age with that.", (["do you want to sail with us to spludit? we are setting off soon"], ["yes", ["change_map", "ocean", (6, 3)]], ["no"])]]

    spongebob = [[""], [[["start_battle", 1]]]]

    boatman = [["mr boat man"], ["wait up! we will reach it soon", "im not sure why, but i think you should check the tutorial section of boss fights right now", "if for some reason you are not ready fast travel back and get stronger!"]]

    ma_samurai = [["samurai"], [(["hello young lad, do you want to learn the samurai techniques?"], ["yes", "ma_samurai1"], ["no"])]]

    ma_samurai_overdo = [["samurai"], ["okay you can use samurai techniques bye bye"]]

    ma_priestess_rejected = [["priestess"], [(["hello child. i am stuck here and i lost all my money. can you give me 150 coins and a mana potion?"], ["nah fam"]), [["proceed_mission", "a lost priestess", 0]]]]

    ma_priestess = [["priestess"], [(["hello child. i am stuck here and i lost all my money. can you give me 150 coins and a small mana potion?"], ["ok", "ma_priestess"], ["nah fam"])]]

if True:
    sp_ninja = [["ninja"], ["hello dear person! i am looking for a disciple, so now you can either die, or prove your worthiness!", [["start_turns", "ninja"]]]]

    sp_ninja_overdo = [["ninja"], ["hello hello :).", "btw you finished the game for now until erez adds more stuff", "go back and check if you did all the npc missions and got all things"]]

# orc man will tell you how to get a class
# woman will give you quest to go to another land

sleep = [[""], [(["go to sleep and restore hp?"], ["yes", ["screen_fade"], ["exec", "Ins.player.hp = Ins.player.max_hp"]], ["no"])]]

inn = [["inn worker"], [["inn_func"]]]

save_progress = [[''], [(['would you like to save your progress?'], ['yes', ['save_progress']], ['no'])]]

man1 = [["johny"], ["hello", (["do you like cbt"], ["yes", "quit"], ["no"])]]

cut = [["", ["offset_x", 60]], [[['start_cut_scene', 'aa']]]]

test = [[""], [[["start_turns", "test"]]]]

shop1 = [["johny", ["fv_set_var", "shop1_overdo"]], [(["hi~ are you perhaps in need of some goods?"], ["yes", ["enter_shop", 0]],
                                      ["no", ["insert_current", "ok~ talk to me if you want something~"]])]]

shop2 = [["freddy"], ["hello customer!", [["enter_shop", 2]]]]

shop1_overdo = [["johny"], [[["enter_shop", 0]]]]

text_list = {}
for text in [attr for attr in locals() if not attr.startswith("__")]:
    if text in ("text_list", "none", "empty"):
        continue
    text_list[text] = locals()[text]

rejected_text_list = {i: none for i in text_list}
for text in [attr for attr in locals() if not attr.startswith("__") and attr.endswith("_rejected")]:
    org = "_".join(text.split("_")[:-1])
    assert org in text_list, "rejected text doesnt have an owner"
    rejected_text_list[org] = locals()[text]

overdo_text_list = {i: none for i in text_list}
for text in [attr for attr in locals() if not attr.startswith("__") and attr.endswith("_overdo")]:
    org = "_".join(text.split("_")[:-1])
    assert org in text_list, "overdo text doesnt have an owner"
    overdo_text_list[org] = locals()[text]

# text_list = {}
# for text in [attr for attr in dir(Texts) if not callable(getattr(Texts, attr)) and not attr.startswith("__")]:
#     text_list[text] = getattr(Texts, text)

# text_list = {
#     "save_progress": save_progress,
#     "cut": [["", ["offset_x", 60]], [[['start_cut_scene', 'aa']]]],
#     "test": [[""], [[["start_turns", "test"]]]],
#     "man1": man1,
# }

# rejected_text_list = {
#     **{i: none for i in text_list},
#     "save_progress": none,
#     "cut": none,
#
# }

# overdo_text_list = {
#     **{i: none for i in text_list},
#     "save_progress": none,
#     "cut": none,
# }

redirected_text = {
}
