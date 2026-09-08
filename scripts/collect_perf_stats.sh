#!/usr/bin/env bash

if [ $# -ne 1 ]; then
    echo "This tool requires strictly 1 argument, $# given" >&2
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Wrong argument passed (not a directory)" >&2
    exit 1
fi

record_ram_stats() {
    local dst_dir="$1"

    set -o pipefail

    if ! free --mega | awk -v dir="$dst_dir" '
    NR==1 { for (i=2; i<=NF; i++) headers[i-1]=$i}
    NR==2 { for (i=2; i<=NF; i++) { print headers[i-1] "=" $i > (dir "/ram_stats") } }
    NR==3 { for (i=2; i<=NF; i++) { print headers[i-1] "=" $i > (dir "/swap_stats") } }
    END {if (NR < 3) exit 1}
    '; then
        echo "Error while collecting or parsing data" >&2
        return 1
    fi
}

record_ram_stats "$1" || exit 1

exit 0