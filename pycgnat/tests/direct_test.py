from pycgnat.translator.direct import cgnat_direct
from ipaddress import IPv4Network, IPv4Address
from collections import OrderedDict
import unittest


class TestDirectTranslate(unittest.TestCase):
    def setUp(self):
        self.privnet = IPv4Network('100.64.0.0/20') 
        self.pubnet = IPv4Network('203.0.113.0/25')
        self.ip = IPv4Address('100.64.12.15')

    def test_cgnat_direct(self):
        self.assertEqual(
            cgnat_direct(self.privnet, self.pubnet, IPv4Address('100.64.0.0')),
            OrderedDict(public_ip=IPv4Address('203.0.113.0'), port_range=(1536, 3535))
        )
        self.assertEqual(
            cgnat_direct(self.privnet, self.pubnet, IPv4Address('100.64.0.255')),
            OrderedDict(public_ip=IPv4Address('203.0.113.127'), port_range=(3536, 5535))
        )
        self.assertEqual(
            cgnat_direct(self.privnet, self.pubnet, IPv4Address('100.64.1.31')),
            OrderedDict(public_ip=IPv4Address('203.0.113.31'), port_range=(5536, 7535))
        )
        self.assertEqual(
            cgnat_direct(self.privnet, self.pubnet, IPv4Address('100.64.14.128')),
            OrderedDict(public_ip=IPv4Address('203.0.113.0'), port_range=(59536, 61535))
        )
    
    def test_ip_out_of_range(self):
        self.assertRaises(ValueError, cgnat_direct, self.privnet, self.pubnet, IPv4Address('1.1.1.1'))
        self.assertRaises(ValueError, cgnat_direct, self.privnet, self.pubnet, IPv4Address('100.63.255.255'))
        self.assertRaises(ValueError, cgnat_direct, self.privnet, self.pubnet, IPv4Address('100.64.16.0'))
        self.assertRaises(ValueError, cgnat_direct, self.privnet, self.pubnet, IPv4Address('100.64.20.10'))

    def test_invalid_ratio(self):
        self.assertRaises(ValueError, cgnat_direct, self.pubnet, self.privnet, self.ip)
        self.assertRaises(ValueError, cgnat_direct, IPv4Network('10.0.0.0/30'), IPv4Network('10.1.0.0/26'), self.ip)
        self.assertRaises(ValueError, cgnat_direct, IPv4Network('10.1.0.0/26'), IPv4Network('10.0.0.0/30'), self.ip)
        self.assertRaises(ValueError, cgnat_direct, IPv4Network('10.1.0.0/21'), IPv4Network('10.0.0.0/27'), self.ip)
        self.assertRaises(ValueError, cgnat_direct, IPv4Network('10.1.0.0/23'), IPv4Network('10.0.0.0/27'), self.ip)
