class Error(Exception):
    pass


class Broken(Error):
    messages = [""]


class InventoryError(Error):
    messages = ["", "took an item from an inventory without the item", 'took too many items from an inventory', "returned negative number of items in inventory", "there is no such item"]


class SoundError(Error):
    messages = ["", "error while playing song (try restarting the computer)", "error while playing sound effect", "there is no previous song to be played"]


class CodeError(Error):
    messages = ["", "union of 2 textures.py dictionaries is not empty"]


class StateCode(Error):
    messages = ["", "game is active with invalid state"]


class AnimationError(Error):
    messages = ["", "animation name already exists"]


class TurnsError(Error):
    messages = ["", "turn id was not found"]


def error(error_type, message_num=0):
    try:
        if message_num <= 0:
            raise AttributeError
        raise error_type("CUSTOM MADE ERROR: " + error_type.messages[message_num])
    except AttributeError:
        raise error_type
