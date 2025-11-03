#! /bin/bash

rm -f output/tg.txt
rm -f output/vk.txt

[[ ! -d output ]] && mkdir output

source .venv/bin/activate
python3 main.py
