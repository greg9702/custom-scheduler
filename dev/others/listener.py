#!/usr/bin/python

import time
import random
import json

from kubernetes import client, config, watch

config.load_kube_config()
v1 = client.CoreV1Api()
print ("v1", v1)

def main():
    print("Listener running... ")
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, "default"):
        print("Event happened")
        print("Used scheduler: " + event['object'].spec.scheduler_name)
        print ("Scheduling pod: ", event['object'].metadata.name)

if __name__ == '__main__':
    main()

