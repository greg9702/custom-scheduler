#!/bin/bash

export PATH=$PATH:$(go env GOPATH)/bin

kind delete cluster
kind create cluster --config cluster-config.yaml


export KUBECONFIG="$(kind get kubeconfig-path --name="kind")" # TODO cluster name make it as variable
# if set to 1, create dashboard
create_dashboard=1

# if set to 1 create admin account
create_admin=1

if [ $create_dashboard == 1 ]; then
    echo "Creating dashboard..."
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta1/aio/deploy/recommended.yaml
	# change dashboard type to NodePort
	kubectl patch svc -n kubernetes-dashboard kubernetes-dashboard --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
	echo "changed type"
	# address and port of node on which dashboard is running
	tmp_address=$(kubectl get nodes -o wide | grep "$(kubectl get pods -o wide --all-namespaces | grep dashboard- |  cut -d" " -f 37)" | cut -d" " -f17) #TODO change this cut to awk
	echo "got address"
	tmp_port=$(kubectl -n kubernetes-dashboard get service kubernetes-dashboard  |  awk 'FNR == 2 {print $5}' | cut -d":" -f 2 | cut -d"/" -f 1)
	echo "got port"

	echo -e "Dashboard can be accesed at https://$tmp_address:$tmp_port"
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
