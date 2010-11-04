#! /usr/bin/env python
import subprocess

class Backend:
  """Implements the backend of the JaKme text editor-a system of
piping text around.
  """
  environment = {}

  def __init__(self, filename):
    """Create a new Backend object with the path set initially to 'filename'
    """
    self.environment["FILENAME"] = filename

if __name__ == '__main__':
  backend = Backend("test.sh")
  if (backend.environment["FILENAME"] != "tst.sh"):
    print("Failed test 1")
