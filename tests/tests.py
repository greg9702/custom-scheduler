import pytest
import os
import sys
import unittest
import json

from unittest.mock import patch
from kubernetes import client

from testenv import creator

sys.path.append(os.path.join(os.path.dirname(__file__), '../pkg/scheduler/src'))
from scheduler import Scheduler

class testClass(unittest.TestCase):

    def setUp(self):
        try:
            self.nodes_list = creator.create_from_file(os.path.join(os.path.dirname(__file__), 'scenario_01/node_01.template'), 'Node')
        except BaseException as e:
            print('Error occured!', str(e))
            sys.exit(-1)

        try:
            self.pods_list = creator.create_from_file(os.path.join(os.path.dirname(__file__), 'scenario_01/pods_01.template'), 'Pod')
        except BaseException as e:
            print('Error occured!', str(e))
            sys.exit(-1)

        self.patcher1 = patch('kubernetes.client.CoreV1Api.list_node')
        self.mock_list_nodes = self.patcher1.start()

        self.patcher2 = patch('kubernetes.client.CoreV1Api.create_namespaced_binding')
        self.mocked_binding = self.patcher2.start()

        self.patcher3 = patch('kubernetes.client.ApiClient.call_api')
        self.mocked_call_api = self.patcher3.start()

        self.patcher4 = patch('kubernetes.client.CoreV1Api.list_pod_for_all_namespaces')
        self.mocked_all_pods = self.patcher4.start()

        return

    def tearDown(self):
        return

    def test_init(self):
        '''
        Test if initialization works fine and if nodes are empty.

        '''
        sched = Scheduler()
        self.assertEqual(sched.scheduler_name, 'custom_scheduler')
        self.assertEqual(sched.all_nodes, [])

        return

    def test_update_nodes(self):
        '''
        Test updateNodes and getNodeUsage methods.
        On this stage scheduler have all static and dynamic (usage)
        data of all nodes.
        '''
        self.mock_list_nodes.return_value = self.nodes_list
        self.mocked_binding.return_value = None
        self.mocked_call_api.side_effect = self.getUsageSideEffect

        sched = Scheduler()
        sched.updateNodes()

        self.assertNotEqual(sched.all_nodes, [])
        self.assertEqual(sched.all_nodes[0].metadata.name , 'control-plane')
        self.assertEqual(sched.all_nodes[1].metadata.name , 'worker-node')
        self.assertEqual(sched.all_nodes[0].pods.items, [])
        self.assertEqual(sched.all_nodes[0].usage , {"cpu":"200000000n","memory":"2000000Ki"})
        self.assertEqual(sched.all_nodes[1].usage , {"cpu":"300000000n","memory":"3000000Ki"})

        return

    def test_pods_on_nodes(self):
        '''
        Test podsOnNodes method.
        Check if all pods were added correctly to nodes
        '''
        self.mock_list_nodes.return_value = self.nodes_list
        self.mocked_binding.return_value = None
        self.mocked_call_api.side_effect = self.getUsageSideEffect
        self.mocked_all_pods.return_value = self.pods_list

        sched = Scheduler()
        sched.updateNodes()
        sched.podsOnNodes()

        for node in sched.all_nodes:
            if node.metadata.name == 'control-plane':
                self.assertNotEqual(node.pods.items, [])
                self.assertEqual(node.pods.items[0].metadata.name, 'test_pod_1')
                self.assertEqual(node.pods.items[0].spec.containers[0].name , 'container_1')
                # TODO test when request == {}
            if node.metadata.name == 'worker-node':
                self.assertEqual(node.pods.items, [])

        return

    def test_pod_usage(self):
        '''
        Check if pod usage is calculated correctly
        '''
        self.mock_list_nodes.return_value = self.nodes_list
        self.mocked_binding.return_value = None
        self.mocked_call_api.side_effect = self.getUsageSideEffect
        self.mocked_all_pods.return_value = self.pods_list
        sched = Scheduler()

        self.assertEqual(sched.podUsage(self.pods_list.items[0].metadata.name, self.pods_list.items[0].metadata.namespace)['cpu'], '1000000n')
        self.assertEqual(sched.podUsage(self.pods_list.items[1].metadata.name, self.pods_list.items[1].metadata.namespace)['memory'], '9000Ki')
        self.assertEqual(self.pods_list.items[2].metadata.name, 'test_pod_3_0_usage_test')
        self.assertEqual(sched.podUsage(self.pods_list.items[2].metadata.name, self.pods_list.items[2].metadata.namespace)['memory'], '0Ki')
        return

    def getUsageSideEffect(self, metrics_url, attr='GET', _preload_content=None):

        test_nodes_list = self.nodes_list
        test_pods_list = self.pods_list

        class tmpHttpObj():
            def __init__(self):
                if metrics_url.split('/')[-2] == 'nodes':
                    node_name = metrics_url.split('/')[-1]
                    self.tmp = ''
                    self.data = b''
                    for node in test_nodes_list.items:
                        if node.metadata.name == node_name:
                            cpu = node.usage['cpu']
                            memory = node.usage['memory']
                            self.tmp ='''{"usage":{"cpu":"''' + str(cpu) + '''","memory":"''' + str(memory) + '''"}}\n'''
                            self.data = bytes(self.tmp, 'utf-8')

                if metrics_url.split('/')[-2] == 'pods':
                    pod_name = metrics_url.split('/')[-1]
                    pod_namespace = metrics_url.split('/')[-3]
                    self.tmp = ''
                    self.data = b''
                    for pod in test_pods_list.items:
                        if pod.metadata.name == pod_name:
                            self.tmp = {'containers': []}
                            for cont in pod.spec.containers:
                                cpu = cont.usage['cpu']
                                memory = cont.usage['memory']
                                self.tmp['containers'].append({"usage": {"cpu": str(cpu),"memory": str(memory)}})
                            string_tmp = json.dumps(self.tmp)
                            self.data = bytes(string_tmp, 'utf-8')

        retobj = tmpHttpObj()
        return [retobj]
