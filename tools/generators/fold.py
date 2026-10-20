import itertools, random, json
import numpy as np
def fold(net):
    R=len(net);C=len(net[0]);cells={}
    start=next((x,y) for y in range(R) for x in range(C) if net[y][x]!='.')
    q=[(start,{'n':np.array([0,0,1]),'u':np.array([1,0,0]),'v':np.array([0,1,0])})];cells[start]=q[0][1]
    while q:
        (x,y),f=q.pop(0)
        for dx,dy,g in [(1,0,{'n':f['u'],'u':-f['n'],'v':f['v']}),(-1,0,{'n':-f['u'],'u':f['n'],'v':f['v']}),(0,1,{'n':f['v'],'u':f['u'],'v':-f['n']}),(0,-1,{'n':-f['v'],'u':f['u'],'v':f['n']})]:
            X,Y=x+dx,y+dy
            if 0<=X<C and 0<=Y<R and net[Y][X]!='.' and (X,Y) not in cells:
                cells[(X,Y)]=g;q.append(((X,Y),g))
    return cells
# 24 rotations
def rots():
    out=[]
    for p in itertools.permutations(range(3)):
        for s in itertools.product([1,-1],repeat=3):
            M=np.zeros((3,3),int)
            for i in range(3):M[i,p[i]]=s[i]
            if round(np.linalg.det(M))==1:out.append(M)
    return out
ROT=rots()
SYMMETRIC={'disc','ring','sq','osq','x','plus'}
def up_vec(f,r):  # local up is -v; rotate basis r times: (u,v)->(v,-u)
    u,v=f['u'],f['v']
    for _ in range(r):u,v=v,-u
    return -v
VIEW=[np.array([0,0,1]),np.array([1,0,0]),np.array([0,1,0])]
def analyse(net,spec):
    cells=fold(net)
    data={c:(spec[c][0],up_vec(f,spec[c][1]),f['n']) for c,f in cells.items()}
    groups={}
    for mi,M in enumerate(ROT):
        vis=[];key=[]
        for vn in VIEW:
            c=next(c for c,(s,u,n) in data.items() if tuple(M@n)==tuple(vn))
            s,u,n=data[c];vis.append(c);key.append((s,None if s in SYMMETRIC else tuple(M@u)))
        groups.setdefault(tuple(key),set()).add(frozenset(vis))
    return cells,groups
def search(net,pool,seed,want_min_rep=2):
    random.seed(seed)
    cellsl=[(x,y) for y in range(len(net)) for x in range(len(net[0])) if net[y][x]!='.']
    best=None
    for it in range(4000):
        spec={c:(random.choice(pool),random.randrange(4)) for c in cellsl}
        names=[s for s,_ in spec.values()]
        if any(names.count(s)<want_min_rep for s in names):continue
        cells,groups=analyse(net,spec)
        uniq=[(k,v) for k,v in groups.items() if len(v)==1]
        # choose a view whose three symbols each appear >=2 times, unique set
        for k,v in uniq:
            return spec,k,list(v)[0],len(groups)
    return None
net1=[".A..","BCDE",".F.."]
net2=["AB..",".CD.","..EF"]
for net,pool,seed in [(net1,['arrow','tri'],1),(net2,['arrow','tri','disc'],5)]:
    r=search(net,pool,seed)
    spec,key,vis,ng=r
    print(json.dumps({'net':net,'spec':{f"{x},{y}":v for (x,y),v in spec.items()},'vis':[list(c) for c in vis],'key':str(key)}))
