#!/usr/bin/python

import time
import random
import json
import sys
import pprint
import copy

from kubernetes import client, config, watch

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
		# bind Pod to Node
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
			node.usage = self.getNodeUsage(node.metadata.name)
			self.all_nodes.append(node)

		return

	def getNodeUsage(self, name_ = None):
		'''
		Get resources usage of Node
		:param str name: Name of node
		:return json object: object containg Node info
		'''
		if name_ == None:
			raise Exception('passed wrong node name')

		metrics_url = '/apis/metrics.k8s.io/v1beta1/nodes/' + name_
		api_client = client.ApiClient()
		response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
		resp = response[0].data.decode('utf-8')
		json_data = json.loads(resp)
		return json_data['usage']

	def filterNodes(self, pod):
		'''
		In v0.1.0 all nodes are passed to next step
		Filter out nodes form self.all_nodes which do not meet pod requirements
		:return Node array: Nodes which met pod requirements
		'''

		return

	def scoreNodes(self, pod):
		'''
		Rate every node returned by self.filterNodes()
		:return: return Node with the highest rating
		'''
		return

	def bindToNode(pod, node):
		'''
		Bind Pod to Node
		:param str pod:
		:param str node:
		'''
		return

	def printNodes(self):
		'''
		For debug purposes only
		'''
		for node in self.all_nodes:
			print(node.metadata.name)
			print('usage')
			print(node.usage)
			print('capacity')
			print(node.status.capacity)


def main():
	scheduler = Scheduler()

if __name__ == '__main__':
    main()
