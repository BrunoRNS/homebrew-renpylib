from typing import Dict, List, Optional, Any, Set, Tuple, Callable, Union
import random
from .Day import DayManager, Day


class DayGraph:
    """
    Full-featured story graph for day-based narratives.

    Features
    --------
    - Weighted edges with music and extra metadata.
    - CRUD operations at runtime.
    - Terminal handling: custom final labels, automatic joining of all ends.
    - Path queries (all paths, leaves, ancestors, etc.).
    - Persistence helpers (store graph structure in a save slot).
    - Fluent interface for building.

    Basic usage
    -----------
        graph = DayGraph("morning")
        graph.add_child("morning", "beach", weight=2, music="beach.ogg")
        graph.add_children("beach", [
            ("cave", 1, "cave.ogg"),
            ("cliff", 1, None, {"wind": "strong"})
        ])
        graph.set_terminal("cave", "game_over_good")
        graph.join_ends("the_end")

        # In game loop:
        graph.advance("morning", day_manager, music_player)
    """
    
    def __init__(self, root: str, default_terminal: str = "fim"):
        """
        Args:
            root: Label of the very first day.
            default_terminal: Default label used when a leaf has no custom terminal.
        """
        
        self.root = root
        self.default_terminal = default_terminal
        
        self._edges: Dict[str, List[Dict[str, Any]]] = {}
        self._parents: Dict[str, str] = {}
        self._terminal_map: Dict[str, Optional[str]] = {}
        self._current_path: List[str] = []

    def add_edge(
        self, parent: str, child: str,
        weight: float = 1.0,
        music: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> None:
        if parent not in self._edges:
            self._edges[parent] = []
        self._edges[parent].append({
            "target": child,
            "weight": weight,
            "music": music,
            "extra": extra or {}
        })
        self._parents[child] = parent

    def add_children(
        self,
        parent: str,
        children: List[Union[Tuple[str, float, Optional[str], Optional[Dict[str, Any]]],
                             Tuple[str, float, Optional[str]],
                             Tuple[str, float],
                             str]]
    ) -> None:
        """
        Add multiple children to a parent. Each child can be:
            - a string (weight=1.0, no music/extra)
            - a tuple (label, weight)
            - a tuple (label, weight, music)
            - a tuple (label, weight, music, extra)
        """
        for child in children:
            if isinstance(child, str):
                lbl, w, m, ex = child, 1.0, None, None
            else:
                lbl = child[0]
                w = child[1] if len(child) > 1 else 1.0
                m = child[2] if len(child) > 2 else None
                ex = child[3] if len(child) > 3 else None
            self.add_edge(parent, lbl, weight=w, music=m, extra=ex)

    def remove_node(self, node: str) -> None:
        """Delete a node and all its incident edges.
        If the node is the root, the graph becomes empty (must set a new root).
        """
        if node == self.root:
            self.root = None
        
        self._edges.pop(node, None)
        parent = self._parents.pop(node, None)
        if parent and parent in self._edges:
            self._edges[parent] = [
                e for e in self._edges[parent] if e["target"] != node
            ]
            if not self._edges[parent]:
                del self._edges[parent]
        for child, par in list(self._parents.items()):
            if par == node:
                del self._parents[child]
        self._terminal_map.pop(node, None)

    def rename_node(self, old: str, new: str) -> None:
        """Rename a node globally (all edges, parent refs, terminal map)."""
        if old == self.root:
            self.root = new
        if old in self._edges:
            self._edges[new] = self._edges.pop(old)
        for _, edges in self._edges.items():
            for e in edges:
                if e["target"] == old:
                    e["target"] = new
        for child, par in list(self._parents.items()):
            if par == old:
                self._parents[child] = new
        if old in self._parents:
            self._parents[new] = self._parents.pop(old)
        if old in self._terminal_map:
            self._terminal_map[new] = self._terminal_map.pop(old)

    def get_children(self, node: str) -> List[Dict[str, Any]]:
        """Return outgoing edges (list of dicts with target, weight, music, extra)."""
        return self._edges.get(node, [])

    def get_parent(self, node: str) -> Optional[str]:
        """Return the parent of a node, or None if root or not present."""
        return self._parents.get(node)

    def get_siblings(self, node: str) -> List[str]:
        """Return labels of all other children of the same parent."""
        parent = self.get_parent(node)
        if parent is None:
            return []
        return [e["target"] for e in self.get_children(parent) if e["target"] != node]

    def get_edge_info(self, parent: str, child: str) -> Optional[Dict[str, Any]]:
        """Return the edge dict from parent to child, or None."""
        for e in self.get_children(parent):
            if e["target"] == child:
                return e
        return None

    def update_edge(self, parent: str, child: str,
                    weight: Optional[float] = None,
                    music: Optional[Union[str, bool]] = False,
                    extra: Optional[Dict[str, Any]] = None) -> bool:
        """
        Modify an existing edge. music=False means leave unchanged; music=None means remove.
        Returns True if the edge was found and updated.
        """
        for e in self._edges.get(parent, []):
            if e["target"] == child:
                if weight is not None:
                    e["weight"] = weight
                if music is not False:
                    e["music"] = music
                if extra is not None:
                    e["extra"] = extra
                return True
        return False

    def remove_edge(self, parent: str, child: str) -> bool:
        """Remove the edge from parent to child. Also removes orphaned node unless
        it has another parent."""
        if parent not in self._edges:
            return False
        before = len(self._edges[parent])
        self._edges[parent] = [e for e in self._edges[parent] if e["target"] != child]
        if len(self._edges[parent]) == before:
            return False
        if not self._edges[parent]:
            del self._edges[parent]
            
        return True

    def set_terminal(self, node: str, label: Optional[str] = None) -> None:
        """
        Mark a node as terminal. If label is provided, that's where the story
        ends when reaching this node. If label is None, it resets to default.
        """
        self._terminal_map[node] = label

    def get_terminal(self, node: str) -> Optional[str]:
        """Return the terminal label for a node, or None if not set."""
        return self._terminal_map.get(node)

    def is_terminal(self, node: str) -> bool:
        """A node is terminal if it has no children or has been explicitly set."""
        if node in self._terminal_map:
            return True
        return node not in self._edges or len(self._edges[node]) == 0

    def get_leaves(self) -> List[str]:
        """Return all leaf nodes (no children)."""
        return [node for node in self._all_nodes() if not self.get_children(node)]

    def join_ends(self, target_label: str = "fim",
                  edge_weight: float = 1.0,
                  music: Optional[str] = None) -> None:
        """
        Connect every current leaf node to a common final node.
        Leaves that already have a custom terminal are skipped.
        """
        leaves = self.get_leaves()
        for leaf in leaves:
            if leaf in self._terminal_map:
                continue
            self.add_edge(leaf, target_label, weight=edge_weight, music=music)
            
        self.set_terminal(target_label)

    def _all_nodes(self) -> Set[str]:
        """Return set of all node labels."""
        nodes: Set[str] = set()
        if self.root:
            nodes.add(self.root)
        for parent, edges in self._edges.items():
            nodes.add(parent)
            for e in edges:
                nodes.add(e["target"])
        return nodes

    def get_all_nodes(self) -> List[str]:
        """Return sorted list of all node labels."""
        return sorted(self._all_nodes())

    def get_path_to(self, target: str) -> Optional[List[str]]:
        """Return the path from root to target (if target reachable)."""
        path: List[str] = []
        current = target
        while current is not None:
            path.append(current)
            current = self.get_parent(current)
            if current == self.root:
                if self.root is not None:
                    path.append(self.root)
                else:
                    return None
                break
        path.reverse()
        if path[0] != self.root:
            return None
        return path

    def get_all_paths(self) -> List[List[str]]:
        """Return all possible paths from root to every leaf."""
        result: List[List[str]] = []
        def dfs(node: str, path: List[str]):
            path.append(node)
            children = self.get_children(node)
            if not children:
                result.append(path.copy())
            else:
                for child in children:
                    dfs(child["target"], path)
            path.pop()
        if self.root:
            dfs(self.root, [])
        return result

    def get_random_path(self) -> Optional[List[str]]:
        """Traverse randomly according to weights, return the resulting path."""
        if not self.root:
            return None
        path = [self.root]
        current = self.root
        while True:
            children = self.get_children(current)
            if not children:
                break
            targets = [c["target"] for c in children]
            weights = [c["weight"] for c in children]
            next_node = random.choices(targets, weights=weights, k=1)[0]
            path.append(next_node)
            current = next_node
        return path

    def _pick_next(self, current_node: str) -> Optional[Dict[str, Any]]:
        """Choose next day using weights. Returns None if terminal."""
        if self.is_terminal(current_node):
            return None
        children = self.get_children(current_node)
        if not children:
            return None
        _ = [c["target"] for c in children]
        weights = [c["weight"] for c in children]
        idx = random.choices(range(len(children)), weights=weights, k=1)[0]
        return dict(children[idx])

    def advance(self, current_label: str,
                day_manager: DayManager,
                music_player: Optional[Any] = None,
                on_terminal: Optional[Callable[[str], None]] = None) -> None:
        """
        End the current day and move to the next. Updates save and plays music.
        If the node is terminal, jumps to the terminal label (custom or default).
        The optional on_terminal callback is called with the terminal label before jumping.

        Args:
            current_label: The day that just finished.
            day_manager: A DayManager instance.
            music_player: Object with play(file, loop=True).
            on_terminal: Callback(label) invoked when reaching a terminal.
        """
        
        next_info = None
        term_label = self._terminal_map.get(current_label)
        if term_label is not None:
            next_label = term_label
        else:
            next_info = self._pick_next(current_label)
            if next_info is None:
                next_label = self.default_terminal
            else:
                next_label = next_info["target"]

        music = next_info.get("music") if next_info else None
        extra: Dict[str, Any] = next_info.get("extra", {}).copy() if next_info else {}

        if self._current_path and self._current_path[-1] == current_label:
            self._current_path.pop()
        self._current_path.append(next_label)
        extra["_path"] = self._current_path.copy()

        day_manager.days.clear()
        day_manager.days.append(Day(next_label, name=next_label, extra=extra))
        day_manager.current_day = None

        if music and music_player:
            music_player.play(music, loop=True)

        if term_label is not None or not self.get_children(next_label):
            if on_terminal:
                on_terminal(next_label)

        day_manager.start_next_day()

    def start(self, day_manager: DayManager,
              music_player: Optional[Any] = None) -> None:
        """Begin a new game from the root, saving state."""
        
        if not self.root:
            raise ValueError("Cannot start DayGraph: root is not set.")
        
        self._current_path = [self.root]
        day_manager.days.clear()
        day_manager.days.append(Day(self.root, name=self.root, extra={"_path": [self.root]}))
        day_manager.current_day = None
        day_manager._auto_save() # type: ignore
        day_manager.start_next_day()

    def restore_path(self, day_manager: DayManager) -> bool:
        """After loading a save, restore the current path from extra data."""
        if day_manager.current_day:
            extra = day_manager.current_day.extra
            if "_path" in extra:
                self._current_path = extra["_path"]
                return True
        return False

    # ------------------------------------------------------------------
    # Persistence of graph structure (optional)
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the graph structure (edges, terminals) to a JSON-friendly dict."""
        edges: Dict[str, List[Dict[str, Any]]] = {}
        for parent, children in self._edges.items():
            edges[parent] = []
            for e in children:
                edges[parent].append({
                    "target": e["target"],
                    "weight": e["weight"],
                    "music": e["music"],
                    "extra": e["extra"]
                })
        return {
            "root": self.root,
            "default_terminal": self.default_terminal,
            "edges": edges,
            "terminal_map": self._terminal_map
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DayGraph":
        """Reconstruct a DayGraph from a dictionary."""
        obj = cls(data["root"], data.get("default_terminal", "fim"))
        for parent, children in data.get("edges", {}).items():
            for e in children:
                obj.add_edge(parent, e["target"],
                             weight=e.get("weight", 1.0),
                             music=e.get("music"),
                             extra=e.get("extra"))
        obj._terminal_map = data.get("terminal_map", {})
        return obj
    
