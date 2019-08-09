import json
import fakeContainer
import pod_template
from kubernetes import client
from fakePod import fakePod

'''
		Original pod class

        'api_version': 'str',
        'items': 'list[V1Pod]',
        'kind': 'str',
        'metadata': 'V1ListMeta'
'''

class fakePodList:
	def __init__(self):
		self.items = []
		pass

	def addPods(self):
		pods_params = pod_template.pods_params
		for pod in pods_params:
			fake_pod = fakePod()
			json_pod = json.loads(pod)
			fake_pod.spec.containers = []
			fake_pod.metadata.generate_name = json_pod['metadata']['generate_name']
			fake_pod.metadata.labels = json_pod['metadata']['labels']
			fake_pod.spec.affinity = json_pod['spec']['affinity']
			fake_pod.spec.node_name = json_pod['spec']['node_name']
			fake_pod.spec.scheduler_name = json_pod['spec']['scheduler_name']
			fake_pod.spec.tolerations = json_pod['spec']['tolerations']
			fake_pod.status.phase = json_pod['status']['phase']
			for el in json_pod['spec']['containers']:
				fake_pod.spec.containers.append(fakeContainer.fakeContainer(el['name'], el['resources']['limits'], el['resources']['requests']))
			self.items.append(fake_pod)

if __name__ == '__main__':
	f = fakePodList()
	f.addPods(pod_template.pods_params)
	for el in f.items:
		for i in el.spec.containers:
			print(i.name)
