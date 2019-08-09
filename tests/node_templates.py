nodes_params = [
'''{"metadata": { "labels": {"beta.kubernetes.io/arch": "amd64",
                         "beta.kubernetes.io/os": "linux",
                         "kubernetes.io/arch": "amd64",
                         "kubernetes.io/hostname": "kind-control-plane",
                         "kubernetes.io/os": "linux",
                         "node-role.kubernetes.io/master": ""},
              "name": "control-plane"},
 "spec": {"taints": [{"effect": "NoSchedule",
                      "key": "node-role.kubernetes.io/master",
                      "time_added": "None",
                      "value": "None"}],
          "unschedulable": "None"},
 "status": {"allocatable": {"cpu": "4",
                            "ephemeral-storage": "479177440Ki",
                            "hugepages-2Mi": "0",
                            "memory": "8045056Ki",
                            "pods": "110"},
            "capacity": {"cpu": "4",
                         "ephemeral-storage": "479177440Ki",
                         "hugepages-2Mi": "0",
                         "memory": "8045056Ki",
                         "pods": "110"}},
 "usage": {"cpu": "253011429n", "memory": "698744Ki"}}''',

'''{"metadata": { "labels": {"beta.kubernetes.io/arch": "amd64",
                         "beta.kubernetes.io/os": "linux",
                         "kubernetes.io/arch": "amd64",
                         "kubernetes.io/hostname": "worker-node",
                         "kubernetes.io/os": "linux",
                         "node-role.kubernetes.io/master": ""},
              "name": "worker-node"},
 "spec": {"taints": [{"effect": "NoSchedule",
                      "key": "node-role.kubernetes.io/master",
                      "time_added": "None",
                      "value": "None"}],
          "unschedulable": "None"},
 "status": {"allocatable": {"cpu": "4",
                            "ephemeral-storage": "479177440Ki",
                            "hugepages-2Mi": "0",
                            "memory": "8045056Ki",
                            "pods": "110"},
            "capacity": {"cpu": "4",
                         "ephemeral-storage": "479177440Ki",
                         "hugepages-2Mi": "0",
                         "memory": "8045056Ki",
                         "pods": "110"}},
 "usage": {"cpu": "253011429n", "memory": "698744Ki"}}'''
 ]
