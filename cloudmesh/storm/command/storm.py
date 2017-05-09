from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand


class StormCommand(PluginCommand):

    @command
    def do_storm(self, args, arguments):
        """
        ::

          Usage:
                storm deploy CLOUD
                storm -f FILE
                storm FILE
                storm list

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        print(arguments)



