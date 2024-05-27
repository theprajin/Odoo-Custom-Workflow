#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([database], [Database])
# ARG_OPTIONAL_SINGLE([user],[u],[User], [\\\$USER])
# ARG_OPTIONAL_SINGLE([port],[p],[Database port], [5432])
# ARG_OPTIONAL_SINGLE([db-host],[o],[Database host], [\\\$HOST])
# ARG_OPTIONAL_BOOLEAN([password],[W],[Force password prompt], [off])
# ARG_HELP([<Connect to postgres database>])
# ARGBASH_GO

# [ <-- needed because of Argbash

if [ "$_arg_password" = "on" ]; then
  force_password='-W'
else
  force_password='-w'
fi

cmd="docker-compose run --rm
  -e COLUMNS=$(tput cols)
  -e LINES=$(tput lines)
  -u odoo
  web
  /bin/bash -c \"PGPASSWORD=\\\$(cat \\\$PASSWORD_FILE) /wait-for-it.sh \\\$HOST:$_arg_port -s -t 10 -- psql $force_password -h $_arg_db_host -U $_arg_user $_arg_database"\"

echo $cmd
eval $cmd

# ] <-- needed because of Argbash
