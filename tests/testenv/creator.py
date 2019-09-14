from testenv.fakeNodeList import fakeNodeList
from testenv.fakePodList import fakePodList

import sys


'''
Read from Node or Pod template file,
than create array of Pods or Nodes
:param filename: name of a input file
:param temp_type: type of template Node or Pod
'''
def create_from_file(file_name, temp_type):

    if temp_type == 'Node':
        node_list = fakeNodeList()
        f = open(file_name)
        line = f.readline()
        str = R''
        while line:
            if line:
                str += line
                line = f.readline()
        f.close()

        node_list.addNodes(str)

        return node_list


    elif temp_type == 'Pod':
        pass
        pod_list = fakePodList()
        f = open(file_name)
        line = f.readline()
        str = R''
        while line:
            if line:
                str += line
                line = f.readline()
        f.close()

        pod_list.addPods(str)

        return pod_list

    else:
        raise ValueError('Invalid template type')

    return
