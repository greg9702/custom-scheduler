#!/usr/bin/python

import time
import random
import json
import sys
import pprint

from kubernetes import client, config, watch
from node import Node

class Scheduler:
	def __init__(self):
		config.load_kube_config(config_file='../kind-config')
		self.v1 = client.CoreV1Api()
		self.scheduler_name = 'custom_scheduler'
		self.all_nodes=[]

		self.run()
		return

	def run(self):
		print('Scheduler running')
		# watch for events
		# update nodes
		# filer nodes
		# score Nodes
		try:
			self.updateNodes()
			self.printNodes()
		except Exception as e:
			print(str(e))
		return

	def updateNodes(self):
		'''
		Update nodes in self.all_nodes.
		to retrive all the data
		'''
		self.all_nodes = []
		for node in self.v1.list_node().items:
			self.all_nodes.append(Node(node))
		return

	def printNodes(self):
		'''
		For debug purposes only
		'''
		for node in self.all_nodes:
			print(node.node_data.metadata.name)
			print('usage')
			print(node.node_usage['usage'])
			print('capacity')
			print(node.node_data.status.capacity)


def main():
	scheduler = Scheduler()

if __name__ == '__main__':
    main()
