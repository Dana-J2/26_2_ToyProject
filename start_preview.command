#!/bin/zsh
cd "$(dirname "$0")"
if [[ ! -x .venv/bin/python ]]; then
  echo '먼저 README의 가상환경 설치 안내를 확인해주세요.'
  read -r '?Enter를 누르면 닫힙니다.'
  exit 1
fi
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
