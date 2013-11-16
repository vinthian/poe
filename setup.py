#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Path of Exile Python API',
    version='0.0.1',
    description='Python API to consume resources from official Path of Exile web site',
    author='Nhat-Tan Duong',
    author_email='vinthian@gmail.com',
    url='http://www.vinthian.com/poe',
    install_requires=[
        'mechanize',
        'sqlalchemy',
    ],
    packages=[
        'poe',
    ],
)