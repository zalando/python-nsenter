=======
NSEnter
=======

This Python package allows entering Linux kernel namespaces (mount, IPC, net, PID, user and UTS) by doing the "setns" syscall.
The command line interface tries to be similar to the nsenter_ C program.

Requires Python 2.6 or higher

See the introductory `blog post "Entering Kernel Namespaces from Python"`_.

Install from PyPI::

    sudo pip3 install nsenter

Install from git source::

    python3 setup.py install

Example command line usage::

    docker run -d --name=redis -t redis
    sudo nsenter --all --target=`docker inspect --format '{{ .State.Pid }}' redis` /bin/bash


Example usage from Python:

.. code:: python

    import subprocess
    from nsenter import Namespace

    with Namespace(mypid, 'net'):
        # output network interfaces as seen from within the mypid's net NS:
        subprocess.check_output(['ip', 'a'])


.. _nsenter: http://man7.org/linux/man-pages/man1/nsenter.1.html
.. _blog post "Entering Kernel Namespaces from Python": http://tech.zalando.com/posts/entering-kernel-namespaces-with-python.html
