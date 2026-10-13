#!/usr/bin/env bash

set -euo pipefail

readonly pattern='(/home/[^/[:space:]]+/|/Users/[^/[:space:]]+/|file://|qmd://|obsidian://|~/Downloads|~/obsidian)'
readonly self_path='scripts/check-public-content.sh'

failed=0

while IFS= read -r revision; do
  if git grep -n -I -E "$pattern" "$revision" -- . ":(exclude)$self_path"; then
    echo "Private or local source marker found in Git revision $revision" >&2
    failed=1
  fi
done < <(git rev-list --all)

while IFS= read -r -d '' file; do
  if grep -nI -E "$pattern" "$file"; then
    echo "Private or local source marker found in working-tree file $file" >&2
    failed=1
  fi
done < <(find . -type f \
  -not -path './.git/*' \
  -not -path './.venv/*' \
  -not -path './.cache/*' \
  -not -path './site/*' \
  -not -path "./$self_path" \
  -print0)

if [[ "$failed" -ne 0 ]]; then
  exit 1
fi

echo "No private or local source markers found in the working tree or reachable Git history."
