# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.


"""Logger implementations."""

# type annotations
from __future__ import annotations
from typing import List, Dict, Callable, Any, Type

# standard libs
import functools

# internal libs
from .level import Level, DEBUG, INFO, WARNING, ERROR, CRITICAL
from .color import Color, BLUE, GREEN, YELLOW, RED, MAGENTA
from .handler import Handler
from .message import Message


# dictionary of parameter-less functions
CallbackMethod = Callable[[], Any]


class Logger:
    """
    Base logging interface.
    """

    # default configuration
    levels: List[Level] = [DEBUG, INFO, WARNING, ERROR, CRITICAL]
    colors: List[Color] = [BLUE, GREEN, YELLOW, RED, MAGENTA]
    handlers: List[Handler] = []

    callbacks: Dict[str, CallbackMethod] = dict()

    # redefine to construct with callbacks
    Message: Type[Message] = Message

    def __init__(self) -> None:
        """Setup instance; define level methods."""
        self._instrument_level_methods()

    def write(self, level: Level, content: Any) -> None:
        """Publish `message` to all `handlers`."""
        message = self.Message(level=level, content=content, **self._evaluate_callbacks())  # noqa: args
        for handler in self.handlers:
            if message.level >= handler.level:
                handler.write(message)

    def _evaluate_callbacks(self) -> Dict[str, Any]:
        """Evaluates all methods in `callbacks` dictionary."""
        return dict(zip(self.callbacks.keys(), map(lambda method: method(), self.callbacks.values())))

    def _instrument_level_methods(self) -> None:
        """Create member functions for all levels."""
        for level in self.levels:
            method = functools.partial(self.write, level)
            method.__doc__ = f'Alias to {self.__class__.__name__}.write(level={level}, content=...)'
            setattr(self, level.name.lower(), method)
