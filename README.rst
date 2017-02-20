=======
NSEnter
=======

.. image:: https://travis-ci.org/zalando/python-nsenter.svg?branch=master
   :target: https://travis-ci.org/zalando/python-nsenter
   :alt: Travis CI build status

**NSEnter** is a Python package that enables you to enter Linux kernel namespaces — mount, IPC, net, PID, user and UTS — with a single, simple "setns" syscall. The command line interface is similar to the nsenter_ C program.

Project Origins
---------------

When working with Docker_ containers, questions usually arise about how to connect into a running container without starting an explicit SSH daemon (`which is considered a bad idea`_). One way is to use Linux Kernel namespaces, which Docker uses to restrict the view from within containers. 

The ``util-linux`` package provides the ``nsenter`` command line utility, but `Ubuntu 16.04 LTS`_ unfortunately does not. Jérôme Petazzoni provides a `Docker recipe`_ for ``nsenter`` on GitHub, or you can compile ``nsenter`` `from source`_. As there is only one simple syscall to enter a namespace, we can do the call directly from within Python using the ``ctypes`` module. We bundled this syscall to create NSEnter.

Additional Links
````````````````
- "Entering Kernel Namespaces from Python," Zalando Tech `blog post`_
- On PyPi_

Requirements
````````````
- Python 2.6 or higher

Installation
````````````
From PyPI::

    sudo pip3 install nsenter

From git source::

    python3 setup.py install

Usage
`````
Example of command line usage::

    docker run -d --name=redis -t redis
    sudo nsenter --all --target=`docker inspect --format '{{ .State.Pid }}' redis` /bin/bash


Example of usage from Python:

.. code:: python

    import subprocess
    from nsenter import Namespace

    with Namespace(mypid, 'net'):
        # output network interfaces as seen from within the mypid's net NS:
        subprocess.check_output(['ip', 'a'])

    # or enter an arbitrary namespace:
    with Namespace('/var/run/netns/foo', 'net'):
        # output network interfaces as seen from within the net NS "foo":
        subprocess.check_output(['ip', 'a'])

Development Status
``````````````````
This project works as-is. There are currently no plans to extend it, but if you have an idea please submit an Issue to the maintainers.

License
-------
See file_.

.. _Docker: https://www.docker.com/
.. _which is considered a bad idea: https://jpetazzo.github.io/2014/06/23/docker-ssh-considered-evil/
.. _Ubuntu 16.04 LTS: https://askubuntu.com/questions/439056/why-there-is-no-nsenter-in-util-linux
.. _Docker recipe: https://github.com/jpetazzo/nsenter
.. _from source: https://askubuntu.com/questions/439056/why-there-is-no-nsenter-in-util-linux
.. _nsenter: http://man7.org/linux/man-pages/man1/nsenter.1.html
.. _blog post: http://tech.zalando.com/posts/entering-kernel-namespaces-with-python.html
.. _PyPi: https://pypi.python.org/pypi/nsenter
.. _file: https://github.com/zalando/python-nsenter/blob/master/LICENSE
