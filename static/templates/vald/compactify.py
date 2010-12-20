#!/usr/bin/env python

from sys import stdin,stdout

for l in stdin:
    stdout.write(l[:-1])
stdout.write('\n')
