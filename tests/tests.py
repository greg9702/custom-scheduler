import pytest
import os
import sys
import unittest
import json

from unittest.mock import patch
from kubernetes import client
from fakeNode import fakeNode
from fakeNodeList import fakeNodeList
from fakePod import fakePod
from fakePodList import fakePodList

import pod_template
import node_template

sys.path.append(os.path.join(os.path.dirname(__file__), '../pkg/scheduler/src'))
from scheduler import Scheduler

class testClass(unittest.TestCase):

    def setUp(self):
        # all nodes in cluster
        self.nodes_list = fakeNodeList()
        self.nodes_list.addNodes()
        # all pods in cluster
        self.pods_list = fakePodList()
        self.pods_list.addPods()

        self.patcher1 = patch('kubernetes.client.CoreV1Api.list_node')
        self.mock_list_nodes = self.patcher1.start()

        self.patcher2 = patch('kubernetes.client.CoreV1Api.create_namespaced_binding')
        self.mocked_binding = self.patcher2.start()

        self.patcher3 = patch('kubernetes.client.ApiClient.call_api')
        self.mocked_get_node_usage = self.patcher3.start()

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
        self.mocked_get_node_usage.side_effect = self.getUsageSideEffect

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
        self.mocked_get_node_usage.side_effect = self.getUsageSideEffect
        self.mocked_all_pods.return_value = self.pods_list

        sched = Scheduler()
        sched.updateNodes()
        sched.podsOnNodes()

        for node in sched.all_nodes:
            if node.metadata.name == 'control-plane':
                self.assertNotEqual(node.pods.items, [])
                self.assertEqual(node.pods.items[0].metadata.generate_name , 'test_pod_1')
                self.assertEqual(node.pods.items[0].spec.containers[0].name , 'container_1')
            if node.metadata.name == 'worker-node':
                self.assertEqual(node.pods.items, [])

        return

    def getUsageSideEffect(self, metrics_url, attr='GET', _preload_content=None):

        a = self.nodes_list

        class tmpHttpObj():
            def __init__(self):
                node_name = metrics_url.split('/')[-1]
                self.tmp = ''
                self.data = b''
                for node in a.items:
                    if node.metadata.name == node_name:
                        cpu = node.usage['cpu']
                        memory = node.usage['memory']
                        self.tmp ='''{"usage":{"cpu":"''' + str(cpu) + '''","memory":"''' + str(memory) + '''"}}\n'''
                        self.data = bytes(self.tmp, 'utf-8')

        retobj = tmpHttpObj()
        return [retobj]
