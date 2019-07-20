#!/bin/sh

export KUBECONFIG=kind-config-kind

python -u watcher.py
