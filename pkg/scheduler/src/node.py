from kubernetes import client
from pod import PodList


class NodeList(object):
    def __init__(self):
        self.items = list()


class Node(object):
    def __init__(self, metadata_, spec_, status_):
        """
        :param V1ObjectMeta metadata_:
        :param V1NodeSpec spec_:
        :param V1NodeStatus status_:
        :return:
        """
        if type(metadata_) is not client.models.v1_object_meta.V1ObjectMeta:
            raise str("Passed invalid type")
        if type(spec_) is not client.models.V1NodeSpec:
            raise str("Passed invalid type")
        if type(status_) is not client.models.V1NodeStatus:
            raise str("Passed invalid type")

        self.usage = dict()
        self.pods = PodList()

        self.metadata = metadata_
        self.spec = spec_
        self.status = status_

    def update_node(self):
        """
        Update Node Pods and usage attributes
        :return:
        """
        self.pods = self.get_pods_on_node()
        self.usage = self.get_node_usage()

    def get_node_usage(self):
        """
        Calculate Node usage based on usage of
        Pods running on this node
        :return:
        """
        memory = 0
        cpu = 0
        for pod in self.pods.items:
            memory += pod.usage['memory']
            cpu += pod.usage['cpu']

        return dict({'cpu': cpu, 'memory': memory})

    def get_pods_on_node(self):
        """
        Browse all avaliable Pods in cluster and
        assign them to Node
        :return PodList:
        """
        result = PodList()
        # search through all Pods and append this Pods
        # which have Node.metadata.name == Pod.spec.node_name


        return result
