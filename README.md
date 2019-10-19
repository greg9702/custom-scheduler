### __Overview__
Main goal of the project is to create my own scheduler. <br>
Found couple cases, where default scheduler do not perform in the most efficient way. <br>
Proposed scheduler algorithm is going to use real time cluster resources usage and statistics.

### __Cluster__
To create a local cluster I am using [kind](https://github.com/kubernetes-sigs/kind). <br>
The biggest advantage of this soulution is lightweightness of a cluser. <br>
We do not waste resources to run multiple OS, because every single node is [Docker](https://www.docker.com/) container, not VM. <br>
More about kind you can read [here](https://kind.sigs.k8s.io/).

#### __ROAD MAP__:
- [x] create cluster								<br>
- [x] make example scheduler working 				 <br>
- [x] force assignment of scheduler to master node 		<br>
- [x] get logs from scheduler pod					<br>
- [ ] make node capacity custom  				<br>
- [x] dashboard							<br>
- [x] build my own node image <br>
- [x] find out cases, where default scheduler is working in inefficient way  <br>
- [x] figure out how default scheduler works in details <br>
- [x] automate process of creating cluster - make script <br>
- [x] automate deployment  				<br>
- [x] make cluster monitoring system working <br>
- [x] Monitor build full view of Pods<br>
- [x] Full state of Nodes<br>
- [x] Implement monitor.update_nodes() method<br>
- [x] Add locks - prepare for multithreading<br>
- [ ] Implement Pods garbage collector<br>
- [ ] Implement scheduler module<br>

#### __Updates__
Working on tests and test environment. <br>
Finished mocking all used API calls. <br>

#### __Scheduling algorithm notes__

##### __Algorithm__

##### __Notes__
- If pod specify Node in deployment, schedule it to this Node, if Node is not running
or do not exists, Pod cannot be scheduled
- If Pod has specified requested resources it should be
- If Pod should be not scheduled by me, I pass it to default scheduler [???] <br>
To achive this, need to make PATH HTTP request to API /apis/extensions/v1beta1/namespaces/$DEPLOYMENT_NAMESPACE/deployments/$DEPLOYMENT_NAME<br>
(example  https://127.0.0.1:34209/apis/extensions/v1beta1/namespaces/default/deployments/hello-node) <br>
Request Body: {"spec":{"template":{"spec":{"schedulerName":"new-scheduler-name"}}}} <br>
__Required headers:__<br>
Accept: application/json <br>
Content-Type: application/strategic-merge-patch+json  <br>
