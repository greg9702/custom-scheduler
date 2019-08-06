# TODO add __repr__

class fakeNode:
	def __init__(self):
		self.metadata = metadata()
		self.spec = spec()
		self.status = status()
		self.usage = usage()


class metadata:
	def __init__(self):
		self.labels = {}
		self.name = ""
		pass

class spec:
	def __init__(self):
		self.taints = []
		self.unschedulable = ''

class status:
	def __init__(self):
		self.allocatable = {}
		self.capacity = {}

class usage:
	def __init__(self):
		pass
