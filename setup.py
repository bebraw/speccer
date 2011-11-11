#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import speccer
from setuptools import setup

description = "Specification based test runner."
cur_dir = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(cur_dir, 'README.md')).read()
except:
    long_description = description

setup(
    name = "speccer",
    version = speccer.__version__,
    url = 'https://github.com/bebraw/speccer',
    license = 'MIT',
    description = description,
    long_description = long_description,
    author = speccer.__author__,
    author_email = 'bebraw@gmail.com',
    packages = ['speccer', ],
    package_dir = {'speccer': 'speccer', },
    install_requires = ['setuptools', ],
    entry_points="""
    [console_scripts]
    speccer = speccer.runner:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
)
