import time
import random
import json
import requests
import pprint

from kubernetes import client, config, watch

config.load_kube_config(config_file='../kind-config')

# TODO change this to object
# TODO change function to return jsons

def nodesUsage():
	'''
	Print resources usage of every node
	:return:
	'''
	metrics_url = '/apis/metrics.k8s.io/v1beta1/nodes'
	api_client = client.ApiClient()
	response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
	resp = response[0].data.decode('utf-8')
	json_data = json.loads(resp)
	pprint.pprint(json_data)
	return

def allNodesUsage():
	'''
	Print resources usage of pods from all namespaces
	:return:
	'''
	metrics_url = '/apis/metrics.k8s.io/v1beta1/pods'
	api_client = client.ApiClient()
	response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
	resp = response[0].data.decode('utf-8')
	json_data = json.loads(resp)
	pprint.pprint(json_data)
	return

def nodesUsageFromNamespace(namespace='default'):
	'''
	:param str namespace: Name of namespace
	Print resources usage of pods from single namespace
	:return:
	'''
	metrics_url = '/apis/metrics.k8s.io/v1beta1/namespaces/' + namespace + '/pods'
	api_client = client.ApiClient()
	response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
	resp = response[0].data.decode('utf-8')
	json_data = json.loads(resp)
	pprint.pprint(json_data)
	return

def main():
	nodesUsageFromNamespace()

if __name__ == '__main__':
	main()
