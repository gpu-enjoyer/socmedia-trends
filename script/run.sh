#!/bin/bash

set -e

ORIG_DIR="$(pwd)"
PROJ_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJ_DIR"

source .venv/bin/activate
python3 -m src.main

cd "$ORIG_DIR"
echo -e "\n run.sh DONE"
