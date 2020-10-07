# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Logger unit tests."""

# type annotations
from typing import Type

# standard libs
from io import StringIO
from string import ascii_letters
from dataclasses import dataclass

# internal libs
from logalpha.handler import StreamHandler
from logalpha.message import Message
from logalpha.level import Level, LEVELS
from logalpha.logger import Logger

# external libs
from hypothesis import given, assume, strategies as st


@dataclass
class InMemoryHandler(StreamHandler):
    """Messages written to in-memory `io.StringIO`."""

    resource: StringIO = None

    def format(self, message: Message) -> str:
        return f'{message.level.name}: {message.content}'


@given(st.text())
def test_level_filter(text: str) -> None:
    """Check levels are filtered."""

    log = Logger()
    for i, h_level in enumerate(LEVELS):

        resource = StringIO()
        log.handlers.clear()
        log.handlers.append(InMemoryHandler(level=h_level, resource=resource))

        for m_level in LEVELS:
            getattr(log, m_level.name.lower())(text)  # i.e., `log.debug('...')`

        expected = '\n'.join([f'{i_level.name}: {text}' for i_level in LEVELS[i:]])
        assert resource.getvalue().strip() == expected.strip()


@dataclass
class MessageWithTopic(Message):
    """A message with a topic."""
    level: Level
    content: str
    topic: str


class NamedLogger(Logger):
    """A logger using the FancyMessage."""

    Message: Type[Message] = MessageWithTopic

    def __init__(self, topic: str) -> None:
        """Assign callback to include `topic`."""
        super().__init__()
        self.callbacks['topic'] = lambda: topic


@dataclass
class DetailedHandler(InMemoryHandler):
    """Format messages with topic name."""

    def format(self, message: MessageWithTopic) -> str:
        return f'{message.level.name} [{message.topic}] {message.content}'


@given(topic=st.text(ascii_letters, min_size=1, max_size=10),
       handler_level=st.integers(min_value=0, max_value=4),
       message_level=st.integers(min_value=0, max_value=4))
def test_named_logger(topic: str, handler_level: int, message_level: int) -> None:
    """Test a derived logger with a named topic."""
    assume(handler_level <= message_level)  # NOTE: the message will not be filtered
    log = NamedLogger(topic)
    resource = StringIO()
    handler = DetailedHandler(level=LEVELS[handler_level], resource=resource)
    log.handlers.append(handler)
    getattr(log, LEVELS[message_level].name.lower())('message')
    assert resource.getvalue().strip() == f'{LEVELS[message_level].name} [{topic}] message'
