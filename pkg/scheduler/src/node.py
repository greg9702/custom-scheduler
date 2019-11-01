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

        self.usage = {}
        self.pods = PodList()

        self.metadata = metadata_
        self.spec = spec_
        self.status = status_

    def update_node(self, pod_list):
        """
        Update Node Pods and usage attributes
        :return:
        """
        self.pods = self.get_pods_on_node(pod_list)
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
            if pod.is_alive:
                # there can be nodes not collected by garbage collector
                memory += int(pod.get_usage()['memory'])
                cpu += int(pod.get_usage()['cpu'])

        return {'cpu': cpu, 'memory': memory}

    def get_pods_on_node(self, pod_list):
        """
        Browse all avaliable Pods in cluster and
        assign them to Node
        :return PodList:
        """
        result = PodList()
        for pod in pod_list:
            if pod.spec.node_name == self.metadata.name:
                result.items.append(pod)

        return result
