from kubernetes import client

'''
    Original pod class attributes

    'api_version': 'str',
    'kind': 'str',
    'metadata': 'V1ObjectMeta',
    'spec': 'V1PodSpec',
    'status': 'V1PodStatus'
'''

class fakePod:
    def __init__(self):
        self.metadata = client.models.V1ObjectMeta()
        self.spec = client.models.V1PodSpec(containers = [])
        self.status = client.models.V1PodStatus()
        return
