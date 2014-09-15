=======
NSEnter
=======

This Python package allows entering Linux kernel namespaces (mount, IPC, net, PID, user and UTS) by doing the "setns" syscall.
The command line interface tries to be similar to the nsenter_ C program.

Requires Python 3.4.

Install from PyPI::

    sudo pip3 install nsenter

Install from git source::

    python3 setup.py install

Example usage::

    docker run -d --name=redis -t redis
    sudo nsenter --all --target=`docker inspect --format '{{ .State.Pid }}' redis` /bin/bash

.. _nsenter: http://man7.org/linux/man-pages/man1/nsenter.1.html
