#!/usr/bin/env bash

set -eo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "This tool requires strictly 1 or 2 arguments, $# given" >&2
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Wrong argument passed (not a directory)" >&2
    exit 1
fi

if [ $# -ne 2 ]; then
    last_timestamp="1970-01-01T00:00:00"
else
    last_timestamp="$2"
fi

get_new_records_count() {
    if ! tail -n 50 "$1" | awk -v last_stamp="$2" '
    found {count++; next}
    $1 ~ /^[0-9]{4}/ && last_stamp < $1 {count=1; found=1}
    END {print count+0}
    '; then
        echo "Error while trying to get most recent records count" >&2
        return 1
    fi

    return 0
}

path="/var/log/"

files=(
    "syslog"
    "auth.log"
    "kern.log"
)

aliases=(
    "syslog.txt"
    "authlog.txt"
    "kernlog.txt"
)

logs_dir="$1""/logs"

mkdir -p "$logs_dir" || exit 1

for i in "${!files[@]}"; do 
    complete_path="$path${files[i]}"

    if [ ! -f "$complete_path" ]; then
        continue
    fi

    new_lines_count=$(get_new_records_count "$complete_path" "$last_timestamp")

    if [ "$new_lines_count" -eq 0 ]; then
        touch "$logs_dir""/""${aliases[i]}"
        continue
    fi

    if ! tail -n "$new_lines_count" "$path${files[i]}" > "$logs_dir""/""${aliases[i]}"; then
        echo "Error while collecting or parsing data" >&2
        exit 1
    fi
done

exit 0