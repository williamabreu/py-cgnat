from ipaddress import IPv4Network

from pycgnat.utils.vlsm import split_subnet


def generate(private_net: IPv4Network, public_net: IPv4Network) -> str:
    """Generate CGNAT rules for RouterOS.

    Args:
        private_net: Private address pool from CGNAT shared space address.
        public_net: Public adddress pool target from netmap.

    Returns:
        RouterOS CLI commands to run via telnet through copy-paste.

    Raises:
        ValueError: When the networks given do not satisfy the 1:32 ratio.
    """

    if public_net.prefixlen - private_net.prefixlen != 5:
        raise ValueError("Only works to netmaps for 1:32 CGNAT ratio")

    private_subnet_list = split_subnet(private_net, public_net.netmask)

    string = "/ip firewall nat\n"

    port_index = 1536
    comment = True

    for private_subnet in private_subnet_list:
        first_port = port_index
        last_port = port_index + 1999
        if comment:
            string += (
                "add action=netmap chain=srcnat protocol=tcp"
                f" src-address={private_subnet}"
                f" to-addresses={public_net}"
                f" to-ports={first_port}-{last_port} disabled=yes"
                f' comment="CGNAT TCP {public_net}"\n'
            )
            comment = False
        else:
            string += (
                "add action=netmap chain=srcnat protocol=tcp"
                f" src-address={private_subnet} to-addresses={public_net}"
                f" to-ports={first_port}-{last_port} disabled=yes\n"
            )
        port_index += 2000

    port_index = 1536
    comment = True

    for private_subnet in private_subnet_list:
        first_port = port_index
        last_port = port_index + 1999
        if comment:
            string += (
                "add action=netmap chain=srcnat protocol=udp"
                f" src-address={private_subnet} to-addresses={public_net}"
                f" to-ports={first_port}-{last_port} disabled=yes"
                f' comment="CGNAT UDP {public_net}"\n'
            )
            comment = False
        else:
            string += (
                "add action=netmap chain=srcnat protocol=udp"
                f" src-address={private_subnet} to-addresses={public_net}"
                f" to-ports={first_port}-{last_port} disabled=yes\n"
            )
        port_index += 2000

    comment = True

    for private_subnet in private_subnet_list:
        if comment:
            string += (
                "add action=netmap chain=srcnat "
                f"src-address={private_subnet} to-addresses={public_net}"
                f' disabled=yes comment="CGNAT ICMP {public_net}"\n'
            )
            comment = False
        else:
            string += (
                "add action=netmap chain=srcnat"
                f" src-address={private_subnet} to-addresses={public_net}"
                f" disabled=yes\n"
            )

    return string
