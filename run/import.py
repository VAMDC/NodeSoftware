#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from vamdc.imptools import *

def main():
    if len(sys.argv) < 2:
        print "need more arguments"
        return

    if sys.argv[1]=='dummy':
        pass # not implemented right now
    
    elif sys.argv[1]=='vald':
        config=vald3cfg
        
    else:
        config=readcfg(sys.argv[1])
        

    do_all(config)

if __name__ == '__main__':
    main()



