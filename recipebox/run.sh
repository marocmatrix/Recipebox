#!/usr/bin/env sh
cd /app

export DATA_DIR="${DATA_DIR:-/data}"
mkdir -p "${DATA_DIR}/uploads"

echo "[RecipeBox] Python: $(python3 --version)"
echo "[RecipeBox] Workdir: $(pwd)"
echo "[RecipeBox] DATA_DIR: ${DATA_DIR}"
echo "[RecipeBox] Checking app import..."

# Import-test first so any error prints a full traceback to the log
python3 -c "import app.main; print('[RecipeBox] Import OK')" || {
  echo "[RecipeBox] IMPORT FAILED — see traceback above"
  exit 1
}

echo "[RecipeBox] Starting server on 0.0.0.0:8099"
exec python3 -m app.main
