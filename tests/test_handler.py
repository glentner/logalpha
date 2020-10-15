# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Handler unit tests."""

# type annotations
from typing import Dict

# standard libs
from io import StringIO
from queue import Queue
from dataclasses import dataclass

# internal libs
from logalpha.handler import Handler, StreamHandler
from logalpha.message import Message
from logalpha.level import LEVELS
from logalpha.logger import Logger

# external libs
from hypothesis import given, strategies as st


@dataclass
class InMemoryHandler(StreamHandler):
    """Messages written to <stderr>."""

    resource: StringIO = None

    def format(self, message: Message) -> str:
        return f'{message.level.name}: {message.content}'


def test_init() -> None:
    """Check level and resource."""
    for level in LEVELS:
        resource = StringIO()
        handler = InMemoryHandler(level=level, resource=resource)
        assert handler.level is level
        assert handler.resource is resource


@given(st.text())
def test_format(text: str) -> None:
    """Check formatting occurs."""
    for level in LEVELS:
        handler = InMemoryHandler(level=level, resource=StringIO())
        handler.write(Message(level=level, content=text))
        assert handler.resource.getvalue().strip() == f'{level.name}: {text}'.strip()


@dataclass
class QueueHandler(Handler):
    """Test overriding method behaviors."""

    resource: Queue = None

    def write(self, message: Message) -> None:
        """Put message on queue."""
        self.resource.put(self.format(message))

    def format(self, message: Message) -> Dict[str, str]:
        """Turn message into dictionary."""
        return {'level': message.level.name, 'content': message.content}


def test_derived_handler() -> None:
    """Test derived queue handler."""

    resource = Queue()
    handler = QueueHandler(level=LEVELS[1], resource=resource)
    log = Logger()
    log.handlers.append(handler)

    getattr(log, LEVELS[0].name.lower())('message')  # send to DEBUG
    assert resource.empty()

    for level in LEVELS[1:]:
        getattr(log, level.name.lower())('message')  # send to INFO
        assert not resource.empty()
        message = resource.get()
        assert message == {'level': level.name, 'content': 'message'}
        assert resource.empty()
