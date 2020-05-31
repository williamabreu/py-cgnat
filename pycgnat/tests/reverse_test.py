from pycgnat.translator.reverse import cgnat_reverse
from ipaddress import IPv4Network, IPv4Address
from collections import OrderedDict
import unittest


class TestReverseTranslate(unittest.TestCase):
    def setUp(self):
        self.privnet = IPv4Network('100.64.0.0/20') 
        self.pubnet = IPv4Network('203.0.113.0/25')
        self.ip = IPv4Address('203.0.113.1')
        self.port = 1537

    def test_cgnat_reverse(self):
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.0'), 1536),
            OrderedDict(private_ip=IPv4Address('100.64.0.0'), port_range=(1536, 3535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.0'), 2534),
            OrderedDict(private_ip=IPv4Address('100.64.0.0'), port_range=(1536, 3535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.0'), 3535),
            OrderedDict(private_ip=IPv4Address('100.64.0.0'), port_range=(1536, 3535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.127'), 3536),
            OrderedDict(private_ip=IPv4Address('100.64.0.255'), port_range=(3536, 5535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.127'), 4534),
            OrderedDict(private_ip=IPv4Address('100.64.0.255'), port_range=(3536, 5535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.127'), 5535),
            OrderedDict(private_ip=IPv4Address('100.64.0.255'), port_range=(3536, 5535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.31'), 6534),
            OrderedDict(private_ip=IPv4Address('100.64.1.31'), port_range=(5536, 7535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.0'), 60534),
            OrderedDict(private_ip=IPv4Address('100.64.14.128'), port_range=(59536, 61535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.3'), 65535),
            OrderedDict(private_ip=IPv4Address('100.64.15.131'), port_range=(63536, 65535))
        )
        self.assertEqual(
            cgnat_reverse(self.privnet, self.pubnet, IPv4Address('203.0.113.3'), 63536),
            OrderedDict(private_ip=IPv4Address('100.64.15.131'), port_range=(63536, 65535))
        )
    
    def test_ip_out_of_range(self):
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, IPv4Address('1.1.1.1'), self.port)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, IPv4Address('203.0.113.128'), self.port)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, IPv4Address('203.0.113.129'), self.port)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, IPv4Address('203.0.113.254'), self.port)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, IPv4Address('203.0.113.255'), self.port)

    def test_invalid_port(self):
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, self.ip, 0)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, self.ip, 1)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, self.ip, 1024)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, self.ip, 1025)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, self.ip, 1535)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, self.ip, 65536)
        self.assertRaises(ValueError, cgnat_reverse, self.privnet, self.pubnet, self.ip, 99999)
    
    def test_invalid_ratio(self):
        self.assertRaises(ValueError, cgnat_reverse, self.pubnet, self.privnet, self.ip, self.port)
        self.assertRaises(ValueError, cgnat_reverse, IPv4Network('10.0.0.0/30'), IPv4Network('10.1.0.0/26'), self.ip, self.port)
        self.assertRaises(ValueError, cgnat_reverse, IPv4Network('10.1.0.0/26'), IPv4Network('10.0.0.0/30'), self.ip, self.port)
        self.assertRaises(ValueError, cgnat_reverse, IPv4Network('10.1.0.0/21'), IPv4Network('10.0.0.0/27'), self.ip, self.port)
        self.assertRaises(ValueError, cgnat_reverse, IPv4Network('10.1.0.0/23'), IPv4Network('10.0.0.0/27'), self.ip, self.port)
