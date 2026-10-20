import itertools,random,json
def vis(seq):
    m=0;c=0
    for v in seq:
        if v>m:m=v;c+=1
    return c
def clues(g):
    N=len(g);cols=[[g[y][x] for y in range(N)] for x in range(N)]
    return {'top':[vis(c) for c in cols],'bottom':[vis(c[::-1]) for c in cols],'left':[vis(r) for r in g],'right':[vis(r[::-1]) for r in g]}
def latins(N):
    perms=list(itertools.permutations(range(1,N+1)))
    out=[]
    def rec(rows):
        if len(rows)==N:out.append([list(r) for r in rows]);return
        for p in perms:
            if all(p[i]!=r[i] for r in rows for i in range(N)):rec(rows+[p])
    rec([]);return out
def solutions(N,cl,L):
    res=[]
    for g in L:
        c=clues(g)
        if all(cl[s][i] is None or cl[s][i]==c[s][i] for s in cl for i in range(N)):res.append(g)
    return res
random.seed(4)
out=[]
for N,keep in ((3,None),(4,None),(4,None)):
    L=latins(N)
    while True:
        g=random.choice(L);c=clues(g)
        # drop clues greedily while unique
        cl={s:list(v) for s,v in c.items()}
        slots=[(s,i) for s in cl for i in range(N)];random.shuffle(slots)
        for s,i in slots:
            v=cl[s][i];cl[s][i]=None
            if len(solutions(N,cl,L))!=1:cl[s][i]=v
        n=sum(v is not None for s in cl for v in cl[s])
        if (N==3 and n<=6) or (N==4 and n<=8):break
    out.append({'N':N,'sol':g,'clues':cl,'n':n})
    print(N,n,g,cl)
json.dump(out,open('sky.json','w'))
