import argparse
import logging
import subprocess
from .config import DEFAULT_DB

PROGRAM = 'gbterp'
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(PROGRAM)

parser = argparse.ArgumentParser(prog=PROGRAM)
subparsers = parser.add_subparsers(help='commands', dest="command")

def no_db_warning():
    _logger.warning('No database is selected \'{db}\' is used by default'.format(db = DEFAULT_DB))

def run_shell_command(cmd):
    print('Running command: {}\n'.format(cmd))
    subprocess.call(cmd, shell = True)

def is_image_running(image_name):
    images = subprocess.check_output('docker ps --format="{{.Image}}"'.split()).splitlines()

    return any([True for image in images if image_name in image])
