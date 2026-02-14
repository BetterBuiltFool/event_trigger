from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class Scheduler(Protocol):
    """
    Object used for following through on callback registered to events.
    """

    def schedule(self, callback: Callable, *args, **kwds) -> None:
        """
        Schedules a callback to be called.

        :param callback: Method or function to be scheduled.
        :type callback: Callable
        :param args: Pass-through positional arguments for _callback_.
        :type args: Any
        :param kwds: Pass-through keyword arguments for _callback_.
        :type kwds: Any
        """
        ...


class SyncScheduler:

    def schedule(self, callback: Callable, *args, **kwds) -> None:
        callback(*args, **kwds)


_active_scheduler: Scheduler = SyncScheduler()


def schedule(callback: Callable, *args, **kwds) -> None:
    _active_scheduler.schedule(callback, *args, **kwds)
