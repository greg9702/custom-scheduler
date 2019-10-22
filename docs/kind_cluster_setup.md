#### __Step by step cluster setup from scratch__

Im using Arch Linux system, so system commands are prepared for this system.<br>

__Install go and kind using kind__
```
pacman -S go
go get sigs.k8s.io/kind
```
__Create cluster__
```
kind create cluster --config example-config.yaml
```
> This generates kubernetes config file in ~/.kube/kind-config-kind


__To use on host machine__
```
export PATH=$PATH:$(go env GOPATH)/bin
export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"
```

__To load docker image into cluster__
```
kind load docker-image XYZ
```
> where XYZ is docker image name

__Launching scheduler__
- Copy configuration file to project directory
```
cp ~/.kube/kind-config-kind .
```
In this file we have to use cluster _Internal IP_ - change line https://127.0.0.1:39505 <br>
to https://XYZ:6443
> where XYZ is master node Internal IP, get it with command `kubectl get nodes -o wide`

- Build image and load it into cluster
```
docker build -t ABC:DEF .
kind load docker-image ABC:DEF
```
> where ABC is image name and DEF is image tag

- Create deploy
```
kubectl apply -f XYZ.yaml
```
> where XYZ is the name of deploy file

__Create dashboard__
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta1/aio/deploy/recommended.yaml
```

To access the dashboard externally, create port binding using kind or make NodePort
> https://github.com/kubernetes/dashboard/wiki/Accessing-Dashboard---1.7.X-and-above

NodePort:

```
kubectl -n kubernetes-dashboard edit service kubernetes-dashboard
```
Change line `type: ClusterIP` to `type: NodePort`
```
kubectl -n kubernetes-dashboard get service kubernetes-dashboard

```
There we get port on which dashboard is exposed
To get to dashboard go to URL _https://<node-IP>:<node-Port>/#/login_
_Node IP_ is the Internal IP of the node on which dashboard is deployed!

To gain full access to dashboard create admin accoount
```
kubectl create -n kube-system serviceaccount admin
kubectl create clusterrolebinding permissive-binding \
 --clusterrole=cluster-admin \
 --user=admin \
 --user=kubelet \
 --group=system:serviceaccounts
```

To generate authentication token
```
kubectl -n kube-system get serviceaccount admin -o yaml
kubectl -n kube-system get secret admin-token-xyz -o yaml
```

The token is base64 encoded. Use a command to decode it:
```
echo "put-token-here" | base64 --decode
```
Use output as authentication token to log in to dashboard
