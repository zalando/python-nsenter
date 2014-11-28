import unittest

import subprocess, os, errno

from nsenter import Namespace, NAMESPACE_NAMES 

class TestNamespaces(unittest.TestCase):

    def setUp(self):
        """Spawn a child process so we have a PID to enter"""
        
        self._child = subprocess.Popen(['/bin/cat'])

    def tearDown(self):
        """SIGTERM the child process"""
        
        self._child.terminate()
        self._child.wait()

    def test_namespaces_except_user(self):
        """Test entering all namespaces execept user

        Must have CAP_SYS_ADMIN to run these tests properly
        """

        #Can't use the assertRaises context manager in python2.6
        def do_test():
            for name in filter(lambda x: x != 'user', NAMESPACE_NAMES):
                with Namespace(self._child.pid, name):
                    pass
            
            #if we aren't root (technically: CAP_SYS_ADMIN)
            #then we'll get OSError (EPERM) for all our tests
            if os.geteuid() != 0:
               self.assertRaises(OSError, do_test)
            else:
                do_test()

    def test_user_namespace(self):
        """Test entering a non-existent namespace"""
        
        def do_test():
            with Namespace(self._child.pid, 'user'):
                pass

        #This process doesn't have a user namespace
        #So this will OSError(EINVAL)
        self.assertRaises(OSError, do_test)

    def test_bad_namespace(self):
        """Test entering a bad namespace type"""
        
        def do_test():
            with Namespace(self._child.pid, 'foo'):
                pass
        self.assertRaises(ValueError, do_test)

    def test_bad_pid(self):
        """Test entering bad pid's name space"""
        
        def do_test():
            with Namespace('foo', 'net'):
                pass

        self.assertRaises(IOError, do_test)



if __name__ == '__main__':
    unittest.main()

