#!/bin/sh

export KUBECONFIG=kind-config

python -u watcher.py
