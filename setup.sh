#!/bin/sh
set -eu
if ! command -v python3 >/dev/null 2>&1; then echo 'Python 3 required: apk add python3'; exit 1; fi
if ! python3 -c 'import segno' >/dev/null 2>&1; then
  if ! python3 -m pip --version >/dev/null 2>&1; then apk add py3-pip; fi
  python3 -m pip install --break-system-packages segno || python3 -m pip install segno
fi
python3 -c 'import segno; print("QR dependency ready")'
