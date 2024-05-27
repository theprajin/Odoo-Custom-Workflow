#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([database], [Database])
# ARG_POSITIONAL_SINGLE([backup-dir], [Backup directory], [$PWD])
# ARG_HELP([<Backup odoo database and filestore>])
# ARGBASH_GO

# [ <-- needed because of Argbash
CONTAINER=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
BACKUP_PATH=$_arg_backup_dir/${_arg_database}-$(date "+%Y-%m-%d-%H-%M-%S").zip
on_trap="trap - INT TERM && docker rm $CONTAINER"
compose="docker-compose run --name $CONTAINER --no-deps
  -u odoo
  -w /
  web
  python -c \"from db_tools import backup; backup('$_arg_database')\"
  && docker cp $CONTAINER:/tmp/backup.zip  $BACKUP_PATH"

echo $compose
eval $compose && echo "Backup success! Backup is located at $BACKUP_PATH"
trap "${on_trap[@]}" INT TERM EXIT
# ] <-- needed because of Argbash
