#!/usr/bin/env bash

set -xe

main() {
    SRC="$(dirname "$0")"
    cd "$SRC"

    ARG=${1:-""}

    case $ARG in
    push)
        isort arigram/*.py
        black arigram/

        python3 -m poetry check
        python3 -m poetry lock

        $0 check
        $0 local

        git diff >/tmp/arigram.diff
        git add -A
        git commit -sa
        git push -u origin main
        ;;

    local)
        python3 -m pip install --user --no-cache --upgrade .
        ;;

    upgrade)
        git reset --hard
        git pull
        $0 local
        ;;

    check)
        black arigram/
        isort arigram/*.py
        chmod u+rx ./check.sh
        ./check.sh
        ;;

    entry)
        mkdir -p /usr/share/applications
        cp -i arigram.desktop /usr/share/applications
        ;;

    *)
        python3 -m arigram
        ;;
    esac
}

main "$@"
