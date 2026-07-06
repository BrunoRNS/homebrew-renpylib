from typing import Optional, Dict, Any

from ..backend import jump_to_scene

class Scene:
    """
    Represents a single scene (Ren'Py label) with optional metadata.

    Attributes:
        label: The Ren'Py label name used for jumping.
        name: A human-readable name for the scene (defaults to label if None).
        description: An optional short description.
        extra: A dictionary for any additional data the developer wants to attach.
    """

    def __init__(
        self,
        label: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        self.label = label
        self.name = name if name is not None else label
        self.description = description
        self.extra = extra or {}

    def jump(self) -> None:
        """
        Jump to this scene immediately. Does not return.
        """
        jump_to_scene(self.label)

    def __repr__(self) -> str:
        return f"<Scene '{self.name}' ({self.label})>"
