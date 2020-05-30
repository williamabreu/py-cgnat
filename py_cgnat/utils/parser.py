from argparse import ArgumentParser, ArgumentTypeError
from ipaddress import IPv4Address, IPv4Network


# Define the supported platforms.
# - Uses the same name defined by the file inside 'generator' package
# - Is used for auto calling the 'generate' function at runtime execution
SUPPORTED_PLATFORMS = (
    'routeros',
)


# Abstract type for parsing IP:port format into tuple.
def IPandPort(string):
    try:
        ip, port = string.split(':')
        ip = IPv4Address(ip)
        port = int(port)
        return ip, port
    except:
        raise ArgumentTypeError(f'{string} is not in format <IPv4Address>:<int>')


# Define the top-level parser for cli arguments.
# -- Import it to __main__ module and call parser.parse_args()
parser = ArgumentParser(description='Command line tool for handling Carrier-Grade NAT rules using netmap.')

# Top-level arguments.
# BEGIN
parser.add_argument('private_net', 
    help='Private address pool from CGNAT shared space address',
    type=IPv4Network,
)

parser.add_argument('public_net', 
    help='Public adddress pool target from netmap',
    type=IPv4Network,
)
# END

# Define the subparser for switching generator/translator module.
subparsers = parser.add_subparsers(title='modules')

# Define the subparser for selecting generator module.
# BEGIN
parser_generator = subparsers.add_parser('gen', 
    help='Select the CGNAT generator module', 
)

parser_generator.add_argument('target_platform',
    help='Target platform where the CGNAT will be deployed',
    choices=SUPPORTED_PLATFORMS, 
)

parser_generator.add_argument('output_file', 
    help='Filename to save the rules generated',
    nargs='?',
)
# END

# Define the subparser for selecting transalator module.
# BEGIN
parser_translator = subparsers.add_parser('trans',
    help='Select the CGNAT translator module', 
)

group = parser_translator.add_mutually_exclusive_group()

group.add_argument('-d', '--direct', 
    help='Set the translator in direct mode (private -> public)', 
    metavar='IP',
    dest='source_addr',
    type=IPv4Address,
)

group.add_argument('-r', '--reverse', 
    help='Set the translator in reverse mode (public -> private)', 
    metavar='IP:port',
    dest='source_addr',
    type=IPandPort,
)
# END


if __name__ == '__main__':
    # Debug command-line syntax.
    parser.print_usage()
    parser_generator.print_usage()
    parser_translator.print_usage()

    print( parser.parse_args() )
    
    # Usage examples:
    # py-cgnat 100.64.0.0/22 203.0.113.0/27 gen routeros output.rsc
    # py-cgnat 100.64.0.0/22 203.0.113.0/27 gen routeros 
    # py-cgnat 100.64.0.0/22 203.0.113.0/27 trans --direct 100.64.2.15
    # py-cgnat 100.64.0.0/22 203.0.113.0/27 trans --reverse 203.0.113.20:13578
    # py-cgnat 100.64.0.0/22 203.0.113.0/27 trans -d 100.64.2.15
    # py-cgnat 100.64.0.0/22 203.0.113.0/27 trans -r 203.0.113.20:13578
