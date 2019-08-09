from kubernetes import client

class fakeContainer:
	def __init__(self, name = "", limits = {}, requests = {}):
		self.name = name
		self.resources = client.models.V1ResourceRequirements()
		self.resources.limits = limits
		self.resources.requests = requests
