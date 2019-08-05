import json
from pprint import pprint
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
		template = {}
		try:
			with open('node_template.json', 'r') as f:
				template = json.load(f)
		except Exception as e:
			pprint(str(e))
		# pprint(json_node)
		pprint(template.usage)
		# for node in nodes_params:
			# json_node = json.loads(node)
			# for element in json_node:
				# pprint(template.metadata)
		return

nodes_params = ['''{"metadata": { "labels": {"beta.kubernetes.io/arch": "amd64",
                         "beta.kubernetes.io/os": "linux",
                         "kubernetes.io/arch": "amd64",
                         "kubernetes.io/hostname": "kind-control-plane",
                         "kubernetes.io/os": "linux",
                         "node-role.kubernetes.io/master": ""},
              "name": "kind-control-plane"},
 "spec": {"taints": [{"effect": "NoSchedule",
                      "key": "node-role.kubernetes.io/master",
                      "time_added": "None",
                      "value": "None"}]},
          "unschedulable": "None",
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
 "usage": {"cpu": "253011429n", "memory": "698744Ki"}}''']

def main():
	f = fakeCluster(nodes_params)
if __name__ == '__main__':
    main()
