import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../pkg/scheduler/src'))
from scheduler import Scheduler
from fake_cluster import fakeCluster

nodes_params = [
	{
	"metadata": { "labels": {"beta.kubernetes.io/arch": "amd64",
	                         "beta.kubernetes.io/os": "linux",
	                         "kubernetes.io/arch": "amd64",
	                         "kubernetes.io/hostname": "kind-control-plane",
	                         "kubernetes.io/os": "linux",
	                         "node-role.kubernetes.io/master": ""},
	              "name": "kind-control-plane",
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
	                         "pods": "110"},
	 "usage": {"cpu": "253011429n", "memory": "698744Ki"}
	 },

]
@pytest.mark.scheduler
class TestClass(object):
	def initTest(self):
		self.scheduler = Scheduler()
		self.f_cluster = fakeCluster(nodes_params)


	def test2(self):
		pass
