import random
from typing import List, TypeVar, Optional

T = TypeVar('T')

class Probability:
    """
    Static utilities for weighted random selection.
    """

    @staticmethod
    def weighted_choice(
        items: List[T],
        weights: List[float]
    ) -> T:
        """
        Pick one item from the list based on the provided weights.

        Args:
            items: List of items to choose from.
            weights: Corresponding weights (positive numbers).

        Returns:
            The chosen item.

        Raises:
            ValueError: If lengths differ or weights are empty.
        """
        if not items or len(items) != len(weights):
            raise ValueError("Items and weights must be non-empty and of equal length.")
        return random.choices(items, weights=weights, k=1)[0]

    @staticmethod
    def weighted_choice_with_exclusion(
        items: List[T],
        weights: List[float],
        exclude: Optional[T] = None
    ) -> Optional[T]:
        """
        Pick an item, optionally excluding one element.

        Args:
            items: List of items.
            weights: Corresponding weights.
            exclude: Item to exclude from the draw.

        Returns:
            Chosen item or None if no valid candidate remains.
        """
        candidates = [
            (it, w) for it, w in zip(items, weights) if it != exclude
        ]
        if not candidates:
            return None
        sel_items, sel_weights = zip(*candidates)
        return random.choices(sel_items, weights=sel_weights, k=1)[0]

    @staticmethod
    def shuffle_weighted(
        items: List[T],
        weights: List[float]
    ) -> List[T]:
        """
        Return a new list with items ordered by weighted random
        without replacement (first item drawn, then removed, etc.).

        Note: This is a straightforward implementation
        (not the most efficient for large lists).

        Args:
            items: List of items.
            weights: Corresponding weights.

        Returns:
            A shuffled list.
        """
        remaining = list(zip(items, weights))
        result: List[T] = []
        while remaining:
            sel_items, sel_weights = zip(*remaining)
            chosen = random.choices(sel_items, weights=sel_weights, k=1)[0]
            idx = sel_items.index(chosen)
            result.append(chosen)
            remaining.pop(idx)
        return result