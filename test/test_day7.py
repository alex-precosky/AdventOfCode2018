from Day7 import Node, priority_graph_traversal
import unittest

class Test(unittest.TestCase):

    def test_priority_graph_traversal_AB(self):
        head_node = Node('A')
        b_node = Node('B')

        head_node.children = [b_node]

        graph_dict = {'A' : head_node, 'B' : b_node}

        expected = "AB"
        actual = priority_graph_traversal([head_node], graph_dict)

        print(actual)
        assert expected == actual

    def test_priority_graph_traversal_ex1(self):
        a_node = Node('A')
        b_node = Node('B')
        c_node = Node('C')
        d_node = Node('D')
        e_node = Node('E')
        f_node = Node('F')

        c_node.children = [a_node, f_node]
        a_node.children = [b_node, d_node]
        f_node.children = [e_node]
        b_node.children = [e_node]
        d_node.children = [e_node]
        
        graph_dict = {'A' : a_node, 'B' : b_node, 'C' : c_node, 'D' : d_node, 'E' : e_node, 'F' : f_node }

        expected = "CABDFE"
        actual = priority_graph_traversal([c_node], graph_dict)

        print(actual)
        assert expected == actual
