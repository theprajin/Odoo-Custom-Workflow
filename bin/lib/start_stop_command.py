from .program import subparsers, run_shell_command, no_db_warning, is_image_running
import re
import platform
import logging

_logger = logging.getLogger('START-STOP-COMMAND')

ms_kernel = re.compile(r'.*(microsoft)$', re.I)
is_WSL = any(ms_kernel.match(i) is not None for i in platform.uname())

parser_start = subparsers.add_parser('start', help='start odoo development server')
parser_start.add_argument("-d", "--database", help="Database name", type=str)
parser_start.add_argument("--no-stop", help="do not halt on exit", action='store_true', default=False)
parser_start.add_argument("-u", "--update", help="Update addons", type=str)
parser_start.add_argument("-i", "--install", help="Install addons", type=str)
parser_start.add_argument('--nginx', help='enable nginx', action='store_true', default=False)
parser_start.add_argument('--no-wsl', help='Disable WSL', action='store_true', default=False)
parser_start.add_argument('-p','--publish', action='append', help='Publish ports', required=False, default=[])
parser_start.add_argument('--db-only', action='store_true', help="Start database service only", required=False, default=False)
parser_start.add_argument('--production', help='start for production environment', action='store_true', default=False)

parser_stop = subparsers.add_parser('stop', help='halt odoo development server')

cmds = {
    'start': 'docker-compose -f docker-compose.yml -f docker-compose.dev.yml run {publish} --name web web',
    'start_with_nginx':'docker-compose -f docker-compose.yml -f docker-compose.dev.yml run {publish} --name nginx nginx',
    'start_production':'docker-compose up -d',
    'db_only': 'docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm {publish} db',
    'stop': 'docker-compose down',
    'wsl_extra': 'docker-volume-watcher.exe web 2>/dev/null'
}


def cmd_start(args):

    if is_image_running(b'odoo'):
        print('already running...')
        exit()

    should_stop = not args.no_stop
    wsl = is_WSL and not args.no_wsl

    if args.production:
        cmd = cmds['start_production']
        should_stop = False
    elif args.nginx:
        cmd = cmds['start_with_nginx']
        default_publish_ports = '-p 80:80'
    elif args.db_only:
        cmd = cmds['db_only']
        default_publish_ports = '--service-ports'
    else:
        cmd = cmds['start']
        default_publish_ports = '--service-ports'

    publish_ports = default_publish_ports if not args.publish else (
        ' '.join('-p {}'.format(p) for p in args.publish)
    )

    cmd = cmd.format(
        publish=publish_ports
    )

    env = ''

    env = 'DB=%s %s' % (args.database, env) if args.database else env
    env = 'UPDATE=%s %s' % (args.update, env) if args.update else env
    env = 'INSTALL=%s %s' % (args.install, env) if args.install else env

    if (args.update or args.install) and not args.database:
        no_db_warning()

    cmd = env + cmd

    if wsl:
        run_shell_command('killall docker-volume-watcher.exe')
        cmd = cmds['wsl_extra'] + ' & ' + cmd

    run_shell_command(cmd)

    if should_stop:
        run_shell_command(cmds['stop'])

def cmd_stop(args):
    run_shell_command(cmds['stop'])
