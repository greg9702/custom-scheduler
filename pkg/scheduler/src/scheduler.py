#!/usr/bin/python

import time
import random
import json
import sys

from kubernetes import client, config, watch

config.load_kube_config(config_file='../kind-config-kind')
v1 = client.CoreV1Api()
print ("v1", v1)

scheduler_name = "foobar"

def nodes_available():
    ready_nodes = []
    for n in v1.list_node().items:
            for status in n.status.conditions:
                if status.status == "True" and status.type == "Ready":
                    ready_nodes.append(n.metadata.name)
    return ready_nodes

def scheduler(name, node, namespace='default'):

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

def main():
	print("Scheduler running... ")
	w = watch.Watch()

	for event in w.stream(v1.list_namespaced_pod, "default"):
		print("Event happened")
		print("Used scheduler: " + event['object'].spec.scheduler_name)
		print ("Scheduling pod: ", event['object'].metadata.name)
		if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name and event['object'].spec.node_name== None:
			try:
				print ("Scheduling pod: ", event['object'].metadata.name)
				print ("nodes aval: ", nodes_available())
				print ("selected node: ",  random.choice(nodes_available()))
				res = scheduler(event['object'].metadata.name, random.choice(nodes_available()))
			except client.rest.ApiException as e:
				print (json.loads(e.body)['message'])


if __name__ == '__main__':
    main()
