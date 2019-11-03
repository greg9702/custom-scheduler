import os
from threading import Thread

from monitor import ClusterMonitor
from node import NodeList
from pod import Pod, SchedulingPriority

from kubernetes import client, config, watch


class Scheduler:
    def __init__(self):
        self.monitor = ClusterMonitor()
        self.watcher = watch.Watch()

        config.load_kube_config(config_file=os.path.join(os.path.dirname(__file__), '../kind-config'))
        self.v1 = client.CoreV1Api()

        self.scheduler_name = 'my_scheduler'

    def run(self):
        """
        Main thread, run and listen for events,
        If an event occurred, call monitor.update_nodes()
        and proceed scoring and scheduling process.
        """
        print('Scheduler running')

        p1 = Thread(target=self.monitor.monitor_runner)
        p1.start()

        while True:
            try:
                for event in self.watcher.stream(self.v1.list_pod_for_all_namespaces):
                    print('Event type ', event['type'])
                    if event['type'] == 'ADDED' and event['object'].spec.scheduler_name == self.scheduler_name:
                        new_pod = Pod(event['object'].metadata, event['object'].spec, event['object'].status)
                        print('New pod ADDED', new_pod.metadata.name)

                        self.monitor.update_nodes()
                        self.monitor.print_nodes_stats()

                        new_node = self.choose_node(new_pod)

                        if new_node is not None:
                            self.bind_to_node(new_pod.metadata.name, new_node.metadata.name)
                        else:
                            print('Pod cannot be scheduled..')
                            # when Pod cannot be scheduled it is being deleted and after
                            # couple seconds new Pod is being created and another attempt
                            # of scheduling this Pod is being made

                # TODO wait for metrics for newly created Pod
                """
                without this cluster for 2nd and next Pods in deployment looks the same, 
                so all Pods from deployment are placed on the same Node, we want to avoid this
                """

            except Exception as e:
                print(str(e))

    def choose_node(self, pod):
        """
        Method that brings together all methods
        responsible for choosing best Node for a Pod
        :param pod.Pod pod: Pod to be scheduled
        :return node.Node: return best selected Node for Pod,
            None if Pod cannot be scheduled
        """
        possible_nodes = self.filter_nodes(pod)

        print('Possible nodes')
        for node in possible_nodes.items:
            print(node.metadata.name)

        selected_node = self.score_nodes(pod, possible_nodes)
        if selected_node is not None:
            print('Selected Node', selected_node.metadata.name)
        else:
            print('No node was being selected')
        return selected_node

    def filter_nodes(self, pod):
        """
        Filter Nodes in self.monitor.all_nodes
        which can run selected Pod
        :param pod.Pod pod: Pod to be scheduled
        :return node.NodeList: List of Node which
            satisfy Pod requirements
        """
        # TODO get rid off copying elements?
        return_node_list = NodeList()

        if pod.spec.node_name is not None:
            for node in self.monitor.all_nodes.items:
                if pod.spec.node_name == node.metadata.name and node.spec.unschedulable is not True:
                    return_node_list.items.append(node)
        else:
            print('All nodes can be used for Pod %s ' % pod.metadata.name)
            for node in self.monitor.all_nodes.items:
                if node.spec.unschedulable is not True:
                    # TODO check labels there and decide if Node can be used for pod
                    return_node_list.items.append(node)

        return return_node_list

    @staticmethod
    def score_nodes(pod, node_list):
        """
        Score Nodes passed in node_list to choose the best one
        :param pod.Pod pod: Pod to be scheduled
        :param node.NodeList node_list: Nodes which meet Pod
            requirements
        :return node.Node: return Node which got highest score
            for Pod passed as pod, None if any node cannot be
            selected
        """
        best_node = None

        if len(node_list.items) == 0:
            pass

        elif len(node_list.items) == 1:
            best_node = node_list.items[0]

        else:
            print('Running scoring process ')

            best_node = node_list.items[0]

            for node in node_list.items:
                print(node.metadata.name, node.usage)

                if pod.scheduling_priority == SchedulingPriority.MEMORY:
                    if node.usage['memory'] < best_node.usage['memory']:
                        best_node = node

                elif pod.scheduling_priority == SchedulingPriority.CPU:
                    if node.usage['cpu'] < best_node.usage['memory']:
                        best_node = node

                elif pod.scheduling_priority == SchedulingPriority.CPU:
                    pass
                    # current_best =

        return best_node

    def calculate_score(self, pod):
        """
        Calculate score for a Node using defined formula
        :param pod.Pod pod:
        :return int: Node score
        """

    def bind_to_node(self, pod_name, node_name, namespace='default'):
        """
        Bind Pod to a Node
        :param str pod_name: pod name which we are binding
        :param str node_name: node name which pod has to be binded
        :param str namespace: namespace of pod
        :return: True if pod was bound successfully, False otherwise
        """
        target = client.V1ObjectReference()
        target.kind = "Node"
        target.api_version = "v1"
        target.name = node_name

        meta = client.V1ObjectMeta()
        meta.name = pod_name
        body = client.V1Binding(target=target)
        body.target = target
        body.metadata = meta
        try:
            self.v1.create_namespaced_binding(namespace, body)
            return True
        except Exception as e:
            """
            create_namespaced_binding() throws exception:
            Invalid value for `target`, must not be `None`
            or 
            despite the fact this exception is being thrown,
            Pod is bound to a Node and Pod is running
            """
            print('here')
            print('exception' + str(e))
            return False

    @staticmethod
    def pass_to_scheduler(name_, namespace_, scheduler_name_='default-scheduler'):
        """
        Pass deployment to be scheduled by different scheduler
        :param str scheduler_name_: name of new scheduler, which will
            schedule this deployment
        :param str name_: name of deployment
        :param str namespace_: namespace of deployment
        :return str: return http response code
        """
        url = '/apis/extensions/v1beta1/namespaces/' + namespace_ + '/deployments/' + name_
        headers = {'Accept': 'application/json', 'Content-Type': 'application/strategic-merge-patch+json'}
        body = {"spec": {"template": {"spec": {"schedulerName": scheduler_name_}}}}

        api_client = client.ApiClient()
        response = []
        try:
            response = api_client.call_api(url, 'PATCH', header_params=headers, body=body)
        except Exception as e:
            return int(str(e)[1:4])

        return response[1]


def main():
    scheduler = Scheduler()
    scheduler.run()


if __name__ == '__main__':
    main()
