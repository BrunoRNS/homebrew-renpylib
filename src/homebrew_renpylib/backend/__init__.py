from typing import Any

from . import wrapper as _wrapper

from .wrapper import (
    goto_url,
    list_saves,
    unlink_save,
    save,
    get_save_data,
    jump_to_scene,
    play_sound,
    sound_duration,
    stop_sound,
    play_music,
    stop_music,
    load_save,
    quit_game,
    restart_game,
)

__all__ = [
    "inject",
    "goto_url",
    "list_saves",
    "unlink_save",
    "save",
    "get_save_data",
    "jump_to_scene",
    "play_sound",
    "sound_duration",
    "stop_sound",
    "play_music",
    "stop_music",
    "load_save",
    "quit_game",
    "restart_game",
]


def inject(
    *,
    open_url: Any|None=None,
    jump: Any|None=None,
    play_music: Any|None=None,
    play_sound: Any|None=None,
    stop_music: Any|None=None,
    sound_duration: Any|None=None,
    list_saves: Any|None=None,
    unlink_save: Any|None=None,
    save: Any|None=None,
    load_save: Any|None=None,
    get_save_data: Any|None=None,
    quit_game: Any|None=None,
    restart_game: Any|None=None
) -> None:
    """
    Set the engine implementations for all backend functions.
    Accepts only keyword arguments; pass the corresponding
    Ren'Py (or other engine) callables.
    """
    _wrapper.goto_url = open_url
    _wrapper.jump_to_scene = jump
    _wrapper.play_music = play_music
    _wrapper.play_sound = play_sound
    _wrapper.stop_music = stop_music
    _wrapper.sound_duration = sound_duration
    _wrapper.list_saves = list_saves
    _wrapper.unlink_save = unlink_save
    _wrapper.save = save
    _wrapper.load_save = load_save
    _wrapper.get_save_data = get_save_data
    _wrapper.quit_game = quit_game
    _wrapper.restart_game = restart_game
