#! /usr/bin/env python
import os
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
                        'JAKME_FILETYPE':'',
                       }

    if env != None:
      for k,v in env.iteritems():
        self.environment["JAKME_"+k] = v

  def sendText(self, command, inputText=""):
    """Send a body of text through a command. Return the output and
error messages of that command.
    """
    pipe = subprocess.Popen(command, stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     env=self.environment,
                                     shell=True)
    
    (output,error) = pipe.communicate(inputText)

    return (output,error)
  

class TestBackend(unittest.TestCase):
  def test_constructor_no_environment(self):
    "We can make a backend without an environment"
    backend = Backend()
    self.assertEqual(backend.environment["JAKME_FILENAME"], '')

  def test_constructor_environment(self):
    "Constructor environment is added to backend"
    backend = Backend({'FILENAME':"test.sh", 'FILETYPE':"bash"})
    self.assertEqual(backend.environment["JAKME_FILENAME"], "test.sh")
    self.assertEqual(backend.environment["JAKME_FILETYPE"], "bash")

  def test_simple_sendText_usage(self):
    "System commands output correctly with sendText"
    backend = Backend()
    (output,extra) = backend.sendText("/usr/bin/wc", "hello world")

    self.assertEqual(output, "       0       2      11\n")
    self.assertEqual(extra,  '')

  def test_env_set_up_properly(self):
    "Check environment is inserted into the sendText command"
    backend = Backend({'FILENAME':'test.txt'})
    (output,extra) = backend.sendText("/usr/bin/env")

    # Try and find the variable in the output of the env command
    target = "JAKME_FILENAME=test.txt"
    pattern = re.compile(target)
    output = output.splitlines()

    foundVar = False
    for var in output:
      if pattern.search(var):
        self.assertEqual(target, var)
        foundVar = True

    self.assertTrue(foundVar)


if __name__ == '__main__':
  unittest.main()

