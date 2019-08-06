import json
from pprint import pprint
from fakeNode import fakeNode

from kubernetes import client, config, watch

nodes_params = [
'''{"metadata": { "labels": {"beta.kubernetes.io/arch": "amd64",
                         "beta.kubernetes.io/os": "linux",
                         "kubernetes.io/arch": "amd64",
                         "kubernetes.io/hostname": "kind-control-plane",
                         "kubernetes.io/os": "linux",
                         "node-role.kubernetes.io/master": ""},
              "name": "kind-control-plane"},
 "spec": {"taints": [{"effect": "NoSchedule",
                      "key": "node-role.kubernetes.io/master",
                      "time_added": "None",
                      "value": "None"}],
          "unschedulable": "None"},
 "status": {"allocatable": {"cpu": "4",
                            "ephemeral-storage": "479177440Ki",
                            "hugepages-2Mi": "0",
                            "memory": "8045056Ki",
                            "pods": "110"},
            "capacity": {"cpu": "4",
                         "ephemeral-storage": "479177440Ki",
                         "hugepages-2Mi": "0",
                         "memory": "8045056Ki",
                         "pods": "110"}},
 "usage": {"cpu": "253011429n", "memory": "698744Ki"}}''',

'''{"metadata": { "labels": {"beta.kubernetes.io/arch": "amd64",
                         "beta.kubernetes.io/os": "linux",
                         "kubernetes.io/arch": "amd64",
                         "kubernetes.io/hostname": "worker-node",
                         "kubernetes.io/os": "linux",
                         "node-role.kubernetes.io/master": ""},
              "name": "worker-node"},
 "spec": {"taints": [{"effect": "NoSchedule",
                      "key": "node-role.kubernetes.io/master",
                      "time_added": "None",
                      "value": "None"}],
          "unschedulable": "None"},
 "status": {"allocatable": {"cpu": "4",
                            "ephemeral-storage": "479177440Ki",
                            "hugepages-2Mi": "0",
                            "memory": "8045056Ki",
                            "pods": "110"},
            "capacity": {"cpu": "4",
                         "ephemeral-storage": "479177440Ki",
                         "hugepages-2Mi": "0",
                         "memory": "8045056Ki",
                         "pods": "110"}},
 "usage": {"cpu": "253011429n", "memory": "698744Ki"}}'''
 ]

class fakeCluster:
	def __init__(self, nodes_params):
		'''
		Creates fake cluster with fake nodes and pods
		:param list nodes_params: params for nodes
		'''
		self.fake_nodes = []
		self.fake_pods = []
		self.createNode(nodes_params)

	def createNode(self, nodes_params):
		'''
		Creates nodes using passed params and node template
		:param list nodes_params: params for nodes
		:return: return list of json object, which imitate nodes
		'''

		for node in nodes_params:
			fake_node = fakeNode()
			json_node = json.loads(node)
			fake_node.metadata.labels = json_node['metadata']['labels']
			fake_node.metadata.name = json_node['metadata']['name']
			fake_node.spec.taints = json_node['spec']['taints']
			fake_node.spec.unschedulable = json_node['spec']['unschedulable']
			fake_node.status.allocatable = json_node['status']['allocatable']
			fake_node.status.capacity = json_node['status']['capacity']
			fake_node.usage = json_node['usage']
			self.fake_nodes.append(fake_node)


		return


def main():
	f = fakeCluster(nodes_params)
if __name__ == '__main__':
    main()
