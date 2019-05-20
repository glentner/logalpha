Welcome to LogAlpha's documentation!
====================================

`LogAlpha <https://github.com/glentner/logalpha>`_ is a generic and extensible 
library for handling logging in Python. It implements a core set of primatives 
that not only allows but expects you to expand on them. What's important is not 
what is included in the library, but what is left out.

In a nut shell ...

* Instead of defining a string-template with keywords used to populate metadata,
  the message structure is not forced into text at all, and custom formatting of
  output is accomplished by defining the *format* function of the Handler. Its
  return value is written (or otherwise given) to a *resource*.

* The notion of a *level* being associated with the *content* of a message is 
  maintained, but the labels used for those levels is not enforced. The typical
  collection of levels (i.e., *DEBUG*, *INFO*, *WARNING*, ...) is defined for 
  convenience, but using *OK*, *ERR* instead is just as easy.

* Because the formatting of messages happens via a function definition, there is
  near infinite flexibility in what and how metadata can be included. This also
  makes it trivial to implement custom colorization.


Instead of trying to define a bunch of common scenarios in
a way that satisfies the lowest common denominator, the library has been left to 
just the primatives and instead a few illustrative examples are provided as
:doc:`recipes </recipes/index>` that can be modified.


.. toctree::
    :maxdepth: 3
    :caption: Contents:

    getting_started/index
    api/index
    recipes/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
