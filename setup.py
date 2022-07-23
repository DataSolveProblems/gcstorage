import os
import sys
from pathlib import Path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='gcstorage',
    author='Jie Jenn',
    author_email='jiejenn@learndataanalysis.org',
    version='1.0.0',
    keywords=['Google Cloud Storage', 'GCS'],
    python_requires='>=3.6',
    install_requires=['google-cloud-core>=2.3.1', 'google-cloud-storage>=2.4.0'],
    packages=['gcstorage'],
    license='MIT'
)   