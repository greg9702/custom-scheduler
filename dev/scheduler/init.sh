#!/bin/sh

export KUBECONFIG=kind-config-kind

python -u scheduler.py
