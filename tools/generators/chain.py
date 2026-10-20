import itertools, random
G=["..##..",
   ".####.",
   "##..##",
   "######",
   "#.##.#",
   "#.##.#"]
N=6
g=[[1 if c=='#' else 0 for c in r] for r in G]
def runs(line):
    out=[];cur=line[0];n=0
    for v in line:
        if v==cur:n+=1
        else: out.append((cur,n));cur=v;n=1
    out.append((cur,n));return out   # list of (type,len)
rows=[runs(r) for r in g]; cols=[runs([g[y][x] for y in range(N)]) for x in range(N)]
def patterns(struct,hidden):
    # struct: list of (type,len); hidden: set of indices with unknown len
    k=len(struct);res=[]
    ranges=[]
    for i,(t,l) in enumerate(struct):
        ranges.append(range(1,N+1) if i in hidden else [l])
    for combo in itertools.product(*ranges):
        if sum(combo)!=N: continue
        line=[]
        for (t,_),l in zip(struct,combo): line+= [t]*l
        res.append(tuple(line))
    return res
def count(hr,hc,limit=2):
    rp=[patterns(rows[i],hr[i]) for i in range(N)]
    cp=[set(patterns(cols[i],hc[i])) for i in range(N)]
    cpre=[set(p[:k] for p in cp[i] for k in range(N+1)) for i in range(N)]
    sol=[0]
    def dfs(y,acc):
        if sol[0]>=limit:return
        if y==N:
            if all(tuple(a[x] for a in acc) in cp[x] for x in range(N)): sol[0]+=1
            return
        for p in rp[y]:
            ok=all(tuple([a[x] for a in acc]+[p[x]]) in cpre[x] for x in range(N))
            if ok: dfs(y+1,acc+[p])
    dfs(0,[]);return sol[0]
random.seed(4)
hr=[set() for _ in range(N)];hc=[set() for _ in range(N)]
cands=[('r',i,j) for i in range(N) for j in range(len(rows[i]))]+[('c',i,j) for i in range(N) for j in range(len(cols[i]))]
random.shuffle(cands)
for t,i,j in cands:
    (hr if t=='r' else hc)[i].add(j)
    if count(hr,hc)!=1: (hr if t=='r' else hc)[i].discard(j)
print('hidden',sum(map(len,hr))+sum(map(len,hc)),'of',sum(map(len,rows))+sum(map(len,cols)))
import json
def enc(structs,hid): return [[[t,(None if j in hid[i] else l)] for j,(t,l) in enumerate(s)] for i,s in enumerate(structs)]
print(json.dumps({'rows':enc(rows,hr),'cols':enc(cols,hc)}))
print(count(hr,hc,5))
