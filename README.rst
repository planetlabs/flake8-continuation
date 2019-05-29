===========================
Flake8 Continuation Plugin
===========================

A `Flake8 <http://flake8.readthedocs.org/en/latest/>`_ plugin that checks for the line continuation style to be in the `preferred method according to PEP-8 <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_, specifically:

    The preferred way of wrapping long lines is by using Python's implied line continuation inside parentheses, brackets and braces. Long lines can be broken over multiple lines by wrapping expressions in parentheses. These should be used in preference to using a backslash for line continuation.

Installation
============

Via pip:

``pip install flake8-continuation``

The `--user <https://pip.pypa.io/en/stable/user_guide/#user-installs>`__
flag is highly recommended for those new to `pip <https://pip.pypa.io>`__.


Warnings
========

This package adds a single new warning, ``C092: prefer implied line continuation inside parentheses, brackets, and braces as opposed to a backslash``. That error code was picked because ``ord('\\') == 92``.
