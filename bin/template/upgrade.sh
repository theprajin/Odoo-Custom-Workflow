#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([database], [Odoo database])
# ARG_POSITIONAL_INF([addons],[Comma separated Odoo addons], 1)
# ARG_OPTIONAL_SINGLE([user],[u],[Database user], [\\\$USER])
# ARG_OPTIONAL_SINGLE([password],[w],[Database password])
# ARG_OPTIONAL_SINGLE([db-host],[o],[Database host], [\\\$HOST])
# ARG_HELP([Upgrade odoo addons for selected database])
# ARGBASH_GO

# [ <-- needed because of Argbash
function join_by { local IFS="$1"; shift; echo "$*"; }

addons=$(join_by , "${_arg_addons[@]}")
addons=$(sed -e 's/addons\///g' -e 's/\///g' -e 's/,$//g' <<< $addons)

password=${_arg_password:-"\\\$(cat \\\$PASSWORD_FILE)"}
cmd="docker-compose run --rm --no-deps
  -e COLUMNS=$(tput cols)
  -e LINES=$(tput lines)
  web
  /bin/bash -c \"reset -w && odoo -d $_arg_database -w $password  -r $_arg_user --db_host $_arg_db_host -u $addons --stop-after-init\""

echo $cmd
eval $cmd

# ] <-- needed because of Argbash
