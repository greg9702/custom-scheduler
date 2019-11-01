#!/usr/bin/python

import time
import os
from kubernetes import client, config
from node import Node, NodeList
from pod import PodList, Pod
from threading import Thread, Lock
from time import sleep

# refresh interval in seconds
TIME_INTERVAL = 3


class ClusterMonitor:
    """
    Build full view of cluster, periodically update
    info about Pods runtime resources usage, use this
    as statistics, to use average value instead of
    instantaneous value
    """

    def __init__(self):
        self.status_lock = Lock()

        # time interval is seconds to update Pods statistics
        self.time_interval = TIME_INTERVAL

        config.load_kube_config(config_file=os.path.join(os.path.dirname(__file__), '../kind-config'))
        self.v1 = client.CoreV1Api()

        self.all_pods = []  # TODO change to podList
        self.all_nodes = []  # TODO change to nodeList
        self.pods_not_to_garbage = []

    def print_nodes_stats(self):
        """
        Print node stats
        :return:
        """
        for node in self.all_nodes:
            print(node.metadata.name, node.usage)

    def update_nodes(self):
        """
        Makes request to API about Nodes in cluster,
        then starts to add rest of attributes
        :return:
        """
        self.status_lock.acquire(blocking=True)
        self.all_nodes = []
        print('Updating nodes')
        for node_ in self.v1.list_node().items:
            node = Node(node_.metadata, node_.spec, node_.status)
            node.update_node(self.all_pods)
            self.all_nodes.append(node)

        self.status_lock.release()

    def monitor_runner(self):
        """
        Run Pod monitor
        :return:
        """
        print('Monitor runner started')
        while True:
            print('monitor tick')
            self.update_pods()
            time.sleep(self.time_interval)

    def update_pods(self):
        """
        Update all Pods in cluster, if Pod exists add usage statistics
        to self.monitor_pods_data
        :return:
        """
        self.status_lock.acquire(blocking=True)

        # set all current pods as inactive
        for pod in self.all_pods:
            pod.is_alive = False
        for pod_ in self.v1.list_pod_for_all_namespaces().items:

            skip = False

            if pod_.status.phase == 'Running':
                for pod in self.all_pods:
                    if pod_.metadata.name == pod.metadata.name:
                        # found in collection, so update its usage
                        skip = True  # skip creating new Pod

                        res = pod.fetch_usage()
                        pod.is_alive = True
                        # TODO what to do when metrics reciving failed
                        if res != 0:
                            if res == 404:
                                print('Metrics for pod %s not found ' % pod.metadata.name)
                            else:
                                print('Unknown metrics server error %s' % res)
                            break

                        #                        print('Updated metrics for pod %s' % pod.metadata.name)

                        break

                if not skip:
                    # this is new pod, add it to
                    pod = Pod(pod_.metadata, pod_.spec, pod_.status)
                    pod.is_alive = True
                    print('Added pod ' + pod.metadata.name)
                    print('number of pods %s' % len(self.all_pods))
                    self.all_pods.append(pod)

        print('Number of Pods ', len(self.all_pods))
        self.status_lock.release()
        self.garbage_old_pods()

    def garbage_old_pods(self):
        """
        Remove dead pods from self.all_pods if Pod
        do not appeared in API response,
        dead Pods have self.is_alive set to False
        :return:
        """
        self.status_lock.acquire(blocking=True)
        for pod in self.all_pods[:]:
            if not pod.is_alive:
                self.all_pods.remove(pod)
                print('Pod %s deleted' % pod.metadata.name)
        self.status_lock.release()

    def monitor_nodes(self):
        """
        Monitor Nodes usage
        :return:
        """
        pass

    def read_async(self):
        """
        Mock function for tests only,
        self.update_nodes() will be called when
        event happened in scheduler.event_monitor
        :return:
        """
        while True:
            # event happened
            self.update_nodes()
            sleep(5)


if __name__ == '__main__':
    print('Running')
    monitor = ClusterMonitor()

    p1 = Thread(target=monitor.monitor_runner)
    p2 = Thread(target=monitor.read_async)

    p2.start()
    p1.start()

    p1.join()
    p2.join()
