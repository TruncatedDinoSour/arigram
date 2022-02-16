#!/usr/bin/env bash

set -xe

main() {
    SRC="$(dirname "$0")"
    cd "$SRC"

    ARG=${1:-""}

    case $ARG in
    review)
        gh pr create -f
        ;;

    push)
        isort arigram/*.py
        black .

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
        python3 -m pip install --user --upgrade .
        ;;

    upgrade)
        git reset --hard
        git pull
        $0 local
        ;;

    check)
        black .
        isort arigram/*.py
        chmod a+rx ./check.sh
        ./check.sh
        ;;

    *)
        python3 -m arigram
        ;;
    esac
}

main "$@"
