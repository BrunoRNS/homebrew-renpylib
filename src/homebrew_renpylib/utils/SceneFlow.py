from typing import Optional
from ..scenes import SceneManager, Scene

class SceneFlow:
    """
    Simplifies navigation using a SceneManager.
    Provides high‑level methods that internally use the manager.
    """

    def __init__(self, manager: SceneManager):
        """
        Args:
            manager: A fully configured SceneManager instance.
        """
        self.manager = manager

    def next_scene(self, current_label: str) -> Optional[Scene]:
        """
        Compute the next scene using the manager’s intelligent algorithm
        (searches sets containing current_label, picks a set by weight,
        then draws a scene from it, excluding the current one).

        Args:
            current_label: Label of the scene the player is in now.

        Returns:
            A Scene object ready for jump, or None if no transition exists.
        """
        return self.manager.get_next_scene(current_label)

    def jump_to_next(self, current_label: str) -> None:
        """
        Find the next scene and immediately jump to it.
        Does not return.

        Args:
            current_label: Current scene label.
        """
        scene = self.next_scene(current_label)
        if scene:
            scene.jump()
        # If no scene, we stay put (or raise an error – adapt as needed)

    def random_scene_from_set(self, set_name: str, exclude: Optional[str] = None) -> Optional[Scene]:
        """
        Draw a random scene from a specific SceneSet, optionally excluding one.

        Args:
            set_name: Name of the SceneSet.
            exclude: Label to exclude (e.g. the current scene).

        Returns:
            A Scene or None if the set doesn't exist or is empty after exclusion.
        """
        sset = self.manager.get_set(set_name)
        if not sset:
            return None
        return sset.get_random_scene(exclude_label=exclude)
