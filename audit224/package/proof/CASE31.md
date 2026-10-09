# Complete case31 occurrence map and certification scope

This is a necessary map for any complete C(54,16,4) covering with exactly223
legal block occurrences whose degree multiset is66^52,67^1,69^1. Whole blocks may
repeat, but each occurrence contains16 distinct points. Padding a smaller
nonempty covering to223 preserves coverage and reviewed floors, but does
not guarantee this degree partition. This case is not the whole problem.

## Floors and the four-excess partition

The internally reviewed child theorem C(53,15,3)>=66 applies to repeated
occurrences. Removing a point from its containing blocks covers all triples
on the other53 points, hence r_x>=66. For223 occurrences the incidence sum
is3568 and sum(r_x-66)=4. Fix partition3+1:52 normal points r=66, point
A with r=69, and point B with r=67. The first intersection moment is
52*C(66,2)+C(67,2)+C(69,2)=116097, distinct from both earlier tested moments.

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
normals,81 at A,51 at B; the total edge excess is1002. Every pair except AB
has a normal endpoint and e<=36. The exceptional pair AB has
e<=min(81,51,min(69,67)-18)=49. Classes(0,0),(0,1),(0,3),(1,3) have respective
populationsC(52,2)=1326,52,52,1. There are no(1,1) or(3,3) cells. These are
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
Its upper is1326 for(0,0),52 for(0,1) and(0,3),1 for(1,3). Class-count rows, J column=p rows,
and class vertex-budget rows follow by exact counting; a(0,0) edge contributes
twice; every other supported pair contributes once at each distinct class.
Class budgets are52*36=1872,51,81. In particular the exceptional pair's
one physical incidence and own weight are counted at both exceptional classes.

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
sum_T C(degree(T),2)=sum_s C(s,j)*n_s. First moment is116097; second is
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
h19..36. Coefficients depend on classes0,1,3, their exact pair domains,
own-edge subtraction, eligibility and integer floors. Normal-touching
pair caps simplify to floor((36-e)/(h-18)); the unique(1,3) pair uses
floor((51-e)/(h-18)), capped by52. The producer keeps both endpoints;
the independent implementation rederives these case-specific simplifications.
No point-disjointness, fractional realizability, symmetry,
incidence independence or selected threshold is needed.

The threshold36 heavy graph is checked separately for this case. Every
edge spends at least18 at BOTH endpoints. Normal degrees are at most2;
B has degree at most floor(51/18)=2; A at most floor(81/18)=4. Distinct
high triangles sharing any vertex besides A would force that vertex to
have at least three different neighbors, impossible. Triangles through A
therefore use distinct neighbor pairs and number k_A<=floor(4/2)=2.
All other53 vertices belong to at most one high triple, so3*T36-k_A<=53,
givingT36<=18. A shared edge would share a non-A vertex, so edges are
disjoint and3*T36<=P36. High triangles may share A; point disjointness
is not assumed or inferred. This is a case-specific proof, not a transfer
of the maximum-degree-two proof in four-ones or the degree-five center in4.

The independent preaudit freshly counts this implication on every literal
toy baseline/threshold whose heavy graph has one center of degree<=4 and
all other vertices degree<=2. A positive shared-center control must occur;
this demonstrates why no stronger point-disjointness assumption is used.
The scalarT36 bound is not an added row. Only the full18 endpoint cuts
are added to the frozen300-row base, with unchanged2404 variables.

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
Cases2+2 and2+1+1 are not tested here; the frozen four-ones and4 packets are
preserved, with4 still awaiting its assigned fresh review. No global224
claim follows before all five case maps and certificates have independent review.
