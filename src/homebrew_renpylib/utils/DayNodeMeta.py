from .DayNode import DayNode

from typing import Any, Dict, Tuple


class DayNodeMeta(type):
    """Metaclass to collect child nodes."""
    
    def __new__(mcs, name: str, bases: Tuple[Any], namespace: Dict[str, Any]):
        cls = super().__new__(mcs, name, bases, namespace)
        cls._children = [] # type: ignore
        for _, attr_value in namespace.items():
            if isinstance(attr_value, type) and issubclass(attr_value, DayNode):
                cls._children.append(attr_value) # type: ignore
        return cls

