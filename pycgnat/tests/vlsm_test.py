from pycgnat.utils.vlsm import split_subnet
from ipaddress import IPv4Address, IPv4Network
import unittest


class TestSplitSubnet(unittest.TestCase):
    def test_invalid_mask(self):
        def _invalid_mask_octet():
            valid = (128, 192, 224, 240, 248, 252, 254, 255)
            for i in range(128, 256):
                if i in valid:
                    continue
                else:
                    yield i
        
        for i in _invalid_mask_octet():
            with self.subTest(i=i):
                self.assertRaises(ValueError, split_subnet, IPv4Network('10.0.0.0/22'), IPv4Address(f'255.255.255.{i}'))

    def test_smaller_netmask(self):
        self.assertRaises(ValueError, split_subnet, IPv4Network('10.0.0.0/24'), IPv4Address('255.255.254.0'))
        self.assertRaises(ValueError, split_subnet, IPv4Network('10.0.0.0/24'), IPv4Address('255.255.252.0'))
        self.assertRaises(ValueError, split_subnet, IPv4Network('10.0.0.0/24'), IPv4Address('255.255.0.0'))

    def test_split_subnet(self):
        self.assertEqual(
            split_subnet(IPv4Network('10.0.0.0/27'), IPv4Address('255.255.255.240')),
            [IPv4Network('10.0.0.0/28'), IPv4Network('10.0.0.16/28')]
        )
        self.assertEqual(
            split_subnet(IPv4Network('10.0.0.0/24'), IPv4Address('255.255.255.0')),
            [IPv4Network('10.0.0.0/24')]
        )
