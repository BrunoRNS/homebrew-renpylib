from datetime import datetime
from typing import Any, Dict, Optional

from ..backend import (
    unlink_save, save, get_save_data
)

class SaveSlot:
    """
    Represents a single save slot with its metadata.

    Attributes:
        slot: The slot name (e.g., '1-1').
        time: The timestamp when this save was created or last modified.
        extra: Additional data stored with the save.
    """

    def __init__(
        self,
        slot: str,
        time: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a SaveSlot.

        Args:
            slot: The slot identifier string.
            time: Datetime of the save; defaults to now if not provided.
            extra: Dictionary of extra data attached to the save.
        """
        self.slot = slot
        self.time = time or datetime.now()
        self.extra = extra or {}

    def delete(self) -> None:
        """
        Delete this save slot from the storage.
        """
        unlink_save(self.slot)

    def load_extra(self) -> Dict[str, Any]:
        """
        Retrieve the extra data dictionary for this save without loading the game state.

        Returns:
            The extra data dictionary stored in this slot.
        """
        return get_save_data(self.slot)

    def save(self, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Overwrite this slot with the current game state and optionally new extra data.
        If no extra is given, the previously stored extra is preserved.

        Args:
            extra: New extra data dictionary. If None, the slot's current extra is used.
        """
        data = extra if extra is not None else self.extra
        save(self.slot, data=data)
        self.time = datetime.now()
        self.extra = data

    def update_extra(self, new_data: Dict[str, Any]) -> None:
        """
        Merge new_data into the existing extra dictionary and save the slot again.

        Args:
            new_data: Dictionary that will be merged with the current extra.
        """
        current = self.load_extra()
        current.update(new_data)
        self.save(extra=current)

    def __repr__(self) -> str:
        return f"<SaveSlot {self.slot} at {self.time.isoformat()}>"
