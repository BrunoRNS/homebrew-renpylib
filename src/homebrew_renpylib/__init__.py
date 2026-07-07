"""
homebrew_renpylib – Utilities for Ren'Py visual novels
========================================================

Version 1.0.0  |  License: MIT

homebrew_renpylib is a collection of reusable Python modules designed
to speed up common tasks in Ren'Py game development. It is engine‑agnostic:
all Ren'Py‑specific calls are injected through the `backend` module,
keeping the rest of the library portable and testable.

Modules
-------
:mod:`homebrew_renpylib.audio`
    Music and sound effect players (Audio, Music).
:mod:`homebrew_renpylib.backend`
    Injectable function hooks – connect to Ren'Py (or any engine) once.
:mod:`homebrew_renpylib.browser`
    In‑game URL opener with navigation history.
:mod:`homebrew_renpylib.clock`
    Real‑time clock and high‑precision counters.
:mod:`homebrew_renpylib.saves`
    Full save‑slot manager: create, list, delete, load metadata.
:mod:`homebrew_renpylib.scenes`
    Scene (label) representation and weighted random scene groups.
:mod:`homebrew_renpylib.stats`
    Character attributes and stat containers.
:mod:`homebrew_renpylib.utils`
    Day‑graph narrative engine (DayGraph, DayNode), probability helpers,
    save serializer, and scene‑flow automation.

Quick start
-----------
1. Install the wheel into ``game/python-packages/``.
2. Copy ``wrapper.rpy`` into ``game/``.
3. Inject the engine functions **once** in an ``init python`` block::

       import homebrew_renpylib.backend as backend
       backend.inject(
           open_url     = renpy.open_url,
           jump         = renpy.jump,
           play_music   = renpy.music.play,
           play_sound   = renpy.sound.play,
           stop_music   = renpy.music.stop,
           unlink_save  = renpy.unlink_save,
           load_save    = renpy.load,
           list_saves   = lambda: [ ... ],   # see wrapper.rpy
           save         = renpy.save,
           get_save_data= lambda slot: renpy.slot_json(slot) or {},
       )

4. Use any module in your scripts::

       $ from homebrew_renpylib.audio import Music
       $ music = Music()
       $ music.play("audio/theme.ogg", loop=True)
"""

__version__ = "1.0.0"

from . import (
    audio,
    backend,
    browser,
    clock,
    saves,
    scenes,
    stats,
    utils,
)

__all__ = [
    "audio",
    "backend",
    "browser",
    "clock",
    "saves",
    "scenes",
    "stats",
    "utils",
]
