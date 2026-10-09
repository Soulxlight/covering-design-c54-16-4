# Complete case211 occurrence map and certification scope

This is a necessary map for any complete C(54,16,4) covering with exactly223
legal block occurrences whose degree multiset is66^51,67^2,68^1. Whole blocks may
repeat, but each occurrence contains16 distinct points. Padding a smaller
nonempty covering to223 preserves coverage and reviewed floors, but does
not guarantee this degree partition. This case is not the whole problem.

## Floors and the four-excess partition

The internally reviewed child theorem C(53,15,3)>=66 applies to repeated
occurrences. Removing a point from its containing blocks covers all triples
on the other53 points, hence r_x>=66. For223 occurrences the incidence sum
is3568 and sum(r_x-66)=4. Fix partition2+1+1:51 normal points r=66, point
A with r=68, and distinct points B,C with r=67. The first intersection
moment is51*C(66,2)+2*C(67,2)+C(68,2)=116095, distinct from earlier cases.

The pair floor18 is independent of this point partition. The link of a fixed
pair is a(52,14,2) cover. Every link point has degree at least4. If b link
occurrences and a degree-four points exist, a>=260-14b. Each degree-four
point sees51 other points in52 incidences, with one codegree-two partner.
On tight points the incidence Gram matrix is3I+matching+J, positive definite:
its form is2*sum u_i^2+sum_isolated u_i^2+sum_edges(u_i+u_j)^2+(sum u_i)^2.
Thus a<=b, giving b>=18; a=0 gives b>=19 directly. Repeated incidence columns
do not affect rank<=b. Triple links give degree>=ceil(51/13)=4 and quadruples
have degree>=1. The reviewed child66 is a premise, not re-proved here.

For actual pairs define e_xy=lambda_xy-18>=0. Summing15 pairs through every
containing occurrence gives S_x=sum_y e_xy=15*r_x-53*18. Hence S=36 for
normals,66 at A,51 at B and C; total edge excess is1002. Every pair except
the three within ABC has a normal endpoint and e<=36. The BC pair has
e<=min(51,51,67-18)=49; AB and AC have e<=min(66,51,67-18)=49.
Classes(0,0),(0,1),(0,2),(1,1),(1,2) have respective populations
C(51,2)=1275,102,51,1,2. There is no(2,2) pair, as A is unique. These are
necessary domains; no attainable endpoint is claimed.

If an s-subset has degree m>18, its s-1 edges through any x in the subset
spend at least m-18 each, so m<=18+floor(S_x/(s-1)); when m<=18 this bound
is automatic. Every triple except ABC contains a normal point and has
degree4..36. ABC is the UNIQUE exceptional-only triple, with degree at most
18+min(floor(66/2),floor(51/2),floor(51/2))=43. Thus the full triple domain
is4..43 and at most one actual triple has degree37..43. In the real model
this is the group cut sum(t37..t43)<=1, not a per-cell assignment or claim
that the exceptional triple is attainable at that endpoint. Every quad
contains a normal point, so quad domains remain1..30 with no exceptional
quad or high-quad tail. This distinction is essential for the final case.

## Histograms, transport, tightness and moments

Let n_s count unordered pairs of distinct occurrence indices intersecting
in s points,0<=s<=16, including s=16 for repeated whole blocks. Let p_e count
actual distinct point pairs of excess e, t_m triples of degree m, q_h quads
of degree h. J_(a,b,e) counts pairs by both actual endpoint excess classes.
Its upper is1275 for(0,0),102 for(0,1),51 for(0,2),1 for(1,1),2 for(1,2).
Class-count rows, J column=p rows,
and class vertex-budget rows follow by exact counting. Same-class00 and11
edges contribute twice to their own class, other supported edges once at
each distinct class. Class budgets are51*36=1836,2*51=102,66. BC has one
physical count but contributes twice its weight to class1. AB and AC each
contribute once to class1 and once to class2; their joint physical count is2.

M_(e,m) counts actual pair/triple inclusions. Each pair has52 possible third
points and sum of triple degrees14*lambda, while every triple has3 pairs.
Thus its count, load and triple-column transport equations are exact.
Domains require m<=lambda, m<=43 and m>=4. For lambda18 or19 the separately
reviewed avoidance argument gives the further cap m<=15, regardless of
endpoint point class or repeated blocks:

In such a pair link let p have degree m>=16; tight other points number
a>=255-14b+m, b=18 or19. A tight point has codegree(p)<=2 and uses at least
two of the b-m avoiders. Zero/one avoider permits none; two avoiders permit
at most one tight point, because both would share their duplicated partner
p and the same avoiders, whereas the incidence inequality requires at
least19(b18) or6(b19). Three avoiders can only mean b19,m16, requiring a>=5.
A tight point using all three avoiders forces a<=2; otherwise all use two
avoiders and have partner p, with distinct avoider pairs giving a<=3. These
contradictions prove cap15. Larger m or fewer avoiders are included above.

A lambda18 pair has52 triple extensions of degree>=4 with total load252.
Only44 surplus incidences above4 are available, so at least8 extensions
have degree4: M_(0,4)>=8*p0. A degree-four triple has52 outside incidences
covering51 points, so exactly one outside point repeats. Five of its six
occurrence pairs intersect exactly in that triple; one intersects in a
quad. Consequently n3>=5*t4 and4*n4>=t4, and its quad extensions have degree
only1 or2. A given intersection contributes one triple when size3 and
four when size4, so these charges do not assume distinct whole blocks.

N_(m,h) counts triple/quad inclusions:51 extensions per triple, total degree
13*m, and4 triples per quad. Domain h<=min(m,30), except m4 gives h1..2.
Histogram totals and loads are the physical counts and223*C(16,j).
For j=1..4, double counting occurrence pairs and contained j-subsets gives
sum_T C(degree(T),2)=sum_s C(s,j)*n_s. First moment is116095; second is
imposed exactly. Let F3,F4 denote triple and quad sides minus intersection
sides. Defect equations F3=z3p-z3m,F4=z4p-z4m use nonnegative finite-bounded
variables. An actual cover sets all four to zero, so H=-(z3p+z3m+z4p+z4m)=0.
H need not be minus absolute defects at arbitrary relaxation points.

All histogram cells are bounded by their total physical counts. M cells
are at most52*C(54,2), N cells51*C(54,3), n cellsC(223,2), and J by actual
class pair populations. Plus-defect upper bounds use C(54,j)*C(max_degree,2),
minus-defect uppersC(223,2)*C(16,j). Those domains contain any actual image
with zero defects and support the finite-correction dual argument.

## Complete new endpoint family, with no disjointness assumption

At any integer h>18, define T_h as actual distinct triples of degree>=h.
For a pair xy of excess e<h-18, its number K_h(xy) of such triple extensions
is0 by containment. Otherwise its own edge spends e from BOTH endpoint
budgets. Each distinct third point z of a high triple spends at least h-18
on the new edge xz and the new edge yz. These edges are distinct at each
endpoint, hence

 K_h(xy)<=min(52,floor((S_x-e)/(h-18)),floor((S_y-e)/(h-18))).

Summing over actual pairs gives3*T_h=sum K_h(xy) and the25 lower cuts for
h19..43. Coefficients depend on classes0,1,2, their exact pair domains,
own-edge subtraction, eligibility and integer floors. Normal-touching
pair caps simplify to floor((36-e)/(h-18)); all three exceptional pairs
have a class1 endpoint and use floor((51-e)/(h-18)), capped by52. The
producer keeps both endpoints;
the independent implementation rederives these case-specific simplifications.
No point-disjointness, fractional realizability, symmetry,
incidence independence or selected threshold is needed.

At h>=37, any eligible normal-touching edge has e>=h-18>=19 and remaining
normal budget at most17<h-18, so its coefficient is0. Every positive J
coefficient is therefore on the actual exceptional BC,AB,AC cells. Its
remaining smaller budget is at most32, so every such coefficient is1.
This directly links the unique high tail to exceptional edges through the
complete generic family; no extra seven linking cuts are needed or added.

## Own degree-three-center proof at threshold36

Every heavy edge lambda>=36 spends at least18 at both endpoints. Normal
points have heavy degree<=2. So do B and C, because floor(51/18)=2.
Only A can exceed2, and its degree is at most floor(66/18)=3. Suppose two
distinct high triples share a vertex. Sharing a non-A vertex requires
at least three distinct neighbors there, impossible. If they share only A,
their other vertices are distinct, requiring four neighbors at A, also
impossible. If they share A and another vertex, the latter already gives
the first contradiction. Thus high triples are point-disjoint by this
own-arrangement proof, yieldingT36<=18 and3*T36<=P36. This conclusion cannot
be taken from the center4/5 cases, which permit sharing, or from case22's
two-center diamond argument. No scalar disjointness row is added.

The independent toy check freshly counts the sole-center3/non-center2
graph implication. Require a nonvacuous disjoint control, and actual shared-
point controls that fail its premise. Separately, for every selected triple
of toy exceptional points, derive normal-containing triple and quad bounds
from literal pair budgets, identify the unique exceptional-only tail, and
bound that triple using all three exceptional budgets. Positive-baseline
tail controls must occur; the census does not assume the final target cover.
All2867 variables and323 base rows remain unchanged; exactly25 rows are added.

## Exact negative-upper inference and limits

For each model row l_i<=A_i*x<=u_i and signed integer w_i at D>0, use u_i
when w_i>0 and l_i when w_i<0. Lower-only rows require w_i<=0. With objective
coefficients c_j and0<=x_j<=U_j, let R_j=D*c_j-sum_i w_i*A_ij. Then

 D*H<=sum_i w_i*chosen_endpoint_i+sum_j max(R_j,0)*U_j.

All quantities are exact integers except the final division byD. A strictly
negative certified upper contradicts the actual-cover image H0, excluding
this partition only. Solver status and rounded objective alone are not a
proof. A saved exact zero profile instead establishes survival of this
continuous necessary relaxation; it is not a covering or integer instance.
This case still requires fresh independent semantic/certificate review.
All earlier four scoped packets remain unchanged. Four-ones,4,3+1,2+2 now
have separate fresh parent-assigned internal reviews PASSWITHLIMITS.
This case211 would require its own fresh review. In addition,
the complete five-case exhaustion/padding argument requires independent
review as one global proof. No global224 theorem, bound adoption or
publication is announced by this final scoped test.
