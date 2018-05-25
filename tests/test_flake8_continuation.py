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
"""Tests for flake8_continuation."""
# stdlib imports
import unittest

# stdlib froms
try:
    from unittest import mock
except ImportError:
    import mock

# project imports
import flake8_continuation


class ContinuationPluginTestCase(unittest.TestCase):
    """Tests for ContinuationPlugin."""

    def assert_not_okay(self, fixture_name):
        """Assert that linting the given fixture will error."""
        actual = self.run_with_fixture(fixture_name)
        self.assertNotEqual([], actual)
        message = actual[0][2]
        self.assertTrue(message.startswith(flake8_continuation.ERROR_CODE))

    def assert_okay(self, fixture_name):
        """Assert that linting the given fixture will pass."""
        actual = self.run_with_fixture(fixture_name)
        self.assertEqual(actual, [])

    def run_with_fixture(self, fixture_name):
        """Run the plugin with the given fixture."""
        path = 'tests/fixtures/{}'.format(fixture_name)
        plugin = flake8_continuation.ContinuationPlugin(None, path)
        return list(plugin.run())

    def test_with(self):
        """Test that with statements can be continued with backslashes."""
        self.assert_okay('with-statement')

    def test_long_comment(self):
        """Test that full-line comments will pass."""
        self.assert_okay('long-comment')

    def test_inline_comment(self):
        """Test that inline comments will pass."""
        self.assert_okay('inline-comment')

    def test_long_if_expression(self):
        """Test that long expressions with backslashes will fail."""
        self.assert_not_okay('long-if-expression')

    def test_long_string_with_backslashes(self):
        """Test that long strings using backslashes will fail."""
        self.assert_not_okay('long-string-with-backslashes')

    def test_noqa(self):
        """Test that noqa comments are honored."""
        self.assert_okay('noqa')

    @mock.patch('flake8_continuation.pycodestyle.stdin_get_value',
                new=mock.Mock(return_value='foo = True  # bar\\\n'))
    def test_stdin(self):
        """Test that reading from stdin also works."""
        plugin = flake8_continuation.ContinuationPlugin(None)
        actual = list(plugin.run())
        self.assertEqual(actual, [])
