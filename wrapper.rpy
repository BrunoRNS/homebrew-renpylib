# wrapper.rpy — MIT License
# -------------------------------------------------------------------
# This file connects homebrew_renpylib to the Ren'Py engine.
# Copy it into your project's game/ folder.
# After that, all modules are available via the alias `hblib`.
# -------------------------------------------------------------------

init python:
    import homebrew_renpylib as hblib
    import homebrew_renpylib.backend as backend

    def _list_saves():
        result = []
        for filename, extra_info, screenshot_time, _ in renpy.list_saved_games():
            result.append({
                "slot": filename,
                "time": screenshot_time,
                "extra": extra_info if extra_info else {}
            })
        return result

    backend.inject(
        open_url       = renpy.open_url,
        jump           = renpy.jump,
        play_music     = renpy.music.play,
        play_sound     = renpy.sound.play,
        stop_music     = renpy.music.stop,
        sound_duration = lambda file: renpy.music.get_duration(file),
        list_saves     = _list_saves,
        unlink_save    = renpy.unlink_save,
        save           = renpy.save,
        load_save      = renpy.load,
        get_save_data  = lambda slot: renpy.slot_json(slot) or {},
        quit_game      = renpy.quit,
        restart_game   = renpy.restart
    )
