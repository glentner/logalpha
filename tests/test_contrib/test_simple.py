# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Units tests for logalpha.contrib.simple interface."""


# standard libs
from io import StringIO
from string import ascii_letters

# internal libs
from logalpha.color import ANSI_RESET
from logalpha.contrib.simple import SimpleHandler, SimpleLogger, ColorHandler

# external libs
from hypothesis import given, strategies as st


@given(handler_level=st.integers(min_value=0, max_value=1),
       message_level=st.integers(min_value=0, max_value=1),
       text=st.text(ascii_letters, min_size=1, max_size=100),
       topic=st.text(ascii_letters, min_size=1, max_size=10))
def test_logger(handler_level: int, message_level: int, text: str, topic: str) -> None:
    """Test logger and handler construction with filtering and formatting."""
    log = SimpleLogger(topic)
    buffer_1 = StringIO()
    buffer_2 = StringIO()
    SimpleLogger.handlers.clear()
    SimpleLogger.handlers.extend([SimpleHandler(level=log.levels[handler_level], resource=buffer_1),
                                  ColorHandler(level=log.levels[handler_level], resource=buffer_2)])
    getattr(log, log.levels[message_level].name.lower())(text)
    if message_level < handler_level:
        assert buffer_1.getvalue().strip() == ''
        assert buffer_2.getvalue().strip() == ''
    else:
        color = log.colors[message_level].foreground
        level = log.levels[message_level].name
        expected_1 = f'{level:<8} [{topic}] {text}'
        expected_2 = f'{color}{level:<8}{ANSI_RESET} [{topic}] {text}'
        assert buffer_1.getvalue().strip() == expected_1
        assert buffer_2.getvalue().strip() == expected_2
