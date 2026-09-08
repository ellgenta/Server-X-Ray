#!/usr/bin/env bash
set -o pipefail

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

    if ! free --mega | awk -v dir="$dst_dir" '
    NR==1 { for (i=2; i<=NF; i++) headers[i-1]=$i }
    NR==2 { for (i=2; i<=NF; i++) { print headers[i-1] "=" $i > (dir "/ram_stats.txt") } }
    NR==3 { for (i=2; i<=NF; i++) { print headers[i-1] "=" $i > (dir "/swap_stats.txt") } }
    END { if (NR < 3) exit 1 }
    '; then
        echo "Error while collecting or parsing data" >&2
        return 1
    fi

    return 0
}

record_cpu_stats() {
    local dst_dir="$1"

    if ! awk -v dir="$dst_dir" '
    {printf "last_1="$1"\nlast_5="$2"\nlast_15="$3"\n" > (dir "/load_avg.txt")}' /proc/loadavg; then 
        echo "Error while collecting or parsing data" >&2
        return 1
    fi

    return 0
}

perf_dir="$1"/perf

mkdir -p "$perf_dir" || exit 1

record_ram_stats "$perf_dir" || exit 1

record_cpu_stats "$perf_dir" || exit 1

exit 0