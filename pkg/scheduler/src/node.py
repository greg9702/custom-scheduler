from kubernetes import client
from pod import PodList


class NodeList(object):
    def __init__(self):
        self.items = list()


class Node(object):
    def __init__(self):
        self.metadata = client.models.V1ObjectMeta()
        self.spec = client.models.V1NodeSpec()
        self.status = client.models.V1NodeStatus()
        self.usage = {}
        self.pods = PodList()
        # if node do not appeared in api request, give it some sec
        self.is_alive = True
        self.last_heartbeat = 0

    def update_node(self, metadata_, spec_, status_, pods_):
        """
        Update existing node
        :param V1etadata metadata_:
        :param spec_:
        :param status_:
        :param pods_:
        :return:
        """

        #TODO set usage
        self.metadata = metadata_
        self.spec = spec_
        self.status = status_
        self.pods = pods_

    def get_node_usage(self):
        memory = 0
        cpu = 0
        for pod in self.pods.items:
            memory += pod.usage['memory']
            cpu += pod.usage['cpu']

        return dict({'cpu': cpu, 'memory': memory})