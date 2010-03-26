#!/usr/bin/env python

from vamdc.tap import *

class MyThread ( threading.Thread ):
    def run ( self ):
        tap=TAP()
        tap.run()
#        print tap


if __name__=='__main__': 
    for i in xrange(1):
        MyThread().start()

