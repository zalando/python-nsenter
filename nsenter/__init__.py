#!/usr/bin/env python3

"""
nsenter - run program with namespaces of other processes
"""

import argparse
import ctypes
import os
import logging
from pathlib import Path
from contextlib import ExitStack

NAMESPACE_NAMES = frozenset('mnt ipc net pid user uts'.split())

log = logging.getLogger('nsenter')

libc = ctypes.CDLL('libc.so.6')


def nsfd(process: str, ns_type: str) -> Path:
    """
    Returns the namespace file descriptor for process (self or PID) and namespace type
    """
    return Path('/proc') / str(process) / 'ns' / ns_type


class Namespace:
    def __init__(self, pid: str, ns_type: str):
        self.pid = pid
        self.ns_type = ns_type
        self.parent_fd = nsfd('self', ns_type).open()
        self.parent_fileno = self.parent_fd.fileno()
        self.target_fd = nsfd(pid, ns_type).open()
        self.target_fileno = self.target_fd.fileno()

    def __enter__(self):
        log.debug('Entering %s namespace %s', self.ns_type, self.pid)
        libc.setns(self.target_fileno, 0)

    def __exit__(self, type, value, tb):
        log.debug('Leaving %s namespace %s', self.ns_type, self.pid)
        libc.setns(self.parent_fileno, 0)
        try:
            self.target_fd.close()
        except:
            pass
        self.parent_fd.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', '-t', required=True, metavar='PID',
                        help='Specify a target process to get contexts from.')
    for ns in NAMESPACE_NAMES:
        parser.add_argument('--{}'.format(ns), action='store_true', help='Enter the {} namespace'.format(ns))
    parser.add_argument('--all', action='store_true', help='Enter all namespaces')
    parser.add_argument('command', nargs='*', default=['/bin/sh'])

    args = parser.parse_args()

    with ExitStack() as stack:
        namespaces = []
        for ns in NAMESPACE_NAMES:
            if getattr(args, ns) or args.all:
                namespaces.append(Namespace(args.target, ns))
        for ns in namespaces:
            stack.enter_context(ns)
        os.execl(args.command[0], *args.command)


if __name__ == '__main__':
    main()
