from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class Notifier(Protocol):

    def call(self, callback: Callable, *args, **kwds) -> None: ...
