from .program import subparsers, run_shell_command
from .config import DEFAULT_DB

parser_shell = subparsers.add_parser('login', help='login to server')
parser_shell.add_argument("-u", "--user", help="User", type=str)
parser_shell.add_argument("-w", "--working-dir", help="Working Directory", type=str)
parser_shell.add_argument("--container", help="Docker container", type=str, default='web')

def cmd_login(args):
    cmd = 'docker exec -e COLUMNS=`tput cols` -e LINES=`tput lines` -it -u {user} -w {working_dir} {container} /bin/bash -c "reset -w && bash"'.format(
        user = args.user or 'odoo',
        working_dir = args.working_dir or '/',
        container=args.container
    )

    run_shell_command(cmd)
