#!/usr/bin/python

import json
from kubernetes import client, config, watch

class Node:
	def __init__(self, node_data_):
		config.load_kube_config(config_file='../kind-config')
		self.v1 = client.CoreV1Api()
		self.node_data = node_data_
		self.node_usage = self.getNodeUsage()
		return

	def getNodeUsage(self):
		'''
		Get resources usage of Node
		:param str name: Name of node
		:return json object: object containg Node info
		'''
		metrics_url = '/apis/metrics.k8s.io/v1beta1/nodes/' + self.node_data.metadata.name
		api_client = client.ApiClient()
		response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
		resp = response[0].data.decode('utf-8')
		json_data = json.loads(resp)
		return json_data
