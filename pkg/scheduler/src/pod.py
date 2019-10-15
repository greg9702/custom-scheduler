from kubernetes import client

import json


class PodList(object):
    def __init__(self):
        self.items = []


class Pod(object):
    def __init__(self, metadata_, spec_, status_):
        """
        :param V1ObjectMeta metadata_:
        :param V1NodeSpec spec_:
        :param V1NodeStatus status_:
        :return:
        """
        if type(metadata_) is not client.models.v1_object_meta.V1ObjectMeta:
            raise str("Passed invalid type")
        if type(spec_) is not client.models.V1PodSpec:
            raise str("Passed invalid type")
        if type(status_) is not client.models.V1PodStatus:
            raise str("Passed invalid type")

        self.metadata = metadata_
        self.spec = spec_
        self.status = status_
        self.usage = list()

    def fetch_usage(self):
        """
        Fetch usage data for pod from metrics server
        :return:
        """
        metrics_url = '/apis/metrics.k8s.io/v1beta1/namespaces/' \
                      + self.metadata.namespace + '/pods/' \
                      + self.metadata.name

        #print(metrics_url)
        api_client = client.ApiClient()
        response = api_client.call_api(metrics_url, 'GET', _preload_content=None)

        resp = response[0].data.decode('utf-8')
        json_data = json.loads(resp)

        # Pod usage is sum of usage of all containers running inside it
        tmp_mem = 0
        tmp_cpu = 0

        # TODO check units of this...
        for container in json_data['containers']:
            # when Pod is in Error state, it containers usage is returned as 0
            if container['usage']['memory'] != '0':
                tmp_mem += int(container['usage']['memory'][:-2])
            if container['usage']['cpu'] != '0':
                tmp_cpu += int(container['usage']['cpu'][:-1])

        if len(self.usage) > 1000:
            self.usage.pop(0)

        self.usage.append(dict({'cpu': tmp_cpu, 'memory': tmp_mem}))

    def get_usage(self):
        """
        Get usage calculated based on Pod statistics
        :return dict: dict('cpu': cpu_usage, 'memory': memory_usage)
        """
        avg_cpu = sum(self.usage['cpu']) / len(self.usage['cpu'])
        avg_mem = sum(self.usage['memory']) / len(self.usage['memory'])

        return dict({'cpu': avg_cpu, 'memory': avg_mem})