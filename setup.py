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
"""Setup for flake8_continuation."""
# stdlib imports
import os.path
import sys

# third-party imports
import setuptools

here = os.path.abspath(os.path.dirname(__file__))


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

if sys.argv[-1] == "test-publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
    sys.exit()


def get_long_description():
    """Read the long description from the README."""
    with open(os.path.join(here, "README.rst"), "r") as f:
        return f.read()


setuptools.setup(
    name="flake8-continuation",
    description="Flake8 Line Continuation Plugin",
    long_description=get_long_description(),
    license="Apache 2.0",
    version="1.0.4",
    install_requires=["flake8", "pycodestyle", "six"],
    provides=["flake8_continuation"],
    py_modules=["flake8_continuation"],
    entry_points={
        "flake8.extension": ["C092 = flake8_continuation:ContinuationPlugin"],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
