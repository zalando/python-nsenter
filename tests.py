import unittest

import subprocess

from nsenter import Namespace, NAMESPACE_NAMES 

class TestNamespaces(unittest.TestCase):

    def setUp(self):
        self._child = subprocess.Popen(['/bin/cat'])

    def tearDown(self):
        self._child.terminate()
        self._child.wait()

    def test_namespace(self):
        for name in NAMESPACE_NAMES: 
            with Namespace(self._child.pid, name):
                assert True

        pass

if __name__ == '__main__':
    unittest.main()

