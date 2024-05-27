# Readme
* for init db
    - ./bin/odoo start -i base -d odoo

* the only time to run the above is when the application is run for the firs time; for the 2nd time onward, run the command below
    - ./bin/odoo start -u base -d odoo
    - .bin/odoo start

## \# Build docker image using docker-compose
1. cd into project root
2. Run command `$ chmod +x odoo-docker/entrypoint.sh odoo-docker/wait-for-it.sh`
3. Run command `$ docker-compose build --no-cache`
    * [OPTIONAL] For custom build args: `$ docker-compose build --no-cache --build-arg APT_MIRROR=http://ubuntu.ntc.net.np`

## \# CLI Commands

* `$ ./bin/odoo start`
* `$ ./bin/odoo start --debug`
* `$ ./bin/odoo start --production`
* `$ ./bin/odoo start -u <module1,module2> -d <dbname>`
* `$ ./bin/odoo shell <dbname>`
* `$ ./bin/odoo login [-u <root|odoo>]`
* `$ ./bin/odoo backup <dbname> [/backup-directory-path]`
* `$ ./bin/odoo upgrade <dbname> addon1 [addons/addon2] [addons/addon3,addon4]`
