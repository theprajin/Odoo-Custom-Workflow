#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_OPTIONAL_SINGLE([user],[u],[User], [odoo])
# ARG_OPTIONAL_SINGLE([container],[c],[Docker container])
# ARG_OPTIONAL_SINGLE([working-dir],[],[Working directory], [/])
# ARG_HELP([<Login to docker container>])
# ARGBASH_GO

# [ <-- needed because of Argbash
app_name=$(basename $PWD)
container=${_arg_container:-"${app_name}_web"}
cmd="docker exec -it
  -e COLUMNS=$(tput cols)
  -e LINES=$(tput lines)
  -u $_arg_user
  -w $_arg_working_dir
  $container
  /bin/bash -c \"reset -w && bash\""

echo $cmd
eval $cmd

# ] <-- needed because of Argbash
