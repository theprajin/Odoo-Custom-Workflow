#!/bin/bash

set -e

# set the postgres database host, port, user and password according to the environment
# and pass them as arguments to the odoo process if not present in the config file
: ${HOST:=${DB_PORT_5432_TCP_ADDR:='db'}}
: ${PORT:=${DB_PORT_5432_TCP_PORT:=5432}}
: ${USER:=${DB_ENV_POSTGRES_USER:=${POSTGRES_USER:='odoo'}}}
: ${PASSWORD:=${DB_ENV_POSTGRES_PASSWORD:=${POSTGRES_PASSWORD:='odoo'}}}
: ${WAIT_TIMEOUT:=60}

if [ ! -z $PASSWORD_FILE ]; then
  PASSWORD=$(cat $PASSWORD_FILE)
fi

DB_ARGS=()
function check_config() {
    param="$1"
    value="$2"
    if ! grep -q -E "^\s*\b${param}\b\s*=" "$ODOO_RC" ; then
        DB_ARGS+=("--${param}")
        DB_ARGS+=("${value}")
    fi;
}
check_config "db_host" "$HOST"
check_config "db_port" "$PORT"
check_config "db_user" "$USER"
check_config "db_password" "$PASSWORD"

case "$1" in
    odoo)
        shift
        if [[ $1 =~ ^(scaffold|shell)$ ]] ; then
            exec odoo "$@"
        else
          PYTHONIOENCODING=utf-8 exec wait-for-it $HOST:$PORT -s -t $WAIT_TIMEOUT -- odoo "$@" "${DB_ARGS[@]}"
        fi
        ;;
    odoo-debug)
        shift
        PYTHONIOENCODING=utf-8 exec wait-for-it $HOST:$PORT -s -t $WAIT_TIMEOUT -- python -m ptvsd --host 0.0.0.0 --port 5678 --wait /usr/bin/odoo "$@" "${DB_ARGS[@]}"
        ;;
    *)
        exec "$@"
esac

exit 1
