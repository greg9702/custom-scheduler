### Overview
Main goal of the project is to create my own scheduler. <br>
Found couple cases, where default scheduler do not perform in the most efficient way. <br>
Proposed scheduler algorithm is going to use real time cluster resources usage and statistics.

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
- [ ] make node capacity custom  				<br>
- [x] dashboard							<br>
- [x] build my own node image <br>
- [x] find out cases, where default scheduler is working in inefficient way  <br>
- [x] figure out how default scheduler works in details <br>
- [x] automate process of creating cluster - make script <br>
- [x] automate deployment  				<br>
- [x] make cluster monitoring system working <br>

#### Updates
Working on tests and test environment. <br>
Finished mocking all used API calls. <br>
Working on creating dynamic environment and writing more test.
