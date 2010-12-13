#! /usr/bin/env python
"""The backend for the jakme editor framework. 

Implements an object capable of suggesting commands to run and piping
input and output between arbitary commands inside a controlled
environment.
"""
__author__  = 'Joseph Hallett & Kiri Baildon-Smith'
__version__ = '1.0'

import subprocess
import os

def get_commands(path):
    """Find all the executable commands in a directory.

    Scans all the files in a path and adds them to a dictionary where
    the name of the program is tied to the path of it.Returns this
    dictionary when all files are scanned. Only top level files in the
    path are scanned. It will not currently recurse any deeper.
    """
    commands = {}
    
    if os.path.exists(path):
        for root, _, files in os.walk(path):
            for program in files:
                fullpath = os.path.join(root, program)
                if os.access(fullpath, os.X_OK):
                    commands[program] = fullpath

    return commands


class Backend:
    """Implements the backend of the JaKme text editor-a system of
    piping text around.
    """

    def __init__(self, prefix='JAKME_', env=None):
        """Create a new backend object.

        Arguments:
        prefix -- prefix given to environment variables (by default 'JAKME_')
        env -- any environment variables you wish to initially set
        """
        self.environment = {}

        self.set_environment({'PREFIX':prefix}, prefix)
        self.set_environment({'FILENAME':'',
                              'FILETYPE':'',
                              'CONFIG_DIR':os.environ['HOME']+'/.jakme/',
                              'PID':str(os.getpid())
                             })
                               
        
        if env != None:
            self.set_environment(env)

    def get_environment(self, var, prefix=None):
        """Gets an environment variable from the environment by taking
        the variable name and preprending the program prefix (if there is one).

        Argumments: 
        var -- the variable you wish to inspect 
        prefix -- the prefix prepended to the variable internally (default is what
                  is defined in the environment
        """
        if prefix == None:
            # yes this really needs refactoring
            prefix = self.environment['JAKME_PREFIX'] 
        return self.environment[prefix+var]

    def set_environment(self, dictionary, prefix=None):
        """Sets a variable in the environment

        Arguments:
        dictionary -- a mapping of variable names to value
        prefix -- the prefix to append to all variables
        """

        if prefix == None:
            prefix = self.get_environment('PREFIX')

        for key, value in dictionary.iteritems():
            #print "key "+str(key)+" is a "+str(key.__class__)
            #print "val "+str(value)+" is a "+str(value.__class__)
            self.environment[prefix+key] = value

    def send_text(self, command, input_text=""):
        """Send a body of text through a command. Return the output and
        error messages of that command.

        Arguments:
        command -- path to executable
        input_text -- text to be piped into the command (default is empty)
        
        """
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                env=self.environment,
                                shell=True)
        
        (output, error) = pipe.communicate(input_text)

        return (output, error)
  
    def get_global_commands(self):
        """Get the paths to commands which should be applied globally to a
        file.  Returns a dictionary of program names to paths.
        """
        return self.get_jakme_commands('global')

    def get_regional_commands(self):
        """Gets the paths to commands which should be applied regionally to
        text.  Returns a dictionary of program names to paths.
        """
        return self.get_jakme_commands('regional')


    def get_jakme_commands(self, subdir):
        """Fetches commands from the usual places by looking in the subdir
        specified.
        
        Arguments:
        subdir -- the subdirectory in the config directory where the
                  commands reside and the same one in the filetype directory.
        """
        commands = {}
    
        config_dir = self.get_environment('CONFIG_DIR')
        filetype = self.get_environment('FILETYPE')


        dirs = [config_dir+subdir,
                config_dir+filetype+subdir]

        for subdir in dirs:        
            additional_commands = get_commands(subdir)
            for (command, path) in additional_commands.items():
                commands[command] = path
    
        return commands

