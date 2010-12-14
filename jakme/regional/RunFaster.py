#! /usr/bin/env python
"""Read a line of input and execute that sending all other input into
that command"""

__author__ = 'Joseph Hallett & Kiri Baildon-Smith'
__version__ = '2.0'

from subprocess import *
from sys import *

def read_command(stream):
    """
    Read the command and its input from a stream
    
    Args:
    stream -- where to read from

    Returns:
    The command to execute, and the text to input into it.

    """
    command =  stream.readline().rstrip("\n\r")
    input_text = stream.read()

    return (command, input_text)

def run_command(command, text):
    """
    Run a command in a shell

    Args:
    command -- the command to run
    text -- the input to that command

    Returns:
    the output and the error from running the command
    """
    pipe = Popen(command, 
                 stdin=PIPE,
                 stdout=PIPE,
                 stderr=PIPE,
                 shell=True)

    return pipe.communicate(text)

def read_and_run(stream):
    """
    Read a command then run it
    
    Args:
    stream -- where to read from

    Returns:
    the output and the error from that command
    """
    command, text = read_command(stream)
    return run_command(command, text)


if __name__ == '__main__':
    out, extra = read_and_run(stdin)

    stdout.write(out)
    stderr.write(extra)
    



