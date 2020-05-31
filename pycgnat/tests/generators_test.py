from pycgnat.settings import SUPPORTED_PLATFORMS
from ipaddress import IPv4Network
import unittest


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.generators = [__import__(f'pycgnat.generator.{platform}', fromlist=['generate']).generate for platform in SUPPORTED_PLATFORMS]
        self.privnet = IPv4Network('100.64.0.0/20') 
        self.pubnet = IPv4Network('203.0.113.0/25')

    def test_generators(self):
        for generate in self.generators:
            rules = generate(self.privnet, self.pubnet)
            self.assertIsInstance(rules, str)
            self.assertGreater(len(rules), 0)
    
    def test_invalid_ratio(self):
        for generate in self.generators:
            self.assertRaises(ValueError, generate, self.pubnet, self.privnet)
            self.assertRaises(ValueError, generate, IPv4Network('10.0.0.0/22'), IPv4Network('10.5.0.0/26'))
            self.assertRaises(ValueError, generate, IPv4Network('10.0.0.0/22'), IPv4Network('10.5.0.0/28'))
