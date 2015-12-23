#!/usr/bin/env python
import hashlib
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--directory", help="")
options = parser.parse_args()

SAME_SIZE = {}
SAME_HASH = {}

def hashmd5(filename):
  f = open(filename)
  filehash = hashlib.md5()
  while True:
    data = f.read(1024*1024)
    if not data: break
    filehash.update(data)
  return filehash.hexdigest()

#find same length files
print "Finding files of same size..."
for root, dirs, files in os.walk(options.directory):
  for name in files:
    full_path = os.path.join(root, name)
    try:
      size = os.path.getsize(full_path)
    except:
      continue
    if size==0: continue
    if size not in SAME_SIZE:
      SAME_SIZE[size] = []

    SAME_SIZE[size].append(full_path)

#find hashes
print "Calculating hashes for those files..."
for size in SAME_SIZE:
  if len(SAME_SIZE[size]) < 2: continue
  for filename in SAME_SIZE[size]:
    filehash = hashmd5(filename)
    if filehash not in SAME_HASH:
      SAME_HASH[filehash] = []
    SAME_HASH[filehash].append(filename)

print "Outputing results..."
for filehash in SAME_HASH:
  if len(SAME_HASH[filehash]) < 2: continue
  for filename in SAME_HASH[filehash]:
    print filehash,filename
  print ""