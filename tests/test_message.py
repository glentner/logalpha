# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Message unit tests."""

# standard libs
from string import ascii_letters

# internal libs
from logalpha.message import Message
from logalpha.level import LEVELS

# external libs
from hypothesis import given, strategies as st


@given(content=st.text(ascii_letters))
def test_init(content: str) -> None:
    """Check initialization."""
    for level in LEVELS:
        message = Message(level=level, content=content)
        assert message.level is level
        assert message.content is content
