#!/bin/bash
set -eu

echo 1 | python3 initialize_card.py
echo 2 | python3 initialize_card.py
echo 4 | python3 initialize_db.py
