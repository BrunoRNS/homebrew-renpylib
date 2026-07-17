# tests/test_audio/game/main.rpy
#
# Interactive test for homebrew_renpylib.audio
# Requires the library wheel and wrapper.rpy (injected by the Makefile).
# Optional: place .ogg files in audio/ (silent files are OK).

define audio_test_music = "audio/aquarela.ogg"
define audio_test_sound = "audio/tada.ogg"

label start:
    scene black # type: ignore
    "Welcome to the Audio module test."
    "You will be guided through music and sound effect tests."
    jump music_test

# ------------------------------------------------------------------
# Music test
# ------------------------------------------------------------------
label music_test:
    python:
        try:
            from hblib.audio import Music
            music = Music()
            music_ok = True
        except Exception:
            music_ok = False

    if not music_ok:
        "Failed to import Music class."
        jump test_failed

    menu:
        "Play test music":
            $ music.play(audio_test_music, loop=True)
            if music.is_playing():
                "Music is playing (flag ON)."
            else:
                "Flag is OFF – something went wrong."
                jump test_failed
            "Press Continue to stop the music and proceed."
            $ music.stop()
            if not music.is_playing():
                "Music stopped correctly."
            else:
                "Music did not stop."
                jump test_failed

        "Stop (if nothing is playing)":
            $ music.stop()
            "Stop called. No assertions made."

        "Skip music test":
            "Skipping music test."

    "Music test complete."
    jump sound_test

# ------------------------------------------------------------------
# Sound effect test
# ------------------------------------------------------------------
label sound_test:
    python:
        try:
            from hblib.audio import Audio
            audio = Audio()
            sound_ok = True
        except Exception:
            sound_ok = False

    if not sound_ok:
        "Failed to import Audio class."
        jump test_failed

    menu:
        "Play test sound":
            $ audio.play(audio_test_sound, loop=False)
            if audio.is_playing():
                "Sound is playing (flag ON)."
            else:
                "Flag is OFF – unexpected."
                jump test_failed
            "Press Continue to stop the sound."
            $ audio.stop()
            if not audio.is_playing():
                "Sound stopped correctly."
            else:
                "Sound did not stop."
                jump test_failed

        "Stop (if nothing is playing)":
            $ audio.stop()
            "Stop called."

        "Skip sound test":
            "Skipping sound test."

    "Sound test complete."
    jump test_passed

# ------------------------------------------------------------------
# Results
# ------------------------------------------------------------------
label test_passed:
    "All audio tests passed successfully!"
    return

label test_failed:
    "A test failed. Check the console for details."
    return