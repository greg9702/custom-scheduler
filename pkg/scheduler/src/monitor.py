#!/usr/bin/python

import time
import os
from kubernetes import client, config
from node import Node, NodeList
from pod import PodList, Pod
from multiprocessing import Process


class ClusterMonitor:
    """
    Build full view of cluster, periodically update
    info about Pods runtime resources usage, use this
    as statistics, to use average value instead of
    instantaneous value
    """
    def __init__(self):
        config.load_kube_config(config_file=os.path.join(os.path.dirname(__file__), '../kind-config'))
        self.v1 = client.CoreV1Api()

        self.all_pods = []
        self.hard_update_counter = 0 # when counter reach high value update whole pod info

        # {'Pod Name' : (Pod cpu usage, Pod memory usage)}
        self.monitor_pods_data = dict()

        # store all V1Node objects which represents Nodes in cluster
        self.all_nodes = []

        self.pods_not_to_garbage = list()

    def update_nodes(self):
        """
        Makes request to API about Nodes in cluster,
        then starts to add rest of attributes
        :return:
        """
        for node_ in self.v1.list_node().items:
            node = Node(node_.metadata, node_.spec, node_.status)
            node.update_node()
            self.all_nodes.append(node)

    def monitor_runner(self):
        """
        Run Pod monitor
        :return:
        """
        while True:
            self.update_pods()
            time.sleep(3)
            print(self.all_pods[0].get_usage())

    def update_pods(self):
        """
        Update all Pods in cluster, if Pod exists add usage statistics
        to self.monitor_pods_data
        :return:
        """
        self.pods_not_to_garbage = []
        for pod_ in self.v1.list_pod_for_all_namespaces().items:

            skip = False

            for pod in self.all_pods:
                if pod_.metadata.name == pod.metadata.name and pod_.status.phase == 'Running':
                    # found in collection, so update its usage
                    res = pod.fetch_usage()
                    if res != 0:
                        skip = True
                        if res == 404:
                            print('Metrics not found for pod %s skipping...' % pod.metadata.name)
                            self.pods_not_to_garbage.append(pod.metadata.name)
                        else:
                            print('Unknown Error')
                        break
                    print('Updated Pod %s' % pod.metadata.name)
                    self.pods_not_to_garbage.append(pod.metadata.name)
                    skip = True
                    break

            if not skip:
                # this is new pod, add it to
                pod = Pod(pod_.metadata,  pod_.spec, pod_.status)
                print('Added Pod %s' % pod.metadata.name)
                self.pods_not_to_garbage.append(pod.metadata.name)
                self.all_pods.append(pod)

        self.garbage_old_pods()

    def garbage_old_pods(self):
        """
        Collect dead pods from self.all_pods if Pod
        do not appeared in API response
        :return:
        """
        for pod in self.all_pods:
            if pod.metadata.name not in self.pods_not_to_garbage:
                # TODO implement garbage collector
                print('Pod %s should be deleted' % pod.metadata.name)

    def monitor_nodes(self):
        """
        Monitor Nodes usage
        :return:
        """
        pass


if __name__ == '__main__':
    print('Running')
    monitor = ClusterMonitor()
    p = Process(target=monitor.monitor_runner())
    p.start()
    p.join()

