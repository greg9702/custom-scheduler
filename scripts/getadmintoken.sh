#!/bin/bash

export PATH=$PATH:$(go env GOPATH)/bin
export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"

admin_token=$(kubectl -n kube-system get serviceaccount admin -o yaml | tail -1 | cut -d" " -f 3)
kubectl -n kube-system get secret $admin_token -o yaml | head -5 | tail -1 | cut -d" " -f 4 | base64 --decode
echo ""
