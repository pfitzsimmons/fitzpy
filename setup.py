#!/usr/bin/env python
from setuptools import setup

setup(
    name='fitzpy',
    version='1.0.1',
    description="A collection of utilities for working with python",
    long_description=open('README.md').read(),
    author='Patrick Fitzsimmons',
    author_email='git@pfitz.net',
    url='https://github.com/pfitzsimmons/fitzpy',
    download_url='https://github.com/pfitzsimmons/fitzpy/tarball/v1.0.1',
    license='LICENSE',
    packages=['fitzpy'],
    install_requires=[
        'nose==1.3.7'
    ],
)
