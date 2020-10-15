.. _handler:

:mod:`logalpha.handler`
=====================

.. module:: logalpha.handler
    :platform: Unix, Windows

|

-------------------

|

The base :class:`~logalpha.handler.Handler` class should be considered an abstract class.
If deriving directly from the base class you should implement both the
:meth:`~logalpha.handler.Handler.format` and the :meth:`~logalpha.handler.Handler.write`.
methods.

.. autoclass:: Handler

    .. automethod:: write
    .. automethod:: format

|

-------------------

A minimum viable implementation is provided in :class:`StreamHandler`. This handler wants
a file-like `resource` to write to. It's :meth:`~StreamHandler.write` method literally
calls :meth:`print` with the `resource` as the `file`.

.. autoclass:: StreamHandler
    :show-inheritance:

    .. automethod:: write
    .. automethod:: format

|

The :class:`~logalpha.handler.StreamHandler` class implements everything needed for
messages to be published to `stderr` or some other file-like object. To customize
formatting, extend the class by overriding the :meth:`~logalpha.handler.Handler.format`
method. Just for formatting this seems like a lot of boilerplate; however, by making
it a function call it's possible to inject any arbitrary code.

.. code-block:: python

    @dataclass
    class MyHandler(StreamHandler):
        """A :class:`~StreamHandler` with custom formatting."""

        def format(self, message: Message) -> str:
            return f'{message.level.name} {message.content}'

|
