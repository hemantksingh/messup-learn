#!/bin/bash
# Check every external URL in the repo's markdown. Usage: audit/tools/linkcheck.sh > linkcheck.tsv
# Statuses: OK, MOVED (2xx on a different host), DEAD (404/410), UNVERIFIED (403/429/5xx), ERR (no response), PLACEHOLDER
cd "$(dirname "$0")/../.." || exit 1
grep -rhoE 'https?://[^ )>\]"'"'"'`]+' --include='*.md' --exclude-dir=audit . | sed -E 's/[.,;:]+$//' | sort -u \
  | xargs -P 8 -I{} "$(dirname "$0")/linkcheck-one.sh" {}
