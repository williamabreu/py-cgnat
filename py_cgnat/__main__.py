import sys

from ipaddress import IPv4Network
from py_cgnat.calculator.direct import cgnat_direct
from py_cgnat.calculator.reverse import cgnat_reverse


SUPPORTED_PLATFORMS = (
    'routeros',
)


def main():
    try:
        privnet = IPv4Network(sys.argv[1])
        pubnet = IPv4Network(sys.argv[2])
        platform = sys.argv[3]
        filename = sys.argv[4]
    except:
        print('Invalid arguments.')
        sys.exit(1)

    if platform in SUPPORTED_PLATFORMS:
        generate = __import__(f'py_cgnat.generator.{platform}', fromlist=['generate']).generate
    else:
        print(f'Platform {platform} isn\'t supported.')
        sys.exit(1)
    
    rules = generate(privnet, pubnet)

    with open(filename, 'w') as fp:
        fp.write(rules)


if __name__ == '__main__':
    main()
