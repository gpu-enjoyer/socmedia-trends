#!/bin/bash

set -e

dpkg -s python3-tk >/dev/null 2>&1 || \
sudo apt install -y python3-tk

[[ -d .venv ]] && rm -rf .venv

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip

pip install -r requirements.txt
pip install TgCrypto

if [[ ! -f /usr/local/bin/mystem ]]; then
    wget http://download.cdn.yandex.net/mystem/mystem-3.1-linux-64bit.tar.gz
    tar -xzf mystem-3.1-linux-64bit.tar.gz
    sudo mv mystem /usr/local/bin/
fi
