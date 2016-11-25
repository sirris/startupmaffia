import os
import unittest
import sys
sys.path.append(os.path.join("/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[0:-1]))) # cheating I know
from bsm import Network


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.network = Network("./testfile.xlsx","Sheet1")

    def test_check_if_loading_workbook_is_ok(self):
        self.assertEqual(len(self.network.bsm.rows[1:]), 14)
        for row in self.network.bsm.rows[1:]: 
            self.assertEqual(len(row), 6)

    def test_lengte_counter_from(self):
        self.network.count_from()
        self.assertEqual(len(self.network.counter), 14)
        self.assertEqual(len(self.network.name_group.keys()), 7)
        self.assertEqual(len(self.network.name_group.values()), 7)

    def test_lengte_counter_to(self):
        self.network.count_to()
        self.assertEqual(len(self.network.counter), 14)
        self.assertEqual(len(self.network.name_group.keys()), 9)
        self.assertEqual(len(self.network.name_group.values()), 9)

    def test_lengte_counter_to_and_from(self):
        self.network.count_from()
        self.network.count_to()
        self.assertEqual(len(self.network.counter), 28)
        self.assertEqual(len(self.network.name_group.keys()), 16)
        self.assertEqual(len(self.network.name_group.values()), 16)

    def test_count_check_values(self):
        self.network.count_from()
        self.network.count_to()
        self.network.count()
        self.assertEqual(len(self.network.values.keys()), 16)
        som = 0
        for name in self.network.values:
            som += self.network.values[name]
        self.assertEqual(som, 28)
        self.assertEqual(set(self.network.values.values()),set([5,1,3,2,1,1,1,1,1,1,1,1,1,1,2,5]))

    def test_check_give_id(self):
        self.network.give_id()
        self.assertEqual(len(self.network.name_id.values()), 16)
        self.assertEqual(len(self.network.name_id.values()), len(set(self.network.name_id.values())))

    def test_check_set_nodes(self):
        self.network.count_from()
        self.network.count_to()
        self.network.count()
        self.network.give_id()
        self.network.set_nodes()
        self.assertEqual(len(self.network.nodes), 16)

    def test_check_set_edges(self):
        self.network.give_id()
        self.network.set_edges()
        self.assertEqual(len(self.network.edges), 28)
                       

if __name__ == '__main__':
    unittest.main()

