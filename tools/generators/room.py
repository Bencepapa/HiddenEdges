import itertools,sys
SUNS={'M':((-1,-1),3.2),'N':((0,-1),2.2),'A':((1,-1),3.2)}
def lit(l,k,cx,cy):
    (dx,dy),depth=SUNS[k];W,H=l['W'],l['H'];px,py=cx+.5,cy+.5
    for w in l['windows']:
        s=w['side']
        if s=='S':
            if dy>=0:continue
            t=(H-py)/-dy;al=px+dx*-t
        elif s=='N':
            if dy<=0:continue
            t=py/dy;al=px-dx*t
        elif s=='E':
            if dx>=0:continue
            t=(W-px)/-dx;al=py+dy*-t
        else:
            if dx<=0:continue
            t=px/dx;al=py-dy*t
        if 0<t<=depth and w['a']<=al<=w['b']+1:return True
    return False
def blocked(l):
    b=set();b.add(tuple(l['chimney']));d=l['door'];a=d['a'];W,H=l['W'],l['H']
    c={'N':[(a,0),(a+1,0),(a,1),(a+1,1)],'S':[(a,H-1),(a+1,H-1),(a,H-2),(a+1,H-2)],'W':[(0,a),(0,a+1),(1,a),(1,a+1)],'E':[(W-1,a),(W-1,a+1),(W-2,a),(W-2,a+1)]}[d['side']]
    return b|set(c)
def show(l):
    for k in 'MNA':
        print(k);[print(''.join('#' if lit(l,k,x,y) else '.' for x in range(l['W']))) for y in range(l['H'])]
def solve(l,verbose=True):
    bl=blocked(l);W,H=l['W'],l['H'];opts=[]
    for it in l['items']:
        o=[]
        for r in (0,1):
            w,h=(it['w'],it['h']) if r==0 else (it['h'],it['w'])
            if r==1 and w==h:continue
            for x in range(W-w+1):
                for y in range(H-h+1):
                    cs=[(x+i,y+j) for i in range(w) for j in range(h)]
                    if any(c in bl for c in cs):continue
                    ok=True
                    for kk,k in enumerate('MNA'):
                        n=sum(lit(l,k,*c) for c in cs);rr=it['rule'][kk]
                        if rr=='L' and n*2<len(cs):ok=False
                        if rr=='D' and n:ok=False
                    if ok:o.append(frozenset(cs))
        opts.append(o)
        if verbose:print(it['id'],len(o))
    cnt=0
    for combo in itertools.product(*opts):
        u=set()
        if sum(len(c) for c in combo)==len(frozenset().union(*combo)):cnt+=1
    return cnt

def touches_wall(cs,W,H):
    return any(x==0 or y==0 or x==W-1 or y==H-1 for x,y in cs)
def options(l):
    bl=blocked(l);W,H=l['W'],l['H'];opts=[]
    for it in l['items']:
        o=[]
        for r in (0,1):
            w,h=(it['w'],it['h']) if r==0 else (it['h'],it['w'])
            if r==1 and w==h:continue
            for x in range(W-w+1):
                for y in range(H-h+1):
                    cs=[(x+i,y+j) for i in range(w) for j in range(h)]
                    if any(c in bl for c in cs):continue
                    if it.get('wall') and not touches_wall(cs,W,H):continue
                    ok=True
                    for kk,k in enumerate('MNA'):
                        n=sum(lit(l,k,*c) for c in cs);rr=it['rule'][kk]
                        if rr=='L' and n*2<len(cs):ok=False
                        if rr=='D' and n:ok=False
                    if ok:o.append(frozenset(cs))
        opts.append(o)
    return opts
def count(l,cap=10**6):
    opts=options(l);opts_i=sorted(range(len(opts)),key=lambda i:len(opts[i]));cnt=0;sols=[]
    def rec(k,used,ch):
        nonlocal cnt
        if cnt>cap:return
        if k==len(opts_i):cnt+=1;sols.append(dict(ch));return
        i=opts_i[k]
        for c in opts[i]:
            if used.isdisjoint(c):ch[i]=c;rec(k+1,used|c,ch)
    rec(0,frozenset(),{})
    return cnt,sols

def access_ok(l,sol_cells):
    W,H=l['W'],l['H'];occ=set().union(*sol_cells);ch=tuple(l['chimney'])
    door=blocked({**l,'chimney':[-9,-9]})
    seen=set(door);st=list(door)
    while st:
        x,y=st.pop()
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(x+d[0],y+d[1])
            if 0<=q[0]<W and 0<=q[1]<H and q not in occ and q!=ch and q not in seen:seen.add(q);st.append(q)
    for cs in sol_cells:
        if not any((x+dx,y+dy) in seen for x,y in cs for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):return False
    return True
def apart(l,sol):
    ids=[it['id'] for it in l['items']]
    if 'table' not in ids:return True
    t=sol[ids.index('table')]
    for o in ('sink','stove'):
        if o in ids:
            c=sol[ids.index(o)]
            if any((x+dx,y+dy) in c for x,y in t for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):return False
    return True
def count2(l,cap=10**6):
    opts=options(l);order=sorted(range(len(opts)),key=lambda i:len(opts[i]));cnt=0;sols=[]
    def rec(k,used,ch):
        nonlocal cnt
        if cnt>cap:return
        if k==len(order):
            sol=[ch[i] for i in range(len(opts))]
            if apart(l,sol) and access_ok(l,sol):cnt+=1;sols.append(sol)
            return
        i=order[k]
        for c in opts[i]:
            if used.isdisjoint(c):ch[i]=c;rec(k+1,used|c,ch)
    rec(0,frozenset(),{})
    return cnt,sols

def sees(l,sol):
    ids=[it['id'] for it in l['items']]
    if 'tv' not in ids or 'sofa' not in ids:return True
    tv=sol[ids.index('tv')];so=sol[ids.index('sofa')];occ=set().union(*sol)|{tuple(l['chimney'])}
    tvh=len({y for _,y in tv})==1  # horizontal tv: look along columns
    for (tx,ty) in tv:
        for (sx,sy) in so:
            if tvh and sx==tx and abs(sy-ty)>=2:
                a,b=sorted((sy,ty));
                if all((tx,y) not in occ for y in range(a+1,b)):return True
            if not tvh and sy==ty and abs(sx-tx)>=2:
                a,b=sorted((sx,tx))
                if all((x,ty) not in occ for x in range(a+1,b)):return True
    return False
def free_ok(l,sol):
    for i,it in enumerate(l['items']):
        if not it.get('free'):continue
        others=set().union(*[c for j,c in enumerate(sol) if j!=i])
        if any((x+dx,y+dy) in others for x,y in sol[i] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):return False
    return True
def count3(l,cap=10**6):
    opts=options(l);order=sorted(range(len(opts)),key=lambda i:len(opts[i]));cnt=0;sols=[]
    def rec(k,used,ch):
        nonlocal cnt
        if cnt>cap:return
        if k==len(order):
            sol=[ch[i] for i in range(len(opts))]
            if apart(l,sol) and free_ok(l,sol) and sees(l,sol) and access_ok(l,sol):cnt+=1;sols.append(sol)
            return
        i=order[k]
        for c in opts[i]:
            if used.isdisjoint(c):ch[i]=c;rec(k+1,used|c,ch)
    rec(0,frozenset(),{})
    return cnt,sols
