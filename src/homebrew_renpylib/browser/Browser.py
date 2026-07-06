from typing import List, Optional
from ..backend import goto_url

class Browser:
    """
    A simple browser abstraction that tracks navigation history.
    Uses the configured backend to open URLs.
    """

    def __init__(self):
        """
        Initialize the browser with an empty history.
        """
        self._history: List[str] = []
        self._current_index: int = -1  # -1 means no page is currently open

    def open(self, url: str) -> None:
        """
        Open a new URL and add it to the history.
        Any forward history beyond the current position is discarded.

        Args:
            url (str): The URL to open.
        """
        # Discard forward history
        if self._current_index < len(self._history) - 1:
            self._history = self._history[: self._current_index + 1]

        self._history.append(url)
        self._current_index = len(self._history) - 1
        goto_url(url)

    def go_back(self) -> Optional[str]:
        """
        Navigate back to the previous URL in the history.

        Returns:
            Optional[str]: The previous URL, or None if there is none.
        """
        if not self.can_go_back():
            return None
        self._current_index -= 1
        previous_url = self._history[self._current_index]
        goto_url(previous_url)
        return previous_url

    def go_forward(self) -> Optional[str]:
        """
        Navigate forward to the next URL in the history.

        Returns:
            Optional[str]: The next URL, or None if there is none.
        """
        if not self.can_go_forward():
            return None
        self._current_index += 1
        next_url = self._history[self._current_index]
        goto_url(next_url)
        return next_url

    def can_go_back(self) -> bool:
        """
        Check whether there is a previous page in the history.

        Returns:
            bool: True if a back navigation is possible.
        """
        return self._current_index > 0

    def can_go_forward(self) -> bool:
        """
        Check whether there is a forward page in the history.

        Returns:
            bool: True if a forward navigation is possible.
        """
        return self._current_index < len(self._history) - 1

    def get_current_url(self) -> Optional[str]:
        """
        Return the currently displayed URL, or None if no page has been opened.

        Returns:
            Optional[str]: The current URL.
        """
        if self._current_index == -1:
            return None
        return self._history[self._current_index]

    def get_history(self) -> List[str]:
        """
        Return a copy of the full browsing history.

        Returns:
            List[str]: A list of visited URLs in chronological order.
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """
        Clear all browsing history and reset the current page.
        """
        self._history.clear()
        self._current_index = -1
