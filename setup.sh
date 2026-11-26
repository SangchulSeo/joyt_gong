#!/bin/sh
set -eu

cd "$(dirname "$0")"
if ! python3 -c 'import sqlite3, sys; sys.exit(sys.version_info < (3, 11))'; then
    printf '%s\n' 'Python 3.11 이상과 SQLite 표준 모듈이 필요합니다.' >&2
    exit 1
fi

python3 joyti.py init
python3 -m unittest -v
