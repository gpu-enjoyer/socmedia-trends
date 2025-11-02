#! /bin/bash

rm -f output/tg_results.txt
rm -f output/vk_results.txt

[[ ! -d output ]] && mkdir output

source venv/bin/activate
python3 main.py
