#!/usr/bin/env python

"""
nsenter - run program with namespaces of other processes
"""

import argparse
import ctypes
import errno
import os
import logging
from pathlib import Path
try:
    from contextlib import ExitStack
except ImportError:
    from contextlib2 import ExitStack

NAMESPACE_NAMES = frozenset(['mnt', 'ipc', 'net', 'pid', 'user', 'uts'])


class Namespace(object):
    """A context manager for entering namespaces

    Args:
        pid: The PID for the owner of the namespace to enter
        ns_type: The type of namespace to enter must be one of
            mnt ipc net pid user uts
        proc: The path to the /proc file system.  If running in a container
            the host proc file system may be binded mounted in a different
            location

    Raises:
        IOError: A non existent PID was provided
        ValueError: An improper ns_type was provided
        OSError: Unable to enter or exit the namespace

    Example:
        with Namespace(<pid>, <ns_type>):
            #do something in the namespace
            pass
    """

    _log = logging.getLogger(__name__)
    _libc = ctypes.CDLL('libc.so.6', use_errno=True)

    def __init__(self, pid, ns_type, proc='/proc'):
        if ns_type not in NAMESPACE_NAMES:
            raise ValueError('ns_type must be one of {0}'.format(
                ', '.join(NAMESPACE_NAMES)
            ))

        self.pid = pid
        self.ns_type = ns_type
        self.proc = proc

        self.target_fd = self._nsfd(pid, ns_type).open()
        self.target_fileno = self.target_fd.fileno()

        self.parent_fd = self._nsfd('self', ns_type).open()
        self.parent_fileno = self.parent_fd.fileno()

    __init__.__annotations__ = {'pid': str, 'ns_type': str}

    def _nsfd(self, pid, ns_type):
        """Utility method to build a pathlib.Path instance pointing at the
        requested namespace entry

        Args:
            pid: The PID
            ns_type: The namespace type to enter

        Returns:
             pathlib.Path pointing to the /proc namespace entry
        """
        return Path(self.proc) / str(pid) / 'ns' / ns_type

    _nsfd.__annotations__ = {'process': str, 'ns_type': str, 'return': Path}

    def _close_files(self):
        """Utility method to close our open file handles"""
        try:
            self.target_fd.close()
        except:
            pass
        self.parent_fd.close()

    def __enter__(self):
        self._log.debug('Entering %s namespace %s', self.ns_type, self.pid)

        if self._libc.setns(self.target_fileno, 0) == -1:
            e = ctypes.get_errno()
            self._close_files()
            raise OSError(e, errno.errorcode[e])

    def __exit__(self, type, value, tb):
        self._log.debug('Leaving %s namespace %s', self.ns_type, self.pid)

        if self._libc.setns(self.parent_fileno, 0) == -1:
            e = ctypes.get_errno()
            self._close_files()
            raise OSError(e, errno.errorcode[e])

        self._close_files()


def main():  # pragma: no cover
    """Command line interface to the Namespace context manager"""

    parser = argparse.ArgumentParser(prog='nsenter', description=__doc__)

    parser.add_argument('--target', '-t', required=True, metavar='PID',
                        help='A target process to get contexts from')

    group = parser.add_argument_group('Namespaces')

    for ns in NAMESPACE_NAMES:
        group.add_argument('--{0}'.format(ns),
                           action='store_true',
                           help='Enter the {0} namespace'.format(ns)
                           )

    parser.add_argument('--all',
                        action='store_true',
                        help='Enter all namespaces'
                        )

    parser.add_argument('command', nargs='*', default=['/bin/sh'])

    args = parser.parse_args()

    # make sure we have --all or at least one namespace
    if (True not in [getattr(args, ns) for ns in NAMESPACE_NAMES]
            and not args.all):
        parser.error('You must specify at least one namespace')

    try:
        with ExitStack() as stack:
            namespaces = []
            for ns in NAMESPACE_NAMES:
                if getattr(args, ns) or args.all:
                    namespaces.append(Namespace(args.target, ns))

            for ns in namespaces:
                stack.enter_context(ns)

            os.execlp(args.command[0], *args.command)
    except IOError as exc:
        parser.error('Unable to access PID: {0}'.format(exc))
    except OSError as exc:
        parser.error('Unable to enter {0} namespace: {1}'.format(
            ns.ns_type, exc
        ))


if __name__ == '__main__':  # pragma: no cover
    main()
