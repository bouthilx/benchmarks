"""Installation script."""
from os import path
from io import open
from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read().strip()

setup(
    name='benchmarks',
    description='',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/bouthilx/benchmarks.git',
    author='Xavier Bouthillier',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=['numpy', 'theano', 'fuel', 'blocks', 'pymongo', 'sacred',
                      'matplotlib', 'configobj'],
)
