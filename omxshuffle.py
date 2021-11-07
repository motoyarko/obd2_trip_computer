import argparse
import random
import os
from glob import glob

parser = argparse.ArgumentParser()

parser.add_argument('--shuffle', '-s', action='store_true', default=False)
args = parser.parse_args()


# extract mp3 files from current folder
files = glob('*.mp3')

if args.shuffle:
  random.shuffle(files)


# play each file in omxplayer:
for f in files:
  try:
    os.system('omxplayer -o local "%s"' % f)
  except KeyboardInterrupt:
    # exit on ctrl+c (does not work, as ctrl+c is captured by omxplayer...)
    exit()
