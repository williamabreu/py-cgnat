from argparse import ArgumentParser, ArgumentTypeError
from ipaddress import IPv4Address, IPv4Network
from typing import Tuple

from pycgnat.settings import SUPPORTED_PLATFORMS


# Abstract type for parsing IP:port format into tuple.
def IPandPort(string: str) -> Tuple[IPv4Address, int]:  # noqa
    ip: IPv4Address
    port: int
    try:
        ip, port = string.split(":")  # type: ignore
        ip = IPv4Address(ip)
        port = int(port)
    except Exception:
        raise ArgumentTypeError(
            f"{string} is not in format <IPv4Address>:<int>"
        )
    return ip, port


# Define the top-level parser for cli arguments.
# -- Import it to __main__ module and call parser.parse_args()
parser = ArgumentParser(
    description="Command line tool for handling Carrier-Grade NAT rules using netmap."  # noqa: E501
)

# Top-level arguments.
# BEGIN
parser.add_argument(
    "private_net",
    help="Private address pool from CGNAT shared space address",
    type=IPv4Network,
)

parser.add_argument(
    "public_net",
    help="Public adddress pool target from netmap",
    type=IPv4Network,
)
# END

# Define the subparser for switching generator/translator module.
subparsers = parser.add_subparsers(
    title="modules", dest="module", required=True
)

# Define the subparser for selecting generator module.
# BEGIN
parser_generator = subparsers.add_parser(
    "gen",
    help="Select the CGNAT generator module",
)

parser_generator.add_argument(
    "target_platform",
    help="Target platform where the CGNAT will be deployed",
    choices=SUPPORTED_PLATFORMS,
)

parser_generator.add_argument(
    "output_file",
    help="Filename to save the rules generated",
    nargs="?",
)
# END

# Define the subparser for selecting transalator module.
# BEGIN
parser_translator = subparsers.add_parser(
    "trans",
    help="Select the CGNAT translator module",
)

group = parser_translator.add_mutually_exclusive_group(required=True)

group.add_argument(
    "-d",
    "--direct",
    help="Set the translator in direct mode (private -> public)",
    metavar="IP",
    dest="source_addr",
    type=IPv4Address,
)

group.add_argument(
    "-r",
    "--reverse",
    help="Set the translator in reverse mode (public -> private)",
    metavar="IP:port",
    dest="source_addr",
    type=IPandPort,
)
# END
