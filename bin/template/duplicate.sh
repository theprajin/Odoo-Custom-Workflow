#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([original-database], [Original Database])
# ARG_POSITIONAL_SINGLE([duplicate-database], [New Database])
# ARG_HELP([<Backup odoo database and filestore>])
# ARGBASH_GO

# [ <-- needed because of Argbash
compose="docker-compose run --rm --no-deps
  -u odoo
  -w /
  web
  python -c \"from db_tools import duplicate; duplicate('$_arg_original_database', '$_arg_duplicate_database')\""

echo $compose
eval $compose && echo "Success! '$_arg_original_database' => '$_arg_duplicate_database'"
# ] <-- needed because of Argbash
