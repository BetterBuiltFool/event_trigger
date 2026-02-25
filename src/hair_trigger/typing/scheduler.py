from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class Scheduler(Protocol):
    """
    Object used for following through on func registered to events.
    """

    def schedule(self, func: Callable, *args, **kwds) -> None:
        """
        Schedules a func to be called.

        :param func: Method or function to be scheduled.
        :type func: Callable
        :param args: Pass-through positional arguments for _func_.
        :type args: Any
        :param kwds: Pass-through keyword arguments for _func_.
        :type kwds: Any
        """
        ...
