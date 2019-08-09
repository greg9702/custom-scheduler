import json
from fakeNode import fakeNode

'''
		Original node list class attributes

        'api_version': 'str',
        'items': 'list[V1Node]',
        'kind': 'str',
        'metadata': 'V1ListMeta'
'''

class fakeNodeList:
	def __init__(self):
		#'items': 'list[V1Node]',
		self.items = []

	def addNodes(self, nodes_params):
		'''
		Creates fakeNodes nodes and append it to self.items
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
			fake_node.usage = json_node['usage'] # this should not be here, but for simplicity it is
			self.items.append(fake_node)
