from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import random

from ..backend import (
    list_saves,
    save,
    jump_to_scene,
    load_save,
    get_save_data,
)

from .SaveSlot import SaveSlot

class Saves:
    """
    Manager for all save slots. Provides methods to query, create, delete,
    and manipulate game saves.
    """

    def __init__(self):
        """
        Initialize the Saves manager.
        
        self.actual_saves might not be up-to-date 
        if saves are modified externally.
        
        Use update_database() to refresh.
        """
        
        self.actual_saves = self._fetch_all()
        

    def _fetch_all(self) -> List[SaveSlot]:
        """
        Retrieve all existing saves from the engine and convert them to SaveSlot objects.

        Returns:
            A list of SaveSlot instances.
        """
        raw_saves: List[Tuple[str, Dict[Any, Any], datetime, bytes]] = list_saves()  # Expected to return a list of dicts: {"slot", "time", "extra"}
        slots: List[SaveSlot] = []
        for item in raw_saves:
            slot: str = item[0]
            time: Optional[datetime] = item[2]
            extra: Optional[Dict[str, Any]] = item[1]
            slots.append(SaveSlot(slot, time, extra))
        return slots

    def get_all(self) -> List[SaveSlot]:
        """
        Get a list of all save slots.

        Returns:
            List of SaveSlot objects.
        """
        return self._fetch_all()

    def get_first(self) -> Optional[SaveSlot]:
        """
        Get the oldest save (earliest timestamp).

        Returns:
            The first SaveSlot, or None if no saves exist.
        """
        all_slots = self._fetch_all()
        if not all_slots:
            return None
        return min(all_slots, key=lambda s: s.time)

    def get_last(self) -> Optional[SaveSlot]:
        """
        Get the newest save (latest timestamp).

        Returns:
            The last SaveSlot, or None if no saves exist.
        """
        all_slots = self._fetch_all()
        if not all_slots:
            return None
        return max(all_slots, key=lambda s: s.time)

    def get_k_first(self, k: int) -> List[SaveSlot]:
        """
        Get the K oldest saves, sorted by time ascending.

        Args:
            k: Number of saves to retrieve.

        Returns:
            A list of up to K oldest SaveSlot objects.
        """
        sorted_slots = sorted(self._fetch_all(), key=lambda s: s.time)
        return sorted_slots[:k]

    def get_k_last(self, k: int) -> List[SaveSlot]:
        """
        Get the K most recent saves, sorted by time ascending.

        Args:
            k: Number of saves to retrieve.

        Returns:
            A list of up to K newest SaveSlot objects (oldest first among them).
        """
        sorted_slots = sorted(self._fetch_all(), key=lambda s: s.time)
        return sorted_slots[-k:] if k <= len(sorted_slots) else sorted_slots

    def get_random(self) -> Optional[SaveSlot]:
        """
        Pick a random save slot.

        Returns:
            A randomly chosen SaveSlot, or None if no saves exist.
        """
        all_slots = self._fetch_all()
        if not all_slots:
            return None
        return random.choice(all_slots)

    def find_by_slot(self, name: str) -> Optional[SaveSlot]:
        """
        Find a save by its slot name.

        Args:
            name: The slot identifier.

        Returns:
            The matching SaveSlot, or None if not found.
        """
        for slot in self._fetch_all():
            if slot.slot == name:
                return slot
        return None

    def create(self, slot: str, extra: Optional[Dict[str, Any]] = None) -> SaveSlot:
        """
        Create a new save with the current game state and attach extra data.

        Args:
            slot: The slot name to save to.
            extra: Optional dictionary of extra information.

        Returns:
            The newly created SaveSlot object.
        """
        save(slot, data=extra or {})
        new_slot = SaveSlot(slot, datetime.now(), extra or {})
        return new_slot

    def delete_all(self) -> None:
        """
        Delete all existing save slots.
        """
        for slot in self._fetch_all():
            slot.delete()

    def save_and_jump(self, slot: str, extra: Optional[Dict[str, Any]], label: str) -> None:
        """
        Save the current state and immediately jump to a new scene (label).

        Args:
            slot: The save slot name.
            extra: Extra data to store with the save.
            label: The Ren'Py label to jump to after saving.
        """
        self.create(slot, extra)
        jump_to_scene(label)
        return
    
    def load_save(self, save: SaveSlot) -> None:
        """
        Load the game state from the given SaveSlot.

        Args:
            save: SaveSlot object representing the save to load.
        """
        load_save(save.slot)

    def get_save_extra_info(self, save: SaveSlot) -> Dict[str, Any]:
        """
        Retrieve the extra information stored in a save slot without loading it.

        Args:
            save: SaveSlot to query.

        Returns:
            Dictionary with the slot's extra data.
        """
        return get_save_data(save.slot)

    def update_database(self) -> None:
        """
        Force a refresh of the internal cache, synchronizing it with the actual
        save system. Useful if saves were modified externally (e.g., by another
        Saves instance or directly via engine commands).
        """
        self.actual_saves = self._fetch_all()
        
