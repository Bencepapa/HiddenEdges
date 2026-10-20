import random,json,itertools
FULL=[0,1,2,3]
def cells(lst):return frozenset((x,y,q) for x,y in lst for q in FULL)
TET={'I':cells([(0,0),(1,0),(2,0),(3,0)]),'O':cells([(0,0),(1,0),(0,1),(1,1)]),'T':cells([(0,0),(1,0),(2,0),(1,1)]),
     'L':cells([(0,0),(0,1),(0,2),(1,2)]),'J':cells([(1,0),(1,1),(1,2),(0,2)]),'S':cells([(1,0),(2,0),(0,1),(1,1)]),'Z':cells([(0,0),(1,0),(1,1),(2,1)])}
TAN={'sq':cells([(0,0)]),'rect':cells([(0,0),(1,0)]),'tri':frozenset({(0,0,2),(0,0,3)}),
     'big':frozenset({(0,1,0),(0,1,1),(0,1,2),(0,1,3),(0,0,2),(0,0,3),(1,1,2),(1,1,3)}),
     'mid':frozenset({(0,0,2),(0,0,3),(1,0,2),(1,0,1)})}  # mid: triangle with hypotenuse along the top: base 2 cells, height 1 cell
def norm(p):
    mx=min(x for x,y,q in p);my=min(y for x,y,q in p);return frozenset((x-mx,y-my,q) for x,y,q in p)
def rot(p):return norm(frozenset((-y-1,x,(q+1)%4) for x,y,q in p))
def rots(p):
    out=[];r=norm(p)
    for _ in range(4):
        if r not in out:out.append(r)
        r=rot(r)
    return out
def shift(p,dx,dy):return frozenset((x+dx,y+dy,q) for x,y,q in p)
def nb(u):
    x,y,q=u;res=[(x,y,(q+1)%4),(x,y,(q+3)%4)]
    res.append({0:(x,y-1,2),1:(x+1,y,3),2:(x,y+1,0),3:(x-1,y,1)}[q]);return res
def build(names,lib,trials=4000,seed=0):
    rnd=random.Random(seed);best=None
    for t in range(trials):
        placed=[];U=set()
        for n in names:
            opts=[]
            for r_i,r in enumerate(rots(lib[n])):
                if not U:opts.append((0,0,r_i,r));continue
                for dx in range(-4,9):
                    for dy in range(-4,9):
                        s=shift(r,dx,dy)
                        if s&U:continue
                        if any(v in U for u in s for v in nb(u)):opts.append((dx,dy,r_i,s))
            if not opts:break
            o=rnd.choice(opts)
            s=o[3] if U else o[3];placed.append((n,o[2],o[0],o[1]));U|=s
        if len(placed)<len(names):continue
        xs=[x for x,y,q in U];ys=[y for x,y,q in U]
        # score: perimeter (boundary unit edges) + bbox area
        per=sum(1 for u in U for v in nb(u) if v not in U)
        sc=per*1.0+(max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)*.6
        if best is None or sc<best[0]:best=(sc,placed,U)
    return best
def count(U,names,lib,cap=50):
    U=frozenset(U);names=sorted(names);cnt=0
    def rec(rem,left):
        nonlocal cnt
        if cnt>=cap:return
        if not rem:
            if not left:cnt+=1
            return
        u=min(rem)
        tried=set()
        for i,n in enumerate(left):
            if n in tried:continue
            tried.add(n)
            for r in rots(lib[n]):
                for a in r:
                    s=shift(r,u[0]-a[0],u[1]-a[1])
                    if u in s and s<=rem:rec(rem-s,left[:i]+left[i+1:])
    rec(U,names);return cnt
