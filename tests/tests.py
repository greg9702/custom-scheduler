import pytest

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../pkg/scheduler/src'))
from scheduler import Scheduler

@pytest.mark.scheduler
class TestClass(object):
	def test_startup(self):
		self.scheduler = Scheduler()

	def test_startup_and_more(self):
		pass
