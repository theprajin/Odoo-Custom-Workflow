#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([database], [Database])
# ARG_OPTIONAL_SINGLE([user],[u],[Database user], [\\\$USER])
# ARG_OPTIONAL_SINGLE([password],[w],[Database password])
# ARG_OPTIONAL_SINGLE([db-host],[o],[Database host], [\\\$HOST])
# ARG_OPTIONAL_SINGLE([container],[c],[Docker container])
# ARG_HELP([<Start odoo shell>])
# ARGBASH_GO

# [ <-- needed because of Argbash
app_name=$(basename $PWD)
container=${_arg_container:-"${app_name}_web"}
password=${_arg_password:-"\\\$(cat \\\$PASSWORD_FILE)"}
cmd="docker exec -it
  -e COLUMNS=$(tput cols)
  -e LINES=$(tput lines)
  $container
  /bin/bash -c \"reset -w && odoo shell -d $_arg_database -w $password  -r $_arg_user --db_host $_arg_db_host\""

echo $cmd
eval $cmd

# ] <-- needed because of Argbash
