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
