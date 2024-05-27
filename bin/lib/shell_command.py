from .program import subparsers, run_shell_command
from .config import DEFAULT_DB

parser_shell = subparsers.add_parser('shell', help='start odoo shell')
parser_shell.add_argument("-d", "--database", help="Database name", type=str, default=DEFAULT_DB)
parser_shell.add_argument("--container", help="Docker container", type=str, default='web')

def cmd_shell(args):
    cmd = 'docker exec -e COLUMNS=`tput cols` -e LINES=`tput lines` -it {container} /bin/bash -c "reset -w && odoo shell -d {db} -r odoo -w odoo --db_host=172.17.0.1"'.format(
        db = args.database,
        container=args.container
    )

    run_shell_command(cmd)
