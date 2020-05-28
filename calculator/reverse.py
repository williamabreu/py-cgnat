import sys
import ipaddress

# uso:
# python3 cgnat_reverse.py <CGNAT-SUBNET> <PUBLIC-SUBNET> <PUBLIC-IP> <PUBLIC-PORT>
# python3 cgnat_reverse.py 100.65.12.0/22 177.66.58.160/27 177.66.58.170 5220


def split_subnet(subnet, netmask):
    if subnet.netmask == netmask:
        return [subnet]
    else:
        branches = list(subnet.subnets())
        return split_subnet(branches[0], netmask) + split_subnet(branches[1], netmask)


def cgnat_reverse(cgnat_net, public_ip, client_ip, client_port):
    private_ips = split_subnet(cgnat_net, public_ip.netmask)

    index = None

    for i in range(32):
        port_base = 1536 + 2000 * i
        port_range = (port_base, port_base + 1999)
        if port_range[0] <= client_port <= port_range[1]:
            index = i
            break

    pool = private_ips[index]
    delta = int(client_ip) - int(public_ip.network_address)
    client_private_ip = ipaddress.IPv4Address(int(pool.network_address) + delta)

    return client_private_ip, client_ip, port_range


if __name__ == '__main__':
    cgnat_net = ipaddress.IPv4Network(sys.argv[1])
    public_ip = ipaddress.IPv4Network(sys.argv[2])
    client_ip = ipaddress.IPv4Address(sys.argv[3])
    client_port = int(sys.argv[4])
    
    client_private_ip, client_ip, port_range = cgnat_reverse(cgnat_net, public_ip, client_ip, client_port)

    print('IP CLIENTE:', client_private_ip)
    print('IP PÚBLICO:', client_ip)
    print('PORTAS:', port_range)

