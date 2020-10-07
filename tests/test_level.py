# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Level unit tests."""

# standard libs
from string import ascii_letters

# internal libs
from logalpha.level import Level, LEVELS, DEBUG, INFO, WARNING, ERROR, CRITICAL

# external libs
from hypothesis import given, assume, strategies as st


@given(st.text(ascii_letters, max_size=10), st.integers(min_value=0, max_value=10))
def test_init(name: str, value: int) -> None:
    """Check initialization."""
    level = Level(name=name, value=value)
    assert level.name == name
    assert level.value == value


@given(st.integers(min_value=0, max_value=10), st.integers(min_value=0, max_value=10))
def test_comparison(a: int, b: int) -> None:
    """Test level comparisons."""
    assume(a < b)
    assert Level(name='A', value=a) < Level(name='B', value=b)


def test_standard_levels() -> None:
    """Test default levels."""
    levels = [DEBUG, INFO, WARNING, ERROR, CRITICAL]
    for i, level in enumerate(levels):
        assert LEVELS[i] is level
        for lower_level in LEVELS[:i]:
            assert lower_level < level


def test_from_names() -> None:
    """Check .from_names factory method."""
    names = ['A', 'B', 'C', 'D', 'F']
    levels = Level.from_names(names)
    for i, level in enumerate(levels):
        assert level.name == names[i]
        assert level.value == i
