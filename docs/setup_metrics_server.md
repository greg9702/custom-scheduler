Using [metrics server](https://github.com/kubernetes-incubator/metrics-server) to monitor cluster resources usage.

#### How to deploy
From project home directory run:
```
kubectl create -f deployment/metrics_server_deploy/1.8+
```

#### Bugs
[For kuberentes version 1.15.0 do not work properly.](https://github.com/kubernetes-incubator/metrics-server/issues/247) <br>
Got error:
> error: metrics not available yet

##### How to fix it
Add
```
command:
  - /metrics-server
  - --kubelet-preferred-address-types=InternalIP
  - --kubelet-insecure-tls
```

to _metrics-server-deployment.yaml_

#### Notes
Note that metrics server need some time to gather statistics, this happen when metrics server <br>
is being set up and when new resource appear in a cluster (for example new Pod).
