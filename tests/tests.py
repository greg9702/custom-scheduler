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
import node_templates

sys.path.append(os.path.join(os.path.dirname(__file__), '../pkg/scheduler/src'))
from scheduler import Scheduler

#TODO remove this from global

class testClass(unittest.TestCase):

	def setUp(self):

		self.nodes_list = fakeNodeList() # TODO automate this
		self.nodes_list.addNodes()

		self.pods_list = fakePodList() 	# TODO automate this
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

	def getUsageSideEffect(self, metrics_url, attr='GET', _preload_content=None):
		#TODO set usage depending on node-name - metrics_url
		class tmpHttpObj():
			def __init__(self):
				self.data =(b'{"kind":"NodeMetrics","apiVersion":"metrics.k8s.io/v1beta1","metadata":{"nam'
				 b'e":"kind-control-plane","selfLink":"/apis/metrics.k8s.io/v1beta1/nodes/kind-'
				 b'control-plane","creationTimestamp":"2019-08-09T10:13:48Z"},"timestamp":"2019'
				 b'-08-09T10:12:48Z","window":"30s","usage":{"cpu":"231151777n","memory":"87917'
				 b'2Ki"}}\n')
		retobj = tmpHttpObj()
		return [retobj]


	def test_init(self):


		self.mock_list_nodes.return_value = self.nodes_list

		self.mocked_binding.return_value = None

		self.mocked_get_node_usage.side_effect = self.getUsageSideEffect

		self.mocked_all_pods.return_value = self.pods_list

		sched = Scheduler()
		sched.updateNodes()

		self.assertNotEqual(sched.all_nodes, [])
		# self.assertEqual(sched.all_nodes[0].metadata.name , 'control-plane')

	def test_get_nodes(self):
		# TODO test if nodes are correctly added
		pass

	def test_pods_on_node(self):
		# self.assertEqual(sched.updateNodes(), "")
		# TODO test if assigning pods work fine

		pass
