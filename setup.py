# -*- coding: utf-8 -*-
#
import os
import codecs

from setuptools import setup, find_packages

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, 'orthopy', '__about__.py'), 'rb') as f:
    # pylint: disable=exec-used
    exec(f.read(), about)


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except FileNotFoundError:
        content = ''
    return content


setup(
    name='orthopy',
    version=about['__version__'],
    packages=find_packages(),
    url='https://github.com/nschloe/orthopy',
    download_url='https://pypi.python.org/pypi/orthopy',
    author=about['__author__'],
    author_email=about['__email__'],
    install_requires=[
        'matplotlib',
        'numpy',
        'pipdate',
        'scipy',
        'sympy',
        ],
    extras_require={
        'sphere-plot': ['meshzoo', 'meshio'],
        'disk-plot': ['pygmsh'],
        },
    description='tools for orthogonal polynomials, Gaussian quadrature',
    long_description=read('README.rst'),
    license=about['__license__'],
    classifiers=[
        about['__license__'],
        about['__status__'],
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics'
        ]
    )
