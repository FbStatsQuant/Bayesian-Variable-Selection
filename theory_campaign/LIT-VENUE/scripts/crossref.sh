#!/bin/bash
# Venue check via the Crossref REST API: crossref.sh "title words" ...
for t in "$@"; do echo "Q: $t"
curl -s -m 20 "https://api.crossref.org/works?rows=2&select=title,container-title,issued,volume,page,DOI,author&query.bibliographic=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$t")" | python3 -I -c 'import json,sys
for it in json.load(sys.stdin)["message"]["items"]:
  print("  ", (it.get("title") or [""])[0][:90],"|",(it.get("container-title") or [""])[0],"|",it.get("issued",{}).get("date-parts",[[None]])[0][0],"|",it.get("volume"),it.get("page"),"|",it.get("DOI"),"|",",".join(a.get("family","") for a in it.get("author",[])[:5]))'
done
