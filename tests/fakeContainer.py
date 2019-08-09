from kubernetes import client

'''
    Original containter class

    'args': 'list[str]',
    'command': 'list[str]',
    'env': 'list[V1EnvVar]',
    'env_from': 'list[V1EnvFromSource]',
    'image': 'str',
    'image_pull_policy': 'str',
    'lifecycle': 'V1Lifecycle',
    'liveness_probe': 'V1Probe',
    'name': 'str',
    'ports': 'list[V1ContainerPort]',
    'readiness_probe': 'V1Probe',
    'resources': 'V1ResourceRequirements',
    'security_context': 'V1SecurityContext',
    'stdin': 'bool',
    'stdin_once': 'bool',
    'termination_message_path': 'str',
    'termination_message_policy': 'str',
    'tty': 'bool',
    'volume_devices': 'list[V1VolumeDevice]',
    'volume_mounts': 'list[V1VolumeMount]',
    'working_dir': 'str'
'''

class fakeContainer:
    def __init__(self, name = "", limits = {}, requests = {}):
        '''
        :param str name: container name
        :param dict limits: container memory and cpu limits
        :param dict requests: container memory and cpu requests
        '''
        self.name = name
        self.resources = client.models.V1ResourceRequirements()
        self.resources.limits = limits
        self.resources.requests = requests
        return
