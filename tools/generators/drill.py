import itertools,random
def views(H,hgt,N):
    front=[frozenset((hgt[y][x],H[y][x]) for y in range(N) if H[y][x]) for x in range(N)]
    side=[frozenset((hgt[y][x],H[y][x]) for x in range(N) if H[y][x]) for y in range(N)]
    return front,side
def consistent(hgt,N,front,side,cuts,sol):
    # enumerate configs consistent with views (+cuts reveal exact row/col)
    cells=[(x,y) for y in range(N) for x in range(N) if front[x] and side[y] and hgt[y][x]]
    fixed={}
    for t,i in cuts:
        for k in range(N):
            x,y=(k,i) if t=='r' else (i,k)
            fixed[(x,y)]=sol[y][x]
    free=[c for c in cells if c not in fixed]
    opts=[]
    for (x,y) in free:
        o=[0]+[d for d in range(1,hgt[y][x]+1) if (hgt[y][x],d) in front[x] and (hgt[y][x],d) in side[y]]
        opts.append(o)
    n=0;found=[]
    for combo in itertools.product(*opts):
        H=[[0]*N for _ in range(N)]
        for (x,y),v in fixed.items():H[y][x]=v
        for (x,y),v in zip(free,combo):H[y][x]=v
        if views(H,hgt,N)==(front,side):
            n+=1
            if n>1: return n
    return n
