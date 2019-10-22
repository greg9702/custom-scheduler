### __Overview__
Main goal of the project is to create my own scheduler. <br>
Writing your own scheduler gives you more flexible way <br>
for scheduling Pods in cluster. In my approach, scheduler uses <br>
runtime resources usage statistics.

### __Cluster__
To create a local cluster I am using [kind](https://github.com/kubernetes-sigs/kind). <br>
The biggest advantage of this solution is lightweightness of a cluster. <br>
We do not waste resources to run multiple OS, because every single node is [Docker](https://www.docker.com/) container, not VM. <br>
More about kind you can read [here](https://kind.sigs.k8s.io/). <br>
Tried also to setting up local cluster as couple virtual machines and installing <br>
kubelet on them to create Kubernetes cluster, but it was <br>


> More in docs

#### __ROAD MAP__:
- [x] create cluster<br>
- [x] make example scheduler working <br>
- [x] dashboard	<br>
- [x] build my own node image <br>
- [x] automate process of creating cluster - scripts <br>
- [x] automate deployment <br>
- [x] make cluster monitoring system working <br>
- [x] Full state of Nodes<br>
- [x] Implement multithreading<br>
- [ ] Implement Pods garbage collector<br>
- [ ] Implement scheduler module<br>
