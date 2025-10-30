#!/bin/bash

if [ ! -f /usr/local/bin/mystem ]; then
    wget http://download.cdn.yandex.net/mystem/mystem-3.1-linux-64bit.tar.gz
    tar -xzf mystem-3.1-linux-64bit.tar.gz
    sudo mv mystem /usr/local/bin/
fi

python3 -m venv venv
source venv/bin/activate

dpkg -s python3-tk >/dev/null 2>&1 || \
sudo apt install -y python3-tk

python3 -m pip install --upgrade pip

pip install -r requirements.txt
pip install TgCrypto
