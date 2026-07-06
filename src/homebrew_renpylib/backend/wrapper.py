from typing import Any, Dict, List, NoReturn, Tuple
import datetime

def goto_url(url: str) -> None|NoReturn:
    """Open a URL in the default web browser.

    Args:
        url (str): The URL to open.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "goto_url is not implemented in this environment."
    )

def list_saves() \
-> List[Tuple[
    str, Dict[Any, Any], datetime.datetime, bytes
]] | NoReturn:
    """List saves
    
    The output List follows that constraint:
    - The first element is the save slot name.
    - The second element are extra metadata.
    - The third element is the save timestamp.
    - The fourth element is the save thumbnail.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "list_saves is not implemented in this environment."
    )
    
def unlink_save(slot: str) -> None | NoReturn:
    """Unlink a save slot.

    Args:
        slot (str): The slot to unlink.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "unlink_save is not implemented in this environment."
    )

def save(
    slot: str, data: Dict[Any, Any] | None = None
    ) -> None | NoReturn:
    """Save data to a save slot.

    Args:
        slot (str): The slot to save to.
        data (Dict[Any, Any]): The data to save.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "save is not implemented in this environment."
    )
    
def load_save(slot: str) -> None | NoReturn:
    """Load data from a save slot.

    Args:
        slot (str): The slot to load from.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "load_save is not implemented in this environment."
    )

def get_save_data(slot: str) -> Dict[Any, Any] | NoReturn:
    """Get the data from a save slot.

    Args:
        slot (str): The slot to get the data from.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "get_save_data is not implemented in this environment."
    )
    
def jump_to_scene(label: str) -> None | NoReturn:
    """Jump to a scene.

    Args:
        label (str): The label to jump to.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "jump_to_scene is not implemented in this environment."
    )
    
def play_sound(sound: str, loop: bool = False) -> None | NoReturn:
    """Play a sound.

    Args:
        sound (str): The sound to play.
        loop (bool): Whether to loop the sound.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "play_sound is not implemented in this environment."
    )

def stop_sound() -> None | NoReturn:
    """Stop the currently playing sound.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "stop_sound is not implemented in this environment."
    )
    
def play_music(music: str, loop: bool = True) -> None | NoReturn:
    """Play music.

    Args:
        music (str): The music to play.
        loop (bool): Whether to loop the music.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "play_music is not implemented in this environment."
    )

def stop_music() -> None | NoReturn:
    """Stop the currently playing music.

    Raises:
        NotImplementedError: When called in an environment without wrapper.rpy.
    """
    raise NotImplementedError(
        "stop_music is not implemented in this environment."
    )