# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Color unit tests."""

# standard libs
import random

# internal libs
from logalpha.color import Color, COLORS, NAMES, ANSI_COLORS

# external libs
from hypothesis import given, strategies as st


def test_all() -> None:
    """Check initialization."""
    for color in COLORS:
        assert color.name in NAMES
        assert color.foreground == ANSI_COLORS['foreground'][color.name]
        assert color.background == ANSI_COLORS['background'][color.name]


def test_from_name() -> None:
    """Check .from_name factory method."""
    for name in NAMES:
        color = Color.from_name(name)
        assert color.name == name
        assert color.foreground == ANSI_COLORS['foreground'][name]
        assert color.background == ANSI_COLORS['background'][name]


@given(count=st.integers(min_value=2, max_value=8))
def test_from_names(count: int) -> None:
    """Check .from_names factory method."""
    names = random.choices(NAMES, k=count)
    colors = Color.from_names(names)
    for name, color in zip(names, colors):
        assert color.name in name
        assert color.foreground == ANSI_COLORS['foreground'][name]
        assert color.background == ANSI_COLORS['background'][name]
