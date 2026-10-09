# Numbered proof audit: the public 222 bound and proposed 223 bounds

Prepared 2026-10-08 under Perry Kern's direction, with AI assistance by
Mopî and the project investigators/reviewer. Status: **internally audited
proposed proofs; qualified external review and literature priority pending**.
The 222 proof and certificate already occur in the public repository at
`946f7ee8931ca9a3b64ef3f1c0f4b0a9fe803c35`. The two 223 routes are additions
submitted for review. Neither independent arithmetic nor this exposition is
external mathematical acceptance. Source identifiers and hashes are in
[SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json); established methods and
their authors are identified in [ATTRIBUTION.md](ATTRIBUTION.md).

The numbered arguments below are semantic proofs. Their relation to executable
checks is in [DEPENDENCIES.md](DEPENDENCIES.md). Every finite enumeration is
specified in [ENUMERATIONS.md](ENUMERATIONS.md). No computation enumerates
all target coverings, and no search failure is a premise of these bounds.

## 1. Definition: blocks, occurrences and coverings

Let V be a set of v distinct points. A legal block is a k-element subset of
V: a point cannot repeat inside it. A family `(B_1,...,B_b)` is indexed by
occurrence, and equal subsets at different indices are allowed. It is a
complete t-cover if every t-element subset of V is contained in at least
one B_i. The usual C(v,k,t) minimizes distinct legal blocks; excluding a
family even when occurrences may repeat also excludes distinct families.
All results here concern **every** complete legal uniform cover. No pool,
pairing, group action, random seed, particular construction or neighborhood
is imposed.

For a j-subset S, let d(S) count containing occurrence indices. Write r_x
for a point degree, lambda_P for a pair degree, and mu_T for a triple
degree. Let n_s count unordered pairs of distinct occurrence indices i<j
for which `|B_i intersect B_j|=s`. Include s=k: equal block occurrences
have intersection k and must not be omitted.

## 2. Lemma: links and padding

The link of S consists of `B_i minus S` for each i with `S subset B_i`.
It has v-|S| points and k-|S| points per block. For a complete t-cover it
covers every (t-|S|)-subset of the remaining points: adjoining S forms
a t-subset, and a block covering it contains S. Equal link blocks retain
their occurrence indices.

A complete cover in the present parameter sets is nonempty. Repeat any
one block to increase its occurrence count to a chosen larger b. Coverage,
uniformity and legality are preserved. Thus excluding exactly 221
occurrences on (54,16,4) excludes every size <=221; excluding exactly 65
on (53,15,3) excludes every size <=65. These reductions require all moments
and capacities to count repeated occurrences. They assert nothing about
padding an incomplete family into a complete one.

## 3. Lemma: universal intersection moments and loads

For any legal uniform family, complete or incomplete, and j>=0,

`sum_s C(s,j)n_s = sum_{S subset V, |S|=j} C(d(S),2)`.

Both sides count `(S,{i,l})` with i<l and S contained in both blocks.
For j=0 both sides equal C(b,2). For j=1,2,3 this gives the point, pair
and triple moments. The right degree domain for an arbitrary family is
0..b. Restricted degree domains used below require completeness and their
proved caps; they are not universal moment identities in isolation.

Count pairs through a fixed point or triples extending a fixed pair:

`sum_{P contains x} lambda_P=(k-1)r_x`,
`sum_{T contains P} mu_T=(k-2)lambda_P`.

Count containing point/triple incidences over all blocks:
`sum_x r_x=bk`, `sum_P lambda_P=b C(k,2)`,
`sum_T mu_T=b C(k,3)`. These identities also allow repeated blocks.

## 4. Lemma: a complete C(52,14,2) needs at least 18 occurrences

First, every point q has degree at least `ceil(51/13)=4`, because each
14-block through q contains only 13 of the 51 other points. If q has degree
four, its blocks have `4*13=52` outside incidences covering 51 distinct
points. Subtract the compulsory one occurrence of each point: total
surplus is `52-51=1`. Exactly one outside point occurs twice and all 50
others occur once. Thus q has exactly one codegree-two partner and all
other pair codegrees are one.

Let a be the number of degree-four points and b the occurrence count.
Other points have integer degree >=5, so

`14b=sum_q r_q >=4a+5(52-a)=260-a`, hence `a>=260-14b`.

Among those a points the codegree-two pairs form a matching: every vertex
has at most one such partner, and the relation is symmetric. Let A be
its adjacency matrix, J the all-ones matrix, and X the a-by-b incidence
matrix of those points against block occurrences. Diagonal entries of
XX^T are 4 and off-diagonal entries are 1+A_ij, so

`XX^T=3I+A+J`.

For any real vector z indexed by the a tight points, with matching edges E
and isolated vertices I_0,

`z^T(3I+A+J)z`
`=3 sum_i z_i^2+2 sum_{ij in E}z_i z_j+(sum_i z_i)^2`
`=2 sum_i z_i^2+sum_{i in I_0}z_i^2`
` +sum_{ij in E}(z_i+z_j)^2+(sum_i z_i)^2`.

This is positive for every nonzero z because its first term is positive
and all remaining terms are nonnegative. If a>0, the matrix is positive
definite and has rank a. Since rank(XX^T)<=rank(X)<=b, b>=a. If a=0,
b>=a still holds and the incidence inequality itself gives 14b>=260.
In all cases `b>=a>=260-14b`, so `15b>=260` and
`b>=ceil(260/15)=18` since `15*17=255<260<=270=15*18`.
Repeated incidence columns do not change this rank upper bound.

This specific derivation discharges the degree floor without an external
theorem premise. It is a parameter specialization of established
Bose/Fisher/Horsley rank reasoning, with no priority claim. It agrees
with [Horsley's Theorem 1](https://arxiv.org/html/1409.0485v3):
`3<=14<52`, `51=4*(14-1)-1`, `0<=1<13`, and `1<4-1=3`.
The theorem gives `ceil(52*(4+1)/(14+1))=ceil(260/15)=18`.
If applying a theorem phrased for distinct blocks, first deduplicate the
link; a lower bound on its distinct blocks also bounds its occurrences.

## 5. Lemma: one-surplus intersection capacities

In a complete (54,16,4) cover, a triple of degree four has four blocks
through it, each with 13 outside points. Its 51 outside points require
51 incidences and there are 52. By the surplus calculation in Lemma 4,
one outside point occurs twice and all others once. Of the `C(4,2)=6`
pairs of these containing occurrences, five have intersection exactly
that triple and one has intersection the triple plus the repeated point.
No further outside common point is possible. Equal blocks among these
four would repeat 13 outside points, exceeding surplus one; hence the
local conclusion remains valid despite allowing repeated blocks globally.

Let t_4 count tight triples. A size-three block intersection has exactly
one contained triple and hence receives at most one such charge; a
size-four intersection contains `C(4,3)=4` triples and receives at most
four. Therefore `n_3>=5t_4` and `4n_4>=t_4`.

Similarly in a complete (53,15,3) cover, a pair of degree four has 51
outside points and 52 outside incidences. Five containing-block pairs
intersect in exactly that pair and one in a triple. If p_0 counts these
tight pairs, capacities `C(2,2)=1` and `C(3,2)=3` give
`n_2>=5p_0` and `3n_3>=p_0`. Larger intersections receive no tight-pair
charge. The capacity arguments allow charges from different tight sets
to overlap up to the stated capacities; they do not assume disjointness.

## 6. Definition and arithmetic: the already-public 222 model

Assume a complete (54,16,4) cover with b=221 occurrences. Pair links are
complete (52,14,2) covers, so Lemma 4 gives lambda_P>=18. Lemma 3 gives
`15r_x>=53*18=954`, so `r_x>=ceil(954/15)=64`:
`15*63=945<954<=960=15*64`. Triple degrees satisfy mu_T>=4 by
`ceil(51/13)=4`, since `13*3=39<51<=52=13*4`.

Set `delta_x=r_x-64`, `e_P=lambda_P-18`. Then

`D=221*16-54*64=3536-3456=80`,
`E=221*C(16,2)-18*C(54,2)=221*120-18*1431`
` =26520-25758=762`.

All excesses are nonnegative integers, so 0<=delta<=80. For pair xy,
containment gives lambda_xy<=min(r_x,r_y). Therefore

`e_xy<=64-18+min(delta_x,delta_y)`
` <=46+floor((delta_x+delta_y)/2)<=46+floor(80/2)=86`.

Every triple degree is bounded by any of its pair degrees, hence
`4<=mu_T<=18+86=104`, with `mu_T<=18+e_P` when P subset T.
The use of these loose caps is intentional; no tighter experimental cap
replaces the frozen certificate domain.

Use nonnegative variables n_s, u_d, p_e, t_m for block-pair intersections,
point excesses, pair excesses and triple degrees, respectively; and M_e,m
for incidences `(P,T)` with P subset T and the indicated excess/degree.

| Family | Complete domain | Per-cell upper bound |
| --- | --- | ---: |
| n_s | s=0..16 | C(221,2)=221*220/2=24310 |
| u_d | d=0..80 | 54 |
| p_e | e=0..86 | C(54,2)=54*53/2=1431 |
| t_m | m=4..104 | C(54,3)=54*53*52/6=24804 |
| M_e,m | e=0..86; m=4..18+e | 1431*52=74412 |

The M bound counts all pair/triple incidences, independent of the chosen
cover. Variable counts are 17+81+87+101+5046=5332, where
`5046=sum_{e=0}^{86}(15+e)=87*15+86*87/2=1305+3741`.
Actual covers map to these integers; relaxing them to real numbers only
enlarges the admissible set. No reverse realization claim is needed.

## 7. Lemma: every row of the 222 model is necessary

Lemma 3 and the counts above give these nine equalities:

```
sum_s n_s=24310; sum_d u_d=54; sum_d d*u_d=80;
sum_s s*n_s - sum_d C(64+d,2)u_d=0;
sum_e p_e=1431; sum_e e*p_e=762;
sum_s C(s,2)n_s - sum_e C(18+e,2)p_e=0;
sum_m t_m=24804; sum_m m*t_m=221*C(16,3)=221*560=123760.
```

For each e=0..86 there are exactly 52 triples extending a pair, and each
16-block through it contributes 14 extensions. Thus

`sum_m M_e,m=52p_e`, `sum_m m*M_e,m=14(18+e)p_e`.

For each m=4..104 each triple has three pairs, so
`sum_e M_e,m=3t_m`. These sums range precisely over the cells of Definition
6; containment proves no actual incidence is discarded.

Lemma 5 supplies two inequalities `n_3-5t_4>=0`, `4n_4-t_4>=0`.
For a pair of degree 18, its 52 triple extensions have degrees >=4 with
sum `18*14=252`. If z have degree four, the sum is at least
`4z+5(52-z)=260-z`; hence `252>=260-z` and z>=8. Summing gives
`M_0,4-8p_0>=0`. Because `sum_e M_e,4=3t_4` and cells are nonnegative,
also `3t_4-8p_0>=0`. Retaining this redundant necessary row is sound.

The complete row count is `9+4+2*87+101=288`. Exact zero-based order:
rows 0..8 are the nine displayed equalities; 9..12 are respectively
the two intersection cuts, `3t_4-8p_0`, `M_0,4-8p_0`; rows `13+2e`
and `14+2e` are M count and load; row `187+(m-4)` is M column.
Equalities have equal lower/upper bounds. Cuts have lower zero and
infinite upper bound. [independent222.py](independent222.py) reconstructs
all 5332 variables, every bound and objective, and all 288 sparse rows;
comparison includes the `5332*288=1535616` possible coefficient positions,
including all implicit zeros.

## 8. Lemma: omitted identity and exact upper-certificate rule

Lemma 3 with j=3 proves, for the hypothetical complete cover in Definition 6,

`F=sum_{m=4}^{104}C(m,2)t_m - sum_{s=0}^{16}C(s,3)n_s=0`.

This is the standard moment identity, not a new general theorem. The
model retains Lemma 7 but omits F=0 and maximizes F over a real relaxation.
Let c be its objective vector and write a row as
`l_i<=A_i x<=h_i`, where h_i may be infinite. For integer row weights w_i
and a positive integer scale S, require `w_i<=0` when h_i is infinite.
For w_i>0 take b_i=h_i; for w_i<=0 take b_i=l_i (zero weights contribute
zero). Then `w_i A_i x<=w_i b_i`. Set

`a_j=sum_i w_i A_ij`, `R_j=max(0,S c_j-a_j)`.

For 0<=x_j<=U_j,

`S F=sum_i w_i(A_i x)+sum_j(S c_j-a_j)x_j`
` <=sum_i w_i b_i+sum_j R_j U_j`.

Negative column residuals are bounded above by zero because x_j>=0;
positive residuals use the physical upper bound. The rule is exact weak
duality with finite corrections; it requires no solver status, tolerance,
floating-point arithmetic or claim of optimality.

## 9. Theorem: the public certificate proves C(54,16,4)>=222

The frozen [model](../data/model.json) and
[certificate](../data/certificate.json) are unchanged. All 288 signed
weights are replayed, each one-sided row sign is checked, and the entire
positive-residual map is reconstructed, not sampled. Exact results:

```
S=1000000000
sum_i w_i b_i=-2660294744798
sum_j R_j U_j=88273944                  (95 positive columns)
H=-2660294744798+88273944=-2660206470854
H/S=-1330103235427/500000000 <0          (divide numerator/denominator by 2)
```

Lemma 8 gives F<=H/S<0, contradicting F=0. Lemma 2 pads any smaller
complete cover to 221 occurrences; hence all sizes <=221 are excluded.
The target lower bound is 222. It excludes no size >=222.

For a diagnostic that the weaker model itself is nonempty, the saved
aggregate has n3=8920,n4=473,n5=4170,n6=10721,n7=26;
u1=28,u2=26; p0=669,p1=762; t4=1784,t5=21496,t6=1524;
M0_4=5352,M0_5=29436,M1_5=35052,M1_6=4572, all other variables zero.
The verifier checks every bound and row, then computes

`sum C(m,2)t_m=6*1784+10*21496+15*1524`
` =10704+214960+22860=248524`,
`sum C(s,3)n_s=8920+4*473+10*4170+20*10721+35*26`
` =8920+1892+41700+214420+910=267842`,
`F=248524-267842=-19318`.

This is a feasible diagnostic histogram, not a cover: a cover would have
F=0. It prevents confusing the supplied certificate with an accidental
empty model but is not necessary for the contradiction.

## 10. Lemma: local floors and complete point-degree cases for 223

In a complete (53,15,3) cover, every point link is (52,14,2), so r_y>=18
by Lemma 4. Every pair has degree m_yz>=4 by the 51 outside extensions
and 13 outside points per containing block. Thus `15b>=53*18=954` and
`b>=64`, because `15*63=945<954<=960=15*64`. To show b>=66 analytically
it suffices to exclude b=64 and b=65.

Write `r_y=18+d_y`. Nonnegative integer excess has
`D=sum_y d_y=15b-954`, equal to `960-954=6` at b=64 and
`975-954=21` at b=65. Hence `0<=d_y<=D<=21`, so `18<=r_y<=39`.
This covers every point degree in either hypothetical family.

## 11. Lemma: a complete 19-block (52,14,2) link has degree at most 15

Assume a point p has degree m>=16 in such a link. It has at most 19.
It is not degree four. Let a be the number of degree-four points other
than p. Of the remaining 51 points, the others have degree >=5. Counting
incidences away from p gives

`19*14-m=266-m>=4a+5(51-a)=255-a`,
so `a>=m-11>=5`.

Let s=19-m<=3 be the number of block occurrences avoiding p. By Lemma 4,
each tight point q has codegree with p at most two, so at least two of
its four occurrences avoid p. If s<=1 this is impossible. If s=2 every
q uses both avoiding blocks and two through p, making p its unique
repeated partner. Two such q would share both avoiding blocks and thus
be repeated partners of each other as well; therefore a<=1, contradiction.

If s=3 and a tight q uses all three avoiding blocks, each other tight
point uses at least two of them and therefore has codegree >=2 with q.
q has only one repeated partner, so there is at most one other tight
point, giving a<=2, contradiction. Consequently every tight point uses
exactly two avoiding blocks and exactly two through p, so its repeated
partner is p. Two tight points cannot use the same outside pair, which
would make them another repeated partner. There are only `C(3,2)=3`
outside pairs, so a<=3, contradiction. This covers m=16,17,18,19 and
proves the cap. Completeness, degree four and single surplus are essential.
No degree-15 existence or sharpness claim is made.

## 12. Definition and lemma: Pētā's intersection quantity

For b in {64,65}, let p4 count pairs of degree four and n_s count block-pair
intersections for the full s=0..15. Let `P(s)=(s-6)(s-7)`.
For integer s, if s<=6 both factors are nonpositive; if s>=7 both are
nonnegative. There is no integer strictly between 6 and 7, so P(s)>=0.
At s=2, P(2)=(-4)(-5)=20; at s=3, P(3)=(-3)(-4)=12.
Lemma 5 therefore gives

`sum_s P(s)n_s>=20n_2+12n_3>=20*5p4+12*p4/3=104p4`.

Define `H=sum_s P(s)n_s-104p4`, so H>=0.

For a point y define a_y as its number of degree-four pair neighbors,
`f(m)=C(m,2)-52*1[m=4]`,
`g_y=sum_{z!=y}f(m_yz)-12C(r_y,2)`.
There are 52 neighbors; their load is `sum_z m_yz=14r_y`, and each
`4<=m_yz<=r_y` by floor and containment. Note
`P(s)=s^2-13s+42=2C(s,2)-12s+42`.
Using Lemma 3 and `sum_y a_y=2p4`,

`sum_y g_y=2 sum_{y<z}C(m_yz,2)-104p4-12 sum_y C(r_y,2)`
`=sum_s [2C(s,2)-12s]n_s-104p4`,
so `H=42C(b,2)+sum_y g_y`.

## 13. Lemma: all three degree cases of the local envelope

**r=18.** Neighbor load is `14*18=252`. If a neighbors are tight,
`252>=4a+5(52-a)=260-a`, so a>=8. For integer m=4,
`f(4)=6-52=-46=11*4-45-45`. For 5<=m<=18,

`11m-45-C(m,2)=(m-5)(18-m)/2>=0`.

Thus `f(m)<=11m-45-45*1[m=4]`. Sum over neighbors:
`sum f<=11*252-45*52-45*8=2772-2340-360=72`.
Since `C(18,2)=153`, `g<=72-12*153=72-1836=-1764`.

**r=19.** The link at y has exactly 19 blocks, so Lemma 11 gives m<=15.
For 5<=m<=15,
`(19m-75)/2-C(m,2)=(m-5)(15-m)/2>=0`.
At m=4, `f(4)=-46<=(76-75)/2=1/2`.
Hence `sum f<=[19*(14*19)-75*52]/2`
` =[19*266-3900]/2=(5054-3900)/2=577`.
With `C(19,2)=171`, `g<=577-2052=-1475=-1764+289`.

**r=18+d with 2<=d<=21.** For 5<=m<=r,
`[(r+4)m-5r]/2-C(m,2)=(m-5)(r-m)/2>=0`.
At m=4 its right side is `(16-r)/2`, and r<=39 gives
`(16-r)/2>=-23/2>-46=f(4)`. Therefore

`sum f<=[(r+4)*14r-5r*52]/2`
` =(14r^2+56r-260r)/2=7r^2-102r`,
`g<=(7r^2-102r)-12*r(r-1)/2=r^2-96r`
` =(18+d)^2-96(18+d)=-1404-60d+d^2`.

Its slack beneath the proposed envelope is
`(-1764+289d)-(-1404-60d+d^2)=-360+349d-d^2`
` =(d-2)(347-d)+334>0`.
Indeed d-2>=0 and 347-d>=326>0, with the additional 334 positive.
All cases therefore give `g_y<=-1764+289d_y`.
The executable checks cover all 557 permitted (r,m) cases, but the chord
factorizations and this complete degree partition supply universality.
Without Lemma 11 the generic r=19 value is `361-1824=-1463`, exceeding
-1475 by 12; removing avoidance would invalidate the stated envelope.

## 14. Theorem: Pētā's analytic route gives C(53,15,3)>=66

Sum Lemma 13 over 53 points and substitute Definition 12:

`0<=H<=42C(b,2)-1764*53+289(15b-954)`.

Here `1764*53=93492`. At b=64, `C(64,2)=2016`,
`42*2016=84672`, `D=6`, `289*6=1734`; hence
`H<=84672-93492+1734=-7086`.
At b=65, `C(65,2)=2080`, `42*2080=87360`, `D=21`,
`289*21=6069`; hence `H<=87360-93492+6069=-63`.
Both contradict H>=0. Lemma 10 already excludes smaller sizes, so
every complete (53,15,3) cover has at least 66 occurrences.

The working label **Pētā Method/Proof** refers to this project's route
and is not a claim of mathematical priority. The general avoidance lemma
from a later stage is not used or published in this package.

## 15. Definition and arithmetic: scout's independent 65-occurrence model

Use Lemma 2 to assume exactly b=65 occurrences in a hypothetical complete
(53,15,3) cover of size <=65. Lemma 10's floors apply. Set
`r_x=18+delta_x`, `lambda_P=4+e_P`. Counts give

`sum delta=65*15-53*18=975-954=21`,
`sum e=65*C(15,2)-4*C(53,2)=65*105-4*1378`
` =6825-5512=1313`,
`sum mu=65*C(15,3)=65*455=29575`.

Thus delta=0..21. If lambda>=18, its two endpoints each consume at least
lambda-18 of the 21-unit excess budget, so
`2(lambda-18)<=21` and lambda<=18+floor(21/2)=28. If lambda<18 the same
cap is automatic. For a triple with mu>=18, its three endpoints give
`3(mu-18)<=21`, so mu<=25; for mu<18 it is automatic. Hence
`e=0..24`, `mu=1..25` are complete integer domains.

For point-pair incidence `(x,P)`, containment requires
`4+e<=18+d`, equivalently e<=14+d. For pair-triple incidence `(P,T)`,
`mu<=4+e`. Moreover the 51 triples extending P satisfy
`sum(mu-1)=13(4+e)-51=1+13e`.
Each summand is nonnegative by completeness, so
`mu-1<=1+13e`, or `mu<=2+13e`. No actual cell outside these supports
exists. These integer deductions justify domains of a real relaxation;
they are not requirements on arbitrary fractional degree objects.

Variables n_s,u_d,p_e,q_m are the corresponding block-intersection,
point-excess,pair-excess,triple-degree histograms. M_d,e counts point-pair
incidences by excess and N_e,m counts pair-triple incidences by degree.

| Family | Complete domain | Per-cell upper bound |
| --- | --- | ---: |
| n_s | s=0..15 | C(65,2)=2080 |
| u_d | d=0..21 | 53 |
| p_e | e=0..24 | C(53,2)=53*52/2=1378 |
| q_m | m=1..25 | C(53,3)=53*52*51/6=23426 |
| M_d,e | e<=14+d | 53*52=2756 |
| N_e,m | m<=4+e and m<=2+13e | 1378*51=70278=3*23426 |

M has 495 cells: at d=0..9 its counts are 15..24, summing
`10*(15+24)/2=195`; at d=10..21 all 25 e values fit, giving 12*25=300.
N has 392 cells: e=0 allows m=1..2 (two cells); e=1..20 allows m=1..4+e
(counts 5..24, sum `20*(5+24)/2=290`); e=21..24 allows all 25 m values
(100 cells). Thus total is `2+290+100=392`, and variable count
`16+22+25+25+495+392=975`.

## 16. Lemma: all 156 scout rows are necessary

Seven profile equalities are

```
sum n=2080; sum u=53; sum d*u=21;
sum p=1378; sum e*p=1313; sum q=23426; sum m*q=29575.
```

Two retained moment rows from Lemma 3 are
`sum_s s*n_s=sum_d C(18+d,2)u_d`,
`sum_s C(s,3)n_s=sum_m C(m,2)q_m`.

The three point-pair transport types are
`sum_e M_d,e=52u_d`,
`sum_e (4+e)M_d,e=14(18+d)u_d`,
`sum_d M_d,e=2p_e`.
There are `2*22+25=69` rows: each point has 52 neighbors, each block
through it supplies 14, and each pair has two endpoints.

The three pair-triple types are
`sum_m N_e,m=51p_e`,
`sum_m m*N_e,m=13(4+e)p_e`,
`sum_e N_e,m=3q_m`.
There are `2*25+25=75` rows: each pair has 51 extensions, each block
through it supplies 13, and a triple has three contained pairs.
All sums use only Definition 15's complete supported cells.

A point of degree 18 has 52 pair neighbors of minimum degree four and
total load 252. Neighbor excess sums to `252-4*52=44`. At most 44
neighbors have positive integer excess, leaving at least `52-44=8`
tight neighbors. Therefore `8u_0-M_0,0<=0`. Lemma 5 gives the other
two cuts `5p_0-n_2<=0` and `p_0-3n_3<=0`.
Total rows `7+2+69+75+3=156`, comprising 153 equalities and three <= cuts.

Frozen ordering is seven profiles at 0..6, first/third moments at 7..8;
M count/load at `9+2d`,`10+2d`; M columns at `53+e`;
the tight-point cut at 78; N count/load at `79+2e`,`80+2e`;
N columns at `129+(m-1)`; tight-pair cuts at 154,155.
The reconstructed comparison checks `975*156=152100` coefficient
positions, all bounds, objective coefficients, row senses and supports.
Unrealizable cells are permitted: a necessary relaxation may contain
profiles that no cover realizes. Only the forward map is asserted.

## 17. Theorem: scout's exact certificate gives C(53,15,3)>=66

By Lemma 3 with j=2, every actual family satisfies

`F2=sum_e C(4+e,2)p_e - sum_s C(s,2)n_s=0`.

The model maximizes F2 while retaining Lemma 16 and omitting this second
moment identity. Its frozen exact certificate is in
[POINT_LINK_65_EXACT_UPPER_CERTIFICATE.json](data/scout/POINT_LINK_65_EXACT_UPPER_CERTIFICATE.json).
For an equality A_i x=b_i, its multiplier w_i is free in sign; for a
<= row require w_i>=0. With S=10^9 and
`R_j=max(0,S c_j-sum_i w_i A_ij)`, the same expansion as Lemma 8 gives
`S F2<=sum_i w_i b_i+sum_j R_j U_j`.

Full exact replay gives

```
S=1000000000
sum_i w_i b_i=-1210499996608
sum_j R_j U_j=867398                   (26 positive columns)
H=-1210499996608+867398=-1210499129210
H/S=-121049912921/100000000 <0          (divide both by 10)
```

The three cut multipliers are 11750000000,6000000000,1000000000 in the
tight-point,tight-intersection-two,tight-intersection-three order.
All are nonnegative. Equalities permit signed weights. Every multiplier,
positive residual and finite correction is checked with exact integers.
The negative upper bound contradicts F2=0. Padding in Lemma 2 excludes
all complete sizes <=65, proving the same local bound 66. This route
uses neither Lemma 11's avoidance cap nor Pētā's envelope; its shared
premises with the analytic route are explicitly listed in the dependency
map.

## 18. Theorem: either 223 route lifts to C(54,16,4)>=223

For each point x of a complete target cover, its link covers all triples
on the other 53 points: adjoining x to any triple forms a covered
quadruple. The link has 15-element blocks. By either Theorem 14 or 17,
its occurrence count r_x>=66. If the target has B occurrences,

`16B=sum_x r_x>=54*66=3564`.

Since `16*222=3552<3564<=3568=16*223`,
`B>=ceil(3564/16)=223`. This is a lower bound, not an exact covering
number. It neither supplies a 335-block cover nor excludes any size >=223.
The existing 336 construction and its credit to Franco Atzeni remain
external comparison context. Qualified researcher verification remains
pending for submission to a maintained covering table.
