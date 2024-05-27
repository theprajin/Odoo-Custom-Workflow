from odoo.service.db import dump_db, restore_db, exp_drop, exp_duplicate_database
from odoo.tools import config
from os import environ as env, path
import logging

logging.basicConfig(format='', level=logging.INFO)

_logger = logging.getLogger('Backup/Restore')

config['db_host'] = env.get('HOST', 'db')
config['db_port'] = env.get('PORT', '5432')
config['db_user'] = env.get('USER', 'odoo')
config['list_db'] = True

PWD_FILE = env.get('PASSWORD_FILE')
if path.exists(PWD_FILE):
    with open(PWD_FILE, 'r') as pwd:
        config['db_password'] = pwd.readline()
else:
    config['db_user'] = env.get('PASSWORD')

def backup(database):
    with open('/tmp/backup.zip', 'wb') as backup_file:
        dump_db(database, backup_file, 'zip')
        backup_file.seek(0)

def restore(database):
    try:
        restore_db(database, '/tmp/backup.zip', copy=True)
    except AttributeError as e:
        pass

def drop(database):
    exp_drop(database)

def duplicate(original_db, duplicate_db):
    try:
        exp_duplicate_database(original_db, duplicate_db)
    except AttributeError as e:
        pass
