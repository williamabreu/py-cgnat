# Usage: 
#   python3 -m unittest -v py_cgnat.tests.parser_test

from py_cgnat.utils.parser import parser
from argparse import Namespace
from ipaddress import IPv4Network, IPv4Address
import unittest


class TestParser(unittest.TestCase):
    def test_cli_toplevel_invalid(self):
        self.assertRaises(SystemExit, parser.parse_args, ''.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22'.split())
        self.assertRaises(SystemExit, parser.parse_args, '203.0.113.0/27'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 CMD'.split())
        self.assertRaises(SystemExit, parser.parse_args, 'A B gen routeros'.split())
        self.assertRaises(SystemExit, parser.parse_args, 'A B gen routeros file.rsc'.split())
        self.assertRaises(SystemExit, parser.parse_args, 'A B trans -d 100.64.2.15'.split())
        self.assertRaises(SystemExit, parser.parse_args, 'A B trans --direct 100.64.2.15'.split())
        self.assertRaises(SystemExit, parser.parse_args, 'A B trans -r 203.0.113.20:13578'.split())
        self.assertRaises(SystemExit, parser.parse_args, 'A B trans --reverse 203.0.113.20:13578'.split())

    def test_cli_gen_invalid(self):
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 gen'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 gen UNKNOWN'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 gen UNKNOWN file.txt'.split())

    def test_cli_trans_invalid(self):
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 trans CMD'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 trans --direct A'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 trans -d A'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 trans -d 100.64.2.15 B'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 trans --reverse A'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 trans -r A'.split())
        self.assertRaises(SystemExit, parser.parse_args, '100.64.0.0/22 203.0.113.0/27 trans -r 203.0.113.20:13578 B'.split())

    def test_cli_parsed(self):
        self.assertEqual(
            parser.parse_args('100.64.0.0/22 203.0.113.0/27 gen routeros output.rsc'.split()), 
            Namespace(module='gen', output_file='output.rsc', private_net=IPv4Network('100.64.0.0/22'), public_net=IPv4Network('203.0.113.0/27'), target_platform='routeros')
        )
        self.assertEqual(
            parser.parse_args('100.64.0.0/22 203.0.113.0/27 gen routeros'.split()), 
            Namespace(module='gen', output_file=None, private_net=IPv4Network('100.64.0.0/22'), public_net=IPv4Network('203.0.113.0/27'), target_platform='routeros')
        )
        self.assertEqual(
            parser.parse_args('100.64.0.0/22 203.0.113.0/27 trans --direct 100.64.2.15'.split()), 
            Namespace(module='trans', private_net=IPv4Network('100.64.0.0/22'), public_net=IPv4Network('203.0.113.0/27'), source_addr=IPv4Address('100.64.2.15'))
        )
        self.assertEqual(
            parser.parse_args('100.64.0.0/22 203.0.113.0/27 trans --reverse 203.0.113.20:13578'.split()), 
            Namespace(module='trans', private_net=IPv4Network('100.64.0.0/22'), public_net=IPv4Network('203.0.113.0/27'), source_addr=(IPv4Address('203.0.113.20'), 13578))
        )
        self.assertEqual(
            parser.parse_args('100.64.0.0/22 203.0.113.0/27 trans -d 100.64.2.15'.split()), 
            Namespace(module='trans', private_net=IPv4Network('100.64.0.0/22'), public_net=IPv4Network('203.0.113.0/27'), source_addr=IPv4Address('100.64.2.15'))
        )
        self.assertEqual(
            parser.parse_args('100.64.0.0/22 203.0.113.0/27 trans -r 203.0.113.20:13578'.split()), 
            Namespace(module='trans', private_net=IPv4Network('100.64.0.0/22'), public_net=IPv4Network('203.0.113.0/27'), source_addr=(IPv4Address('203.0.113.20'), 13578))
        )
