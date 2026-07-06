from typing import Any, Optional
from ..saves import Saves

class SaveSerializer:
    """
    Handy bridge to save/load any serialisable object (like SceneManager or DayManager)
    into a save slot's extra_info.
    """

    def __init__(self, saves: Saves):
        """
        Args:
            saves: An instance of the Saves manager.
        """
        self.saves = saves

    def save_object(self, slot: str, key: str, obj: Any) -> None:
        """
        Save an object (as part of extra_info) under a given key.
        If the slot doesn't exist, it is created; otherwise the extra_info is updated.

        Args:
            slot: Save slot name.
            key: Key under which to store the object (e.g. 'scene_manager').
            obj: The object (must be serialisable to JSON).
        """
        existing = self.saves.find_by_slot(slot)
        if existing:
            existing.update_extra({key: obj})
        else:
            self.saves.create(slot, extra={key: obj})

    def load_object(self, slot: str, key: str) -> Optional[Any]:
        """
        Retrieve an object from a save slot's extra_info.

        Args:
            slot: Save slot name.
            key: The key used when saving.

        Returns:
            The stored object, or None if not found.
        """
        slot_obj = self.saves.find_by_slot(slot)
        if not slot_obj:
            return None
        data = self.saves.get_save_extra_info(slot_obj)
        return data.get(key)
