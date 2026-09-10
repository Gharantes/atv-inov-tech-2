#!/usr/bin/env bash
# Faz o build e roda o backend (FastAPI) no Docker em http://localhost:8000
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f backend/.env ]; then
  echo "Erro: backend/.env não encontrado. Copie backend/.env.example para backend/.env e preencha a GEMINI_API_KEY." >&2
  exit 1
fi

exec docker compose up --build backend
