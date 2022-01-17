#!/usr/bin/env python3

import os
import re
import sys

from collections import defaultdict as ddict
from glob import glob
from os import path

# TODO move this into a separately-loaded file
tagwordToTitle = {
  "docs": "Documentation",
  "hott": "HoTT",
  "impl": "Implementation",
  "lang": "Language",
  "todo": "TODO",
}

byTag = ddict(lambda: []) # {tag: [(title, filename), …], …}
untagged = [] # [(title, fname), …]

def main():
  tagRegex = r'[a-z-]+'
  tagMatch = r'tag:\s+('+tagRegex+r')\s*'
  tagsMatch = r'tag:\s+('+tagRegex+r'(?:\s*,\s+'+tagRegex+r')*)(?:\s*,)?\s*'

  os.chdir(path.realpath(path.dirname(__file__)))
  for fname in glob("./notes/*.md"):
    title, tags = processNote(fname)
    if tags:
      for tag in tags:
        byTag[tag].append((title, fname, tags))
    else:
      print(f"[WARN] no tags for {fname}", file=sys.stderr)
      untagged.append((title, fname))

  with open("index.md", 'wt') as fp:
    print("# Technical Notes Index", file=fp)
    print("", file=fp)
    generateTagIndex(fp)
  with open("tags.txt", 'wt') as fp:
    # counts = sorted(
    #     ((tag, len(byTag[tag])) for tag in byTag.keys())
    #   , key=lambda x: (-x[1], x[0]) # ordered by descending frequency, then ascending name
    #   )
    counts = sorted((tag, len(byTag[tag])) for tag in byTag.keys()) # ordered by ascending name
    for tag, count in counts:
      msg = f"{count}\t{tag}"
      print(msg, file=sys.stderr)
      print(msg, file=fp)

def generateTagIndex(fp):
  out = lambda msg: print(msg, file=fp)
  out("## Notes by Tag")
  out("")
  for tag in sorted(byTag.keys()):
    humanTag = " ".join(toTagword(tag) for tag in tag.split("-"))
    out(f"### {humanTag}")
    out("")
    for title, fname, ftags in byTag[tag]:
      out(f"  * [{title}]({fname}): {', '.join(ftags)}")
    out("")
  if untagged:
    out("### WARNING: Untagged Notes")
    out("")
    for title, fname in untagged:
      out(f"  * [{title}]({fname})")
    out("")
  out("")

def toTagword(tagpart):
  return tagwordToTitle.get(tagpart, tagpart.title())


def processNote(fname):
  (title, _) = path.splitext(fname)
  tags = set()
  with open(fname, 'rt') as fp:
    state = 'titleSearch'
    for line in fp.readlines():
      if state == 'titleSearch':
        if re.match(r'^#\s*\S+', line):
          title = line[1:].strip()
          state = 'tagSearch'
          continue
        # skip blank lines
        elif not line.strip():
          continue
        # no title in file
        else:
          state = 'tagSearch'
      # I'm using an `if` here b/c then `titleSearch` can fall-through when it transitions to `tagSearch`
      if state == 'titleSearch':
        pass # already processed
      elif state == 'tagSearch':
        # skip blank lines
        if not line.strip():
          continue
        tagRegex = r'[a-z]+(?:-[a-z]+|\d+)*'
        tagsMatch = re.match(r'tags:\s+('+tagRegex+r'(?:\s*,\s+'+tagRegex+r')*)(?:\s*,\s*)?\s*', line)
        # extract tag and tags lines
        if tagsMatch:
          tags |= set(tag.strip() for tag in tagsMatch.group(1).split(","))
        else:
          break
      else:
        raise Exception(f"internal error: unknown state {repr(state)}")
    return title, tags

if __name__ == "__main__":
  main()
