from collections import OrderedDict
from ipaddress import IPv4Address, IPv4Network

from pycgnat.utils.vlsm import split_subnet


def cgnat_direct(
    private_net: IPv4Network, public_net: IPv4Network, private_ip: IPv4Address
) -> OrderedDict:
    """Calculate the public IP and port range from private IP given.

    Args:
        private_net: Private address pool from CGNAT shared space address.
        public_net: Public adddress pool target from netmap.
        private_ip: Unique private IP from CGNAT to be converted to the public
            one.

    Returns:
        Dict containing the public_ip and port_range for the query.

    Raises:
        ValueError: When the private IP is out of the private net given.
        ValueError: When the networks given do not satisfy the 1:32 ratio.
    """

    if private_ip not in private_net:
        raise ValueError("Private IP is out of the network given")

    if public_net.prefixlen - private_net.prefixlen != 5:
        raise ValueError("Only works to netmaps for 1:32 CGNAT ratio")

    private_ips = split_subnet(private_net, public_net.netmask)
    index = None  # to discover the port range

    for i, pool in enumerate(private_ips):
        if private_ip in pool:
            index = i
            break

    port_base = 1536 + 2000 * index
    port_range = (port_base, port_base + 1999)

    pool = private_ips[index]
    delta = int(private_ip) - int(pool.network_address)
    public_ip = IPv4Address(int(public_net.network_address) + delta)

    return OrderedDict(public_ip=public_ip, port_range=port_range)
