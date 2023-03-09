#!/usr/bin/env python
from setuptools import setup, find_packages
from io import open

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='dn3',
    version='1.1.1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/k1R4/deathnot3/',
    author='k1R4',
    author_email='srijiith@outlook.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    keywords='pwn',
    python_requires='>=3.6, <4',
    install_requires=['pyelftools',
                      'zstandard',
                      'unix_ar',
                      'wget',
                      'requests'],
    entry_points={
        'console_scripts': [
            'dn3=dn3.__init__:cli',
        ],
    },
)
