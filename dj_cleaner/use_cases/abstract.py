"""Contains the abstract base class all use-cases must inherit."""
from abc import ABC, abstractmethod


class UseCase(ABC):
    """Abstract base class for all use-cases."""

    def __call__(self) -> None:
        """Execute the use-case."""
        self._execute()

    @abstractmethod
    def _execute(self) -> None:
        """Execute the use-case."""
