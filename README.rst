=======
NSEnter
=======

Requires Python 3.4.

Install::

    python3 setup.py install

Example usage::

    docker run -d --name=redis -t redis
    sudo nsenter --all --target=`docker inspect --format '{{ .State.Pid }}' redis` /bin/bash

