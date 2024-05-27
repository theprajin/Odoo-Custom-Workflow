from .program import subparsers, _logger, is_image_running, run_shell_command
import subprocess

parser_connect = subparsers.add_parser('connect', help='connect to postgres database')
parser_connect.add_argument('database', action='store', nargs='?', type=str)

def cmd_connect(args):
    if not is_image_running(b'postgres'):
        _logger.error('you must start postgres database server first')
        exit()

    if not args.database:
        parser_connect.print_usage()

        print('\navailable databases:')
        dbs = subprocess.check_output(['psql', '-h', '172.16.238.12', '-U', 'odoo', '-d', 'template1', '-t', '-c', 'select datname from pg_database']).splitlines()

        for db in sorted(dbs):
            print(db.decode('utf-8'))
    else:
        cmd = 'psql -h 172.16.238.12 -U odoo -d {db}'.format(
            db = args.database
        )

        run_shell_command(cmd)
