## __Overview__
Main goal of the project is to create my own scheduler. <br>
Default one schedule Pods on Nodes according to labels assigned to each Pod. [link](https://link.springer.com/content/pdf/10.1007%2F978-3-319-68066-8_13.pdf) <br>
Assigning label to Pod isn't required. Idea for my custom scheduler is to schedule <br>
Pods based on real time resources usage for Pods which do not have labels assigned. <br>

### __Cluster__
To create a local cluster I am using [kind](https://github.com/kubernetes-sigs/kind). <br>
The biggest advantage of this solution is lightweightness of a cluster. <br>
We do not waste resources to run multiple OS, because every single node is Docker container, not VM. <br>
More about kind you can read [here](https://kind.sigs.k8s.io/). <br>

### __Used 3rd part__
Used [metrics-server](https://github.com/kubernetes-incubator/metrics-server) as a tool which provides
resources used by Pods.
