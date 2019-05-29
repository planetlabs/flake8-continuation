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
import setuptools


def get_long_description():
    with open('README.md', 'r') as f:
        return f.read()

def get_version():
    with open('VERSION', 'r') as f:
        return f.readline().strip()

setuptools.setup(
    name='flake8-continuation',
    description='Flake8 Line Continuation Plugin',
    long_description=get_long_description(),
    license='Apache 2.0',
    version=get_version(),
    install_requires=['flake8'],
    provides=['flake8_continuation'],
    py_modules=['flake8_continuation'],
    entry_points={
        'flake8.extension': [
            'C092 = flake8_continuation:ContinuationPlugin',
        ],
    },
    classifiers=[
        'Framework :: Flake8',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
