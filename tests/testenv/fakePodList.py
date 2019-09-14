import json

from testenv.fakeContainer import fakeContainer
from testenv.fakePod import fakePod

from kubernetes import client

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
        return

    def addPods(self, pods_params):
        '''
        Creates fakePods and add it to self.items
        '''
        for pod in pods_params.split('$$$$'):
            fake_pod = fakePod()
            json_pod = json.loads(pod)
            fake_pod.spec.containers = []
            fake_pod.metadata.name = json_pod['metadata']['name']
            fake_pod.metadata.namespace = json_pod['metadata']['namespace']
            fake_pod.metadata.labels = json_pod['metadata']['labels']
            fake_pod.spec.affinity = json_pod['spec']['affinity']
            fake_pod.spec.node_name = json_pod['spec']['node_name']
            fake_pod.spec.scheduler_name = json_pod['spec']['scheduler_name']
            fake_pod.spec.tolerations = json_pod['spec']['tolerations']
            fake_pod.status.phase = json_pod['status']['phase']
            for el in json_pod['spec']['containers']:
                fake_pod.spec.containers.append(fakeContainer(el['name'], el['resources']['limits'], el['resources']['requests'], el['usage']))
            self.items.append(fake_pod)
        return
