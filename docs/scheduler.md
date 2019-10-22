#### Overview

Scheduler role is finding the best Node for that Pod to run on. <br>
For every newly created Pods or other unscheduled Pods, kube-scheduler selects <br>
a optimal Node for them to run on. Newly created Pods it is meant Pod in phase _Pending_. <br>
We can point out two steps in Pod scheduling process:
- filtering
- scoring.

In filtering phase we select only this Nodes, which satisfy Pod's requirements. <br>
What is important, if the list is empty, that Pod isn’t schedulable. <br>
In scoring phase, we rate every Node (selected in filtering phase) in different ways. <br>

#### Scheduling criteria

Default scheduler scheduling criteria are in details described [here](https://kubernetes.io/docs/concepts/scheduling/kube-scheduler/#default-policies). <br>
In my approach scheduler, have also filtering and scoring phases. <br>
_TODO implement filtering phase first_<br>
In scoring phase I use criteria not used by default scheduler.<br>
Default scheduler have no idea about resources usage by Pods running on Nodes.<br>
My scheduler gather usage statistics and than based on this select Node with <br>
the highest score. Used statistics of every not Node statistics, gives more opportunities of <br>
metrics manipulation. Lets two different approaches there. <br>
First one, only run time statistics are used, and _Requests_ and _Limits_ <br>
set in deployment are omitted.
Second one, if _Requests_ and _Limits_ are set in deployment let's use them <br>
and combine them with metrics received from metrics server for Pods, which do not have <br>
this attributes specified in the deployment.
It is worth to mention about _Limits_ attribute, that it is also used by _kubelet_ <br>
to kill Pods which exceed resources limits of Node. <br>
Two options described above are both implemented and can be set using _settings_ module.


#### Notes for scheduler components

##### General structure
Scheduler works in two main threads - monitor and scheduler. <br>
Role of a monitor is to gather Pods usage statistics from set back time. <br>
Scheduler listen for Pods events from all namespaces. When an event occurs, <br>
using data gathered by monitor, Node objects are created. <br>
Pod life time consist of couple steps reported by event listener. <br>
Listener can spot _modified_ and _add_ events. For scheduler, _add_ event <br>
is only important - in this step Pod must get a Node to run on.<br>
Then scheduling process described above is running, after this binding <br>
function is called.

##### Passing Pod to a different scheduler
If Pods requirements or labels exceed capabilities of a scheduler, Pod can be assigned to <br>
a different scheduler if it is running inside cluster. <br>
To achive this, need to make PATH HTTP request to apiserver <br>
> /apis/extensions/v1beta1/namespaces/$DEPLOYMENT_NAMESPACE/deployments/$DEPLOYMENT_NAME<br>
```
(example  https://127.0.0.1:34209/apis/extensions/v1beta1/namespaces/default/deployments/hello-node)
Request Body: {"spec":{"template":{"spec":{"schedulerName":"new-scheduler-name"}}}}
Required headers:
Accept: application/json
Content-Type: application/strategic-merge-patch+json
```


#### Bugs
In versions v1.14 and v1.15 there is a bug in binding method. <br>
Binding method raise exception even when target attribute is passed as not None.
```
ValueError("Invalid value for target, must not be None")
ValueError: Invalid value for target, must not be None
```
Reported [here](https://github.com/kubernetes-client/python/issues/825). <br>
