#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([database], [Database])
# ARG_POSITIONAL_SINGLE([backup], [Backup])
# ARG_OPTIONAL_SINGLE([server],[s],[Odoo server], [localhost])
# ARG_HELP([<Backup odoo database and filestore>])
# ARGBASH_GO

# [ <-- needed because of Argbash
stty -echo
printf "Database Manager Password: "
read PASSWORD
stty echo

printf "\n"

compose="curl -F master_pwd=$PASSWORD -F backup_file=@$_arg_backup -F copy=true -F name=$_arg_database http://$_arg_server/web/database/restore"

echo ${compose/$PASSWORD/***}
if $compose | grep -q '/web/database/manager'; then
  printf "Success: Database restore success!"
else
  printf "Error: Cannot restore database!"
fi

# ] <-- needed because of Argbash
