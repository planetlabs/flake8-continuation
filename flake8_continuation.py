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

__version__ = pkg_resources.get_distribution('flake8-continuation').version

STDINS = {'stdin', '-', '(none)', None}

ERROR_CODE = 'C092'
ERROR_MESSAGE = ('prefer implied line continuation inside parentheses, '
                 'brackets, and braces as opposed to a backslash')


class ContinuationPlugin(object):
    """Checker for invalid line continuations."""

    name = 'flake8-continuation'
    version = __version__

    def __init__(self, tree, filename='(none)'):
        """Create the plugin and split the file into lines if needed."""
        self.tree = tree
        self.filename = filename
        self.lines = load_file(self.filename)

    def run(self):
        """Run and return errors."""
        for error in check_errors(self.lines):
            yield (
                error.get('line'),
                error.get('col'),
                error.get('message'),
                type(self),
            )


def check_errors(lines):
    """Find and yield continuation errors in the source lines."""
    noqa_rows = get_noqa_line_numbers(lines)
    for i, line in enumerate(strip_comments(lines)):
        end_row = i + 1
        if has_bad_continuation(line) and end_row not in noqa_rows:
            end_col = len(line)
            yield {
                'message': '{0} {1}'.format(ERROR_CODE, ERROR_MESSAGE),
                'line': end_row,
                'col': end_col
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
    return (stripped.endswith('\\') and
            not (stripped.startswith('assert') or stripped.startswith('with')))


def is_noqa_line(line):
    """Tell whether or not a line is a NOQA line for this plugin."""
    stripped = line.strip()
    return (stripped.endswith('# noqa: {}'.format(ERROR_CODE)) or
            stripped.endswith('# noqa'))


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
    tokens = generate_tokens(lines)
    comments = [token for token in tokens if token[0] == tokenize.COMMENT]
    stripped = lines[:]
    for comment in comments:
        lineno = comment[3][0]
        start = comment[2][1]
        stop = comment[3][1]
        content = stripped[lineno - 1]
        without_comment = content[:start] + content[stop:]
        stripped[lineno - 1] = without_comment.rstrip()
    return stripped
