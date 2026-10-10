# Internally reviewed lower bound230 for C(54,16,4)

This complete computer-assisted ordinary proof establishes C(52,14,2)>=19,
then C(53,15,3)>=68 and C(54,16,4)>=230. Independent internal semantic review
is PASS WITH LIMITS, with no mathematical gap or required mathematical edit
reported. Qualified external human acceptance, formal-kernel verification and
literature priority remain pending. Research and verification used AI assistance
under Perry Kern's direction. The recorded upper336 and Franco Atzeni credit
remain unchanged; no335 cover, upper witness or exact covering number is supplied.

Sections1-10 below preserve the reviewed manuscript's mathematical text exactly.
Generation-era certificate/status flags remain frozen; current publication and
review status are documented separately in REVIEW_STATUS.json and CHANGELOG.md.
Read REVIEWER_START.md and ENUMERATIONS.md for reproduction and finite-universe
limits. Stage08 is deliberately inconclusive; the complete proof uses BOTH stages
or the independent full reconstruction. Neither224 nor227 is a premise.

## 1. Definitions and domain

A C(v,k,t) covering is a finite family of k-element subsets of a v-element point
set such that every t-element subset lies in at least one block. The covering
number is the minimum number of blocks. We prove the contradiction in the larger
domain of **indexed block occurrences**, permitting repetitions. Each occurrence
is still a k-element set: a point occurs at most once in a row.

Suppose there is an18-occurrence C(52,14,2) covering. Let x_p in {0,1}^18 be
point p's column, r_p=x_p^T x_p its degree, and m_pq=x_p^T x_q its codegree.
There are18*14=252 point incidences. Every pair is covered, so m_pq>=1 for p!=q.
Let u be the all-ones vector in R^18. Then u^T u=18 and u^T x_p=r_p.
All dimensions, degrees and codegrees count occurrences, including repetitions.

## 2. Tight degree-four columns and their matching

Each occurrence through p covers13 other points. There are51 partners; thus
13*r_p>=51. Since13*3=39<51<=52=13*4, r_p>=4. If r_p=4, its total partner
incidence is52. The51 positive integer codegrees sum52. Exactly one is2 and
every other is1. Call its codegree2 partner its repeated partner.

Let a be the number of degree-four (tight) points. All other degrees are at
least5, so252>=4a+5(52-a)=260-a, hence a>=8. If two tight points are repeated
partners, the relation is reciprocal because codegree is symmetric. Each tight
point has at most one such neighbor; the internal tight-partner graph is a
matching of j edges,0<=j<=floor(a/2). Relabel its2j endpoints first. The tight
column Gram is T=J_a+C, where C=3I_a+A_j and A_j is the matching adjacency.

For an unmatched coordinate C has eigenvalue3; for a matched pair its2x2 block
has eigenvalues2 and4. Thus C and T are positive definite. Tight columns are
linearly independent. If t=1^T C^-1 1, unmatched coordinates contribute1/3
each and matched pairs contribute1/2 each:

    t=(a-2j)/3+j/2=(2a-j)/6.

The rank-one inverse formula, verified by multiplying both sides by J+C, is

    T^-1=C^-1-C^-1*1*1^T*C^-1/(1+t).

Therefore1^T T^-1 1=t/(1+t). The squared projection norm of u on the tight
span is16*t/(1+t)<16<18=u^T u. Thus u is independent of that span. There are
a+1 independent vectors in R^18, so a<=17. The complete macro universe is
a=8,...,17,j=0,...,floor(a/2):5+5+6+6+7+7+8+8+9+9=70 cases.

## 3. Complete normal-column parameters

There are N=52-a normal points. Write their degrees r_p=5+d_p with integer
d_p>=0. Their total degree is252-4a, so

    sum d_p=(252-4a)-5(52-a)=a-8=:D.

The a-2j tight points whose repeated partner is external each select exactly
one normal point. Let H_p be the tight-coordinate set selecting normal p and
h_p=|H_p|. These sets are pairwise disjoint, including when h_p=h_q, and

    sum h_p=a-2j=:H.

For every normal point p its tight cross vector has value2 on H_p and1 on all
other tight coordinates. Its u cross value is r_p. Thus the joint type multiset
of (r_p,h_p) completely determines all needed projection coefficients. It need
not determine an actual covering. At most D points have d_p>0, and at most H
have h_p>0. At least

    N-D-H=52-a-(a-8)-(a-2j)=60-3a+2j=:L

points have (r,h)=(5,0). No disjointness between the positive-d and positive-h
point classes is assumed in this lower count.

## 4. Residual Gram and exact coefficients

The basis consisting of the tight columns followed by u has Gram

    B=[[T,4*1],[4*1^T,18]].

Its Schur complement is18-16t/(1+t)>2, so B is positive definite. Project
all normal columns orthogonally onto the complement of this (a+1)-dimensional
span. Their residual Gram S is positive semidefinite, rank<=18-(a+1)=17-a=:R.
If b_p is normal p's tight-plus-u cross vector, its projected inner product
with q is Q_pq=b_p^T B^-1 b_q. Put

    v_p=t+h_p/3, v_q=t+h_q/3, W=18-16t/(1+t).

The tight external coordinates are unmatched in C, with inverse diagonal1/3.
Their supports are disjoint for p!=q. The block inverse formula gives

    Q_pq=t+(h_p+h_q)/3+delta_pq*h_p/3-v_p*v_q/(1+t)
          +(r_p-4v_p/(1+t))*(r_q-4v_q/(1+t))/W.

Here delta_pq=1 only on the diagonal; equal types at different points still
have disjoint H supports. The full formula can also be reconstructed by exact
inversion of the actual B and direct multiplication of the cross vectors.
Stage08's checker does this for all70 bases; Stage09's checker independently
uses LDL decomposition, triangular solves and all inverse identities.

Write m_pq=1+e_pq for distinct normal points. Integers satisfy
0<=e_pq<=min(r_p,r_q)-1. Total partner incidence for normal p is13r_p. Tight
partners contribute a+h_p; other normal partners contribute(N-1)+sum_q e_pq.
Because a+N-1=51,

    sum_q e_pq=13r_p-51-h_p.

Consequently S_pp=r_p-Q_pp and S_pq=1-Q_pq+e_pq. Negative diagonal entries
would exclude a case by positive semidefiniteness, though none occur among the
574 cases below. Every row domain used below contains the row of any actual
cover. Independent row optimization relaxes symmetry and compatibility; this
can only increase the upper bound on sum S_pq^2.

## 5. Rank inequality and uniform integer row maxima

For a real symmetric rank<=R matrix with nonzero eigenvalues lambda_i,
Cauchy-Schwarz gives (sum lambda_i)^2<=R*sum lambda_i^2. Thus

    (tr S)^2<=R*tr(S^2)=R*sum_pq S_pq^2.

If R=0 the trace and Frobenius norm are zero. Let U be any proved upper bound
on the latter sum. An exact positive gap (tr S)^2-RU excludes the case.

For integers0<=e_i<=c with fixed sum l, maximize
sum_i(e_i^2+2z_i e_i). Regard its domain as a box intersected with a sum
hyperplane. A convex function attains a maximum at a vertex. Each vertex has
all but at most one coordinate at0 or c. Since l is integer, the remaining
coordinate is the integer remainder. Rearrangement pairs larger e_i with
larger z_i. If q=floor(l/c),s=l-cq, and z is sorted decreasingly, the maximum is

    sum_{i=1}^q(c^2+2c*z_i)+(s^2+2s*z_{q+1} if s>0).

This statement is equally valid with repeated coefficients. For one exceptional
cap, enumerate that coordinate's complete integer range then use the uniform
formula. For several exceptional caps, enumerate their complete Cartesian
product and apply the uniform formula to the remainder. Independent integer
knapsacks reconstruct all needed maxima without using this formula.

## 6. Complete seventy-case principal reduction

Choose L plain normal columns. Their equal projection coefficient is
q=Q((5,0),(5,0)); all70 exact cases give1<q<3/2 and L>=5. Each selected row
has diagonal5-q, off baseline z=1-q, excess cap4, and within-subset excess
sum<=14. Each positive increment raises e^2+2ze because1+2z=3-2q>0.
Hence the maximum uses load14. There are at least4 other selected coordinates,
so that load fits. Three4s and one2 give square sum3*16+4=52 and linear term
2*z*14=28z. Therefore

    trace=L(5-q),
    U=L[(5-q)^2+(L-1)(1-q)^2+52+28(1-q)].

The complete finite arithmetic in Stage08 excludes63 macros. The seven
remaining are (8,0),(8,1),(8,2),(8,3),(9,0),(9,1),(10,0). Their exact nonpositive
gaps and every excluded macro's coefficient/gap are retained in the complete
case ledger. In particular all a>10 are excluded before any joint-type reduction.
The code fails UNKNOWN if that condition fails; it cannot silently skip them.

## 7. Complete joint-type enumeration and full residual bound

In the seven remaining macros D=a-8 is0,1 or2. All degrees are5 except:
D0 has no exception; D1 has one6; D2 has either one7 or two6s. All joint
partner distributions are enumerated, including zero partners on high-degree
points, repeated partner-count values and all assignments to the high degrees.

For D0 use every integer partition of H. For D1 enumerate h=0,...,H on the
degree6 point and partition H-h among degree5 points. For D2 do the same for
one degree7, or enumerate0<=h1<=h2,h1+h2<=H on two degree6 points and partition
the remainder. Add (5,0) points to reach exactly N. Every joint type occurs
once up to permutations of equal-degree points. The independent checker instead
enumerates nonnegative multiplicities of vectors(d,h) whose sums are(D,H),
then adds the necessary zero vectors. Agreement covers the complete universe.

The seven case counts are respectively22,11,5,2,97,45,392, summing574.
The case ledger retains all574 normal-type lists, traces, row maxima and gaps.
For a row, its diagonal-square plus sum of baseline off-square terms is known.
Add the exact maximum of sum(e^2+2(1-Q)e), at load13r-51-h, to get a row upper.
Sum it with the type multiplicities to obtain U. A degree5 row, or the sole
degree7 row, has all caps4. A degree6 row has at most one cap5 neighbor, the
other degree6; enumerate its excess0..5. There is no omitted second exception.

All2363 independent row maxima agree. Exactly559 of574 joint types have
positive gaps. The remaining15 all have a8,j0,44 normal degree5 columns and
sum h=8. Their complete positive-h partitions appear in Section9. Stage08
alone does not prove the stronger bound; it is preserved as inconclusive.

## 8. New binary containment lemma

If two binary incidence columns both have weight5 and have inner product5,
their support intersection has size5. Both supports have size5, so they are
equal and the columns are identical. Their cross values with every tight
column must then agree. If h_p>0, choose a tight coordinate in H_p. Its cross
value with p is2 and with every other normal point q is1, because each tight
point has exactly one repeated partner. These columns cannot be identical.
The same applies if h_q>0. Thus

    e_pq<=3 if h_p>0 or h_q>0; e_pq<=4 otherwise.

Plain columns may be identical; their cap remains4. Repeated block occurrences
do not change binary coordinates, equal-support containment, or this argument.
No distinct-point-column hypothesis, distinct-row hypothesis or twin prohibition
for plain points has been added.

## 9. Complete refined fifteen-case arithmetic

Now a8,j0,t=8/3,N44,R9,all r=5. Projection coefficients use Section4 without
modification. Row excess is13*5-51-h=14-h. A positive-h row has43 cap3 neighbors;
use the uniform cap3 formula. A plain row has cap3 on its P positive-h neighbors
and cap4 on its43-P other plain neighbors. In the fifteen cases P<=5. Enumerate
all4^P assignments0..3 to those partner neighbors, retain each feasible remaining
load, and use the uniform cap4 maximum for the other coordinates. No actual
target coverings or Gram matrices are enumerated. This is an upper bound on
each residual row over its complete necessary integer domain.

The independently reconstructed gaps (trace^2-9U) are:

| Positive partner partition (pad to44 with zeros) | Exact gap |
|---|---:|
|1+1+1+2+3|228278/245|
|1+1+1+5|952482/1225|
|1+1+2+2+2|10257028/11025|
|1+1+2+4|985228/1225|
|1+1+3+3|9466012/11025|
|1+1+6|7458058/11025|
|1+2+2+3|1288534/1575|
|1+2+5|7307842/11025|
|1+3+4|1612034/2205|
|2+2+2+2|40120/49|
|2+2+4|7614088/11025|
|2+3+3|913828/1225|
|2+6|686878/1225|
|3+5|721012/1225|
|4+4|145048/225|

All are positive; the minimum is686878/1225. All48 distinct row maxima agree
with the independent full integer knapsack. Combining63 excluded macros,
559 excluded full types, and15 refined exclusions leaves no possible cover.
That proves the proposed nonexistence of an18-occurrence C(52,14,2) covering.

For a fully worked weakest case, simplify Section4 at a8,j0,r5:

    Q_pq=(297-6h_p-6h_q-2h_p*h_q)/210 for p!=q,
    Q_pp=(297+58h_p-2h_p^2)/210.

The partition2+6 has42 plain columns, one h2 and one h6. Their diagonals are
251/70,43/14,159/70, respectively. The off baselines are plain/plain -29/70,
plain/h2 -5/14,plain/h6 -17/70,h2/h6 -1/14. The plain row's load14 maximum
uses three plain excesses4, an h6 excess2 and all other excesses0:
48+4-24*29/70-4*17/70=1438/35. The h2 row load12 maximum uses excess3 on
h6 and on three plains:36-6/14-18*5/14=204/7. The h6 row load8 maximum
uses3 on h2,3 and2 on plains:22-6/14-10*17/70=134/7. Complete enumeration/
knapsack proves these attainments are maxima, not only candidate assignments.

Adding baseline and diagonal squares gives row uppers74929/1225,2153/49,
32811/1225. Hence

    trace=42*251/70+43/14+159/70=5458/35,
    U=(42*74929+25*2153+32811)/1225=3233654/1225,
    trace^2-9U=(29789764-29102886)/1225=686878/1225>0.

The full ledger supplies the same exact trace/U/gap arithmetic for every other
case; all row coefficients and maxima are retained in the two JSON certificates.

## 10. Padding and the two lifts

Any covering with fewer than18 blocks is nonempty, because it covers pairs on
52 points. Repeat any one of its blocks until there are exactly18 indexed
occurrences. Coverage remains true. The preceding contradiction permits repeated
rows, so it excludes all smaller coverings too. Thus the proposed pair floor
is C(52,14,2)>=19.

For any indexed C(53,15,3) covering, each point link (delete that point from
each containing occurrence) is a C(52,14,2) covering, retaining occurrences
and repetitions. Every point degree is at least19. If there are b blocks,

    15b=sum_{53 points} degree>=53*19=1007.
    15*67=1005<1007<=1020=15*68.

Hence b>=68. For an indexed C(54,16,4), each point link similarly has at least68
blocks. Therefore

    16B>=54*68=3672.
    16*229=3664<3672<=3680=16*230.

Hence the proposed parent bound is B>=230. These are lower bounds only. No
335-block construction or exact covering number is supplied or claimed.

## 11. Dependencies, trust and attribution

Dependency graph: indexed18 pair cover -> tight matching and independent ones
direction -> complete70 macros -> complete574 joint types ->15 survivors ->
binary containment cap ->15 positive rank gaps -> pair floor19 -> repeated-block
padding -> child68 -> parent230. Sections1-5, case-universe completeness in6-7,
binary containment in8 and padding/lifts in10 are semantic mathematics. Exact
finite checks reconstruct70 macros,574 joint types/2363 row maxima, and15
refinements/48 maxima. Row optimizations are necessary relaxations of actual
incidence, not searches for target coverings or feasibility certificates.

General incidence-matrix rank methods have prior art, including Daniel Horsley,
[Generalising Fisher's inequality to coverings and packings](https://arxiv.org/html/1409.0485v3).
Point-link counting is classical. This proof derives its own bounds and invokes
no published theorem as a premise. The parameter-specific reduction and binary
refinement were prepared by Mopi; a separate internal investigator independently
checked the semantic implications and reconstructed coefficients/types/maxima
with a third algorithm. All contributions were AI-assisted under Perry Kern's
direction. Internal review is not qualified-human endorsement or priority.

Project-owned materials use the retained MIT license. Third-party papers retain
their rights and are linked rather than copied. No private correspondence,
unrelated investigation, failed construction, or upper witness is reproduced.
The retained upper336 credit belongs to Franco Atzeni/current repository.
The previous public222/223/224 material remains available with unchanged
mathematical bytes. No later private endpoint research is a dependency here.

Reproducing arithmetic does not by itself establish the universal cover-to-model
maps. Read the proof and ASSUMPTION_CODE_MAP.md as well as the exact case ledgers.
Integrity hashes bind inspected bytes; they do not replace a trust anchor,
formal kernel, qualified external review or a priority investigation.
