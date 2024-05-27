#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([name], [Addon name])
# ARG_HELP([<Scaffold odoo module>])
# ARGBASH_GO

# [ <-- needed because of Argbash

cmd="docker-compose run --rm --no-deps -u 1000:1000 -w /mnt/extra-addons web odoo scaffold $_arg_name ."

echo $cmd
eval $cmd

# ] <-- needed because of Argbash
