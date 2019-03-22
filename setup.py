#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='curl2py',
    version='0.0.2',
    description='Conver cURL command line to python-requests code.',
    author='codeif',
    author_email='me@codeif.com',
    url='https://github.com/codeif/curl2py',
    entry_points={
        'console_scripts': [
            'curl2py = curl2py:main',
        ],
    },
    install_requires=['requests', 'werkzeug', 'six'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
