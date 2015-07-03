.. Linker documentation master file, created by
   sphinx-quickstart on Fri Jul  3 22:02:57 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Linker's documentation!
==================================

Here's a fairly short and basic description of the application code

Models.py
------------------
.. automodule:: models
    :members:

    .. autoexception:: AuthorizationError

    .. autoclass:: MetaModel

    .. autoclass:: User
        :members: name, email, password, register, authenticate

    .. autoclass:: Group
        :members:

    .. autoclass:: Link
        :members:

    .. autoclass:: Comment
        :members:

    .. autoclass:: UserToGroup
        :members:

    .. autoclass:: UserToLink
        :members:


Routes.py
------------------
.. automodule:: routes
    :members:

App.py
------------------
.. automodule:: app
    :members:

Run.py
------------------
.. automodule:: run
    :members:

Utils.py
------------------
.. automodule:: utils
    :members:
