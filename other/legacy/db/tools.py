from string import join

def cols2lists(curs,tab,cols=None):
    if cols:
        curs.execute('SELECT %s FROM %s'%(join(cols,','),tab))
    else:
        curs.execute('SELECT * FROM %s'%tab)
    
    data=curs.fetchall()
    ll=[]
    for i in xrange(len(data[0])): ll.append([])
    for row in data:
        for i in xrange(len(ll)): ll[i].append(row[i])
    return tuple(ll)
        
