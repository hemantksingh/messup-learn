#!/bin/bash
u="$1"
case "$u" in *example.com*|*example.org*|*example.net*|*localhost*|*169.254.*|*'$'*|*starter-agent*|*schemas.android.com*|*foo.example*|*nuget.example*) printf 'PLACEHOLDER\t-\t%s\t-\n' "$u"; exit;; esac
out=$(curl -s -o /dev/null -m 20 -L --max-redirs 5 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" -w "%{http_code} %{url_effective}" "$u" 2>/dev/null)
code=${out%% *}; eff=${out#* }
case "$code" in
  000|"") status="ERR" ;;
  2*)  h1=$(echo "$u" | awk -F/ '{print $3}' | sed 's/^www\.//'); h2=$(echo "$eff" | awk -F/ '{print $3}' | sed 's/^www\.//'); [ "$h1" != "$h2" ] && status="MOVED" || status="OK" ;;
  404|410) status="DEAD" ;;
  401|403|429|5*) status="UNVERIFIED" ;;
  *) status="OTHER" ;;
esac
printf '%s\t%s\t%s\t%s\n' "$status" "$code" "$u" "$eff"
