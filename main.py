import json,os,urllib.request as u
E=os.environ["MAKEFUN_ENV_URL"]
def P(p,b):
 q=u.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 return json.load(u.urlopen(q))
V=[0,100,320,330,500,900,0]
Q=(5,4,3,2)
J=[-33,-31,-18,-14,14,18,31,33]
K=[-17,-16,-15,-1,1,15,16,17]
D=[-17,-15,15,17]
R=[-16,-1,1,16]
def O(t):return 0<=t<128 and not t&136
B=[0]*128;C=0;Y=-1
def fen(f):
 global C,Y
 a=f.split();B[:]=[0]*128
 for y,w in enumerate(a[0].split('/')):
  x=0
  for c in w:
   if c.isdigit():x+=int(c)
   else:
    p='PNBRQK'.index(c.upper())+1;B[(7-y)*16+x]=p if c.isupper() else -p;x+=1
 C=sum(1<<'KQkq'.index(c)for c in a[2]if c in'KQkq')
 Y=-1 if a[3]=='-' else ord(a[3][0])-97+(int(a[3][1])-1)*16
 return 1-2*(a[1]=='b')
def atk(q,s):
 for d in(-15,-17)if s>0 else(15,17):
  t=q+d
  if O(t)and B[t]==s:return 1
 for d in J+K:
  t=q+d
  if O(t)and B[t]==(2 if d in J else 6)*s:return 1
 for d in D+R:
  t=q+d
  while O(t)and not B[t]:t+=d
  if O(t)and(B[t]==5*s or B[t]==(3 if d in D else 4)*s):return 1
 return 0
def gen(s,cp):
 m=[]
 for i,p in enumerate(B):
  if p*s<1 or i&136:continue
  a=abs(p)
  if a==1:
   d=16*s;t=i+d
   if not B[t]:
    if t//16 in(0,7):m+=[(i,t,q)for q in Q]
    elif not cp:
     m.append((i,t,0))
     if i//16==(1 if s>0 else 6)and not B[i+2*d]:m.append((i,i+2*d,0))
   for t in(i+d-1,i+d+1):
    if O(t)and((B[t]*s<0 and abs(B[t])<6)or t==Y):
     if t//16 in(0,7):m+=[(i,t,q)for q in Q]
     else:m.append((i,t,0))
  else:
   ds=J if a==2 else K if a==6 else D if a==3 else R if a==4 else D+R
   for d in ds:
    t=i+d
    while O(t):
     if B[t]*s>0:break
     if abs(B[t])<6 and(not cp or B[t]):m.append((i,t,0))
     if B[t]or a in(2,6):break
     t+=d
 if not cp:
  for r,f,t,rf,rt in[(1,4,6,7,5),(2,4,2,0,3),(4,116,118,119,117),(8,116,114,112,115)]:
   if C&r and not any(B[x]for x in range(min(f,rf)+1,max(f,rf)))and not any(atk(x,-s)for x in(f,(f+t)//2,t)):m.append((f,t,0))
 return m
def mk(m,s):
 global C,Y
 f,t,p=m;q=B[f];u=[f,t,q,B[t],C,Y,0,0,-1]
 B[f]=0
 if t==Y and abs(q)==1:
  e=t-16*s;u[8]=e;u[3]=B[e];B[e]=0
 B[t]=p*s if p else q
 if abs(q)==6 and abs(t-f)==2:
  rf,rt=(f+3,f+1)if t>f else(f-4,f-1);u[6]=rf;u[7]=rt
  B[rt]=B[rf];B[rf]=0
 for x in(f,t):C&={4:12,116:3,0:13,7:14,112:7,119:11}.get(x,15)
 Y=f+16*s if abs(q)==1 and abs(t-f)==32 else -1
 return u
def un(u):
 global C,Y
 f,t,q,c,C,Y,rf,rt,e=u
 if rt:B[rf]=B[rt];B[rt]=0
 if e>=0:B[e]=c;B[t]=0
 else:B[t]=c
 B[f]=q
def ev(s):
 t=0
 for i,p in enumerate(B):
  if p and not i&136:
   a=abs(p);v=V[a];r=i>>4
   if a==1:v+=(r if p>0 else 7-r)*9
   t+=v if p>0 else -v
 return t*s
T={};N=0;NB=60000
def sr(d,a,b,s,pl):
 global N,Y
 N+=1
 if N>NB:1/0
 if d<=0:
  v=ev(s)
  if v>=b:return b
  a=max(a,v);e=0;k=0
 else:
  k=(tuple(B),s,C,Y);e=T.get(k)
  if e and e[0]>=d and(e[2]==0 or e[1]>=b):return e[1]
  if d>2 and not atk(B.index(6*s),-s):
   q=Y;Y=-1;v=-sr(d-3,-b,-a,-s,pl+1);Y=q
   if v>=b:return b
 ms=gen(s,d<=0);n=0;bm=0;f=2
 ms.sort(key=lambda m:-(9999*(e and m==e[3]or 0)+V[abs(B[m[1]])]))
 for m in ms:
  u=mk(m,s)
  if atk(B.index(6*s),-s):un(u);continue
  n+=1;R=n>3 and not u[3] and d>2;v=-sr(d-1-R,-b,-a,-s,pl+1)
  if v>a and R:v=-sr(d-1,-b,-a,-s,pl+1)
  un(u)
  if v>=b:T[k]=(d,b,1,m);return b
  if v>a:a=v;bm=m;f=0
 if d<=0:return a
 if not n:return -19999+pl if atk(B.index(6*s),-s) else 0
 if f<2:T[k]=(d,a,f,bm)
 return a
def uc(m):
 return chr((m[0]&7)+97)+str((m[0]>>4)+1)+chr((m[1]&7)+97)+str((m[1]>>4)+1)+('nbrq'[m[2]-2]if m[2]else'')
def ch(f,legal):
 global N
 s=fen(f)
 T.clear();L=set(legal);lm=[]
 for m in gen(s,0):
  u=mk(m,s)
  if not atk(B.index(6*s),-s) and uc(m) in L:lm.append(m)
  un(u)
 if not lm:return legal[0]
 bm=lm[0]
 for d in range(1,64):
  try:
   N=0;a=-99999;nb=bm
   for m in lm:
    u=mk(m,s)
    v=-sr(d-1,-99999,-a,-s,1);un(u)
    if v>a:a=v;nb=m
   bm=nb;lm.remove(bm);lm.insert(0,bm)
  except ZeroDivisionError:break
 return uc(bm)
while 1:
 g=P('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=P('/move',{'game':g['game'],'move':ch(g['fen'],g['legal_moves'])})
