#!/usr/bin/env python

from vamdc.server import tap as t

class MyThread ( t.threading.Thread ):
    def run ( self ):
        tap=t.TAP()
        tap.run()
#        print tap


if __name__=='__main__': 
    for i in xrange(1):
        MyThread().start()

