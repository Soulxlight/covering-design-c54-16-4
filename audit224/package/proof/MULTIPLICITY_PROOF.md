# Independent derivation and scope of the new multiplicity restrictions

This proof does not infer feasibility or infeasibility from numerical LP
output. Points inside a block are distinct; whole block occurrences may
repeat. Degrees and intersections count occurrence indices.

## Assumptions and local floors

The reviewed child theorem says every complete covering of triples on 53
points by 15-element blocks has at least 66 occurrences. Its reviewed proof
allows repeated occurrences. In a complete quadruple covering on 54 points,
adjoining a fixed point to any outside triple shows its point link is such
a child covering. Thus every point degree is at least 66. This is the
existing reviewed theorem, not a new result of this pass.

For completeness, the pair-degree floor 18 can be derived directly.
Fix a pair; its containing blocks, with that pair removed, cover every
pair on the remaining 52 points with 14-element blocks. Suppose this link
has b occurrences. Every point has degree at least ceil(51/13)=4.
Let a points have degree four. Incidence counting gives a >= 260-14b.
A degree-four point covers the other 51 points in 52 incidences, so exactly
one partner has codegree two and every other codegree is one. Among the
a tight points these double-codegree edges therefore form a matching A.
For their point-by-occurrence incidence matrix X,

    X X^T = 3 I + A + J.

For any nonzero vector u the corresponding quadratic form is

    2 sum u_i^2 + sum_isolated u_i^2
      + sum_matching_edges (u_i+u_j)^2 + (sum u_i)^2 > 0.

Thus X has row rank a and b >= a >= 260-14b. This gives b >= 18.
If a=0, the incidence inequality itself gives b>=ceil(260/14)=19.
Identical block columns do not affect this proof. Hence every original
pair has degree lambda_xy >= 18. Independently, each triple has degree
at least ceil(51/13)=4 and each quadruple has degree at least one.

If a target covering has fewer than 223 occurrences, repeat an existing
block until it has exactly 223. It is nonempty by coverage. Padding keeps
all local links complete. The following restrictions concern this padded
size, without imposing distinctness or symmetry.

## Excess graph: a second double-counting derivation

At size 223 put d_x=r_x-66. These are nonnegative integers with

    sum d_x = 223*16-54*66 = 4.

The five partitions are 4, 3+1, 2+2, 2+1+1, and 1+1+1+1. There are at
least 50 normal points with d_x=0; no point has degree above 70.
Set e_xy=lambda_xy-18. Each occurrence containing x contributes 15
pairs through x, so its weighted excess degree is exactly

    S_x=sum_(y!=x)e_xy = 15r_x-53*18 = 36+15d_x.

The total edge excess is 223*C(16,2)-18*C(54,2)=1002. Nonnegativity
and containment give e_xy<=min(S_x,S_y,48+min(d_x,d_y)).

Consider an s-element set T, s>=2, contained in h occurrences. Fix x in T.
Those same h occurrences contain every pair xy with y in T minus x.
If h>18, each of these s-1 distinct edges has e_xy>=h-18. Consequently

    (s-1)(h-18) <= S_x,
    h <= 18+floor(S_x/(s-1)).

When h<=18 the last inequality is automatic. This uses the actual shared
point labels and integer h. No average degree, independent histogram,
fractional realizability, or optimal-pairing assumption enters the proof.

## Triple restriction

A triple containing any normal point has degree at most 18+floor(36/2)=36.
Therefore every triple with degree at least 37 consists of exceptional
points. The first three degree partitions have fewer than three such
points, so no such triple exists. The 2+1+1 partition has just one possible
exceptional triple; its least exceptional degree has d=1, giving cap 43.

In the four-ones partition every exceptional point has S=51. If two
distinct triples on those four points both had degree at least 37, pick
a point in their intersection. Their union supplies three distinct edges
at that point, each with excess at least 37-18=19. This requires S>=57,
contradicting S=51. Thus there is at most one high triple in every case,
and its degree is at most 18+floor(51/2)=43.

The strict threshold is integral: "above 36" means degree at least 37.
The proof excludes two high triples; it does not assert one can exist.

## Quadruple restriction

A quadruple containing a normal point has degree at most
18+floor(36/3)=30. An exceptional-only quadruple is possible solely in the
four-ones partition, is unique, and has degree at most
18+floor(51/3)=35. Hence at most one quadruple can have degree above 30.
These facts hold for arbitrary legal coverings, including repeated blocks.

## Missing structural coupling in the present relaxation

The aggregate transport M records pair/triple incidences without the
endpoint classes recorded by J. A triple above 36 must use three actual
exceptional pairs, each with edge excess at least 19. Since there is at
most one high triple, the following is a necessary shared-label condition
in either case permitting a high triple:

    3 * sum_(m>=37)t_m
      <= sum_(exceptional endpoint classes a,b; e>=19) J_(a,b,e).

For any threshold h in 37..43, replace m>=37 and e>=19 by m>=h and e>=h-18.
This inequality follows from the same occurrence subset and at-most-one
argument. It was not a row of the frozen Pass 24 model. This pass may
evaluate it on the saved and corrected profiles, but makes no new solve
or global exclusion using it. Class-aware triple/pair incidence transport
and weighted triangle realization are materially different ingredients
from independently rounding or refining the existing histograms.

