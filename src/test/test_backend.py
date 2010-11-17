#! /usr/bin/env python
import sys
import unittest
import re
sys.path.append('..')
from  backend import *

class TestBackend(unittest.TestCase):
    """Unit tests for the backend"""

    def test_get_commands(self):
        "We can find executable programs"
        commands = get_commands('/bin')
        self.assertTrue(len(commands) > 0)

    def test_get_global(self):
        "We can find global commands"
        backend = Backend({'FILETYPE':'c'})
        commands = backend.get_global_commands()
        with self.assertRaises(KeyError):
            commands['START_SKYNET']

        self.assertEquals(commands['Open'], 
                backend.environment['JAKME_CONFIG_DIR']+'global/Open')

    def test_get_regional(self):
        "We can find regional commands"
        backend = Backend({'FILETYPE':'c'})
        commands = backend.get_regional_commands()
        with self.assertRaises(KeyError):
            commands['START_SKYNET']

        self.assertEquals(commands['Copy'], 
                backend.environment['JAKME_CONFIG_DIR']+'regional/Copy')

    def test_constructor_no_environment(self):
        "We can make a backend without an environment"
        backend = Backend()
        self.assertEqual(backend.environment["JAKME_FILENAME"], '')

    def test_constructor_environment(self):
        "Constructor environment is added to backend"
        backend = Backend({'FILENAME':"test.sh", 'FILETYPE':"bash"})
        self.assertEqual(backend.environment["JAKME_FILENAME"], "test.sh")
        self.assertEqual(backend.environment["JAKME_FILETYPE"], "bash")

    def test_simple_send_text_usage(self):
        "System commands output correctly with send_text"
        backend = Backend()
        (output, extra) = backend.send_text("/usr/bin/wc", "hello world")

        self.assertEqual(output, "       0       2      11\n")
        self.assertEqual(extra,  '')

    def test_env_set_up_properly(self):
        "Check environment is inserted into the send_text command"
        backend = Backend({'FILENAME':'test.txt'})
        (output, extra) = backend.send_text("/usr/bin/env")

        # Try and find the variable in the output of the env command
        target = "JAKME_FILENAME=test.txt"
        pattern = re.compile(target)
        output = str(output).splitlines()

        found_var = False
        for var in output:
            if pattern.search(var):
                self.assertEqual(target, var)
                found_var = True

        self.assertTrue(found_var)
        self.assertEqual(extra, '')

if __name__ == '__main__':
    unittest.main()

