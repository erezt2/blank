# Blank

this is a very simple and crude game, that can be also used as a game engine, though the user interface is not intuitive.

this repository includes both the game, which is missing a bunch of content, and the tools that I built that were used to create it. The systems themselves of the game + tools are mostly done, but they are not very user friendly nor are they coded with good practices in mind as I started the project eons ago and just built upon it with minor changes.

### The Game

![Menu Screen](readme/ss1.png)

The game is a RPG genred game. There are the expected systems for such a genre of games; such as combat, dialog, menus, quests, cutscenes and classes.

From the main menu you can choose to load your save or to create a new game, alongside changing the settings.

##### navigation

![World Travel](readme/ss2.png)

The game uses block textures as the building block of the map, for convinience for building more maps using the map creation tool. All textures were stolen from minecraft texturepacks + itch.io, and most music was stolen from Octopath Traveler.

##### functionality

![interactions](readme/ss3.png)

The game only requires a keyboard to be played, though there are some functionalities that can be imitated using a mouse I wouldn't recommend using it at all.

There are 12 default key inputs: esc for menu exit, tab for menu selection, wasd for navigation, e for interact and battle choose, q for secondary interact and battle selection, shift for sprint and 1-3 for battle menu choosing.

all keybinds aside from esc and tab can be changed in the settings alongside volume, autosaves and more.

##### menu

![menu](readme/ss4.png)

Inside the game, you can access the menu after pressing esc. 

As you may have noticed, the screen size of the game changes according to what you are viewing, which is one of the many bad choices I included early on and decided to ignore later.

The menu has 7 sections:

Inventory: a list of all the items you have. You can equip items from here on your character, and equip consumable items to use in battle.
Equipment: a list of all the items you are equiping
Stats: a list of the stats of your character. You can use LP (level points) to increase your stats after leveling up.
Scrolls/ Scripts: a list of all the scrolls and scripts you can use. these function as a collection of attacks you can use in battle.
Misc: these are miscellaneous menus that are self explanatory by their names.

The 'class' menu can be used to change your class, which can give you access to class actions in battle and to extra stat points.

The 'journal' menu can be used to get hints for quests or accept quest rewards.

#### battle

there are two types of battles in this game.
- encoutner battles: includes battles with random enemies or minibosses. These battles are turn orianted.
- boss battles: battles with bosses. These are not turn orianted, you need to dodge while attacking, similar to undertail battles but you need to multitask dodging and using your skills.

In both battles, you need to 

##### encoutner battles




## Project details (old readme)

runs on python 3.9 (will probably work on 3.7 or 3.8)
uses the modules:
pygame, shapely, mutagen, pydub, simpleaudio

* ONLY KEYBOARD IS FULLY SUPPORTED, IT IS POSSIBLE AND RECOMMENDED PLAYING WITHOUT TOUCHING THE MOUSE
* (meaning that there are some functions that are NOT supported by the mouse)

default controls:
w - up, a - left, s - down, d -right
e - interact, q - secondary action
tab - switch modes (used in menu or in shop)
e - battle confirm
q - battle switch menu
1, 2, 3 - pick option battle


for the full tutorial, go into the tutorial category inside the game
(start menu -> start button -> view tutorial)
or inside the game
(esc -> misc -> tutorial)

to start run init.py

notes:
if you decide to check the editors/ generators, check the MAP_GENERATOR only AFTER you have graded my work, since it
automatically edits resource files when you close it, and may ruin some maps if you are not familiar with it 
