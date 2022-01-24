def fetch_datatype(cur):
    types = []
    for item in cur.description:
        if item[1] == 3:
            types.append('int')
        elif item[1] == 5:
            types.append('double')
        elif item[1] == 253:
            types.append('varchar')
        else:
            types.append('unknown')
    return types

def fetch_header(cur):
    return [item[0] for item in cur.description]

def fetch_EDA(cur, fname, col, names = ['max', 'min', 'mean', 'median', 'std', 'nNULLs', 'card']):
    res = []
    for name in names:
        if name == 'max':
            cur.execute('SELECT MAX(%s) FROM %s WHERE %s IS NOT NULL' %(col, fname, col))
        if name == 'min':
            cur.execute('SELECT MIN(%s) FROM %s WHERE %s IS NOT NULL' %(col, fname, col))
        if name == 'mean':
            cur.execute('SELECT AVG(%s) FROM %s WHERE %s IS NOT NULL' %(col, fname, col))
        if name == 'median':
            cur.execute('SELECT x.%s from %s x, %s y \
                    GROUP BY x.%s \
                    HAVING SUM(SIGN(1-SIGN(y.%s-x.%s)))/COUNT(*) > .5 \
                    LIMIT 1' %(col, fname, fname, col, col, col))
        if name == 'std':
            cur.execute('SELECT STD(%s) FROM %s WHERE %s IS NOT NULL' %(col, fname, col))
        if name == 'nNULLs':
            cur.execute('SELECT COUNT(IFNULL(%s, 1)) FROM %s WHERE %s IS NULL' %(col, fname, col))
        if name == 'card':
            cur.execute('SELECT COUNT(DISTINCT(%s)) FROM %s' %(col, fname))
            
        tempVal = cur.fetchall()[0][0]
        if name in ['mean', 'median', 'std']: tempVal = float(tempVal)
        res.append(tempVal)
    return res

def fetch_corr(cur, fname, col1, col2):
    cur.execute('SELECT (Count(*)*Sum(d.%s*d.%s)-Sum(d.%s)*Sum(d.%s)) / \
         (sqrt(Count(*)*Sum(d.%s*d.%s)-Sum(d.%s)*Sum(d.%s)) * \
          sqrt(Count(*)*Sum(d.%s*d.%s)-Sum(d.%s)*Sum(d.%s))) AS TotalCorelation \
          FROM %s d' %(col1, col2, col1, col2, col1, col1, col1, col1, col2, col2, col2, col2, fname))
    return cur.fetchall()[0][0]