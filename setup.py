#!/usr/bin/env python3

import inspect
import os
import setuptools

__location__ = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))


def read(fname):
    return open(os.path.join(__location__, fname)).read()


def setup_package():
    setuptools.setup(
        name='nsenter',
        version='0.1.4-2',
        url='https://github.com/zalando/python-nsenter',
        description='Enter kernel namespaces from Python',
        author='Henning Jacobs',
        author_email='henning.jacobs@zalando.de',
        long_description=read('README.rst'),
        license='Apache License 2.0',
        keywords='docker container namespace kernel setns',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: CPython',
            'Operating System :: POSIX :: Linux',
            'License :: OSI Approved :: Apache Software License'],
        test_suite='tests',
        setup_requires=['flake8'],
        packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
        entry_points={'console_scripts': ['nsenter = nsenter:main']}
    )

if __name__ == '__main__':
    setup_package()
