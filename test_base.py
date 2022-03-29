from base import *
import unittest


class TestComp(unittest.TestCase):
    def test_ip(self):
        comp = Computer()
        net = Network()
        net.add_host(comp, "192.168.0.2")
        ans = comp.ip()
        self.assertEqual(ans, "192.168.0.2")

    def test_no_ping(self):
        comp = Computer()
        ans = comp.ping("1.2.3.4")
        self.assertEqual(ans, "No network")

    def test_send_to_host(self):
        net = Network()
        comp1 = Computer()
        comp2 = Computer()

        net.add_host(comp1, "192.168.0.2")
        net.add_host(comp2, "192.168.0.4")

        ans = comp1.call("192.168.0.4", "Standart_Program", "receive_message", "Привет!")
        self.assertEqual(ans, "Data from 192.168.0.2 has been received.")

    def test_send_to_unknown_host(self):
        net = Network()
        comp1 = Computer()
        comp2 = Computer()

        net.add_host(comp1, "192.168.0.2")
        net.add_host(comp2, "192.168.0.4")

        ans = comp1.call("192.168.0.5", "Standart_Program", "receive_message", "Привет!")
        self.assertEqual(ans, "Unknown host")


class TestNetwork(unittest.TestCase):
    def test_empty_network(self):
        net = Network()
        ans = net.ping("", "1.2.3.4")
        self.assertEqual(ans, "Unknown host")

    def test_empty(self):
        net = Network()
        ans = net.number_hosts()
        self.assertEqual(ans, 0)

    def test_ping_from_comp1_to_comp2(self):
        net = Network()
        comp1 = Computer()
        comp2 = Computer()

        net.add_host(comp1, "192.168.0.2")
        net.add_host(comp2, "192.168.0.4")
        ans = comp1.ping("192.168.0.4")
        self.assertEqual(ans, "ping from 192.168.0.2 to 192.168.0.4")

    def test_no_ping(self):
        net = Network()
        comp1 = Computer()
        comp2 = Computer()

        net.add_host(comp1, "192.168.0.2")
        net.add_host(comp2, "192.168.0.3")
        ans = comp1.ping("192.168.0.4")
        self.assertEqual(ans, "Unknown host")

    def test_ping(self):
        net = Network()
        comp1 = Computer()
        comp2 = Computer()

        net.add_host(comp1, "192.168.0.2")
        net.add_host(comp2, "192.168.0.4")

        ans = comp1.ping("192.168.0.4")
        self.assertEqual(ans, "ping from 192.168.0.2 to 192.168.0.4")

        ans = comp2.ping("192.168.0.2")
        self.assertEqual(ans, "ping from 192.168.0.4 to 192.168.0.2")


if __name__ == '__main__':
    unittest.main()
