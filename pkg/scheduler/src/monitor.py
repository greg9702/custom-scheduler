import time
import os
from time import sleep
from datetime import datetime
from threading import Thread, Lock

from kubernetes import client, config

import settings
from node import Node, NodeList
from pod import Pod, PodList

NUMBER_OF_RETRIES = 7


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
        self.time_interval = settings.TIME_INTERVAL

        config.load_kube_config(config_file=os.path.join(os.path.dirname(__file__), '../kind-config'))
        self.v1 = client.CoreV1Api()

        self.all_pods = PodList()
        self.all_nodes = NodeList()  # TODO change to nodeList
        self.pods_not_to_garbage = []

    def print_nodes_stats(self):
        """
        Print node stats
        :return:
        """
        for node in self.all_nodes.items:
            print(node.metadata.name, node.usage)

    def update_nodes(self):
        """
        Makes request to API about Nodes in cluster,
        then starts to add rest of attributes
        :return:
        """
        self.status_lock.acquire(blocking=True)
        self.all_nodes = NodeList()
        print('Updating nodes')
        for node_ in self.v1.list_node().items:
            node = Node(node_.metadata, node_.spec, node_.status)
            node.update_node(self.all_pods)
            self.all_nodes.items.append(node)

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

    def wait_for_pod(self, new_pod):
        """
        Wait for Pod to be ready - got metrics from
        metrics server
        :param pod.Pod new_pod: Pod to wait for
        :return:
        """
        retries = 0

        while True:
            found = False

            self.status_lock.acquire(blocking=True)

            for pod in self.all_pods.items:
                if new_pod.metadata.name == pod.metadata.name:
                    found = True
                    break

            self.status_lock.release()

            if found:
                print('Waiting for pod %s' % new_pod.metadata.name)
                val = new_pod.fetch_usage()

                # do not add anything
                new_pod.usage = []

                if val == 0:
                    print('Pod %s ready...' % new_pod.metadata.name)
                    print(new_pod.usage)
                    break
                else:
                    print('Pod %s not ready...' % new_pod.metadata.name)

            else:
                print('Pod %s not found' % new_pod.metadata.name)

                retries += 1

                if retries == NUMBER_OF_RETRIES:
                    break

            sleep(1)

    def update_pods(self):
        """
        Update all Pods in cluster, if Pod exists add usage statistics
        to self.monitor_pods_data
        :return:
        """
        self.status_lock.acquire(blocking=True)

        # set all current pods as inactive
        for pod in self.all_pods.items:
            pod.is_alive = False

        for pod_ in self.v1.list_pod_for_all_namespaces().items:

            skip = False

            if pod_.status.phase == 'Running':
                for pod in self.all_pods.items:
                    if pod_.metadata.name == pod.metadata.name:
                        # found in collection, so update its usage
                        skip = True  # skip creating new Pod
                        pod.is_alive = True

                        res = pod.fetch_usage()

                        if res != 0:
                            if res == 404:
                                print('Metrics for pod %s not found ' % pod.metadata.name)
                            else:
                                print('Unknown metrics server error %s' % res)
                            break

                        # print('Updated metrics for pod %s' % pod.metadata.name)

                        break

                if not skip:
                    # this is new pod, add it to
                    pod = Pod(pod_.metadata, pod_.spec, pod_.status)
                    pod.is_alive = True
                    print('Added pod ' + pod.metadata.name)
                    self.all_pods.items.append(pod)

        print('Number of Pods ', len(self.all_pods.items))
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
        for pod in self.all_pods.items[:]:
            if not pod.is_alive:
                self.all_pods.items.remove(pod)
                print('Pod %s deleted' % pod.metadata.name)
        self.status_lock.release()

    def monitor_nodes(self):
        """
        Monitor Nodes usage
        :return:
        """
        pass


if __name__ == '__main__':
    print('Running')
    monitor = ClusterMonitor()

    p1 = Thread(target=monitor.monitor_runner)
    p2 = Thread(target=monitor.read_async)

    p1.start()

    p1.join()
