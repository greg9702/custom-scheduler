#### Overview

Project consist of:
- cluster - scripts to bootstrap kind cluster with all needed dependencies
- deployment - directory for deployments
- pkg - scheduler
- scripts - directory for other scripts

#### Cluster scripts
Scripts used to set up cluster. <br>
_CLUSTERNAME_ stores cluster name used by kind. <br>
_cluster-config.yaml_ is a configuration file in which cluster configuration are set. <br>
_setup.sh_ - set up cluster with dashboard and all privileges to use it. <br>
Metrics server also is set up. <br>
In configuration file number of Nodes and Nodes names can be set.

#### Deploying to cluster
To deploy image to cluster, ```kind load``` command can be used. <br>
It let you not to upload image every time to DockerHub. <br>
To automate this process, scripts/deply.sh is being created. <br>
Application name is passed as a first parameter. <br>
When launched, new docker container image is being built with unique hash, <br>
than new created image is being loaded to kind cluster and deployment can <br>
be successfully applied.
