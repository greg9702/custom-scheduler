### Overview
Main goal of the project is to create my own scheduler. <br>
Already found couple cases, where default scheduler do not perform in the most efficient way. <br>
Unfortunately documentation do not specify too much details about scheduling process, <br>
so I am working on to finding this out by myself.

### Cluster
To create a local cluster I am using [kind](https://github.com/kubernetes-sigs/kind). <br>
The biggest advantage of this soulution is lightweightness of a cluser. <br>
We do not waste resources to run multiple OS, because every single node is [Docker](https://www.docker.com/) container, not VM. <br>
More about kind you can read [here](https://kind.sigs.k8s.io/).

#### ROAD MAP:
- [x] create cluster								<br>
- [x] make example scheduler working 				 <br>
- [x] force assignment of scheduler to master node 		<br>
- [x] get logs from scheduler pod					<br>
- [ ] make node capacity custom 				-<br>
- [ ] make it possible to develop easily				<br>
- [x] dashboard							<br>
- [x] build my own node image <br>
- [ ] figure out how default scheduler works in details <br>
- [x] find out cases, where default scheduler is working in inefficient way  <br>
- [x] automate process of creating cluster - make script <br>
- [ ] propose scheduling algorithm <br>
- [ ] create scheduler using new algorithm <br>
- [ ] test it <br>
