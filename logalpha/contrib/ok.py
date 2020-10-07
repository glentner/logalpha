# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.


"""Simple colorized Ok/Err logging setup."""

# type annotations
from __future__ import annotations
from typing import Callable

# standard libs
from dataclasses import dataclass

# internal libs
from logalpha.color import Color, ANSI_RESET
from logalpha.level import Level
from logalpha.message import Message
from logalpha.handler import StreamHandler
from logalpha.logger import Logger


LEVELS = Level.from_names(['Ok', 'Err'])
COLORS = Color.from_names(['green', 'red'])
OK = LEVELS[0]
ERR = LEVELS[1]


@dataclass
class OkayHandler(StreamHandler):
    """
    A standard message handler writes to <stderr> by default.
    Message format includes the level and the text.
    """

    def format(self, message: Message) -> str:
        """Format the message."""
        color = COLORS[message.level.value].foreground
        return f'{color}{message.level.name:<3}{ANSI_RESET} {message.content}'


class OkayLogger(Logger):
    """Logger with StandardMessage and StandardHandler."""

    levels = LEVELS
    colors = COLORS

    # stubs for instrumented level methods
    ok: Callable[[str], None]
    err: Callable[[str], None]
