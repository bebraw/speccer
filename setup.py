#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

version = '0.1.0'

description = "Specification based test runner."
cur_dir = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(cur_dir, 'README.md')).read()
except:
    long_description = description

setup(
    name = "speccer",
    version = version,
    url = 'https://github.com/bebraw/speccer',
    license = 'BSD',
    description = description,
    long_description = long_description,
    author = 'Juho Vepsäläinen',
    author_email = 'bebraw@gmail.com',
    packages = find_packages('speccer'),
    package_dir = {'': 'speccer'},
    install_requires = ['setuptools', ],
    entry_points="""
    [console_scripts]
    spec = speccer.speccer:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
)
