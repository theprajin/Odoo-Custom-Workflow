#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([command], [Command], [])
# ARG_OPTIONAL_BOOLEAN([db-only],,[Start database only])
# ARG_OPTIONAL_BOOLEAN([production],,[Start production session])
# ARG_OPTIONAL_BOOLEAN([debug],,[Start debug session])
# ARG_OPTIONAL_SINGLE([name],[n],[Service name], [web])
# ARG_OPTIONAL_SINGLE([database],[d],[Database])
# ARG_OPTIONAL_SINGLE([update],[u],[Update addons])
# ARG_OPTIONAL_SINGLE([install],[i],[Install addons])
# ARG_OPTIONAL_BOOLEAN([wsl],,[Enable WSL support], [off])
# ARG_OPTIONAL_REPEATED([publish],[p],[Service ports])
# ARG_HELP([<Start or stop erp service>])
# ARG_LEFTOVERS([help text (optional)])
# ARGBASH_GO

# [ <-- needed because of Argbash
ext_watcher=false
publish_ports=()
app_name=$(basename $PWD)
container_name="${app_name}_${_arg_name}"
on_trap="trap - INT TERM && docker-compose down"

if [ ${#_arg_publish} -eq 0 ]; then
  publish_ports=(--service-ports)
else
  for p in "${_arg_publish[@]}"; do publish_ports+=(-p $p); done
fi

if grep -q Microsoft /proc/version; then
  ext_watcher=true
fi

case $_arg_command in
  start )

    web_cmd=(web)
    run_cmd=()
    cmd=()

    if [ "$_arg_production" = "on" ]; then
      compose_cmd=(docker-compose)
      on_trap="trap - INT TERM && echo 'Success!'"

      if [ $_arg_update ]; then
        compose_cmd=(UPDATE=$(sed -e 's/addons\///g' -e 's/\///g' -e 's/,$//g' <<< $_arg_update) "${compose_cmd[@]}")
      fi

      ext_watcher=false

      cmd=("${compose_cmd[@]}" up -d)
    else
      compose_cmd=(docker-compose -f docker-compose.yml -f docker-compose.dev.yml)

      if [ "$_arg_debug" = "on" ]; then
        web_cmd+=(odoo-debug)
        run_cmd=("${compose_cmd[@]}" run)
      else
        web_cmd+=(odoo --dev all)
        run_cmd=("${compose_cmd[@]}" run)
      fi
    fi

    if [ "$_arg_db_only" = "on" ]; then
      on_trap="trap - INT TERM"
      cmd=("${compose_cmd[@]}" run --rm --no-deps "${publish_ports[@]}" db)
    fi

    run_cmd+=("${publish_ports[@]}" --name $container_name)

    if [ $_arg_database ]; then
      web_cmd+=(-d $_arg_database)

      if [ $_arg_update ]; then
        web_cmd+=(-u $(sed -e 's/addons\///g' -e 's/\///g' -e 's/,$//g' <<< $_arg_update))
      fi

      if [ $_arg_install ]; then
        web_cmd+=(-i $(sed -e 's/addons\///g' -e 's/\///g' -e 's/,$//g' <<< $_arg_install))
      fi
    fi

    if [ ${#cmd} -eq 0 ]; then
      cmd=("${run_cmd[@]}" "${web_cmd[@]}" "${_arg_leftovers[@]}")
    fi

    if [ $ext_watcher = true ]; then
      on_trap="${on_trap[@]} && kill -- -\$\$"
      cmd=(docker-volume-watcher.exe $container_name 2\>/dev/null \& "${cmd[@]}")
    fi

    echo "${cmd[@]}"
    trap "${on_trap[@]}" INT TERM EXIT
    eval "${cmd[@]}"
    ;;
  stop )
    docker-compose down
  ;;
  * )
    print_help
    ;;
esac
# ] <-- needed because of Argbash
