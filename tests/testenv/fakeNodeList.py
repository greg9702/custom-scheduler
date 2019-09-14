import json

from testenv.fakeNode import fakeNode

"""
    Original node list class attributes
    v1_node_list.py
        'api_version': 'str',
        'items': 'list[V1Node]',
        'kind': 'str',
        'metadata': 'V1ListMeta'
"""

class fakeNodeList:
    """Mock class used in tests"""

    def __init__(self):
        self.items = []

    def addNodes(self, node_params):
        """Creates fakeNodes and append it to self.items"""

        for node in node_params.split('$$$$'):
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
        return
