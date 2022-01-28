#!/bin/sh
set -e

show_usage() {
  echo "md2code <EXT> <INPUT>"
  echo "  create a code file which contains only the code blocks from the input"
  echo "  only code blocks tagged with EXT are output"
  echo "  NOTE: the input filename should end in '.md'"
  echo "        that extension is replaced with EXT"
}

case "$1" in
  --help|-h) show_usage; exit 0 ;;
  '') should >&2; exit 1 ;;
  *) ext="$1" ;;
esac

case "$2" in
  '') show_usage >&2; exit 1 ;;
  *.md) fname="${2%.md}" ;;
  *) show_usage >&2; exit 1 ;;
esac

awk '
/^```('"$ext"')?$/ {
  print ""
  rc = getline
  while(rc > 0) {
    if ($0 ~ /```/) {
      print ""
      break
    } else {
      print $0
      rc = getline
    }
  }
  next
}

{ print "" }
' <"$fname.md" >"$fname.$ext"