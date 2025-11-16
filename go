#!/usr/bin/env bash

__test() {
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
