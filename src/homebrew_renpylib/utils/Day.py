from typing import List, Optional, Dict, Any
from ..saves import Saves
from ..scenes import Scene

from .SaveSerializer import SaveSerializer

class Day:
    """
    Represents a single day, defined by its starting scene.
    """

    def __init__(self, label: str, name: Optional[str] = None, extra: Optional[Dict[str, Any]] = None):
        self.label = label
        self.name = name or f"Day {label}"
        self.extra = extra or {}

    def __repr__(self):
        return f"<Day '{self.name}' start='{self.label}'>"


class DayManager:
    """
    Manages a list of Day objects representing the game's day cycle.
    Each day has a starting scene. When a day ends, the manager
    automatically advances to the next day, removes the completed one,
    and saves progress.
    """

    def __init__(self, saves: Saves, auto_save_slot: str = "day_cycle"):
        """
        Args:
            saves: Saves manager instance.
            auto_save_slot: Slot used to persist the DayManager state.
        """
        self.saves = saves
        self.auto_save_slot = auto_save_slot
        self.days: List[Day] = []
        self.current_day: Optional[Day] = None

    def add_day(self, label: str, name: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Schedule a new day.

        Args:
            label: Starting scene label for this day.
            name: Optional display name.
            extra: Optional extra data.
        """
        day = Day(label, name, extra)
        self.days.append(day)

    def start_next_day(self) -> None:
        """
        Mark the current day as finished, remove it from the queue,
        save the updated state, and jump to the next day’s starting scene.
        If no days remain, this method does nothing (game over / free roam).
        """
        if self.current_day and self.days and self.days[0] == self.current_day:
            self.days.pop(0)

        if not self.days:
            self.current_day = None
            return

        self.current_day = self.days[0]
        self._auto_save()
        scene = Scene(self.current_day.label)
        scene.jump()

    def peek_next_day(self) -> Optional[Day]:
        """
        Return the next day without advancing.

        Returns:
            The next Day, or None if the queue is empty.
        """
        
        if self.days:
            return self.days[0]
        return None

    def _auto_save(self) -> None:
        """
        Persist the current state (list of remaining days and current day)
        into the configured save slot.
        """
        
        data: Dict[str, Any] = {
            "days": [{"label": d.label, "name": d.name, "extra": d.extra} for d in self.days],
            "current_day_label": self.current_day.label if self.current_day else None,
        }
        serializer = SaveSerializer(self.saves)
        serializer.save_object(self.auto_save_slot, "day_manager", data)

    def load_state(self) -> bool:
        """
        Load the DayManager state from the auto_save_slot.

        Returns:
            True if a saved state was found and restored.
        """
        
        serializer = SaveSerializer(self.saves)
        data = serializer.load_object(self.auto_save_slot, "day_manager")
        if not data:
            return False
        self.days = [
            Day(d["label"], d.get("name"), d.get("extra"))
            for d in data["days"]
        ]
        current_label = data.get("current_day_label")
        if current_label:
            for day in self.days:
                if day.label == current_label:
                    self.current_day = day
                    break
        return True
