#!/usr/bin/python
import re, os, sys, string

if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
    sys.path.append(os.path.abspath('..'))
    os.environ['DJANGO_SETTINGS_MODULE']='dictionary.settings'

from dictionary.browse.models import KeyWord,Usage

def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

reg = re.compile('G\([\'"][a-zA-Z0-9]*[\'"]\)')
gen = open('../vamdctap/generators.py').readlines()
gen = [reg.findall(l) for l in gen]
gen = flatten(gen)
gen = filter(lambda g: 'LOG(' not in g,gen)
gen = [l[3:-2] for l in gen]

implkws = map(string.lower,gen)
########################
for kw in gen:
    try: k=KeyWord.objects.get(name__iexact=kw)
    except: print 'Not in dictionary: %s'%kw

reg = re.compile('makeDataType\([\'"][a-zA-Z0-9]*[\'"],\s*[\'"][a-zA-Z0-9]*[\'"]')
gen = open('../vamdctap/generators.py').readlines()
gen = [reg.findall(l) for l in gen]
gen = flatten(gen)
gen = [l.split("'")[3] for l in gen]

for kw in gen:
    try: k=KeyWord.objects.get(name__iexact=kw)
    except:
        print 'Not in dictionary: %s'%kw
        continue
    if not k.datatype:
        print 'Not a DataType: %s'%kw

implkws += map(string.lower,gen)
########
returnable = Usage.objects.get(name__iexact='returnable')
for kw in returnable.keyword_set.iterator():
    if kw.name.lower() not in implkws:
        print 'Unimplemented Returnable: %s'%kw
