from collections import OrderedDict
from ipaddress import IPv4Address, IPv4Network

from pycgnat.utils.vlsm import split_subnet


def cgnat_reverse(
    private_net: IPv4Network,
    public_net: IPv4Network,
    public_ip: IPv4Address,
    public_port: int,
) -> OrderedDict:
    """Calculate the private IP and port range from public IP given.

    Args:
        private_net: Private address pool from CGNAT shared space address.
        public_net: Public adddress pool target from netmap.
        public_ip: Unique public IP from CGNAT to be converted to the private
            one.
        public_port: Target port for the network translation.

    Returns:
        Dict containing the private_ip and port_range for the query.

    Raises:
        ValueError: When the public IP is out of the public net given.
        ValueError: When the networks given do not satisfy the 1:32 ratio.
    """

    if not 1536 <= public_port <= 65535:
        raise ValueError("Port index is out of range 1536-65535")

    if public_ip not in public_net:
        raise ValueError("Public IP is out of the network given")

    if public_net.prefixlen - private_net.prefixlen != 5:
        raise ValueError("Only works to netmaps for 1:32 CGNAT ratio")

    private_ips = split_subnet(private_net, public_net.netmask)
    index = None  # to discover the port range

    for i in range(32):
        port_base = 1536 + 2000 * i
        port_range = (port_base, port_base + 1999)
        if port_range[0] <= public_port <= port_range[1]:
            index = i
            break

    pool = private_ips[index]
    delta = int(public_ip) - int(public_net.network_address)
    private_ip = IPv4Address(int(pool.network_address) + delta)

    return OrderedDict(private_ip=private_ip, port_range=port_range)
