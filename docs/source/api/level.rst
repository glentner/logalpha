.. _level:

:mod:`logalpha.level`
=====================

.. module:: logalpha.level
    :platform: Unix, Windows

|

-------------------

|

.. autoclass:: Level

    |

    .. automethod:: from_names

    |

    Comparisons operate on the ``value`` attribute.

    .. automethod:: __lt__
    .. automethod:: __gt__
    .. automethod:: __le__
    .. automethod:: __ge__

|

-------------------

|

For convenience and readability, a set of global named instances are included
for the standard set of logging levels.

.. autodata:: DEBUG
.. autodata:: INFO
.. autodata:: WARNING
.. autodata:: ERROR
.. autodata:: CRITICAL
.. autodata:: LEVELS

|

