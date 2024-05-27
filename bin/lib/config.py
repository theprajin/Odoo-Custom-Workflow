from configparser import ConfigParser
from os import path

config = ConfigParser()
config.read(path.abspath('odoo.conf'))

DEFAULT_DB = config.get('options', 'db_name') or 'main'
