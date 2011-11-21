#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='domfo',
    version='1.0.0',
    author='Jeff Lindsay',
    author_email='jeff.lindsay@twilio.com',
    description='Simple DNS-configured domain forwarding service',
    packages=find_packages(),
    install_requires=['gservice', 'dnspython'],
    data_files=[],
)
