#!/bin/bash
set -eu

rm -f game.db
echo 1 | python3 initialize_card.py
echo 2 | python3 initialize_card.py
echo 4 | python3 initialize_db.py

set +eu
ps aux | grep -e main.py | head -n 1 | sed 's/^.....\ *\([0-9]*\)\ *.*/\1/g' | xargs kill
ps aux | grep -e main_api.py | head -n 1 | sed 's/^.....\ *\([0-9]*\)\ *.*/\1/g' | xargs kill

