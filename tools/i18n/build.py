import json,re,sys
import os
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
sys.path.insert(0,HERE);from en import EN,CTX_EXTRA
from de import DE
from it import IT
from easy_tr import NEW,CTX_NEW
for k,(e,d,i) in NEW.items():
    EN.setdefault(k,e);DE.setdefault(k,d);IT.setdefault(k,i)
CTX_EXTRA.update(CTX_NEW)
from review_fix import EN_FIX,DE_FIX,IT_FIX
for D_,F_ in ((EN,EN_FIX),(DE,DE_FIX),(IT,IT_FIX)):
    for k,v in F_.items():
        assert k in EN,k
        D_[k]=v
cap=json.load(open(os.path.join(HERE,'capture.json')))
p=os.path.join(ROOT,'index.html');s=open(p).read()
# role notes from the level table
roles={}
for m in re.finditer(r"name:'([^']+)',sub:'([^']+)',rev:'([^']+)'",s):
    n,sub,rev=m.groups()
    roles.setdefault(n,f"Level title (header and contents list), level “{n}”.")
    roles[sub]=f"Level subtitle / riddle hint under the title, level “{n}”."
    roles[rev]=f"Revision note at the bottom of every sheet: the instruction of level “{n}”. Keep the ‘REV. X —’ prefix."
for m in re.finditer(r'"name": "([^"]+)"',s):roles.setdefault(m.group(1),"Furniture name on the floor plan and in the requirements table of the room puzzles. Keep it short (fits one grid cell).")
def ctx(k):
    if k in CTX_EXTRA:return CTX_EXTRA[k]
    if k in roles:return roles[k]
    w=cap.get(k) or cap.get(k.upper()) or []
    w=sorted(set(re.sub(r' – solved','',x) for x in w))
    if not w:return "Shown in game (dynamic state)."
    more=f" (+{len(w)-2} more)" if len(w)>2 else ""
    return "Appears on: "+"; ".join(w[:2])+more+"."
entries=[{"hu":k,"ctx":ctx(k),"en":v,"de":DE.get(k,""),"it":IT.get(k,"")} for k,v in EN.items()]
doc={"_about":"Takart élek / Hidden Edges – UI text. 'hu' is the source text and the lookup key. Placeholders in {braces} must be kept. 'ctx' says where the text appears. Leave a language empty to fall back to Hungarian.",
     "languages":{"hu":"Magyar","en":"English","de":"Deutsch","it":"Italiano"},"entries":entries}
js=json.dumps(doc,ensure_ascii=False,indent=1)
open(os.path.join(ROOT,'i18n','takart-elek-lang.json'),'w').write(js)
blk='<script type="application/json" id="i18n">\n'+js.replace('</','<\\/')+'\n</script>\n'
if 'id="i18n"' in s:
    s=re.sub(r'<script type="application/json" id="i18n">.*?</script>\n',lambda m:blk,s,flags=re.S)
else:
    i=s.index('<script>');s=s[:i]+blk+s[i:]
open(p,'w').write(s)
print(len(entries))
