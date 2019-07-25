#!/bin/bash

set -e

# script creates a Kubernetes cluser from scratch
# configuration file is cluser-config.yaml


# if set to 1, create dashboard
create_dashboard=1
# if set to 1 create admin account
create_admin=1

# set path to kind
export PATH=$PATH:$(go env GOPATH)/bin

if [ "$1" != "" ]; then
    cluster_name=$1
else
    cluster_name="kind"
fi

if [ "$2" != "" ]; then
    echo "Passed to many arguments"
	echo -e "usage:\n./setup.sh 'cluster name' "
	exit 1
fi

kind delete cluster --name=$cluster_name
kind create cluster --config cluster-config.yaml --name=$cluster_name

export KUBECONFIG="$(kind get kubeconfig-path --name=$cluster_name)"

if [ $create_dashboard == 1 ]; then
    echo "Creating dashboard..."
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta1/aio/deploy/recommended.yaml

	#we have to wait to assign ip address to this pod TODO do while loop
	sleep 10

	# change dashboard type to NodePort
	kubectl patch svc -n kubernetes-dashboard kubernetes-dashboard --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'

	# address and port of node on which dashboard is running
	node_name=$(kubectl get pods -o wide --all-namespaces | grep dashboard- | awk '{print $8}')
	tmp_address=$(kubectl get nodes -o wide | grep "$(echo $node_name)" | awk '{print $6}')
	tmp_port=$(kubectl -n kubernetes-dashboard get service kubernetes-dashboard  |  awk 'FNR == 2 {print $5}' | cut -d":" -f 2 | cut -d"/" -f 1)

	echo -e "Dashboard is running at https://$tmp_address:$tmp_port"
else
    echo "Dashboard not created"
fi

if [ $create_admin == 1 ]; then
    echo "Admin account created"
	kubectl create -n kube-system serviceaccount admin
	kubectl create clusterrolebinding permissive-binding \
	 --clusterrole=cluster-admin \
	 --user=admin \
	 --user=kubelet \
	 --group=system:serviceaccounts

	 admin_token_name=$(kubectl -n kube-system get serviceaccount admin -o yaml | tail -1 | cut -d":" -f 2 | cut -d" " -f2)
	 admin_token=$(kubectl -n kube-system get secret $admin_token_name -o yaml | grep token | head -1 | sed -e 's/.* \(.*\)$/\1/')
	 echo "Admin token: "
	 echo $admin_token | base64 --decode
	 echo ""
else
	echo "Admin account not created"
fi
