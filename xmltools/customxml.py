import vamdc.db.tools as t

metatab='meta'
cname='cname'
tname='tname'
ccom='ccom'
cunit='cunit'
cfmt='cfmt'

cols='%s,%s,%s,%s,%s'%(cname,tname,ccom,cunit,cfmt)
colsl=cols.split(',')
colst=tuple(colsl)

def run(curs):
    ll=t.cols2lists(curs,metatab,colsl)
    exec('%s=ll'%cols)
    for i,col in enumerate(cname):
        pass

    
    
