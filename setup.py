#!/usr/bin/env python3

import inspect
import os
import setuptools

__location__ = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))


def read(fname):
    return open(os.path.join(__location__, fname)).read()


def get_install_requirements(path):
    content = open(os.path.join(__location__, path)).read()
    return [req for req in content.split('\\n') if req != '']


def setup_package():
    setuptools.setup(
        name='nsenter',
        version='0.1.6',
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
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: CPython',
            'Operating System :: POSIX :: Linux',
            'License :: OSI Approved :: Apache Software License'],
        test_suite='tests',
        setup_requires=['flake8'],
        install_requires=get_install_requirements('requirements.txt'),
        packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
        entry_points={'console_scripts': ['nsenter = nsenter:main']}
    )

if __name__ == '__main__':
    setup_package()
