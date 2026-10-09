# Complete case22 occurrence map and certification scope

This is a necessary map for any complete C(54,16,4) covering with exactly223
legal block occurrences whose degree multiset is66^52,68^2. Whole blocks may
repeat, but each occurrence contains16 distinct points. Padding a smaller
nonempty covering to223 preserves coverage and reviewed floors, but does
not guarantee this degree partition. This case is not the whole problem.

## Floors and the four-excess partition

The internally reviewed child theorem C(53,15,3)>=66 applies to repeated
occurrences. Removing a point from its containing blocks covers all triples
on the other53 points, hence r_x>=66. For223 occurrences the incidence sum
is3568 and sum(r_x-66)=4. Fix partition2+2:52 normal points r=66 and two
exceptional points A,B with r=68. The first intersection moment is
52*C(66,2)+2*C(68,2)=116096, distinct from all three earlier tested moments.

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
normals and66 at both A,B; the total edge excess is1002. Every pair except AB
has a normal endpoint and e<=36. The exceptional pair AB has
e<=min(66,66,68-18)=50. Classes(0,0),(0,2),(2,2) have respective
populationsC(52,2)=1326,104,1. No other class pairs exist. These are
necessary domains; no attainable endpoint is claimed.

If an s-subset has degree m>18, its s-1 edges through any x in the subset
spend at least m-18 each, so m<=18+floor(S_x/(s-1)); when m<=18 this bound
is automatic. Every triple and quad has a normal point. Thus triple domains
are4..36 and quad domains1..30. No exceptional-only high tail is possible.

## Histograms, transport, tightness and moments

Let n_s count unordered pairs of distinct occurrence indices intersecting
in s points,0<=s<=16, including s=16 for repeated whole blocks. Let p_e count
actual distinct point pairs of excess e, t_m triples of degree m, q_h quads
of degree h. J_(a,b,e) counts pairs by both actual endpoint excess classes.
Its upper is1326 for(0,0),104 for(0,2),1 for(2,2). Class-count rows, J column=p rows,
and class vertex-budget rows follow by exact counting; a(0,0) edge contributes
twice, as does a(2,2) edge at its own class; a(0,2) edge contributes once
at each class. Class budgets are52*36=1872 and2*66=132. In particular AB
has one physical pair count but contributes twice its weight to class2.

M_(e,m) counts actual pair/triple inclusions. Each pair has52 possible third
points and sum of triple degrees14*lambda, while every triple has3 pairs.
Thus its count, load and triple-column transport equations are exact.
Domains require m<=lambda, m<=36 and m>=4. For lambda18 or19 the separately
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
sum_T C(degree(T),2)=sum_s C(s,j)*n_s. First moment is116096; second is
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

Summing over actual pairs gives3*T_h=sum K_h(xy) and the18 lower cuts for
h19..36. Coefficients depend on classes0,2, their exact pair domains,
own-edge subtraction, eligibility and integer floors. Normal-touching
pair caps simplify to floor((36-e)/(h-18)); the unique(2,2) pair uses
floor((66-e)/(h-18)), capped by52. The producer keeps both endpoints;
the independent implementation rederives these case-specific simplifications.
No point-disjointness, fractional realizability, symmetry,
incidence independence or selected threshold is needed.

## Own two-center graph and occurrence compatibility

At threshold36 every heavy edge spends at least18 at each endpoint. Normal
heavy degrees are at most2, and both A,B have degree at most floor(66/18)=3.
These graph degree bounds PERMIT the diamond ABu,ABv; a one-center or
maximum-degree-two disjointness argument is insufficient.

Suppose two distinct high triples ABu,ABv have degree at least36, with u,v
normal. At u its edges to A and B each spend at least18, exhausting its
budget36. Every other incident excess is therefore0; in particular
lambda_uv=18. Let U,V be their containing occurrence-index sets. Their union
is inside the AB occurrence set, and their intersection is inside the uv
occurrence set. Thus |U|+|V|<=lambda_AB+lambda_uv. Consequently
lambda_AB>=72-18=54, e_AB>=36. The budget at A must include e_AB>=36 and
e_Au,e_Av>=18, requiring at least72>66. The same holds at B, contradiction.

Hence a shared exceptional edge is impossible under the full occurrence
and budget map. Sharing only A or only B would require four heavy neighbors,
exceeding3; sharing a normal point requires at least three, exceeding2.
High triples are therefore point-disjoint by this separately derived
two-center argument, givingT36<=18 and3*T36<=P36. This conclusion is not
borrowed from another point arrangement.

The general lemma independently tested on literal toys is: at a nonnegative
pair baseline L and threshold h>L, delta=h-L, if two high triples xyU,xyV
share xy and S_U,S_V<=2*delta, then lambda_UV=L, lambda_xy>=2*h-L and
S_x,S_y>=4*delta. The same saturation and occurrence-union argument proves
it. If all normal budgets are<=2*delta and both exceptional budgets are
strictly below4*delta, all high triples are point-disjoint. Target budgets
36=2*18 and66<4*18 meet this premise. A real toy diamond at equality4*delta
must be preserved as a control; graph degree bounds alone admit it.

This pass retains the generic endpoint-family coefficients. In particular
the raw(2,2) coefficient at h36 is2 for e18..30,1 for e31..48,0 for e49..50.
It is not silently tightened to1 using the new lemma. No scalarT36 or
point-disjointness row is added. Exactly18 complete endpoint cuts extend
the frozen301-row base, with unchanged2402 variables. The independent
preaudit checks both the raw capacity2 cells and the separate stronger
occurrence consequence, including positive and equality-boundary controls.

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
Case2+1+1 remains uncomputed. Four-ones has a fresh parent-assigned internal
review PASSWITHLIMITS;4 and3+1 packets await their separately assigned reviews.
The present2+2 packet would require its own fresh review. No global224
claim follows before all five case maps and certificates have independent review.
