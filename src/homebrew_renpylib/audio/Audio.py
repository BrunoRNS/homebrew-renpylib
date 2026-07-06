from typing import Optional
from ..backend import play_sound, stop_sound

class Audio:
    """
    Controls sound effects playback.
    Keeps track of the last played sound and its state.
    """

    def __init__(self):
        """
        Initialize the audio controller with no active sound.
        """
        self._last_sound: Optional[str] = None
        self._playing: bool = False

    def play(self, file: str, loop: bool = False) -> None:
        """
        Play a sound effect.

        Args:
            file: Path to the sound file.
            loop: Whether the sound should repeat continuously.
        """
        play_sound(file, loop=loop)
        self._last_sound = file
        self._playing = True

    def stop(self) -> None:
        """
        Stop the currently playing sound effect.
        """
        stop_sound()
        self._playing = False

    def is_playing(self) -> bool:
        """
        Check whether a sound effect is currently playing.

        Returns:
            True if a sound was started and not yet stopped.
        """
        return self._playing

    def get_last_sound(self) -> Optional[str]:
        """
        Return the filename of the last played sound, or None.

        Returns:
            The path of the last sound.
        """
        return self._last_sound