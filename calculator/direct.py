import sys
import ipaddress

# uso:
# python3 cgnat_direct.py <CGNAT-SUBNET> <PUBLIC-SUBNET> <CLIENT-IP>
# python3 cgnat_direct.py 100.65.12.0/22 177.66.58.160/27 100.65.15.42


def split_subnet(subnet, netmask):
    if subnet.netmask == netmask:
        return [subnet]
    else:
        branches = list(subnet.subnets())
        return split_subnet(branches[0], netmask) + split_subnet(branches[1], netmask)


if __name__ == '__main__':
    cgnat_net = ipaddress.IPv4Network(sys.argv[1])
    public_ip = ipaddress.IPv4Network(sys.argv[2])
    client_ip = ipaddress.IPv4Address(sys.argv[3])
    private_ips = split_subnet(cgnat_net, public_ip.netmask)

    index = None # para descubrir a faixa de portas

    for i, pool in enumerate(private_ips):
        if client_ip in pool:
            index = i
            break
    
    port_base = 1536 + 2000 * index
    port_range = (port_base, port_base + 1999)

    pool = private_ips[index]
    delta = int(client_ip) - int(pool.network_address)
    client_public_ip = ipaddress.IPv4Address(int(public_ip.network_address) + delta)

    print('IP CLIENTE:', client_ip)
    print('IP PÚBLICO:', client_public_ip)
    print('PORTAS:', port_range)

