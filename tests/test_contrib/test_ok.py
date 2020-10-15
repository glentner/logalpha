# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Units tests for OkayLogger and OkayHandler."""


# standard libs
from io import StringIO
from string import ascii_letters

# internal libs
from logalpha.color import ANSI_RESET
from logalpha.contrib.ok import OkayHandler, OkayLogger

# external libs
from hypothesis import given, strategies as st


@given(handler_level=st.integers(min_value=0, max_value=1),
       message_level=st.integers(min_value=0, max_value=1),
       text=st.text(ascii_letters, min_size=1, max_size=100))
def test_logger(handler_level: int, message_level: int, text: str) -> None:
    """Test logger and handler construction with filtering and formatting."""
    log = OkayLogger()
    buffer = StringIO()
    handler = OkayHandler(level=log.levels[handler_level], resource=buffer)
    log.handlers.clear()
    log.handlers.append(handler)
    getattr(log, log.levels[message_level].name.lower())(text)
    if message_level < handler_level:
        assert buffer.getvalue().strip() == ''
    else:
        color = log.colors[message_level].foreground
        level = log.levels[message_level].name
        expected = f'{color}{level:<3}{ANSI_RESET} {text}'
        assert buffer.getvalue().strip() == expected
