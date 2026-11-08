#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_PATH="${SCRIPT_DIR}/model_config.json"
DEFAULT_FALLBACK_MODEL="gemma3:1b"

usage() {
  cat <<'EOF'
Usage:
  ./setup_ollama.sh [model]

Starts the local Ollama server if needed, then pulls the requested model.
When no model is provided, the script uses ollama.default_model from
model_config.json.

Environment:
  OLLAMA_SETUP_LOG  Path for ollama serve logs when this script starts it.
EOF
}

read_default_model() {
  if command -v python3 >/dev/null 2>&1; then
    python3 - "$CONFIG_PATH" "$DEFAULT_FALLBACK_MODEL" <<'PY'
import json
import sys

config_path = sys.argv[1]
fallback = sys.argv[2]

try:
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
    model = config.get("ollama", {}).get("default_model") or fallback
except Exception:
    model = fallback

print(model)
PY
  else
    printf '%s\n' "$DEFAULT_FALLBACK_MODEL"
  fi
}

wait_for_ollama() {
  local pid="${1:-}"
  local log_file="${2:-}"

  for _ in {1..30}; do
    if ollama list >/dev/null 2>&1; then
      return 0
    fi

    if [[ -n "$pid" ]] && ! kill -0 "$pid" >/dev/null 2>&1; then
      printf 'ollama serve exited before it became ready.\n' >&2
      if [[ -n "$log_file" && -f "$log_file" ]]; then
        printf 'Last log lines from %s:\n' "$log_file" >&2
        tail -20 "$log_file" >&2 || true
      fi
      return 1
    fi

    sleep 1
  done

  printf 'Timed out waiting for Ollama to become ready.\n' >&2
  if [[ -n "$log_file" && -f "$log_file" ]]; then
    printf 'Last log lines from %s:\n' "$log_file" >&2
    tail -20 "$log_file" >&2 || true
  fi
  return 1
}

model_is_pulled() {
  local model="$1"
  ollama list | awk 'NR > 1 { print $1 }' | grep -qxF "$model"
}

main() {
  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    return 0
  fi

  if ! command -v ollama >/dev/null 2>&1; then
    printf 'ollama command was not found. Install Ollama first: https://ollama.com/download\n' >&2
    return 1
  fi

  local model="${1:-}"
  if [[ -z "$model" ]]; then
    model="$(read_default_model)"
  fi

  printf 'Using Ollama model: %s\n' "$model"

  if ollama list >/dev/null 2>&1; then
    printf 'Ollama server is already running.\n'
  else
    local log_file="${OLLAMA_SETUP_LOG:-${TMPDIR:-/tmp}/voice-ai-chat-ollama-serve.log}"
    printf 'Starting Ollama server with: ollama serve\n'
    nohup ollama serve >"$log_file" 2>&1 &
    local ollama_pid=$!
    printf 'ollama serve started in the background. PID: %s, log: %s\n' "$ollama_pid" "$log_file"
    wait_for_ollama "$ollama_pid" "$log_file"
  fi

  if model_is_pulled "$model"; then
    printf 'Model is already available locally: %s\n' "$model"
  else
    printf 'Pulling model: %s\n' "$model"
    ollama pull "$model"
  fi

  printf 'Ollama setup complete. Model ready: %s\n' "$model"
}

main "$@"
