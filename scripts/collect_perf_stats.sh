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
    NR==1 { for (i=1; i<=NF; i++) headers[i]=$i }
    NR==2 { for (i=2; i<=NF; i++) {print headers[i-1] "=" $i > (dir "/ram_stats.txt")} }
    NR==3 { for (i=2; i<=NF; i++) {print headers[i-1] "=" $i > (dir "/swap_stats.txt")} }
    END { if (NR < 3) exit 1 }
    '; then
        echo "Error while collecting or parsing data" >&2
        return 1
    fi

    return 0
}

record_cpu_stats() {
    local dst_dir="$1"

    if ! awk -v path="$dst_dir""/la_stats.txt" '
    {
    print "last_1="$1 > path
    print "last_5="$2 >> path
    print "last_15="$3 >> path
    }
    END {if (NR != 1) exit 1}
    ' /proc/loadavg; then
        echo "Error while collecting or parsing data" >&2
        return 1
    fi

    return 0
}

record_disk_stats() {
    local dst_dir="$1"

    if ! df -B MB | tail -n +2 | awk -v dir="$dst_dir" '
    {
    path=dir"/fs_"NR
    print "fs_name=" $1 > path".txt"
    print "size=" $2 >> path".txt"
    print "used=" $3 >> path".txt"
    print "available=" $4 >> path".txt"
    print "mount=" $6 >> path".txt"
    }
    END {if (NR < 1) exit 1}
    '; then
        echo "Error while collecting or parsing data" >&2
        return 1
    fi

    return 0
}

record_proc_list() {
    local dst_dir="$1"

    if ! ps aux | awk -v dir="$dst_dir" '
        NR != 1 {print $1, $2, $3, $4, $8, $9, $11 > dir"/proc_list.txt"}
    '; then
        echo "Error while collecting data" >&2
        return 1
    fi

    return 0
}

perf_dir="$1"/perf

mkdir -p "$perf_dir" || exit 1

record_ram_stats "$perf_dir" || exit 1

record_cpu_stats "$perf_dir" || exit 1

record_disk_stats "$perf_dir" || exit 1

record_proc_list "$perf_dir" || exit 1

exit 0