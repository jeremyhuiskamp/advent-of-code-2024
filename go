#!/usr/bin/env bash

set -euo pipefail

__typecheck() {
  # ty is faster, so have it fail first
  echo ty
  uv run ty check
  echo mypy
  uv run mypy .
}

__test() {
  __typecheck
  uv run pytest "$@"
}

__repl() {
  uv run python "$@"
}

CMD=${1:-}
shift || true
if [[ $(type -t "__${CMD}") == function ]]; then
  "__${CMD}" "$@"
else
  echo -e "available sub-commands:\n$(declare -F | sed -n "s/declare -f __/ - /p")"
fi
