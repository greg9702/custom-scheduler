import time
import random
import json
import requests
import pprint

from kubernetes import client, config, watch

config.load_kube_config(config_file='../kind-config')

metrics_url = '/apis/metrics.k8s.io/v1beta1/nodes'
api_client = client.ApiClient()
response = api_client.call_api(metrics_url, 'GET', _preload_content=None)
# api_client.request('GET', metrics_url, headers=None, _preload_content=True)
resp = response[0].data.decode('utf-8') 
json_data = json.loads(resp)

pprint.pprint(json_data)


