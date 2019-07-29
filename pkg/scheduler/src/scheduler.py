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
		Use getNodesUsage() and self.v1.list_node()
		to retrive all the data
		'''
		self.all_nodes = []
		for node in self.v1.list_node().items:
			tmp_node = Node(node, self.getNodeUsage(node.metadata.name))
			self.all_nodes.append(tmp_node)
		return

	def getNodeUsage(self, name=None):
		'''
		TODO move to Node module
		Get resources usage of Node
		:param str name: Name of node
		:return json object: object containg Node info
		'''

		if name == None:
			raise Exception('Not passed Node name')

		metrics_url = '/apis/metrics.k8s.io/v1beta1/nodes/' + name
		api_client = client.ApiClient()
		response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
		resp = response[0].data.decode('utf-8')
		json_data = json.loads(resp)
		return json_data

	def printNodes(self):
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
