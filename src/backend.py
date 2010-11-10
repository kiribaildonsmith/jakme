#! /usr/bin/env python
"""The backend for the jakme editor framework"""
import re
import subprocess
import os

def get_commands(root):
    """Find all the commands under a root"""
    commands = {}
    
    if os.path.exists(root):
        for root, _, files in os.walk(root):
            for program in files:
                fullpath = os.path.join(root, program)
                if os.access(fullpath, os.X_OK):
                    commands[program] = fullpath

    return commands


class Backend:
    """Implements the backend of the JaKme text editor-a system of
    piping text around.
    """
    def __init__(self, env=None):
        """Create a new backend with an optional environment"""
        self.environment = {'JAKME_FILENAME':'',
                            'JAKME_FILETYPE':'',
                            'JAKME_PREFIX':'JAKME_',
                            'JAKME_CONFIG_DIR':os.environ['HOME']+'/.jakme/'}
        
        if env != None:
            for key, value in env.iteritems():
                self.environment[self.environment['JAKME_PREFIX']+key] = value
            
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
  
    def get_global_commands(self):
        """Get the paths to commands which should be applied globally to a
        file
        """
        return self.get_jakme_commands('global')

    def get_regional_commands(self):
        """Gets the paths to commands which should be applied regionally to
        text
        """
        return self.get_jakme_commands('regional')


    def get_jakme_commands(self, subdir):
        """Fetches commands from the usual places"""
        commands = {}

        dirs = [self.environment['JAKME_CONFIG_DIR']+subdir,
                self.environment['JAKME_CONFIG_DIR']
                +self.environment['JAKME_FILETYPE']+subdir]

        for subdir in dirs:        
            additional_commands = get_commands(subdir)
            for (command, path) in additional_commands.items():
                commands[command] = path
    
        return commands

