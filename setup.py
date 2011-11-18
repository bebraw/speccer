#!/usr/bin/env python
# -*- coding: utf-8 -*-
import speccer
from setuptools import setup

description = "Specification based test runner."
try:
    from pypandoc import convert

    long_description = convert('README.md', 'rst')
except (ImportError, IOError, OSError):
    print 'check that you have installed pandoc properly and that README.md exists!'
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
    run_specs = speccer.runner:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
)
