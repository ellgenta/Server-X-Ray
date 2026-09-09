#!/usr/bin/env bash

set -eo pipefail

if [ $# -ne 3 ]; then
    echo "This tool requires strictly 3 arguments, $# given" >&2
    exit 1
fi

if [ ! -d "$1" ] || [ ! -d "$2" ]; then
    echo "Wrong arguments passed (not directories)" >&2
    exit 1
fi

if ! (cd "$(dirname "$1")" && zip -r "$2/$3" "$(basename "$1")" > /dev/null); then
    echo "Error while trying to archive $1" >&2
    exit 1
fi

echo "$2/$3.zip"

exit 0