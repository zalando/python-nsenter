import ctypes
import os
import subprocess
import tempfile
import unittest

from nsenter import Namespace, NAMESPACE_NAMES


class TestNamespaces(unittest.TestCase):

    _libc = ctypes.CDLL('libc.so.6', use_errno=True)

    def setUp(self):
        """Spawn a child process so we have a PID to enter"""

        self._child = subprocess.Popen(['/bin/cat'])

    def tearDown(self):
        """SIGTERM the child process"""

        self._child.terminate()
        self._child.wait()

    def test_namespace_non_exist_path(self):
        """Test entering a non-existent path"""

        def do_test():
            fd, filename = tempfile.mkstemp()
            os.close(fd)
            os.remove(filename)

            with Namespace(filename, 'net'):
                pass

        self.assertRaises(IOError, do_test)

    def test_namespace_plain_file_path(self):
        """Test entering a plain file path"""

        fd, filename = tempfile.mkstemp()
        os.close(fd)

        def do_test():
            with Namespace(filename, 'net'):
                pass

        self.assertRaises(OSError, do_test)

        os.remove(filename)

    def test_namespace_directory_path(self):
        """Test entering a directory path"""

        def do_test():
            with Namespace('/tmp', 'net'):
                pass

        self.assertRaises(IOError, do_test)

    @unittest.skipIf(os.geteuid() != 0, "Must be root to bind mount")
    def test_namespace_good_path(self):
        """Test entering an arbirtrary namespace"""

        try:
            # get the path to it's network namespace
            ns_path = os.path.join('/proc', str(self._child.pid), 'ns', 'net')

            # bind mount it to a temp location
            fd, filename = tempfile.mkstemp()
            os.close(fd)

            assert self._libc.mount(ns_path.encode('ascii'), filename.encode('ascii'), 0, 4096, 0) == 0

            # enter the bind mount
            with Namespace(filename, 'net'):
                pass

        finally:
            # ensure we clean up the bind
            self._libc.umount(filename.encode('ascii'))
            os.remove(filename)

    @unittest.skipIf(os.geteuid() != 0, "Must be root to setns()")
    def test_namespaces_as_root(self):
        """Test entering all namespaces the pid has as root"""

        for name in filter(lambda x: x != 'user', NAMESPACE_NAMES):
            if os.path.exists(os.path.join('/proc', str(self._child.pid), 'ns', name)):
                with Namespace(self._child.pid, name):
                    pass

    @unittest.skipIf(os.geteuid() == 0, "Must not be root to trigger OSError")
    def test_namespaces_except_user_as_normal(self):
        """Test entering all namespaces execept user as non-root"""

        def do_test():
            for name in filter(lambda x: x != 'user', NAMESPACE_NAMES):
                with Namespace(self._child.pid, name):
                    pass

        self.assertRaises(OSError, do_test)

    @unittest.skipIf(os.geteuid() != 0, "Must be root to setns()")
    def test_user_namespace(self):
        """Test entering a non-existent namespace"""

        def do_test():
            with Namespace(self._child.pid, 'user'):
                pass

        # this will railse a IOError on python2 and OSError on python 3
        # as the file for this namespace does not exist!
        self.assertRaises((IOError, OSError), do_test)

    def test_bad_namespace(self):
        """Test entering a bad namespace type"""

        def do_test():
            with Namespace(self._child.pid, 'foo'):
                pass
        self.assertRaises(ValueError, do_test)

    def test_bad_pid(self):
        """Test entering bad pid's namespace"""

        def do_test():
            with Namespace('foo', 'net'):
                pass

        self.assertRaises(IOError, do_test)


if __name__ == '__main__':
    unittest.main()
