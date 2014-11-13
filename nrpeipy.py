#!/usr/bin/env python

'''nrpeipy.py - A script for use with SSH to execute commands the NRPE way'''
# Author: Joel Rangsmo <joel@rangsmo.se>

import re
import sys
import glob
import subprocess


# Set command configuration directory
configdir = '/etc/nrpe.d'

commands = []
pattern = re.compile(
    r'command\[(?P<name>.*)\]=(?P<cmd>.*)')

# Opens all files in config dir and loads the commands into the commands array
try:
    for config in glob.glob(configdir + '/*.cfg'):
        config = open(config, 'r')

        rows = config.readlines()
        config.close()

        for command in rows:
            command = pattern.search(command)

            if command:
                commands.append(
                    {'name': command.group('name'),
                     'cmd': command.group('cmd')})

except IOError:
    print 'UNKNOWN - Failed to read configuration files'
    exit(3)

# Checks if a argument has been provided
if not sys.argv[2]:
    print 'UNKNOWN - A command has not been provided'
    exit(3)

# Executes the provided command if it's in the commands array
for command in commands:
    if sys.argv[2] in command['name']:
        command = subprocess.Popen(
            command['cmd'], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)

        command.wait()

        # Checks if stderr and stdout has been provided and strips newline
        for output in command.communicate():
            if output:
                if output[-1] == '\n':
                    output = output[:-1]

                print output

        exit(command.returncode)

else:
    print 'UNKNOWN - command "%s" was not found in configuration' % sys.argv[2]
    exit(3)
