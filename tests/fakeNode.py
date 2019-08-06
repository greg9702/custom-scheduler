from kubernetes import client

class fakeNode(client.models.V1Node):
	def __init__(self):
		client.models.v1_node.V1Node.swagger_types['usage'] = 'object'
		client.models.v1_node.V1Node.attribute_map['usage'] = 'usage'
		self.api_version = "fakenode"
		self.kind = "fakenode"
		self.metadata = client.models.V1ObjectMeta()
		self.spec = client.models.V1NodeSpec()
		self.status = client.models.V1NodeStatus()
		self.usage = {}

def main():
	f = fakeNode()
	print(f.usage)

if __name__ == '__main__':
	main()
