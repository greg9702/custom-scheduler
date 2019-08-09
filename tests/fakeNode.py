from kubernetes import client

'''
	Original node class attributes

	'api_version': 'str',
    'kind': 'str',
    'metadata': 'V1ObjectMeta',
    'spec': 'V1NodeSpec',
    'status': 'V1NodeStatus'
'''

class fakeNode():
	def __init__(self):
		self.metadata = client.models.V1ObjectMeta()
		self.spec = client.models.V1NodeSpec()
		self.status = client.models.V1NodeStatus()
		self.usage = {}
		# TODO add pods on this node attribute
