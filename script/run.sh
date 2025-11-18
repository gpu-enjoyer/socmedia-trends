#!/bin/bash

set -e

ORIG_DIR="$(pwd)"
PROJ_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJ_DIR"


if [ -d output ]; then
    do_backup="/usr/local/bin/backupd_run"
    if [ -f $do_backup ]; then
        ./do_backup ./output ./output_archive
    fi
else
    mkdir output
fi

rm -f output/tg.txt
rm -f output/vk.txt

source .venv/bin/activate
python3 -m src.main

cd "$ORIG_DIR"
echo -e "\n run.sh DONE"
