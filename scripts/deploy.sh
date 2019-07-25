#!/bin/bash

# perform commit before usage, get hash of commit 
# script to deploy whole application to kind cluster

cluster_name=$(cat ../cluster/CLUSTERNAME)

if [ "$1" != "" ]; then
    app_name=$1
else
	echo "Not specified app name"
	echo -e "usage: ./deploy.sh 'app name' "
	exit 1
fi

if [ "$2" != "" ]; then
    echo "Passed to many arguments"
	echo -e "usage: ./deploy.sh 'app name' "
	exit 1
fi

export PATH=$PATH:$(go env GOPATH)/bin
export KUBECONFIG="$(kind get kubeconfig-path --name=$cluster_name)"

# copy new config file to app folder
cp $KUBECONFIG ../pkg/$app_name/kind-config
#replace line with IP to masterIP:6443
master_addr=$(kubectl get nodes -o wide | grep master | awk '{print $6}') # TODO potential bugs here with this grep
master_port=6443
sed -i "s|\(server: https://\).*$|\1$master_addr:$master_port|g" ../pkg/$app_name/kind-config

git_tag=$(git log -1 --format=%h)

# build new image
docker build -t $app_name:$git_tag ../pkg/$app_name

# change line in deploy
sed -i "s/\(image: \).*$/\1$app_name:$git_tag/g" ../deployment/$app_name.yaml
echo "Replaced image to $app_name:$git_tag in deployment/$app_name.yaml"

# load image to kind
echo "Loading docker image into cluster..."
kind load docker-image $app_name:$git_tag

echo "Creating deployment..."
kubectl apply -f ../deployment/$app_name.yaml
