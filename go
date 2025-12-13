#!/usr/bin/env bash

set -euo pipefail

__lint() {
  echo ruff:
  uv run ruff check
}

__typecheck() {
  # ty is faster, so have it fail first
  echo ty:
  uv run ty check
  echo mypy:
  uv run mypy .
}

__test() {
  __lint
  __typecheck
  uv run pytest "$@"
}

__test-watch() {
  fd | entr -s './go test --durations=0'
}

__repl() {
  uv run python "$@"
}

__edit() {
  local day="$1"
  nvim -O {,test_}day"$day".py
}

CMD=${1:-}
shift || true
if [[ $(type -t "__${CMD}") == function ]]; then
  "__${CMD}" "$@"
else
  echo -e "available sub-commands:\n$(declare -F | sed -n "s/declare -f __/ - /p")"
fi
