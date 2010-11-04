#! /usr/bin/env python
import subprocess

class Backend:
  """Implements the backend of the JaKme text editor-a system of
piping text around.
  """
  environment = {"FILENAME":None}

  def __init__(self, env=None):
    """Create a new backend with an optional environment"""
    if env != None:
      for k,v in env.iteritems():
        self.environment[k] = v

  def sendText(self, command, inputText):
    """Send a body of text through a command. Return the output and
error messages of that command.
    """
    pipe = subprocess.Popen(command, stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     env=self.environment,
                                     universal_newlines=True,
                                     shell=True)
    
    (output,error) = pipe.communicate(inputText)

    return (output,error)
  
if __name__ == '__main__':
  backend = Backend({"FILENAME":"test.sh"})
  if (backend.environment["FILENAME"] != "test.sh"):
    print("Failed test 1")

  print backend.sendText('/usr/bin/wc', "hello world")


