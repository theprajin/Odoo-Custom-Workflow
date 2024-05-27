from os import path
from .program import subparsers, run_shell_command

parser_scaffold = subparsers.add_parser('scaffold', help='creation of a skeleton structure')
parser_scaffold.add_argument("--container", help="Docker container", type=str, default='web')
parser_scaffold.add_argument('name', action='store', nargs=1, type=str)

def cmd_scaffold(args):

    if not args.name:
        parser_scaffold.print_usage()
        exit()

    cmd = 'docker exec -u 1000:1000 -w /mnt/extra-addons {container} odoo scaffold {name} .'.format(
        container = args.container,
        name = args.name[0]
    )

    run_shell_command(cmd)
