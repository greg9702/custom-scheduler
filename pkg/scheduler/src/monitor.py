#!/usr/bin/python

import os
import json
from kubernetes import client, config
from node import Node, NodeList
from pod import PodList, Pod


class ClusterMonitor:
    """
    Build full view of cluster, periodically update
    info about Nodes runtime resources usage, use this
    as statistics, to use average value instead of
    instantaneous value
    """
    def __init__(self):
        config.load_kube_config(config_file=os.path.join(os.path.dirname(__file__), '../kind-config'))
        self.v1 = client.CoreV1Api()

        # {'Pod Name' : (Pod cpu usage, Pod memory usage)}
        self.monitor_pods_data = dict()

        # {'Node Name' : [(Node cpu usage, Node memory usage)]}
        self.monitor_nodes_data = dict()

        # store all V1Node objects which represents Nodes in cluster
        self.all_nodes = []

        # extend V1Node class
        # usage attribute is calculated using average value
        client.models.v1_node.V1Node.swagger_types['usage'] = 'dict(str, str)'
        client.models.v1_node.V1Node.attribute_map['usage'] = 'usage'

        client.models.v1_node.V1Node.swagger_types['pods'] = 'V1PodList'
        client.models.v1_node.V1Node.attribute_map['pods'] = 'pods'

        # Node usage can be calculated as usage of every Pod running on this Node
        client.models.v1_pod.V1Pod.swagger_types['usage'] = 'dict(str, str)'
        client.models.v1_pod.V1Pod.attribute_map['usage'] = 'usage'

    def get_nodes(self):
        return self.nodes

    def update_nodes(self):
        """
        Makes request to API about Nodes in cluster,
        then starts to add rest of attributes
        :return:
        """
        for node in self.v1.list_node().items:
            for n in self.all_nodes:
                # check if node exists, it is update, else create
                pass

    def set_pods_on_node(self, name_):
        """
        Assign pod on node
        :param str name_: name of a Node
        :return:
        """
        result = PodList()
        for pod in self.v1.list_pod_for_all_namespaces().items:
            if pod.status.phase == 'Running':
                if pod.spec.node_name == name_:
                    pass
                    # create Pod
                    # pod.fetch_usage()
            pass





if __name__ == '__main__':
    print('Running')
    monitor = ClusterMonitor()
    monitor.update_nodes()
