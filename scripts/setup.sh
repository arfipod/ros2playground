#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")/.."
course_root="$PWD"
bash scripts/build.sh
env_line="source $(printf '%q' "$course_root/scripts/env.sh")"
if ! rg -F -x "$env_line" "$HOME/.bashrc" >/dev/null; then
  printf '\n%s\n' "$env_line" >> "$HOME/.bashrc"
fi
printf '\nEntorno preparado. Abre una terminal NUEVA y lee curso/00-empezar.md.\n'
