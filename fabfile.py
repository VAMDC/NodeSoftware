"""
This file contains a few helpers for testing, administration
development and deployment. They are to be used with *fabric*,
see http://fabfile.org.

For setting up your VAMDC node, you need not care about this file.
"""

from fabric.api import *

env.roledefs = {\
    'balin':['balin.tmy.se'],
    'melkor':['melkor.astro.uu.se'],
    }

@roles('balin','melkor')
def pullall():
    wdir = 'py/vamdc/'
    with cd(wdir):
        run("git pull")

def cp(vamdc=False):
    "commit and push"
    local('git add -p && git commit')
    local('git push origin master')
    if vamdc: local('git push vamdc master')
