#!/bin/use/python

from os.path import join, dirname, abspath
from setuptools import setup, find_packages

__HERE__ = abspath(dirname(__file__))
__SRC__ = join(__HERE__, 'src')

def read(file_path):
    ret_value ={}
    with open(file_path, 'r') as file_reader:
        exec(file_reader.read(), ret_value)
    return ret_value

def read_requirements():
    with open('requirements.txt', 'r') as file_reader:
        return [line.rstrip() for line in file_reader] 


ABOUT = read(join(__SRC__, 'gmutils', '__version__.py'))


setup(
    name=ABOUT['__name__'],
    fullname=ABOUT['__name__'] + '.' + ABOUT['__version__'],
    version=ABOUT['__version__'],

    author=ABOUT['__author__'],
    author_email=ABOUT['__email__'],

    license=ABOUT['__license__'],

    description=ABOUT['__description__'],
    long_description=ABOUT['__summary__'],

    url=ABOUT['__url__'],
    project_urls = {
        'Source Code': 'https://github.com/GeekMasher/GMUtils',
        'Bug Tracker': 'https://github.com/GeekMasher/GMUtils/issues'
    },

    packages=find_packages(__SRC__),
    package_dir={'':'src'},

    exclude_package_data={
        '': ['README.md']
    },

    install_requires=read_requirements(),
    include_package_data=True,

    scripts = {

    },

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ]
)
