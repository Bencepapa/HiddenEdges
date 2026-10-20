import json,random,sys
import os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from room import *
def ok_extra(l,sol):
    ids=[it['id'] for it in l['items']]
    for a,b in l.get('apart',[]):
        A=sol[ids.index(a)];B=sol[ids.index(b)]
        if any((x+dx,y+dy) in B for x,y in A for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):return False
    return access_ok(l,sol)
def opts_water(l):
    o=options(l);W=set(map(tuple,l.get('water',[])))
    for i,it in enumerate(l['items']):
        if it.get('water'):o[i]=[cs for cs in o[i] if cs&W]
        elif W:o[i]=[cs for cs in o[i] if not (cs&W)]   # dry pieces keep off the water points
    return o
def count_e(l,cap=200):
    opts=opts_water(l);order=sorted(range(len(opts)),key=lambda i:len(opts[i]));cnt=0;sols=[]
    def rec(k,used,ch):
        nonlocal cnt
        if cnt>=cap:return
        if k==len(order):
            sol=[ch[i] for i in range(len(opts))]
            if ok_extra(l,sol):cnt+=1;sols.append(sol)
            return
        i=order[k]
        for c in opts[i]:
            if used.isdisjoint(c):ch[i]=c;rec(k+1,used|c,ch)
    rec(0,frozenset(),{});return cnt,sols
def start(l,seed):
    rnd=random.Random(seed);bl=blocked(l);W,H=l['W'],l['H'];Wt=set(map(tuple,l.get('water',[])))
    for t in range(200000):
        used=set();pl=[];ok=True;sol=[]
        for it in l['items']:
            r=rnd.randint(0,1);w,h=(it['w'],it['h']) if r==0 else (it['h'],it['w'])
            x=rnd.randint(0,W-w);y=rnd.randint(0,H-h);cs=frozenset((x+i,y+j) for i in range(w) for j in range(h))
            if cs&bl or cs&used or (it['wall'] and not touches_wall(cs,W,H)):ok=False;break
            used|=cs;pl.append([x,y,r]);sol.append(cs)
        if ok and not ok_extra(l,sol):return pl
R=[
 dict(W=6,H=5,windows=[{'side':'S','a':1,'b':2,'dbl':True}],chimney=[5,0],door={'side':'W','a':0,'hinge':'L'},part={'side':'N','a':3},
   apart=[['bed','wardrobe'],['desk','bed']],
   items=[{'id':'bed','name':'ágy','w':2,'h':3,'rule':'---','wall':False},{'id':'wardrobe','name':'szekrény','w':1,'h':2,'rule':'---','wall':True},
          {'id':'desk','name':'íróasztal','w':2,'h':1,'rule':'---','wall':True},{'id':'chair','name':'szék','w':1,'h':1,'rule':'---','wall':False},
          {'id':'shelf','name':'polc','w':1,'h':2,'rule':'---','wall':True},{'id':'plant','name':'növény','w':1,'h':1,'rule':'---','wall':False}]),
 dict(W=7,H=5,windows=[{'side':'S','a':2,'b':4,'dbl':True}],chimney=[0,0],door={'side':'E','a':0,'hinge':'L'},part={'side':'W','a':3},
   apart=[['desk1','desk2'],['printer','desk1'],['printer','desk2']],
   items=[{'id':'desk1','kind':'desk','name':'asztal 1','w':2,'h':1,'rule':'---','wall':True},{'id':'desk2','kind':'desk','name':'asztal 2','w':2,'h':1,'rule':'---','wall':True},
          {'id':'printer','name':'nyomtató','w':1,'h':1,'rule':'---','wall':True},{'id':'meet','name':'tárgyaló','w':2,'h':2,'rule':'---','wall':False},
          {'id':'shelf','name':'polc','w':1,'h':2,'rule':'---','wall':True},{'id':'plant','name':'növény','w':1,'h':1,'rule':'---','wall':False}]),
 dict(W=5,H=4,windows=[{'side':'N','a':1,'b':1}],chimney=None,door={'side':'S','a':1,'hinge':'L'},part={'side':'E','a':2},
   water=[[0,0],[3,0],[4,2]],apart=[['wc','shower']],
   items=[{'id':'wc','name':'WC','w':1,'h':1,'rule':'---','wall':True,'water':True},{'id':'basin','name':'mosdó','w':1,'h':1,'rule':'---','wall':True,'water':True},
          {'id':'shower','name':'zuhany','w':2,'h':2,'rule':'---','wall':True,'water':True},{'id':'cab','name':'szekrény','w':1,'h':2,'rule':'---','wall':True},
          {'id':'laundry','name':'szennyes','w':1,'h':1,'rule':'---','wall':False}]),
]
out=[]
for i,l in enumerate(R):
    if l['chimney'] is None:l['chimney']=[-5,-5]
    c,s=count_e(l,500);print(i,c)
    if c:
        pl=start(l,i+3)
        for it,p in zip(l['items'],pl):it['at']=p
    out.append(l)
json.dump(out,open('rooms.json','w'),ensure_ascii=False)
