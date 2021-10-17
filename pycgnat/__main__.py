import json
import sys

from pycgnat.translator.direct import cgnat_direct
from pycgnat.translator.reverse import cgnat_reverse
from pycgnat.utils.parser import parser


# Main program run at terminal.
def main():
    args = parser.parse_args()
    kwargs = args._get_kwargs()
    keys = sorted(key for key, _ in kwargs)
    try:
        if keys == ["module", "private_net", "public_net", "source_addr"]:
            # Using translator module
            if type(args.source_addr) == tuple:  # using --reverse
                query = cgnat_reverse(
                    args.private_net,
                    args.public_net,
                    args.source_addr[0],
                    args.source_addr[1],
                )
            else:  # using --direct
                query = cgnat_direct(
                    args.private_net, args.public_net, args.source_addr
                )
            print(json.dumps(query, default=lambda x: str(x)))
        else:  # keys == ['module', 'output_file', 'private_net', 'public_net', 'target_platform']  # noqa: E501
            # Using generator module
            gen_call(
                args.output_file,
                args.private_net,
                args.public_net,
                args.target_platform,
            )
    except BaseException as e:
        print("error:", e, file=sys.stderr)
        sys.exit(1)


# Call to run generator module.
def gen_call(output_file, private_net, public_net, target_platform):
    generate = __import__(
        f"pycgnat.generator.{target_platform}", fromlist=["generate"]
    ).generate
    rules = generate(private_net, public_net)
    if output_file:
        with open(output_file, "w") as fp:
            fp.write(rules)
    else:
        print(rules, end="")


if __name__ == "__main__":
    main()
