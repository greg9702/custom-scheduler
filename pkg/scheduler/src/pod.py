from kubernetes import client

import json

LIMIT_OF_RECORDS = 1000

MIX_METRICS = False


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
        self.usage = []
        self.is_alive = True

    def __eq__(self, other):
        return self.metadata.name == other.metadata.name

    def fetch_usage(self):
        """
        Fetch usage data for pod from metrics server
        :return:
        """
        metrics_url = '/apis/metrics.k8s.io/v1beta1/namespaces/' \
                      + self.metadata.namespace + '/pods/' \
                      + self.metadata.name

        try:
            api_client = client.ApiClient()
            response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
            resp = response[0].data.decode('utf-8')
            json_data = json.loads(resp)
        except Exception as e:
            if len(self.usage) <= 1:
                self.usage = []
            self.usage.append({'cpu': 0, 'memory': 0})
            return int(str(e)[1:4])

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

        if len(self.usage) > LIMIT_OF_RECORDS:
            self.usage.pop(0)

        self.usage.append({'cpu': tmp_cpu, 'memory': tmp_mem})

        return 0

    def get_usage(self):
        """
        Get usage calculated based on Pod statistics
        TODO round this value
        :return dict: dict('cpu': cpu_usage, 'memory': memory_usage)
        """
        sum_cpu = 0
        sum_mem = 0
        if len(self.usage) > 0:
            if not MIX_METRICS:
                for entry in self.usage:
                    sum_cpu += int(entry['cpu'])
                    sum_mem += int(entry['memory'])
                avg_cpu = sum_cpu / len(self.usage)
                avg_mem = sum_mem / len(self.usage)
                return {'cpu': avg_cpu, 'memory': avg_mem}
        else:
            return {'cpu': 0, 'memory': 0}
