# Numbered semantic proof and exact parameter arithmetic

This exposition indexes and expands the frozen internally reviewed sources.
It adds no inequality to their models and changes no certificate value.
External expert acceptance, formal verification and priority are pending.
For the already-public 222 proof and the second exact 223 route, see the
complete [earlier numbered audit](../audit/PROOFS.md). The following route
proves the intermediate 223 statement analytically and then strengthens it.

## 1. Definition: the occurrence domain

A legal block is a 16-element subset of a labeled 54-point set V; points
inside it are distinct. A family B_1,...,B_b has indexed occurrences;
equal whole blocks at different indices are permitted. Completeness means
every four-element subset of V is contained in at least one occurrence.
Ruling out this larger repeated-occurrence domain also rules out distinct
block families in the usual definition of C(v,k,t). There is no restriction
to a selected pool, symmetry, construction, seed or neighborhood.

For a point subset T let d(T)=#{i:T subset B_i}. Write r_x=d({x}) and
lambda_xy=d({x,y}). Let n_s count unordered *different occurrence indices*
{i,j} with |B_i intersect B_j|=s. Include s=16. Equal subsets at different
indices contribute to n_16 and must never be discarded.

## 2. Lemma: links, incidence and universal moments

For T, the occurrences containing T, after removing its points, cover
all (4-|T|)-subsets outside T: adjoin T to such a subset and apply coverage.
Hence point links have parameters (53,15,3), pair links (52,14,2), and
triple links (51,13,1). Links retain occurrence indices.

For any uniform block family, including incomplete and repeated ones,

    sum_s C(s,j)n_s = sum_(|T|=j) C(d(T),2),
    sum_(|T|=j) d(T) = b C(16,j).

The first equation counts (T,{i,l}) with i<l and T inside both blocks;
the second counts (T,i). Its unrestricted degree domain is 0..b.
Restricted histogram ranges below require completeness and proved caps.
For a fixed pair, 52 triple extensions have degree load 14*lambda;
for a fixed triple, 51 quadruple extensions have load 13*d(T).

## 3. Lemma: C(52,14,2)>=18 without a table premise

Each point in a complete 52-point pair link has degree at least
ceil(51/13)=4 because 3*13=39<51<=52=4*13. A degree-four point has exactly
52 outside incidences covering 51 distinct points, so precisely one
partner has codegree two and all others codegree one. Let a points be
degree four among b occurrences. Other degrees are integers >=5, so

    14b >= 4a+5(52-a)=260-a;  a>=260-14b.

Among these a tight points the double-codegree relation is a matching A.
Their a-by-b incidence matrix X satisfies XX^T=3I+A+J, with J all ones.
For a nonzero real vector u, its quadratic form is

    2 sum u_i^2 + sum_isolated u_i^2
      + sum_matching_edges (u_i+u_j)^2 + (sum u_i)^2 >0.

Thus rank X=a<=b. For a=0, b>=a still holds and the incidence inequality
alone gives 14b>=260. In every case 15b>=260, and
15*17=255<260<=270=15*18 proves b>=18. Repeated columns cannot invalidate
the Gram identity or rank upper bound. This self-contained specialization
uses established rank methods; it asserts no new general rank theorem.

## 4. Lemma: single-surplus tight sets

Four occurrences through a tight pair in a (53,15,3) cover have 52
incidences outside that pair and must cover 51 distinct outside points.
One outside point repeats twice and the other 50 occur once. Of the six
occurrence pairs, five intersect in exactly the tight pair and one in a
triple. If p4 counts tight pairs, then n2>=5p4 and 3n3>=p4: a size-two
intersection contains one pair and a size-three intersection contains
three pairs. Larger intersections get no such tight charge.

Likewise a tight triple in the target has five containing-occurrence
pairs intersecting exactly in that triple and one in a quadruple. Thus
n3>=5t4 and 4n4>=t4, because a four-set has four triples. Its quadruple
extensions have degree only one or two. Two of the four tight occurrences
cannot be equal whole blocks: that would repeat thirteen outside points,
exceeding surplus one. Whole-block repetition elsewhere remains allowed.

## 5. Lemma: the complete 18/19-occurrence avoidance cap

In a complete (52,14,2) cover with b=18 or 19, suppose p has degree
m>=16. Let a count other points of degree four. Incidences off p give

    14b-m >= 4a+5(51-a)=255-a;
    a>=255-14b+m.

Every tight q has codegree(p,q)<=2, so at least two of its four
occurrences avoid p. Put s=b-m<=3. For s<=1 no tight q is possible;
for s=2 every q uses both avoiders and two p-occurrences, making p its
unique repeated partner. Two q would also share both avoiders and give
each a second repeated partner; hence a<=1. At b=18 the required a is
at least 255-252+16=19, and at b=19,s=2 it is at least 255-266+17=6.

Only b=19,m=16 gives s=3, requiring a>=5. If some tight q uses all
three avoiders, every other tight point shares at least two of them
with q. Unique repeated partnership allows at most one other point,
so a<=2. Otherwise every tight q uses exactly two avoiders and has
repeated partner p; two q cannot use the same avoider pair. Only
C(3,2)=3 pairs exist, so a<=3. Both contradict a>=5. These cases include
every m=16..b. The degree cap is therefore 15. Completeness, integer
degrees, four occurrences and one outside surplus are essential.

## 6. Theorem: the analytic child bound C(53,15,3)>=66

Assume a child covering of size <=65. It is nonempty; repeat one legal
block until exactly 65 occurrences remain. Each point link satisfies
Step 3, so r_y=18+d_y with d_y>=0 and

    sum d_y=65*15-53*18=975-954=21;
    0<=d_y<=21; 18<=r_y<=39; 4<=m_yz<=r_y.

Let P(s)=(s-6)(s-7). It is nonnegative at every integer s=0..15;
P(2)=20 and P(3)=12. Step 4 yields

    H=sum_s P(s)n_s-104p4>=0,
    20*5p4+12*(p4/3)=104p4.

Define f(m)=C(m,2)-52*[m=4] and
g_y=sum_(z!=y)f(m_yz)-12C(r_y,2). Since P(s)=2C(s,2)-12s+42,
Step 2 and sum_z m_yz=14r_y give

    H=42C(65,2)+sum_y g_y.

All local degrees fall into these three exhaustive cases:

* r=18: at least eight of the 52 pair degrees are four, since
  252>=4a+5(52-a)=260-a. On m=4..18,
  f(m)<=11m-45-45*[m=4]; for m>=5 the slack is
  (m-5)(18-m)/2>=0, and m=4 gives equality. Therefore
  g<=11*252-45*52-45*8-12*153
  =2772-2340-360-1836=-1764.
* r=19: Step 5 gives m<=15. For m=5..15,
  f(m)<=(19m-75)/2 with slack (m-5)(15-m)/2>=0;
  at m=4, f(4)=6-52=-46<=1/2. Hence
  g<=(19*266-75*52)/2-12*171
  =(5054-3900)/2-2052=577-2052=-1475=-1764+289.
* r=18+d, d=2..21: for m=5..r,
  f(m)<=((r+4)m-5r)/2 with slack (m-5)(r-m)/2>=0.
  At m=4 its slack is (108-r)/2>0 because r<=39.
  Thus g<=((r+4)*14r-5r*52)/2-12*r*(r-1)/2
  =r^2-96r=-1404-60d+d^2<=-1764+289d.
  The last upper-bound slack is
  -360+349d-d^2=(d-2)(347-d)+334>0 throughout d=2..21.

Summing g<=-1764+289d gives

    0<=H<=42*2080-1764*53+289*21
          =87360-93492+6069=-63,

a contradiction. The independently checked b=64 substitution is
42*2016-93492+289*6=84672-93492+1734=-7086. It is redundant to padding
to 65 but records the older analytic route completely. See the unchanged
[child semantic certificate](package/proof/CHILD_BOUND_66.md).

## 7. Corollary: the intermediate target lower bound 223

Every point link needs at least 66 occurrences by Step 6. Hence
16b>=54*66=3564. Since 16*222=3552<3564<=3568=16*223,
b>=223. This is a semantic child argument followed by incidence arithmetic;
it assumes none of the five target models below. The older independent
975-variable/156-row child certificate reaches the same intermediate
bound, with F2<=-121049912921/100000000; it remains in `audit/`.

## 8. Lemma: all 223-occurrence profiles, including their labels

Suppose b=223. Put d_x=r_x-66. Then sum d_x=223*16-54*66=4.
Nonnegative integer excess has precisely the partitions
4, 3+1, 2+2, 2+1+1 and 1+1+1+1: classify the largest positive part;
four leaves none, three leaves one, two leaves two or two ones, and
one requires four ones. Zeros fill the other point labels.

| Case | Degrees | Labeled assignments | First intersection moment |
| --- | --- | ---: | ---: |
| 4 | 66^53,70^1 | 54 | 53*2145+2415=116100 |
| 31 | 66^52,67^1,69^1 | 54*53=2862 | 52*2145+2211+2346=116097 |
| 22 | 66^52,68^2 | C(54,2)=1431 | 52*2145+2*2278=116096 |
| 211 | 66^51,67^2,68^1 | 54*C(53,2)=54*1378=74412 | 51*2145+2*2211+2278=116095 |
| 1111 | 66^50,67^4 | C(54,4)=316251 | 50*2145+4*2211=116094 |

The counts sum to 395010=C(57,4), the count of weak compositions of
four over 54 labels. This is analytic exhaustion, not enumeration of
395010 cover witnesses. Every case map uses the actual exceptional labels.
No fractional histogram is asserted to realize an integer cover.

## 9. Lemma: pair budgets and all high-subset caps

Define e_xy=lambda_xy-18>=0. Every occurrence through x contributes
15 incident pairs, giving S_x=sum_y e_xy=15r_x-53*18=36+15d_x.
The total edge excess is
223*C(16,2)-18*C(54,2)=26760-25758=1002.
Containment and nonnegativity give
e_xy<=min(S_x,S_y,48+min(d_x,d_y)).

If an s-set T has degree h>18, each of its s-1 edges through x spends
at least h-18, so (s-1)(h-18)<=S_x. Thus
h<=18+floor(S_x/(s-1)); for h<=18 this is automatic.
Normal-containing triples have degree <=36 and quadruples <=30.
Only case211's unique exceptional triple can exceed 36 there, and its
smallest budget 51 caps it at 18+floor(51/2)=43. In case1111 any two
exceptional triples share a point and their union spends at least
3*(37-18)=57>51 at it, so at most one has degree >=37. Its cap is 43.
The unique exceptional quadruple in case1111 has cap
18+floor(51/3)=35. Cases4,31,22 have no exceptional-only triple or quad;
case211 has no exceptional-only quad. These distinctions prevent missing
high-tail cases or transplanting stronger degree caps.

## 10. Definition: the complete necessary models

In each case count physical point subsets in p_e (pairs), t_m (triples),
q_h (quads), and J_(a,b,e) (pairs with actual endpoint excess classes a,b).
M_(e,m) counts pair/triple inclusions; N_(m,h) counts triple/quad inclusions.
n_s has s=0..16. All variables are nonnegative. Histogram cell bounds
are their full physical populations; J bounds use actual class-pair
populations; M<=52*1431=74412 and N<=51*24804=1265004.

Let Emax,Tmax,Qmax be the case caps. M has e=0..Emax and
m=4..min(Tmax,15 if e<=1 else 18+e). The 15 restriction is Step 5
applied to pair links of size 18 or 19. N has m=4..Tmax and
h=1..(2 if m=4 else min(m,Qmax)), by Step 4 and containment.
Full histograms have p e=0..Emax, t m=4..Tmax, q h=1..Qmax.

| Case | (Emax,Tmax,Qmax) | Endpoint classes (a,b): population/cap e |
| --- | --- | --- |
| 4 | (36,36,30) | (0,0):1378/36; (0,4):53/36 |
| 31 | (49,36,30) | (0,0):1326/36; (0,1):52/36; (0,3):52/36; (1,3):1/49 |
| 22 | (50,36,30) | (0,0):1326/36; (0,2):104/36; (2,2):1/50 |
| 211 | (49,43,30) | (0,0):1275/36; (0,1):102/36; (0,2):51/36; (1,1):1/49; (1,2):2/49 |
| 1111 | (49,43,35) | (0,0):1225/36; (0,1):200/36; (1,1):6/49 |

The [arithmetic index](ARITHMETIC_INDEX.json) supplies every family count,
row-family count, variable finite bound, coefficient position count and
exact certificate subtotal. Its independent closed-form generator is
[derive_arithmetic_index.py](derive_arithmetic_index.py). Full model equality
is also checked against all five independently reviewed reconstructors.

## 11. Lemma: every row family has an arbitrary-cover map

The nine base histogram rows are block-pair count, point moment, pair
count/excess/moment, triple count/load and quad count/load. Their constants
are C(223,2)=24753, the Step 8 moment, C(54,2)=1431, excess1002,
C(54,3)=24804 with load223*560=124880, and C(54,4)=316251 with
load223*1820=405860. Counts and moments follow from Step 2.

Three tight rows are n3-5t4>=0, 4n4-t4>=0 and M_(0,4)-8p0>=0.
The last follows because a degree-18 pair has 52 triple extensions,
load14*18=252, and degrees >=4: if a extensions are four then
252>=4a+5(52-a)=260-a, hence a>=8.

For each endpoint class, J counts exactly its physical population.
For every e, sum_(a,b)J_(a,b,e)=p_e. Weighted endpoint-class rows give
population(a)*S_a; an (a,a) pair contributes twice, an (a,b) pair with
a!=b once to each class. Their budgets are respectively
(1908,96), (1872,51,81), (1872,132), (1836,102,66), (1800,204).
Every same-class multiplicity and unique-class absence is essential.

For each e, sum_m M_(e,m)=52p_e and
sum_m m M_(e,m)=14(18+e)p_e; for each m,
sum_e M_(e,m)=3t_m. For each m, sum_h N_(m,h)=51t_m and
sum_h h N_(m,h)=13m t_m; for each h, sum_m N_(m,h)=4q_h.
The domain caps in Step 10 ensure every actual inclusion is retained.

Add sum_(m=37..43)t_m<=1 only in211/1111 and
sum_(h=31..35)q_h<=1 only in1111, justified by Step 9.
Define F3=sum_m C(m,2)t_m-sum_s C(s,3)n_s and
F4=sum_h C(h,2)q_h-sum_s C(s,4)n_s. Two defect equalities are
Fj=zjp-zjm with four nonnegative finite variables and objective
H=-(z3p+z3m+z4p+z4m). Their plus caps are population_j*C(maxdegree_j,2),
and minus caps C(223,2)*C(16,j). An actual cover takes every defect
variable zero by Step 2, hence H=0. Arbitrary relaxed points need not have
minimal defects or correspond to covers. The contradiction uses only
the forward mapping and the actual H=0 image.

## 12. Lemma: every endpoint threshold cut is necessary

For h>18, let T_h count actual distinct triples of degree >=h.
For a pair xy of excess e<h-18 no such extension is possible.
Otherwise let K_h(xy) count its high-triple extensions. Each distinct
third point z spends at least h-18 on a new edge xz and yz. The edge xy
already spends e at both endpoints, so

    K_h(xy)<=cap(a,b,e,h)
    =min(52,floor((36+15a-e)/(h-18)),
            floor((36+15b-e)/(h-18))).

Since sum_(x<y)K_h(xy)=3T_h, each model retains the row
sum_(a,b,e>=h-18)cap*J_(a,b,e)-3 sum_(m>=h)t_m>=0.
The complete threshold family is h=19..36 (18 rows) for4/31/22 and
h=19..43 (25 rows) for211/1111. Own-edge subtraction, threshold eligibility,
both endpoint budgets and integer floors cannot be omitted.

Case1111 also retains the earlier seven exceptional-only cuts h=37..43:
3T_h<=sum_(e>=h-18)J_(1,1,e). Step 9 supplies at most one high triple;
if one exists it uses three distinct exceptional pairs. This proof
requires uniqueness. The generic endpoint family alone requires no
disjointness. Separate threshold-36 center/diamond arguments in the
historical case drafts are not appended scalar rows and are not needed
for the certificates. In particular case4/31 allow shared centers and
case22 retains its raw exceptional endpoint capacity2; no stronger
coefficient is silently transplanted from another case.

## 13. Lemma: exact signed upper certificates with every correction

For rows l_i<=A_i x<=u_i, integer weights w_i and positive D, select u_i
for w_i>0 and l_i for w_i<=0. A lower-only row requires w_i<=0.
Let R_j=D*c_j-sum_i w_i A_ij for objective H=sum_j c_j x_j.
Using 0<=x_j<=U_j gives exactly

    D H <= sum_i w_i*selected_endpoint_i
             +sum_j max(R_j,0)*U_j.

Negative residuals contribute an upper bound zero; every positive one,
however small, uses its finite bound. No tolerance, solver status,
optimality claim or floating-point calculation is a premise.

| Case | Variables/rows | Signed row subtotal | Finite correction | Strict H upper (D=10^12) |
| --- | --- | ---: | ---: | --- |
| 4 | 1875/276 | -456886856276935 | 66263335 | -571108487517/1250000000 |
| 31 | 2404/318 | -284555555605155 | 88999769 | -142277733302693/500000000000 |
| 22 | 2402/319 | -132999999998810 | 42902437 | -132999957096373/1000000000000 |
| 211 | 2867/348 | -123951389013326 | 1345674378 | -30987510834737/250000000000 |
| 1111 | 2840/358 | -3333333540963 | 2180698965 | -1665576420999/500000000000 |

For each row the numerator is precisely subtotal+correction; division
by D and reduction gives the stated rational. The full residual maps
have137,126,56,551,658 positive columns respectively. All coefficients,
implicit zeros, domains, weights, residuals and exact values are checked.

## 14. Theorem: exclusion of 223 and the proposed lower bound 224

An arbitrary hypothetical 223-occurrence cover has exactly one of Step8's
profiles. Steps9-12 map it into that case with H=0. Step13 proves H<0
through its exact certificate, a contradiction in every case. No223
cover exists. Step7 has already excluded b<=222, so C(54,16,4)>=224.

Alternatively pad any smaller nonempty complete target family to223.
For p added copies of a fixed B0,

    n'_s=n_s+p*#{old i:|B_i intersect B0|=s}+C(p,2)*[s=16],
    d'(T)=d(T)+p*[T subset B0].

Both sides of the j-th moment gain
p*sum_(T subset B0,|T|=j)d(T)+C(p,2)*C(16,j).
Thus equal-block intersections and every moment remain valid. Padding
can change the excess partition; map the padded family to its resulting
case rather than retaining its earlier profile. This proof supplies no
224-block construction, no335 cover, no sharpness or exact value, and no
external review or literature priority certification.
