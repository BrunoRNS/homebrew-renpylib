from typing import Dict, Optional, Any
from .DayGraph import DayGraph
from .DayNodeMeta import DayNodeMeta

class DayNode(metaclass=DayNodeMeta):
    """
    Base class for declarative day trees.

    Example
    -------
    class MyStory(DayNode):
        label = "morning"
        music = "morning.ogg"

        class Beach(DayNode):
            label = "beach"
            weight = 2
            music = "beach.ogg"
            extra = {"weather": "sunny"}

        class Forest(DayNode):
            label = "forest"
            weight = 1
            music = "forest.ogg"

            class Cave(DayNode):
                label = "cave"
                weight = 1
                terminal = "good_end"
    """
    label: Optional[str] = None
    weight: float = 1.0
    music: Optional[str] = None
    extra: Dict[str, Any] = {}
    terminal: Optional[str] = None

    @classmethod
    def to_graph(cls, default_terminal: str,
                 root_label: Optional[str] = None) -> DayGraph:
        """
        Convert this class hierarchy into a DayGraph.
        The top-level class becomes the root.
        """
        # Determine root label
        label = cls.label or cls.__name__.lower()
        graph = DayGraph(root_label or label, default_terminal)
        cls._add_to_graph(graph, parent_label=None)
        return graph

    @classmethod
    def _add_to_graph(cls, graph: DayGraph, parent_label: Optional[str] = None):
        """Recursively add this node and its children to the graph."""
        own_label = cls.label or cls.__name__.lower()
        if parent_label is not None:
            graph.add_edge(parent_label, own_label,
                           weight=cls.weight,
                           music=cls.music,
                           extra=cls.extra)
        if cls.terminal is not None:
            graph.set_terminal(own_label, cls.terminal)
            
        cls._children = getattr(cls, "_children", [])
        
        for child_cls in cls._children:
            child_cls._add_to_graph(graph, own_label)
    
