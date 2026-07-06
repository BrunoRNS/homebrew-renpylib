from typing import Optional
from ..backend import play_music, stop_music

class Music:
    """
    Controls background music playback.
    Tracks the current file, loop setting, and play state.
    """

    def __init__(self):
        """
        Initialize the music controller with no active track.
        """
        self._current_file: Optional[str] = None
        self._loop: bool = True
        self._playing: bool = False

    def play(self, file: str, loop: bool = True) -> None:
        """
        Start playing a music file.

        Args:
            file: Path to the audio file (as accepted by the engine).
            loop: Whether the music should repeat after finishing.
        """
        self._current_file = file
        self._loop = loop
        play_music(file, loop=loop)
        self._playing = True

    def stop(self) -> None:
        """
        Stop the currently playing music.
        """
        stop_music()
        self._playing = False

    def is_playing(self) -> bool:
        """
        Check whether music is currently playing.

        Returns:
            True if a track was started and not yet stopped.
        """
        return self._playing

    def get_current_file(self) -> Optional[str]:
        """
        Return the filename of the current track, or None if none set.

        Returns:
            The current music file path.
        """
        return self._current_file

    def get_loop(self) -> bool:
        """
        Return the loop setting of the current track.

        Returns:
            The loop flag.
        """
        return self._loop