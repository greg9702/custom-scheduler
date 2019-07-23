#!/usr/bin/python

import time
import random
import json
import requests

from kubernetes import client, config, watch

config.load_kube_config(config_file='../kind-config-kind')
v1 = client.CoreV1Api()

def main():
	# while True:
	# 	ready_nodes = []
	# 	for n in v1.list_node().items:
	# 		for status in n.status.conditions:
	# 			if status.status == "True" and status.type == "Ready":
	# 				ready_nodes.append(n.metadata.name)
	# 				ready_nodes.append(n.metadata.name)
	# 				api_res = v1.read_node(n.metadata.name)
	# 				print (api_res)
	# 	print('ready nodes', ready_nodes)
	# 	time.sleep(5)
	endpoint = "https://172.17.0.3:6443/api/v1/nodes/kind-worker"
	# data = {"ip": "1.1.2.3"}
	headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi10aDJwcCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImVkMjUzMGU2LTk5ZjMtNDNkYy04YzE5LTgyMDg0YmFlN2I4NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.VMn9AoaOlkMICYLCVhzHcjZX5vmCw7fKzSk5uynAaJHHBuDOKvnh_QbcBpUffpslfjuN6VXXb8xt3xvwZNMeU8oA-6q8O2tpRLzFnEkOfwykgOYq7zqR-45_wKM54OhUhX6LwUwzjRzY5vEn9sqJG2IbZdochjiHPFpltgvkq3h07cfHpvsghOWQyPS9gB4BCweukmp21kIBqi_JE0itBjMS3S6vnOZvQd7-9CxnQZ3rTjW9itD-YFCi1kkSb8NSblW3BhZ0nDYd7WlRgVxtRC6v6ensZeVSZyzdg14N9Z8xFk2Q36SvceBi4Va7DWembesWNz9u6ImZhNVJzMTN9w"}

	print(requests.post(endpoint, headers=headers).json())


if __name__ == '__main__':
	main()
