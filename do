#!/bin/bash

set -e

SRC=$(dirname $0)

cd $SRC

ARG=${1:-""}


case $ARG in
    build)
        python3 -m pip install --upgrade setuptools wheel
        python3 setup.py sdist bdist_wheel
        python3 -m pip install --upgrade twine
        python3 -m twine upload --repository testpypi dist/*
        ;;

    review)
        gh pr create -f
        ;;

    release)
        CURRENT_VERSION=$(cat arigram/__init__.py | grep version | cut -d '"' -f 2)
        echo Current version $CURRENT_VERSION

        NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print $1 "." $2+1 "." $3}')
        echo New version $NEW_VERSION
        sed -i '' "s|$CURRENT_VERSION|$NEW_VERSION|g" arigram/__init__.py
        poetry version $NEW_VERSION

        git add -u arigram/__init__.py pyproject.toml
        git commit -m "Release v$NEW_VERSION"
        git tag v$NEW_VERSION

        poetry build
        poetry publish -u $(pass show i/pypi | grep username | cut -d ' ' -f 2 | tr -d '\n') -p $(pass show i/pypi | head -n 1 | tr -d '\n')
        git log --pretty=format:"%cn: %s" v$CURRENT_VERSION...v$NEW_VERSION  | grep -v -e "Merge" | grep -v "Release"| awk '!x[$0]++' > changelog.md
        git push origin master --tags
        gh release create v$NEW_VERSION -F changelog.md
        rm changelog.md
        ;;

    release-brew)
        CURRENT_VERSION=$(cat arigram/__init__.py | grep version | cut -d '"' -f 2)
        echo Current version $CURRENT_VERSION

        URL="https://github.com/TruncatedDinosour/arigram/archive/refs/tags/v$CURRENT_VERSION.tar.gz"
        echo $URL
        wget $URL -O /tmp/arigram.tar.gz
        HASH=$(sha256sum /tmp/arigram.tar.gz | cut -d ' ' -f 1)
        rm /tmp/arigram.tar.gz

        cd /opt/homebrew/Library/Taps/TruncatedDinosour/dino-bar
        sed -i '' "6s|.*|  url \"https://github.com/TruncatedDinosour/arigram/archive/refs/tags/v$CURRENT_VERSION.tar.gz\"|" arigram.rb
        sed -i '' "7s|.*|  sha256 \"$HASH\"|" arigram.rb

        brew audit --new arigram
        brew uninstall arigram || true
        brew install arigram
        brew test arigram

        git add -u arigram.rb
        git commit -m "Release arigram.rb v$CURRENT_VERSION"
        git push origin master
        ;;

    check)
        black .
        isort arigran/*.py
        sh check.sh
        ;;

    *)
        python3 -m arigram
        ;;
esac
