#!/usr/bin/python

import time
import random
import json
import sys
import pprint

from kubernetes import client, config, watch

class Scheduler:
	def __init__(self):
		config.load_kube_config(config_file='../kind-config')
		self.v1 = client.CoreV1Api()
		self.scheduler_name = 'custom_scheduler'
		self.ready_nodes = []
		self.run()

	def run(self):
		self.ready_nodes = self.filterNodes()

		# nodes_usage =
		for node in self.ready_nodes:
			print(node.metadata.name) # there we can get general info about node, e.g. name
			print(node.status.allocatable['memory']) # there we can get more details about node
			print('///////' * 10)

		aa = self.nodesUsage()['items']

		for item in aa :
			pprint.pprint(item['metadata'])
		# pprint.pprint(self.nodesUsage()['items'][0]['metadata']['name'])
		# print('Listing pods with their IPs:')
		# ret = self.v1.list_pod_for_all_namespaces(watch=False)
		# for i in ret.items:
		# 	print("%s\t%s\t%s\t%s" % (i.status.pod_ip, i.status.phase, i.metadata.namespace, i.metadata.name))
		# 	if i.status.phase == 'Pending':
		# 		self.bindToNode(i.metadata.name, self.ready_nodes[1], i.metadata.namespace)
		# print('Exit scheduler...')
		return


	def filterNodes(self):
		'''
		Filter Nodes, to select only this which
		satisfy Pod requirements
		v0.1.0 this function return all Nodes
		:return: array of Nodes
		'''
		ready_nodes = []

		for n in self.v1.list_node().items:
			for status in n.status.conditions:
				if status.status == "True" and status.type == "Ready":
					if n.metadata.name not in ready_nodes:
						ready_nodes.append(n)
		return ready_nodes

	def scoreNodes(self, passed_nodes):
		'''
		Score every Node passed to this function
		v0.1.0 return Node which has least memory usage
		:param array passed_nodes: Nodes which satisfy Pod requests
		:return: return the Best Node
		'''
		returnallNodesUsage

	def bindToNode(self, name, node, namespace='default'):
		'''
		Bind pod to node
		'''
		target = client.V1ObjectReference()
		target.kind = "Node"
		target.api_version = "v1"
		target.name = node

		meta = client.V1ObjectMeta()
		meta.name = name
		body = client.V1Binding(target = target)
		body.target = target
		body.metadata = meta
		try:
			v1.create_namespaced_binding(namespace, body)
			return True
		except:
			print ('exception')
			return False

	def nodesUsage(self):
		'''
		Print resources usage of every node
		:return:
		'''
		metrics_url = '/apis/metrics.k8s.io/v1beta1/nodes'
		api_client = client.ApiClient()
		response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
		resp = response[0].data.decode('utf-8')
		json_data = json.loads(resp)

		return json_data

def main():
	print("Scheduler running... ")
	scheduler = Scheduler()

if __name__ == '__main__':
    main()
