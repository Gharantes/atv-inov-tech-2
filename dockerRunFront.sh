#!/usr/bin/env bash
# Faz o build e roda o frontend (React + Vite, servido pelo nginx) no Docker em http://localhost:5173
set -euo pipefail
cd "$(dirname "$0")"

exec docker compose up --build frontend
