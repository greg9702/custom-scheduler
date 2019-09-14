import sys

from testenv.fakeNodeList import fakeNodeList
from testenv.fakePodList import fakePodList


class Creator:
    """Creates test enviroment using template files"""

    def read_from_file(self, filename):
        """Read from template file, return file content as
        raw string
        :param str filename: path to a file
        :return: return raw string with content"""

        f = open(filename)
        line = f.readline()
        str = R''
        while line:
            if line:
                str += line
                line = f.readline()
        f.close()
        return str

    def create_from_file(self, filename, temp_type):
        """Read from Node or Pod template file,
        than create fakePodsList or fakeNodeList object.
        :param str filename: name of a input file
        :param str temp_type: type of template Node or Pod"""

        if temp_type == 'Node':
            node_list = fakeNodeList()
            str = self.read_from_file(filename)

            node_list.addNodes(str)

            return node_list

        elif temp_type == 'Pod':
            pod_list = fakePodList()
            str = self.read_from_file(filename)

            pod_list.addPods(str)

            return pod_list

        else:
            raise ValueError('Invalid template type')

        return
