# flake8-continuation

A [flake8](http://flake8.readthedocs.org/en/latest/) plugin that checks for the line continuation style to be in the [preferred method according to PEP-8](https://www.python.org/dev/peps/pep-0008/#maximum-line-length), specifically:

>The preferred way of wrapping long lines is by using Python's implied line continuation inside parentheses, brackets and braces. Long lines can be broken over multiple lines by wrapping expressions in parentheses. These should be used in preference to using a backslash for line continuation.

## Warnings

This package adds a single new warning, `C092: prefer implied line continuation inside parentheses, brackets, and braces as opposed to a backslash`. That error code was picked because `ord('\\') == 92`.
