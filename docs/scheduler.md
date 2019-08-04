#### Overview
For every Pod that the scheduler discovers, the scheduler becomes responsible <br>
for finding the best Node for that Pod to run on. <br>
For every newly created Pods or other unscheduled Pods, kube-scheduler selects <br>
a optimal Node for them to run on. Newly created Pods it is meant Pod in phase _Pending_. <br>
Default scheduler use two phases to schedule a Pod. It is reasonable, so this idea should be kept.
- filtering
- scoring.

In filtering phase we select only this Nodes, which satisfy Pod's requirements. <br>
What is important, if the list is empty, that Pod isn’t schedulable. <br>
In scoring phase, we rate every Node (selected in filtering phase) in different ways. <br>

#### Scheduling criteria
This is the critical point. We have to decide which criteria we take under <br>
consideration when scheduling a pod. Default scheduler has a lot of it both <br>
in filtering phase and as in scoring phase. All are in details described [here](https://kubernetes.io/docs/concepts/scheduling/kube-scheduler/#default-policies). <br>


#### Code overview
__scheduler.py__
```
class Scheduler:
	def __init__(self):
		self.scheduler_name = 'custom_scheduler'
		self.all_nodes=[]
		self.run()
		return

	def run(self):
		# watch for events
		# update nodes
		# filter nodes
		# score Nodes
		# bind Pod to Node
		return

	def updateNodes(self):
		'''
		Update nodes in self.all_nodes
		'''
		return

	def filterNodes(self, pod):
		'''
		Filter out nodes form  which do not meet pod requirements
		:return Node array: Nodes which met pod requirements
		'''
		return

	def scoreNodes(self, pod):
		'''
		Rate every node returned by self.filterNodes()
		:return: return Node with the highest rating
		'''
		return

	def bindToNode(pod, node):
		'''
		Bind Pod to Node
		:param str pod:
		:param str node:
		'''
		return

	def getNodeUsage(self):
		'''
		Get resources usage of Node
		:param str name: Name of node
		:return json object: object containg Node info
		'''
		return

```

#### TODO
Retrive Node requests and limits 
