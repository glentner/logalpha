.. _getting_started:

Getting Started
===============

Installation
------------

*LogAlpha* can be installed using Pip.

.. code-block:: none

    ➜ pip install logalpha

|

-------------------

Basic Usage
-----------

Pre-built Arrangements
^^^^^^^^^^^^^^^^^^^^^^

`LogAlpha` expects you to build your own arrangement. That said, some typical arrangements have
been pre-built for both easy-of-use and the sake of demonstration.

The standard behavior one might expect is to have the canonical five logging levels and detailed
messages printed to `stderr` with a timestamp, hostname, and a topic. This is available from the
:ref:`logalpha.contrib.standard <standard>` module.

.. code-block:: python

    from logalpha.contrib.standard import StandardLogger, StandardHandler

    handler = StandardHandler()
    StandardLogger.handlers.append(handler)

In other modules create instances with a named `topic`.

.. code-block:: python

    log = StandardLogger(__name__)

The logger will automatically be instrumented with methods for each logging level.
As is conventional, the default logging level is `WARNING`.

.. code-block:: python

    log.info('message')

.. code-block:: python

    log.warning('message')

.. code-block:: none

    2020-10-12 20:48:10.555 hostname.local WARNING  [__main__] message

|

Do-It Yourself
^^^^^^^^^^^^^^

Instead of using a pre-built arrangement, let's define our own custom logging behavior.
For simple programs, it might be more appropriate to just log a status of `Ok` or `Error`.

We need to build a :class:`~logalpha.logger.Logger` with out own custom set of
:class:`~logalpha.level.Level`\s. Then a :class:`~logalpha.handler.Handler` for
our messages.

.. code-block:: python

    import sys
    from dataclasses import dataclass
    from typing import List, IO, Callable

    from logalpha.color import Color, ANSI_RESET
    from logalpha.level import Level
    from logalpha.message import Message
    from logalpha.handler import StreamHandler
    from logalpha.logger import Logger


    class OkayLogger(Logger):
        """Logger with Ok/Err levels."""

        levels: List[Level] = Level.from_names(['Ok', 'Err'])
        colors: List[Color] = Color.from_names(['green', 'red'])


    @dataclass
    class OkayHandler(StreamHandler):
        """
        Writes to <stderr> by default.
        Message format includes the colorized level and the text.
        """

        level: Level = OkayLogger.levels[0]  # Ok
        resource: IO = sys.stderr

        def format(self, message: Message) -> str:
            """Format the message."""
            color = OkayLogger.colors[message.level.value].foreground
            return f'{color}{message.level.name:<3}{ANSI_RESET} {message.content}'

.. warning::

    Don't forget to include the :class:`~dataclasses.dataclass` decorator on your
    :class:`~logalpha.handler.Handler` and :class:`~logalpha.message.Message` derived
    classes. If you aren't adding any new fields then things should work find though.

|

We can setup our logger the same way we did for the standard logger.

.. code-block:: python

    handler = OkayHandler()
    OkayLogger.handlers.append(handler)

Again, the logger is automatically instrumented with level methods.

.. code-block:: python

    log = OkayLogger()

.. code-block:: python

    log.ok('operation succeeded')

.. code-block:: none

    Ok  operation succeeded

.. note::

    If you get warnings from your IDE about these level methods being unknown
    when using your logger, this is because they are dynamically generated.
    You can add type annotations to your class to avoid this if you like.

    The names of these methods will always be the ``Level.name`` in lower-case.

    .. code-block:: python

        class OkayLogger(Logger):
            """Logger with Ok/Err levels."""

            levels: List[Level] = Level.from_names(['Ok', 'Err'])
            colors: List[Color] = Color.from_names(['green', 'red'])

            # stubs for instrumented level methods
            ok: Callable[[str], None]
            err: Callable[[str], None]

|

Adding Custom Metadata
^^^^^^^^^^^^^^^^^^^^^^

For more advanced logging setups you might want to specifically define additional
metadata you want attached to every message. A :class:`~logalpha.message.Message` is
a simple :class:`~dataclasses.dataclass`. Be default it only includes a ``level`` and
``content``. Extend it by subclassing the :class:`~logalpha.message.Message` class
and adding your attributes.

.. code-block:: python

    from datetime import datetime

    from logalpha.level import Level
    from logalpha.message import Message


    @dataclass
    class DetailedMessage(Message):
        """A message with additional attributes."""
        level: Level
        content: str
        timestamp: datetime
        topic: str
        host: str

.. note::

    You can in fact define the `content`
    of a message to be something other than a string, and the handler(s) can
    in turn define a `format` and `write` method accordingly.

Again, the message itself just a simple :class:`~dataclasses.dataclass`. The
:class:`~logalpha.logger.Logger` creates the message when you call one of the level
methods and will need `callbacks` defined for each of these attributes that return
a value.

.. code-block:: python

    from datetime import datetime
    from socket import gethostname
    from typing import Type, Callable, IO

    from logalpha.level import Level
    from logalpha.message import Message
    from logalpha.logger import Logger


    HOST: str = gethostname()

    class DetailedLogger(Logger):
        """Logger with detailed messages."""

        Message: Type[Message] = DetailedMessage
        topic: str

        def __init__(self, topic: str) -> None:
            """Initialize with `topic`."""
            super().__init__()
            self.topic = topic
            self.callbacks = {'timestamp': datetime.now,
                              'host': (lambda: HOST),
                              'topic': (lambda: topic)}

|

-------------------

Discussion
^^^^^^^^^^

There is a one-to-one relationship between the ``Logger`` and the ``Message`` you
define. You should implement one or more ``Handler`` classes that expect the same
``Message`` as input but differing in how they `format` the message or what type of
`resource` they `write` to.

|
