from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.default import Default
from cloudmesh.common.console import Console

class StormCommand(PluginCommand):

    @command
    def do_storm(self, args, arguments):
        """
        ::

          Usage:
                storm deploy CLOUD
                storm info
                storm status
                storm cloud
                storm image
                storm -f FILE
                storm FILE
                storm list

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        
        default = Default()
        cloud = arguments.CLOUD or default["global"]["cloud"]
        
        arguments.user = arguments["--user"]
        
        if arguments.info:
        	Console.error("Not yet implemented")
        elif arguments.cloud:
        	default["storm","cloud"] = arguments.cloud
        elif arguments.image:
        	default["storm","image"] = arguments.image
        
