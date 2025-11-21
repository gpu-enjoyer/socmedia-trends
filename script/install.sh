#!/bin/bash

set -e

ORIG_DIR="$(pwd)"
PROJ_DIR="$(cd "$(dirname "$0")/.." && pwd)" 
cd "$PROJ_DIR"

rm -rf .venv
rm -rf src/__pycache__

dpkg -s python3-tk >/dev/null 2>&1 \
|| sudo apt install -y python3-tk

if [[ ! -f /usr/local/bin/mystem ]]; then
    STM="mystem-3.1-linux-64bit.tar.gz"
    wget "http://download.cdn.yandex.net/mystem/$STM"
    tar -xzf "$STM" && rm "$STM"
    sudo mv mystem /usr/local/bin/
fi

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r script/requirements.txt

cd "$ORIG_DIR"
echo -e "\n install.sh DONE"

