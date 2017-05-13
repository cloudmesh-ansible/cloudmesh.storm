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

	def make_hosts(self):
		path = os.getcwd()
		os.system('cm cluster inventory > ' + path + '/hosts.txt')
		f = open(path + '/hosts.txt', 'r')
		w = open(path + '/hosts', 'w')
		w.write("[cluster]\n")
		for i, line in enumerate(f):
			if i <= 0:
				continue
			else:
				w.write("node{} host=".format(i) + line)
		f.close()
		w.write("\n[nimbus]\n")
		f = open(path + '/hosts.txt', 'r')
		for i, line in enumerate(f):
			if i == 1:
				w.write("node{} host=".format(i) + line)
		f.close()
		w.write("\n[supervisors]\n")
		f = open(path + '/hosts.txt', 'r')
		for i, line in enumerate(f):
			if i >= 2:
				w.write("node{} host=".format(i) + line)
		f.close()
		w.close()
		os.system('rm hosts.txt')

	@command
	def do_storm(self, args, arguments):
		"""
		::

			Usage:
				storm name NAME
				storm size SIZE
				storm image IMAGE
				storm flavor FLAVOR
				storm cloud CLOUD
				storm cluster info
				storm cluster deploy
				storm cluster status
				storm cluster delete
				storm submit JAR CLASS JOB

			Arguments:
			NAME	name of the cluster
			SIZE	size of the cluster
			IMAGE	image to be used
			FLAVOR	flavor of the vm to be created
			CLOUD	cloud to create a cluster on
			JAR		jar file to submit to cluster

			Description:
			Creates a cluster and deploys storm on the cluster
			
				1. Requires the cloud to be deployed on as a variable
				2. Set cluster variables using
					storm name <name>
					storm size <size>
					storm image <image>
					storm flavor <flavor>
					storm cloud <cloud>
				3. Deploy cluster
					storm cluster create
				
				Cluster status may be checked using
					storm cluster status
				
				Cluster may be deleted using 
					storm cluster delete
				This unsets all the variables
				
				Topologies may now be submitted to the cluster. 
				Topologies need to be in a jar file.
				To submit a topology to storm cluster, use
					storm submit <jar> <name of class> <job name>
		"""

		default = Default()

		if arguments.name and arguments.NAME:
			print("Set name to {}.".format(arguments.NAME))
			default["storm","name"] = arguments.NAME

		elif arguments.size and arguments.SIZE:
			print("Set size to {}.".format(arguments.SIZE))
			default["storm","size"] = arguments.SIZE

		elif arguments.image and arguments.IMAGE:
			print("Set image to {}.".format(arguments.IMAGE))
			default["storm","image"] = arguments.IMAGE

		elif arguments.flavor and arguments.FLAVOR:
			print("Set flavor to {}.".format(arguments.FLAVOR))
			default["storm","flavor"] = arguments.FLAVOR

		elif arguments.cloud and arguments.CLOUD:
			print("Set cloud to {}.".format(arguments.CLOUD))
			default["storm","cloud"] = arguments.CLOUD
		
		elif arguments.cluster and arguments.info:
			print("Cluster details:")
			print("\tCloud\t: {}".format(default["storm","cloud"]))
			print("\tName\t: {}".format(default["storm","name"]))
			print("\tSize\t: {}".format(default["storm","size"]))
			print("\tImage\t: {}".format(default["storm","image"]))
			print("\tFlavor\t: {}".format(default["storm","flavor"]))
			print("\nIf any of the above details are None/False,")
			print("please set them using the appropriate command, before deploying the cluster.")

		elif arguments.cluster and arguments.deploy:
			# check arguments to ensure cloud, name, size, image and flavor are true
			if default["storm","name"] is not None and default["storm","size"] is not None and default["storm","image"] is not None and default["storm","flavor"] is not None and default["storm","cloud"] is not None:

				print("Creating and adding storm secgroup...")
				print("secgroup: storm storm 1 9000 tcp 0.0.0.0/0")
				# Define a secgroup
				command = 'cm secgroup add storm storm 1 9000 tcp 0.0.0.0/0'
				os.system(command)

				# Upload secgroup
				command = 'cm secgroup upload storm --cloud {}'.format(default["storm","cloud"])
				os.system(command)

				print("Creating cluster {}...".format(default["storm","name"]))
				# Define a cluster
				command = "cm cluster define --name {} --count {} --image {} --flavor {} -C {} --secgroup storm".format(default["storm","name"], default["storm","size"], default["storm","image"], default["storm","flavor"], default["storm","cloud"])
				os.system(command)

				# Use defined cluster
				command = "cm cluster use {}".format(default["storm","name"])
				os.system(command)

				# Create defined cluster
				command = "cm cluster allocate"
				os.system(command)

				# Make hosts file
				self.make_hosts()

				# Run ansible script
				command = 'ansible-playbook -i hosts storm.yml -e "cloud={}"'.format(default["storm","cloud"])
				os.system(command)

				print("Ansible tasks completed.")
				print("Cluster {} created and storm is running on cluster.".format(default["storm","name"]))
				default["storm","deploy"] = True
			else:
				print("Please set all the required variables.")

		elif arguments.cluster and arguments.status:
			if default["storm","deploy"]:

				# Check status
				print("Checking status of zookeeper and storm nimbus.")
				command = 'ansible-playbook -i hosts status.yml'
				os.system(command)
				
				print("Ansible scripts completed.")
			else:
				print("Please deploy a cluster first.")

		elif arguments.cluster and arguments.delete:
			if default["storm","deploy"]:
				print("Deleting cluster {}...".format(default["storm","cloud"]))

				# Delete cluster
				command = 'cm cluster delete'
				os.system(command)

				# Undefine cluster
				command = 'cm cluster undefine {}'.format(default["storm","name"])
				os.system(command)

				# Delete secgroup
				command = 'cm secgroup delete storm --cloud {}'.format(default["storm","cloud"])
				default["storm","deploy"] = False
			else:
				print("Please deploy a cluster first.")

		elif arguments.submit and arguments.JAR and arguments.CLASS and arguments.JOB:
			# if zookeeper is set to true
			# 	run the startStorm.sh script on supervisors
			# else
			# 	request zookeeper command to be run
			if default["storm","deploy"]:
				print("Submitting jar to cluster {}...".format(default["storm","cloud"]))
				
				# Submit jar
				command = 'ansible-playbook -i hosts submit.yml -e "cloud={} source={} class_file={} job_name={}"'.format(default["storm","cloud"], arguments.JAR, arguments.CLASS, arguments.JOB)
				os.system(command)
				
			else:
				print("Please deploy a cluster first.")

		default.close()
		return ""
