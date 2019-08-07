from kubernetes import client
from fakePod import fakePod


'''
		Original pod class

        'api_version': 'str',
        'items': 'list[V1Pod]',
        'kind': 'str',
        'metadata': 'V1ListMeta'
'''

class fakePod:
	def __init__(self):
		self.items = []
		pass

	def addPods(self, pods_params):
		
		pass
