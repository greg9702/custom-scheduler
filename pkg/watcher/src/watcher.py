#!/usr/bin/python

import time
import random
import json
import requests

from kubernetes import client, config, watch

config.load_kube_config(config_file='../kind-config-kind')
v1 = client.CoreV1Api()

scheduler_name = "foobar"

def main():
	while True:
		ready_nodes = []
		for n in v1.list_node().items:
			for status in n.status.conditions:
				if status.status == "True" and status.type == "Ready":
					ready_nodes.append(n.metadata.name)
					ready_nodes.append(n.metadata.name)
					api_res = v1.read_node(n.metadata.name)
					print (api_res)
		print('ready nodes', ready_nodes)
		time.sleep(5)


if __name__ == '__main__':
	main()
