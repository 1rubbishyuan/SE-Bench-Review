#!/usr/bin/env python3
"""Setup script for zwc."""

from setuptools import setup, find_packages

setup(
    name="zwc",
    version="0.1.0",
    description="Mathematical computation library for array processing and numerical calculations",
    author="Claude",
    packages=find_packages(),
    install_requires=[
        "numpy==2.3.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)