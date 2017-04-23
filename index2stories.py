#!/usr/bin/env python

import os
import re
import sys
import getopt
import random
import copy
from bs4 import BeautifulSoup
import re
#import html

def cleanhtml(raw_html):
  text = BeautifulSoup(raw_html[13:-2], "html.parser").get_text().encode('utf-8').strip()
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  cleantext = re.sub('"', '', cleantext)
  cleantext = re.sub('~', '', cleantext)
  #cleantext = html.unescape(cleantext)
  return cleantext

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def usage():
  print >> sys.stderr, "usage: index2stories.py index-file base-spinn3r-directory"
  print >> sys.stderr, "\tCreates a new Spinn3r xml file that only consists of the stories specified in the index-file\n"
  print >> sys.stderr, "\t%-2s %-10s %-s" % ("-h", "--help", "print this help message")

def read_index(index_path):
  tiergroups = dict()
  index_file = open(index_path)

  for line in index_file:
    (path, confidence, start, stop) = line.split()
    stories = tiergroups.get(path, [])
    stories.append((int(start), int(stop), confidence))
    tiergroups[path] = stories

  return tiergroups

def run(index_path, spinn3r_dirpath):
  tiergroups = read_index(index_path)

  paths = tiergroups.keys()
  paths.sort()

  print("text,score")

  for path in paths:
    absolute_path = os.path.join(spinn3r_dirpath, path)

    if os.path.exists(absolute_path):
      f = open(absolute_path)

      line_number = 0
      for (begin, end, confidence) in tiergroups[path]:
        while line_number < begin - 1:
          line = f.readline()
          if line == None: break
          line_number = line_number + 1
        while line_number <= end:
          line = f.readline()
          if line == None: break
          line_number = line_number + 1
          if line.find('<description>') == 0:
            text = cleanhtml(line)
            if len(text) > 20:
              print '"' + text + '",' + confidence

      f.close()

def main(argv=None):
  if argv == None: argv = sys.argv

  try:
    # Get options
    try:
      opts, args = getopt.gnu_getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
      raise Usage(msg)

    # Process options
    for option, value in opts:
      if option in ("-h", "--help"):
        usage()
        return 0

    if len(args) != 2: raise Usage("Wrong number of arguments")

    run(args[0], args[1])

  except Usage, err:
    print >> sys.stderr, err.msg
    usage()
    return 2

  return 0

if __name__ == "__main__":
    sys.exit(main())
