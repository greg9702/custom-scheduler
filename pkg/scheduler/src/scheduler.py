#!/usr/bin/python

import time
import random
import json
import sys
import os
import copy


from pprint import pprint
from kubernetes import client, config, watch

class Scheduler:
	def __init__(self):
		# adding my own attribute to V1Node object for tracking usage
		client.models.v1_node.V1Node.swagger_types['usage'] = 'object'
		client.models.v1_node.V1Node.attribute_map['usage'] = 'usage'
		# adding my own attribute to V1Node object for
		client.models.v1_node.V1Node.swagger_types['pods'] = 'V1PodList'
		client.models.v1_node.V1Node.attribute_map['pods'] = 'pods'

		self.scheduler_name = 'custom_scheduler'
		self.all_nodes=[]

		config.load_kube_config(config_file=os.path.join(os.path.dirname(__file__), '../kind-config'))
		self.v1 = client.CoreV1Api()

		return

	def run(self):
		print('Scheduler running')
		self.updateNodes()
		self.podsOnNodes()
		return
		try:
			w = watch.Watch()
			for event in w.stream(self.v1.list_namespaced_pod, "default"): # TODO watch all namespaces
				print("Event happened")
				self.updateNodes()
				print("Used scheduler: " + event['object'].spec.scheduler_name)
				print ("Scheduling pod: ", event['object'].metadata.name)
				if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == self.scheduler_name:
					try:
						print ("Scheduling pod: ", event['object'].metadata.name)
						res = self.bindToNode(event['object'].metadata.name, self.scoreNodes())
					except client.rest.ApiException as e:
						print (json.loads(e.body)['message'])
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
			node.pods = client.models.V1PodList(items = [])
			node.pods.items = []
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

	def filterNodes(self):
		'''
		In v0.1.0 all nodes are passed to next step
		#TODO if after this phase there is only one node, select it
		Filter out nodes form self.all_nodes which do not meet pod requirements
		:return Node array: Nodes which met pod requirements
		'''
		return self.all_nodes

	def scoreNodes(self):
		'''
		Rate every node returned by self.filterNodes()
		:return: return Node with the highest rating
		'''
		filtered_nodes = self.filterNodes()
		ret_node = filtered_nodes[0]
		for node in filtered_nodes:
			# print (node.metadata.name)
			node_mem_usage = int(node.usage['memory'][:-2])
			# print (node_mem_usage)
			ret_node_mem_usage = int(ret_node.usage['memory'][:-2])
			if node_mem_usage < ret_node_mem_usage:
				ret_node = node

		print('selected node', ret_node.metadata.name)
		return ret_node.metadata.name

	def bindToNode(self, pod_name, node, namespace='default'):
		'''
		Bind Pod to Node
		:param str pod:
		:param str node:
		'''
		target = client.V1ObjectReference()
		target.kind = "Node"
		target.api_version = "v1"
		target.name = node

		meta = client.V1ObjectMeta()
		meta.name = pod_name
		body = client.V1Binding(target = target)
		body.target = target
		body.metadata = meta
		try:
			self.v1.create_namespaced_binding(namespace, body)
			return True
		except:
			print ('exception')
			return False

	def retNode(self, name_ = None):
		'''
		Get node object
		:param str name: name of the node
		:return: return node object
		'''
		if name_ == None:
			raise Exception('passed wrong node name')

		for node in self.all_nodes:
			if node.metadata.name == name_:
				return node

		return None

	def podsOnNodes(self):
		'''
		Assign Pod to node which
		'''
		for pod in self.v1.list_pod_for_all_namespaces().items:
			# if pod is running, it is assigned to node
			if pod.status.phase == 'Running':
				for node in self.all_nodes:
					if node.metadata.name == pod.spec.node_name:
						node.pods.items.append(pod)

		return

def main():
	scheduler = Scheduler()
	scheduler.run()

if __name__ == '__main__':
    main()
