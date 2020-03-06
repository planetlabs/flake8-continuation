# Copyright 2018, Planet Labs, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""Warnings for line continuation methods not suggested by PEP-8."""
# stdlib imports
import tokenize

# third-party imports
import pkg_resources
import pycodestyle
import six

__version__ = pkg_resources.get_distribution("flake8-continuation").version

STDINS = {"stdin", "-", "(none)", None}

ERROR_CODE = "C092"
ERROR_MESSAGE = (
    "prefer implied line continuation inside parentheses, "
    "brackets, and braces as opposed to a backslash"
)


class ContinuationPlugin(object):
    """Checker for invalid line continuations."""

    name = "flake8-continuation"
    version = __version__

    def __init__(self, tree, filename="(none)"):
        """Create the plugin and split the file into lines if needed."""
        self.tree = tree
        self.filename = filename
        self.lines = load_file(self.filename)

    def run(self):
        """Run and return errors."""
        for error in check_errors(self.lines):
            yield (
                error.get("line"),
                error.get("col"),
                error.get("message"),
                type(self),
            )


def check_errors(lines):
    """Find and yield continuation errors in the source lines."""
    noqa_rows = get_noqa_line_numbers(lines)
    stripped = strip_docstrings(strip_comments(lines))
    for i, line in enumerate(stripped):
        end_row = i + 1
        if has_bad_continuation(line) and end_row not in noqa_rows:
            end_col = len(line)
            yield {
                "message": "{0} {1}".format(ERROR_CODE, ERROR_MESSAGE),
                "line": end_row,
                "col": end_col,
            }


def generate_tokens(lines):
    """Tokenize the lines.

    This is specifically used to filter out Python comments.
    """
    lines_iter = iter(lines)
    return tokenize.generate_tokens(lambda: next(lines_iter))


def get_noqa_line_numbers(lines):
    """Strip all relevant flake8 noqa directives from the source lines."""
    return [i for i, line in enumerate(lines) if is_noqa_line(line)]


def has_bad_continuation(line):
    """Tell whether or not a non-comment line is bad."""
    stripped = line.strip()
    return stripped.endswith("\\") and not (
        stripped.startswith("assert") or stripped.startswith("with")
    )


def is_docstring(s):
    """Tell whether or not a string is a docstring."""
    return s.startswith("'''") or s.startswith('"""')


def is_noqa_line(line):
    """Tell whether or not a line is a NOQA line for this plugin."""
    s = line.strip()
    return s.endswith("# noqa: {}".format(ERROR_CODE)) or s.endswith("# noqa")


def is_stdin(name):
    """Tell whether or not the given name represents stdin."""
    return name in STDINS


def load_file(name):
    """Load the named path as a file-like object and return the lines."""
    return read_stdin_lines() if is_stdin(name) else read_file_lines(name)


def read_file_lines(name):
    """Read and return all the lines of a file."""
    return pycodestyle.readlines(name)


def read_stdin_lines():
    """Read and return all the lines of stdin."""
    return pycodestyle.stdin_get_value().splitlines(True)


def strip_comments(lines):
    """Strip all comments from the source lines."""
    return strip_with(lambda t: t[0] == tokenize.COMMENT, lines)


def strip_docstrings(lines):
    """Strip all docstrings from the source lines."""
    return strip_with(lambda t: t[0] == tokenize.STRING and is_docstring(t[1]), lines)


def strip_with(predicate, lines):
    """Strip any tokens that match the given predicate."""
    tokens = list(generate_tokens(lines))
    # filter all the tokens based on the predicate
    filtered = list(filter(predicate, tokens))
    # copy the lines to modify and return
    stripped = lines[:]

    for token in filtered:
        # grab the starting line number and column number for the token
        # this is especially important for multiline tokens, e.g docstrings
        start_lineno = token[2][0] - 1
        start_colno = token[2][1]
        # grab the ending line number and column number for the token
        end_lineno, end_colno = token[3]
        affected_lines = six.moves.range(start_lineno, end_lineno)
        for lineno in affected_lines:
            line = lines[lineno]
            # remove the token from the given line
            start = start_colno if lineno == start_lineno else 0
            end = end_colno if lineno == end_lineno else (len(line) - 1)
            without_token = line[:start] + line[end:]
            stripped[lineno] = without_token.rstrip()
    return stripped
