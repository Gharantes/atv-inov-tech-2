#!/usr/bin/env bash
# Faz o build e roda backend (http://localhost:8000) e frontend (http://localhost:5173) no Docker
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f backend/.env ]; then
  echo "Erro: backend/.env não encontrado. Copie backend/.env.example para backend/.env e preencha a GEMINI_API_KEY." >&2
  exit 1
fi

exec docker compose up --build
