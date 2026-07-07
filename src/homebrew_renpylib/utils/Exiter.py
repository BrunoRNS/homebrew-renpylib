from typing import Optional, Dict, Any
from ..backend import quit_game, restart_game, jump_to_scene
from ..saves import Saves
from ..utils.SaveSerializer import SaveSerializer


class Exiter:
    """
    Handles quitting, fake‑restarting, and deferred actions after restart.

    Uses a dedicated save slot to store an action (label + extra data) that
    will be executed the next time the game is launched (real quit) or
    restarted (fake quit).

    Example usage:
        exiter = Exiter(saves, slot="exit_data")
        exiter.set_next_action("morning_after")
        exiter.quit_immediately()           # really close the game
        exiter.fake_quit()                  # restart without really closing

        # In startup code:
        exiter.execute_next_action()        # jump to stored label, if any
    """

    def __init__(self, saves: Saves, slot: str = "exit_data"):
        self._saves = saves
        self._slot = slot
        self._serializer = SaveSerializer(saves)

    def quit_immediately(self) -> None:
        """Close the game immediately (Android/iOS/Desktop)."""
        quit_game()

    def fake_quit(self) -> None:
        """
        Simulate quitting by restarting the game to the main menu.
        The current game state is lost, but the next action (if set) will
        be available after the restart.
        """
        restart_game()

    def set_next_action(self, label: str, **extra: Any) -> None:
        """
        Store an action to be executed on the next start (real or fake).
        The label will be jumped to automatically when you call
        `execute_next_action()`.

        Args:
            label: Ren'Py label to jump to.
            **extra: Additional data stored alongside the label.
        """
        data: Dict[str, Any] = {"label": label, "extra": extra}
        self._serializer.save_object(self._slot, "next_action", data)

    def get_next_action(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve the stored next action without executing it.
        After retrieval the data is cleared from the save slot.

        Returns:
            A dict with keys 'label' and 'extra', or None if nothing stored.
        """
        data: Optional[Dict[str, Any]] = self._serializer.load_object(self._slot, "next_action")
        if data:
            self._clear_next_action()
        return data

    def execute_next_action(self) -> None:
        """
        If a next action was stored, jump to the label immediately.
        This is meant to be called once at game startup (e.g., after load).
        """
        action = self.get_next_action()
        if action:
            label = action.get("label")
            if label:
                jump_to_scene(label)

    def _clear_next_action(self) -> None:
        """Remove the stored action from the save slot."""
        existing = self._saves.find_by_slot(self._slot)
        if existing:
            existing.update_extra({"next_action": None})   # overwrites with None
        self._serializer.save_object(self._slot, "next_action", None)
        
