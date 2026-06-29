#!/bin/bash
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ -f venv/bin/activate ]; then
  source venv/bin/activate
elif [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi

if [ "${ENIGMA_SKIP_CHECK:-0}" != "1" ]; then
  python3 "$ROOT/check_env.py" --gui || exit 1
fi

exec python3 "$ROOT/Enigma-SC.py" "$@"
