# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.


from typing import Tuple
from dataclasses import dataclass


NAMES = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

ANSI_RESET = '\033[0m'
ANSI_COLORS = {prefix: {color: '\033[{prefix}{num}m'.format(prefix=i + 3, num=j) for j, color in enumerate(NAMES)}
               for i, prefix in enumerate(['foreground', 'background'])}


@dataclass
class Color:
    """
    Associates a `name` (str) with its corresponding `foreground` and `background` (str) 
    ANSI codes. You can construct a collection of `Color`s with the `from_names` factory method.
    
    The `from_names` factory method lets you easily build a collection.

    >>> colors = Color.from_names(['blue', 'green'])
    >>> colors
    (Color(name='blue', value='\x1b[34m', reset='\x1b[0m'),
     Color(name='green', value='\x1b[32m', reset='\x1b[0m'))
    """

    name: str
    foreground: str
    background: str
    reset: str = ANSI_RESET

    @classmethod
    def from_name(cls, name: str) -> 'Color':
        """Lookup ANSI code by `name`."""
        return cls(name, ANSI_COLORS['foreground'][name], ANSI_COLORS['background'][name])

    @classmethod
    def from_names(cls, names: Tuple[str]) -> Tuple['Color']:
        """Create collection of colors by `name`."""
        return tuple(cls.from_name(name) for name in names)


# sensible defaults
COLORS  = Color.from_names(NAMES)
BLACK   = COLORS[0]
RED     = COLORS[1]
GREEN   = COLORS[2]
YELLOW  = COLORS[3]
BLUE    = COLORS[4]
MAGENTA = COLORS[5]
CYAN    = COLORS[6]
WHITE   = COLORS[7]
