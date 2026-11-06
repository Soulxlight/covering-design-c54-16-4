"""Exact weighted NAE model of exclusive-row a/b point switches."""
import itertools,collections

def read_rows(path):
 return [frozenset(int(x)-1 for x in line.split()) for line in open(path) if line.strip() and not line.lstrip().startswith('#')]
def missing(rows,v):
 cols=[sum(1<<i for i,row in enumerate(rows) if x in row) for x in range(v)]
 return [q for q in itertools.combinations(range(v),4) if not(cols[q[0]]&cols[q[1]]&cols[q[2]]&cols[q[3]])]
def build(rows,v,a,b,holes=None):
 if holes is None:holes=missing(rows,v)
 cols=[sum(1<<i for i,row in enumerate(rows) if x in row) for x in range(v)]
 both=cols[a]&cols[b];exclusive=cols[a]^cols[b]
 ids=[i for i in range(len(rows)) if exclusive>>i&1];variable={row:j+1 for j,row in enumerate(ids)}
 groups=collections.Counter();empty=single=0
 for q in itertools.combinations([x for x in range(v) if x not in (a,b)],3):
  support=cols[q[0]]&cols[q[1]]&cols[q[2]]
  if support&both:continue
  support&=exclusive
  if not support:empty+=1;continue
  if support&(support-1)==0:single+=1;continue
  vs=[]
  while support:
   bit=support&-support;vs.append(variable[bit.bit_length()-1]);support-=bit
  groups[tuple(vs)]+=1
 invariant=sum(len(set(q)&{a,b})!=1 for q in holes)
 assignment={variable[i]:int(a in rows[i]) for i in ids}
 fixed=invariant+2*empty+single
 current=fixed+sum(w for vs,w in groups.items() if len({assignment[x] for x in vs})==1)
 if current!=len(holes):raise RuntimeError('Original point-pair deficit mismatch')
 return {'a':a,'b':b,'variable_rows':ids,'groups':dict(groups),'fixed':fixed,'empty':empty,'singleton':single,'invariant':invariant,'original_assignment':assignment,'current_holes':current}
def reconstruct(rows,model,assignment):
 result=list(rows);a,b=model['a'],model['b']
 for variable,i in enumerate(model['variable_rows'],1):result[i]=frozenset((set(rows[i])-{a,b})|{a if assignment[variable] else b})
 return result

def score(model,assignment):return model['fixed']+sum(w for vs,w in model['groups'].items() if len({assignment[x] for x in vs})==1)

class Parity:
 def __init__(self,n):self.p=list(range(n+1));self.x=[0]*(n+1)
 def find(self,a):
  if self.p[a]!=a:
   root,x=self.find(self.p[a]);self.x[a]^=x;self.p[a]=root
  return self.p[a],self.x[a]
 def join(self,a,b,xor):
  ra,pa=self.find(a);rb,pb=self.find(b)
  if ra==rb:return (pa^pb)==xor
  self.p[ra]=rb;self.x[ra]=pa^pb^xor;return True

def reduce(model,target):
 """Sound threshold-specific parity contraction; never assumes optional edges hard."""
 n=len(model['variable_rows']);d=Parity(n);base=model['fixed'];merges=0
 while True:
  fixed=base;groups=collections.Counter()
  for vs,w in model['groups'].items():
   lits=set()
   for var in vs:
    root,par=d.find(var);lits.add(root if par==0 else -root)
   if any(-x in lits for x in lits):continue
   if len(lits)==1:fixed+=w;continue
   # NAE is invariant under complementing every literal.
   key=tuple(sorted(lits));neg=tuple(sorted(-x for x in lits));groups[min(key,neg)]+=w
  budget=target-fixed
  if budget<0:return {'infeasible':True,'reason':'fixed deficit after parity contraction exceeds target','fixed':fixed,'parity':d,'merges':merges}
  changed=False
  for lits,w in groups.items():
   if len(lits)==2 and w>budget:
    a,b=lits;ra,_=d.find(abs(a));rb,_=d.find(abs(b))
    if ra!=rb:
     if not d.join(abs(a),abs(b),1^(a<0)^(b<0)):raise RuntimeError('Contradictory parity merge')
     merges+=1;changed=True
  if not changed:return {'infeasible':False,'fixed':fixed,'budget':budget,'groups':dict(groups),'parity':d,'merges':merges}
