from __future__ import print_function

import os

from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.default import Default
from cloudmesh.common.console import Console
from pprint import pprint

class StormCommand(PluginCommand):

	@command
	def do_storm(self, args, arguments):
		"""
		::

			Usage:
				storm info
				storm name <NAME>
				storm size <SIZE>
				storm image <IMAGE>
				storm flavor <FLAVOR>
				storm cloud <CLOUD>
				storm cluster info
				storm cluster create
				storm install
				storm start zookeper
				storm start nimbus
				storm start zookeeper
				storm submit <JAR>

			Arguments:
			NAME	name of the cluster
			SIZE	size of the cluster
			IMAGE	image to be used
			FLAVOR	flavor of the vm to be created
			CLOUD	cloud to create a cluster on
			JAR		jar file to submit to cluster

		"""
		
		#print(arguments)
		
		default = Default()

		if arguments.info:
			print("Creates a cluster and deploys storm on the cluster")
			print("\t1. Requires the cloud to be deployed on as a variable")
			print("\t2. Set cluster variables using")
			print("\t\tstorm name <name>")
			print("\t\tstorm size <size>")
			print("\t\tstorm image <image>")
			print("\t\tstorm flavor <flavor>")
			print("\t\tstorm cloud <cloud>")
			print("\t3. Create a cluster")
			print("\t\tstorm cluster create")
			print("\t4. Install requirements")
			print("\t\tstorm install")
			print("\t5. Start zookeeper server cluster")
			print("\t\tstorm start zookeeper")
			print("\t6. Check if zookeeper is started")
			print("\t\tstorm status zookeeper")
			print("\t7. Start storm daemons")
			print("\t\tstorm start nimbus")
			print("\t\tstorm start supervisors")
			print("\tTopologies may now be submitted to the cluster. Topologies need to be in a jar file")
			print("\tTo submit a topology to storm cluster, use")
			print("\t\tstorm submit <path to jar>")

		elif arguments.name and arguments.NAME:
			print("Set name to {}".format(arguments.NAME))
			default["storm","name"] = arguments.NAME

		elif arguments.size and arguments.SIZE:
			print("Set size to {}".format(arguments.SIZE))
			default["storm","size"] = arguments.SIZE

		elif arguments.image and arguments.IMAGE:
			print("Set image to {}".format(arguments.IMAGE))
			default["storm","image"] = arguments.IMAGE
		
		elif arguments.flavor and arguments.FLAVOR:
			print("Set flavor to {}".format(arguments.FLAVOR))
			default["storm","flavor"] = arguments.FLAVOR

		elif arguments.cloud and arguments.CLOUD:
			print("Set cloud to {}".format(arguments.CLOUD))
			default["storm","cloud"] = arguments.CLOUD

		elif arguments.cluster and arguments.info:
			print("Cluster details:")
			print("\tCloud\t: " + default["storm","cloud"])
			print("\tName\t: " + default["storm","name"])
			print("\tSize\t: " + default["storm","size"])
			print("\tImage\t: " + default["storm","image"])
			print("\tFlavor\t: " + default["storm","flavor"])
			print("\nIf any of the above details are None/False, please set them using the appropriate command")

		elif arguments.cluster and arguments.create:
			# check arguments to ensure cloud, name, size, image and flavor are true
			# get path of cloudmesh.storm directory to run scripts
			
			# run the cluster.sh and hosts.sh script
			
			#set variable deploy to true
			Console.error("not yet implemented")
		
		elif arguments.install:
			# if deploy is set to true
			# 	run the ansible script using the hosts file created in "cluster create" command
			command = 'ansible-playbook -i hosts install.yml --extra-vars "cloud="' + default["storm","cloud"]
			os.system(command)
			# else
			# 	request creation of cluster
			print("Please create a cluster first")
			# set install to true
			
			Console.error("not yet implemented")
		
		elif arguments.start and arguments.zookeeper:
			# if install is set to true
			# 	run the ansible script to start zookeeper server
			command = 'ansible-playbook -i hosts start.yml --extra-vars "cloud="' + default["storm","cloud"]
			os.system(command)
			# else
			# 	request creation of cluster
			print("Please create a cluster first")
			# set zookeeper variable to true
			Console.error("not yet implemented")
		
		elif arguments.start and arguments.nimbus:
			# if zookeeper is set to true
			# 	run the startStorm.sh script on nimbus
			# else
			# 	request zookeeper command to be run
			Console.error("not yet implemented")
		
		elif arguments.start and arguments.supervisor:
			# if zookeeper is set to true
			# 	run the startStorm.sh script on supervisors
			# else
			# 	request zookeeper command to be run
			Console.error("not yet implemented")
		
		elif arguments.start and arguments.ui:
			# if zookeeper is set to true
			# 	run the startStorm.sh script on nimbus
			# else
			# 	request zookeeper command to be run
			Console.error("not yet implemented")
		
		elif arguments.submit and arguments.JAR:
			# use submit.sh to submit topology to storm cluster
			Console.error("not yet implemented")
		
		default.close()
		return ""
