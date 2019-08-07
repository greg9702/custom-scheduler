import pytest
import os
import sys
import unittest
from unittest.mock import patch
from kubernetes import client
from fakeNode import fakeNode
from fakeNodeList import fakeNodeList

sys.path.append(os.path.join(os.path.dirname(__file__), '../pkg/scheduler/src'))
from scheduler import Scheduler

#TODO remove this from global
nodes_params = [
'''{"metadata": { "labels": {"beta.kubernetes.io/arch": "amd64",
                         "beta.kubernetes.io/os": "linux",
                         "kubernetes.io/arch": "amd64",
                         "kubernetes.io/hostname": "kind-control-plane",
                         "kubernetes.io/os": "linux",
                         "node-role.kubernetes.io/master": ""},
              "name": "kind-control-plane"},
 "spec": {"taints": [{"effect": "NoSchedule",
                      "key": "node-role.kubernetes.io/master",
                      "time_added": "None",
                      "value": "None"}],
          "unschedulable": "None"},
 "status": {"allocatable": {"cpu": "4",
                            "ephemeral-storage": "479177440Ki",
                            "hugepages-2Mi": "0",
                            "memory": "8045056Ki",
                            "pods": "110"},
            "capacity": {"cpu": "4",
                         "ephemeral-storage": "479177440Ki",
                         "hugepages-2Mi": "0",
                         "memory": "8045056Ki",
                         "pods": "110"}},
 "usage": {"cpu": "253011429n", "memory": "698744Ki"}}''',

'''{"metadata": { "labels": {"beta.kubernetes.io/arch": "amd64",
                         "beta.kubernetes.io/os": "linux",
                         "kubernetes.io/arch": "amd64",
                         "kubernetes.io/hostname": "worker-node",
                         "kubernetes.io/os": "linux",
                         "node-role.kubernetes.io/master": ""},
              "name": "worker-node"},
 "spec": {"taints": [{"effect": "NoSchedule",
                      "key": "node-role.kubernetes.io/master",
                      "time_added": "None",
                      "value": "None"}],
          "unschedulable": "None"},
 "status": {"allocatable": {"cpu": "4",
                            "ephemeral-storage": "479177440Ki",
                            "hugepages-2Mi": "0",
                            "memory": "8045056Ki",
                            "pods": "110"},
            "capacity": {"cpu": "4",
                         "ephemeral-storage": "479177440Ki",
                         "hugepages-2Mi": "0",
                         "memory": "8045056Ki",
                         "pods": "110"}},
 "usage": {"cpu": "253011429n", "memory": "698744Ki"}}'''
 ]


class testClass(unittest.TestCase):

	def setUp(self):
		self.patcher1 = patch('kubernetes.client.CoreV1Api.list_node')
		self.mock_list_nodes = self.patcher1.start()

		self.patcher2 = patch('kubernetes.client.CoreV1Api.create_namespaced_binding')
		self.mocked_binding = self.patcher2.start()

		return

	def tearDown(self):
		return

	def test_init(self):

		nodes_list = fakeNodeList()
		nodes_list.addNodes(nodes_params)

		self.mock_list_nodes.return_value = nodes_list

		self.mocked_binding.return_value = None
		sched = Scheduler()

	def test_get_nodes(self):
		# TODO test if nodes are correctly added
		pass

	def test_pods_on_node(self):
		# self.assertEqual(sched.updateNodes(), "")
		# TODO test if assigning pods work fine 

		pass
