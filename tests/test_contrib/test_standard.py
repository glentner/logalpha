# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Units tests for StandardLogger and StandardHandler."""


# standard libs
from io import StringIO
from string import ascii_letters

# internal libs
from logalpha.contrib.standard import StandardHandler, StandardLogger, HOST

# external libs
from hypothesis import given, strategies as st


@given(topic=st.text(ascii_letters, min_size=1, max_size=10),
       handler_level=st.integers(min_value=0, max_value=4),
       message_level=st.integers(min_value=0, max_value=4),
       text=st.text(ascii_letters, min_size=1, max_size=100))
def test_logger(topic: str, handler_level: int, message_level: int, text: str) -> None:
    """Test logger and handler construction with filtering and formatting."""
    log = StandardLogger(topic)
    buffer = StringIO()
    handler = StandardHandler(level=log.levels[handler_level], resource=buffer)
    log.handlers.clear()
    log.handlers.append(handler)
    getattr(log, log.levels[message_level].name.lower())(text)
    if message_level < handler_level:
        assert buffer.getvalue().strip() == ''
    else:
        expected = f' {HOST} {log.levels[message_level].name:<8} [{topic}] {text}'
        assert buffer.getvalue().strip().endswith(expected)
