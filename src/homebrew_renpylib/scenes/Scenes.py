from typing import Any, Dict, List, Optional, Tuple
import random

from .Scene import Scene
from ..saves import Saves


class SceneSet:
    """
    A named collection of Scenes with associated weights.
    Each SceneSet can also have its own weight for prioritisation
    when multiple sets contain the same scene.

    Attributes:
        name: Human-readable identifier for the set.
        weight: Global weight of this set used for set selection.
        scenes: Dictionary mapping Scene -> weight (float).
    """

    def __init__(self, name: str, weight: float = 1.0):
        """
        Initialize a SceneSet.

        Args:
            name: Name of the set (e.g. 'forest_paths', 'coastal').
            weight: Default weight for this set when choosing between multiple sets.
        """
        self.name = name
        self.weight = weight
        self._scenes: Dict[str, Tuple[Scene, float]] = {}  # label -> (Scene, weight)

    def add_scene(self, scene: Scene, weight: float = 1.0) -> None:
        """
        Add or overwrite a scene in the set with a given weight.

        Args:
            scene: Scene object to add.
            weight: Weight for random selection (default 1.0).
        """
        self._scenes[scene.label] = (scene, weight)

    def remove_scene(self, label: str) -> bool:
        """
        Remove a scene by its label.

        Args:
            label: The scene label to remove.

        Returns:
            True if the scene was found and removed, False otherwise.
        """
        if label in self._scenes:
            del self._scenes[label]
            return True
        return False

    def update_weight(self, label: str, new_weight: float) -> bool:
        """
        Update the weight of a scene already in the set.

        Args:
            label: The scene label.
            new_weight: New weight value.

        Returns:
            True if updated, False if the scene was not found.
        """
        if label in self._scenes:
            scene, _ = self._scenes[label]
            self._scenes[label] = (scene, new_weight)
            return True
        return False

    def contains(self, label: str) -> bool:
        """
        Check if a scene (by label) belongs to this set.

        Args:
            label: Scene label.

        Returns:
            True if the scene is present.
        """
        return label in self._scenes

    def get_random_scene(self, exclude_label: Optional[str] = None) -> Optional[Scene]:
        """
        Pick a random scene from the set using the defined weights.
        Optionally exclude a scene (e.g. the current one) to avoid immediate repetition.

        Args:
            exclude_label: Label of a scene to exclude from the draw.

        Returns:
            A Scene or None if no valid scene is available.
        """
        candidates = [
            (scene, weight)
            for label, (scene, weight) in self._scenes.items()
            if label != exclude_label
        ]
        if not candidates:
            return None

        scenes, weights = zip(*candidates)
        return random.choices(scenes, weights=weights, k=1)[0]

    def get_scenes(self) -> List[Scene]:
        """
        Return a list of all Scenes in this set (without weights).

        Returns:
            List of Scene objects.
        """
        return [scene for scene, _ in self._scenes.values()]

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialise the SceneSet to a dictionary for saving.

        Returns:
            A JSON-serialisable dict.
        """
        return {
            "name": self.name,
            "weight": self.weight,
            "scenes": [
                {"label": scene.label, "weight": weight}
                for scene, weight in self._scenes.values()
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], scenes_library: Dict[str, Scene]) -> "SceneSet":
        """
        Reconstruct a SceneSet from a dictionary and a library of Scene objects.

        Args:
            data: Dictionary as produced by to_dict().
            scenes_library: Mapping of label -> Scene to rebuild references.

        Returns:
            A new SceneSet instance.
        """
        instance = cls(data["name"], data["weight"])
        for item in data["scenes"]:
            label = item["label"]
            if label in scenes_library:
                instance.add_scene(scenes_library[label], item["weight"])
        return instance


class SceneManager:
    """
    Manages multiple SceneSets and provides intelligent transitions:
    - Given the current scene, finds all sets containing it.
    - Selects one set based on set weights (or uniformly if none).
    - Draws a random next scene from the chosen set (excluding the current scene).
    - Can save/load its entire state via the Saves class.
    """

    def __init__(self):
        self._sets: Dict[str, SceneSet] = {}
        self._scene_library: Dict[str, Scene] = {}

    def add_set(self, set_obj: SceneSet) -> None:
        """
        Register a SceneSet.

        Args:
            set_obj: The SceneSet to add.
        """
        self._sets[set_obj.name] = set_obj

    def remove_set(self, name: str) -> bool:
        """
        Remove a SceneSet by name.

        Args:
            name: Name of the set to remove.

        Returns:
            True if removed, False if not found.
        """
        if name in self._sets:
            del self._sets[name]
            return True
        return False

    def get_set(self, name: str) -> Optional[SceneSet]:
        """
        Retrieve a SceneSet by name.

        Args:
            name: The set name.

        Returns:
            The matching SceneSet or None.
        """
        return self._sets.get(name)

    def get_all_sets(self) -> List[SceneSet]:
        """
        Return all registered SceneSets.

        Returns:
            List of SceneSet objects.
        """
        return list(self._sets.values())

    # ---------- SCENE LIBRARY (required for serialisation) ----------
    def register_scene(self, scene: Scene) -> None:
        """
        Register a Scene in the global library so it can be referenced later.

        Args:
            scene: Scene object.
        """
        self._scene_library[scene.label] = scene

    def get_scene_by_label(self, label: str) -> Optional[Scene]:
        """
        Find a registered Scene by label.

        Args:
            label: Scene label.

        Returns:
            Scene or None.
        """
        return self._scene_library.get(label)

    def get_next_scene(self, current_label: str) -> Optional[Scene]:
        """
        Based on the current scene, find all SceneSets that contain it,
        select one set (by weight or uniformly), and draw a random next scene
        from that set (excluding the current one).

        Args:
            current_label: Label of the scene the player is currently in.

        Returns:
            A Scene object for the next jump, or None if no valid transition found.
        """
        matching_sets = [
            s for s in self._sets.values() if s.contains(current_label)
        ]
        if not matching_sets:
            return None

        if len(matching_sets) == 1:
            chosen_set = matching_sets[0]
        else:
            weights = [s.weight for s in matching_sets]
            if all(w == 1.0 for w in weights):
                chosen_set = random.choice(matching_sets)
            else:
                chosen_set = random.choices(matching_sets, weights=weights, k=1)[0]

        next_scene = chosen_set.get_random_scene(exclude_label=current_label)
        return next_scene

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialise the entire manager state to a dictionary.

        Returns:
            A JSON-serialisable dict with sets and scene library (labels only for ref).
        """
        return {
            "sets": [s.to_dict() for s in self._sets.values()],
            "scene_library": [
                {"label": scene.label, "name": scene.name, "description": scene.description}
                for scene in self._scene_library.values()
            ]
        }

    def save_state(self, saves: Saves, slot_name: str) -> None:
        """
        Save the current SceneManager configuration into a save slot's extra info.
        Creates or updates the slot.

        Args:
            saves: Instance of the Saves manager.
            slot_name: The save slot name (e.g., '1-1').
        """
        existing = saves.find_by_slot(slot_name)
        data = self.to_dict()
        if existing:
            existing.update_extra({"scene_manager": data})
        else:
            saves.create(slot_name, extra={"scene_manager": data})

    def load_state(self, saves: Saves, slot_name: str) -> bool:
        """
        Load SceneManager configuration from a save slot's extra info.

        Args:
            saves: Instance of the Saves manager.
            slot_name: The save slot name.

        Returns:
            True if loading succeeded, False otherwise.
        """
        slot = saves.find_by_slot(slot_name)
        if not slot:
            return False
        extra = saves.get_save_extra_info(slot)
        data = extra.get("scene_manager")
        if not data:
            return False

        self._scene_library.clear()
        for lib_entry in data.get("scene_library", []):
            scene = Scene(
                label=lib_entry["label"],
                name=lib_entry.get("name"),
                description=lib_entry.get("description")
            )
            self._scene_library[scene.label] = scene

        self._sets.clear()
        for set_data in data.get("sets", []):
            sset = SceneSet.from_dict(set_data, self._scene_library)
            self._sets[sset.name] = sset

        return True
    
