from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from hair_trigger.event import Event


class Scheduler(Protocol):
    """
    Object used for following through on func registered to events.
    """

    def schedule(self, event: Event, *args, **kwds) -> None:
        """
        Schedules a event to be triggered.

        :param event: Event to be scheduled.
        :param args: Pass-through positional arguments for _event_.
        :param kwds: Pass-through keyword arguments for _event_.
        """
        ...

    def pump(self) -> None:
        """
        Processes all pending events, if any.
        Will attempt to run until backlog is cleared.
        """
        ...
