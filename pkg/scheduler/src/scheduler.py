#!/usr/bin/python

import time
import json
import os

from time import sleep
from threading import Thread, Lock

from monitor import ClusterMonitor
from node import Node, NodeList

from kubernetes import client, config, watch


class Scheduler:
    def __init__(self):
        self.monitor = ClusterMonitor()
        self.watcher = watch.Watch()

        config.load_kube_config(config_file=os.path.join(os.path.dirname(__file__), '../kind-config'))
        self.v1 = client.CoreV1Api()

    def run(self):
        """
        Main thread, run and listen for events,
        If an event occurred, call monitor.update_nodes()
        and proceed scoring and scheduling process.
        """
        print('Scheduler running')

        p1 = Thread(target=self.monitor.monitor_runner)
        p1.start()

        while True:
            try:
                for event in self.watcher.stream(self.v1.list_pod_for_all_namespaces):
                    if event['type'] == 'ADDED':
                        print('New pod ' + event['object'].metadata.name)
                        # TODO create Pod object from received event data here
                        self.monitor.update_nodes()
                        print('Used scheduler: ' + event['object'].spec.scheduler_name)
            except Exception as e:
                print(str(e))
            sleep(5)

        p1.join()

    def choose_node(self, pod):
        """
        Method that brings together all methods
        responsible for choosing best Node for a Pod
        :param pod.Pod pod: Pod to be scheduled
        :return node.Node: return best selected Node for Pod,
            None if Pod cannot be scheduled
        """
        filtered_nodes = self.filter_nodes(pod)
        selected_node = self.score_nodes(pod, filtered_nodes)

        return selected_node

    def filter_nodes(self, pod):
        """
        Filter Nodes in self.monitor.all_nodes
        which can run selected Pod
        :param pod.Pod pod: Pod to be scheduled
        :return node.NodeList: List of Node which
            satisfy Pod requirements
        """
        return NodeList()

    def score_nodes(self, pod, node_list):
        """
        Score Nodes passed in node_list to choose the best one
        :param pod.Pod pod: Pod to be scheduled
        :param node.NodeList node_list: Nodes which meet Pod
            requirements
        :return node.Node: return Node which got highest score
            for Pod passed as pod, None if any node cannot be
            selected
        """
        return Node()

    def bind_to_node(self, pod_name, node_name, namespace='default'):
        """
        Bind Pod to a Node
        :param str pod_name: pod name which we are binding
        :param str node_name: node name which pod has to be binded
        :param str namespace: namespace of pod
        :return: True if pod was binded successfully, False otherwise
        """
        # 2nd method TODO test it
        # body = client.V1Binding()
        #
        # target = client.V1ObjectReference()
        # target.kind = "Node"
        # target.apiVersion = "v1"
        # target.name = node
        #
        # meta = client.V1ObjectMeta()
        # meta.name = name
        #
        # body.target = target
        # body.metadata = meta
        #
        # return v1.create_namespaced_binding_binding(name, namespace, body)

        target = client.V1ObjectReference()
        target.kind = "Node"
        target.api_version = "v1"
        target.name = node_name

        meta = client.V1ObjectMeta()
        meta.name = pod_name
        body = client.V1Binding(target=target)
        body.target = target
        body.metadata = meta

        try:
            self.v1.create_namespaced_binding(namespace, body)
            return True
        except Exception as e:
            print('exception' + str(e))
            return False

    @staticmethod
    def pass_to_scheduler(self, name_, namespace_, scheduler_name_='default-scheduler'):
        """
        Pass deployment to be scheduled by different scheduler
        :param str scheduler_name_: name of new scheduler, which will
            schedule this deployment
        :param str name_: name of deployment
        :param str namespace_: namespace of deployment
        :return str: return http response code
        """
        url = '/apis/extensions/v1beta1/namespaces/' + namespace_ + '/deployments/' + name_
        headers = {'Accept': 'application/json', 'Content-Type': 'application/strategic-merge-patch+json'}
        body = {"spec": {"template": {"spec": {"schedulerName": scheduler_name_}}}}

        api_client = client.ApiClient()
        response = []
        try:
            response = api_client.call_api(url, 'PATCH', header_params=headers, body=body)
        except Exception as e:
            return int(str(e)[1:4])

        return response[1]


def main():
    scheduler = Scheduler()
    scheduler.run()


if __name__ == '__main__':
    main()
