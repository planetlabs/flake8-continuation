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

setuptools.setup(
    name='flake8-continuation',
    license='MIT',
    version='0.1.1',
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
