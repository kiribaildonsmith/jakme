#! /usr/bin/env python
"""The backend for the jakme editor framework"""
import re
import subprocess
import unittest

class Backend:
    """Implements the backend of the JaKme text editor-a system of
    piping text around.
    """
    def __init__(self, env=None):
        """Create a new backend with an optional environment"""
        self.environment = {'JAKME_FILENAME':'',
                            'JAKME_FILETYPE':''}
        
        if env != None:
            for key, value in env.iteritems():
                self.environment["JAKME_"+key] = value
            
    def send_text(self, command, input_text=""):
        """Send a body of text through a command. Return the output and
        error messages of that command.
        """
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                env=self.environment,
                                shell=True)
        
        (output, error) = pipe.communicate(input_text)

        return (output, error)
  

class TestBackend(unittest.TestCase):
    """Unit tests for the backend"""

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

