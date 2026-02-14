from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TYPE_CHECKING
from weakref import ref, WeakKeyDictionary


if TYPE_CHECKING:
    pass


class _Sentinel:
    pass


SENTINEL = _Sentinel()


class Event[T](ABC):

    def __init__(self, instance: T) -> None:
        self._instance = ref(instance)
        self.listeners: WeakKeyDictionary[Any, list[Callable]] = WeakKeyDictionary()

    @property
    def instance(self) -> T | None:
        """
        The owning instance of the event.

        If the instance has expired, returns `None`.
        """
        return self._instance()

    @abstractmethod
    def trigger(self, *args, **kwds) -> None:
        self._notify(*args, **kwds)

    def _register(self, caller, listener: Callable):
        listeners = self.listeners.setdefault(caller, [])
        # TODO Test if method, keep methods and function in two different sets?
        listeners.append(listener)

    def _deregister(self, listener: Callable):
        for caller, listeners in self.listeners.items():
            if listener in listeners:
                listeners.remove(listener)
                # Note: if a listener managed to get in there multiple times,
                # this will only remove one occurence.
                # If that happens, though, something went horribly wrong.
                # See you in 2 years!
                break

    def _notify(self, *args, **kwds) -> None:
        """
        Calls all registered listeners, passing along the args and kwds.
        This is never called directly, the instance event subclass will have its own
        defined call method that defines its parameters, which are passed on to the
        listeners.
        """
        pass
