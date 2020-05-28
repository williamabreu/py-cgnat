# USO:
#       python3 cgnat.py <CGNAT-SUBNET> <PUBLIC-SUBNET> 
# EXEMPLO:
#       python3 cgnat.py 100.64.40.0/22 179.106.165.192/27 > CGNAT.rsc


import sys
import ipaddress


def split_subnet(subnet, netmask):
    if subnet.netmask == netmask:
        return [subnet.exploded]
    else:
        branches = list(subnet.subnets())
        return split_subnet(branches[0], netmask) + split_subnet(branches[1], netmask)


def main(private_ips, public_ip):
    string = '/ip firewall nat\n'

    port_index = 1536
    comment = True

    for private_ip in private_ips:
        first_port = port_index
        last_port = port_index + 1999
        if comment:
            string += f'add action=netmap chain=srcnat protocol=tcp src-address={private_ip} to-addresses={public_ip} to-ports={first_port}-{last_port} disabled=yes comment="CGNAT TCP {public_ip}"\n'
            comment = False
        else:
            string += f'add action=netmap chain=srcnat protocol=tcp src-address={private_ip} to-addresses={public_ip} to-ports={first_port}-{last_port} disabled=yes\n'
        port_index += 2000

    port_index = 1536
    comment = True

    for private_ip in private_ips:
        first_port = port_index
        last_port = port_index + 1999
        if comment:
            string += f'add action=netmap chain=srcnat protocol=udp src-address={private_ip} to-addresses={public_ip} to-ports={first_port}-{last_port} disabled=yes comment="CGNAT UDP {public_ip}"\n'
            comment = False
        else:
            string += f'add action=netmap chain=srcnat protocol=udp src-address={private_ip} to-addresses={public_ip} to-ports={first_port}-{last_port} disabled=yes\n'
        port_index += 2000

    comment = True

    for private_ip in private_ips:
        if comment:
            string += f'add action=netmap chain=srcnat src-address={private_ip} to-addresses={public_ip} disabled=yes comment="CGNAT ICMP {public_ip}"\n'
            comment = False
        else:    
            string += f'add action=netmap chain=srcnat src-address={private_ip} to-addresses={public_ip} disabled=yes\n'
    
    return string


if __name__ == '__main__':
    cgnat_net = ipaddress.IPv4Network(sys.argv[1])
    public_ip = ipaddress.IPv4Network(sys.argv[2])
    private_ips = split_subnet(cgnat_net, public_ip.netmask)
    result = main(private_ips, public_ip)
    print(result, end='')
