# Compact semantic certificate for the proposed lower bound 223

Review draft. This is a mathematical proof with explicit semantic steps,
not a proof-assistant artifact, executable formal verification, literature
priority claim, or record certification. No solver or search result is a
premise. The argument applies to every complete covering in the stated
scope, not just a finite block pool.

**Statement.** Every family of 15-element subsets of a 53-element set
covering every triple has at least 66 block occurrences. Consequently,
every family of 16-element subsets of a 54-element set covering every
quadruple has at least 223 block occurrences. Whole blocks may repeat;
points inside a block are distinct.

## 1. The local floor 18

Every complete pair covering on 52 points with 14-element blocks has at
least 18 block occurrences. Here is a short derivation at these parameters.

Every point has degree at least `ceil(51/13)=4`. Suppose there are b
occurrences, and a points have degree 4. The incidence count gives

`14b >= 4a+5(52-a)`, hence `a>=260-14b`.

A degree-four point covers the other 51 points in 52 incidences. Pair
coverage forces exactly one other point to occur twice and all others once.
Among the a degree-four points, the codegree-two edges therefore form a
matching, with adjacency matrix A. Let X be their point-by-occurrence
incidence matrix. Its Gram matrix is

`XX^T=3I+A+J`.

For every nonzero real vector x,

`x^T(3I+A+J)x = 2 sum_i x_i^2 + sum_isolated x_i^2
                + sum_edges (x_i+x_j)^2 + (sum_i x_i)^2 > 0`.

Thus X has row rank a, so `b>=a>=260-14b`. Therefore `15b>=260`, and
`b>=18`. If a=0, incidence counting itself gives the same conclusion.
Repeated block columns do not invalidate the Gram or rank argument.

## 2. Padding, degree domains, and tight pairs

Suppose the stated triple covering has at most 65 blocks. It is nonempty;
repeat an existing block until there are exactly 65 occurrences, keeping
distinct indices for repetitions. Each point link is a complete pair
covering from step 1, so every point degree r_y is at least 18. Set

`r_y=18+d_y`, `sum_y d_y=65*15-53*18=21`.

Therefore each `d_y` is an integer in `0..21` and `r_y<=39`. Every pair
degree m_yz is at least `ceil(51/13)=4` and at most r_y.

Call a pair tight if its degree is 4, and let p4 count tight pairs. The
four blocks containing a tight pair cover 51 outside points with 52
incidences. Exactly one outside point occurs twice; every other occurs
once. Of the six unordered pairs of these block occurrences, five
intersect in precisely the tight pair and one in precisely three points.

Let n_s count all unordered pairs of occurrence indices with intersection
size s, for `s=0..15`. A size-two intersection can be charged by just one
tight pair; a size-three intersection by at most three. Hence

`n_2>=5p4`, `3n_3>=p4`.                                      (A)

These charge bounds use exact intersections. Identical blocks are counted
at s=15, and receive no tight-pair charge.

## 3. The avoidance cap for a 19-block point link

Consider any complete pair covering on 52 points by 19 occurrences of
14-element blocks. Suppose a point p has degree m>=16. Let a count the
other points of degree 4. All remaining point degrees are at least 5, so

`266-m >= 4a+5(51-a)`, and `a>=m-11>=5`.

Each degree-four point q has exactly one codegree-two partner and no
codegree exceeding 2, by the one-surplus argument in step 1. There are
`s=19-m<=3` occurrences avoiding p. Each q uses at least two of them.

If s<=1, no such q exists. If s=2, each q uses both avoiding occurrences
and two containing p, making p its repeated partner. Two such q would
also share both avoiding occurrences, contradicting uniqueness. Thus a<=1.

If s=3 and some q uses all three avoiding occurrences, it shares at least
two with every other tight point. Uniqueness allows at most one other
tight point, contradicting a>=5. Hence every q uses exactly two avoiding
occurrences and two containing p, again with repeated partner p. No two
can have the same outside pair. There are only three such pairs, so a<=3,
another contradiction.

All possible `m=16,17,18,19` are excluded. Every point degree in a
complete 19-occurrence pair link is consequently at most 15.

## 4. A nonnegative intersection expression

For integer s, `P(s)=(s-6)(s-7)>=0`. Since `P(2)=20`, `P(3)=12`, (A)
implies

`H := sum_s P(s)n_s - 104p4 >= 0`.                          (B)

Define

`f(m)=C(m,2)-52*[m=4]`,
`g_y=sum_{z!=y} f(m_yz)-12C(r_y,2)`.

Each containing block contributes fourteen neighbors at y, so

`sum_{z!=y}m_yz=14r_y`.

Counting two occurrence indices containing a point or a point-pair gives

`sum_s s*n_s=sum_y C(r_y,2)`,
`sum_s C(s,2)n_s=sum_{y<z} C(m_yz,2)`.

Using `P(s)=2C(s,2)-12s+42`, and counting each tight pair at its two
endpoints, these identities give exactly

`H=42C(65,2)+sum_y g_y`.                                   (C)

These identities count occurrences, including equal block sets.

## 5. Three complete local degree cases

For `r_y=18`, its 52 pair degrees sum to 252. If a_y are 4, then
`252>=4a_y+5(52-a_y)`, so `a_y>=8`. On `4<=m<=18`,

`f(m)<=11m-45-45*[m=4]`.

At m=4 this is equality; for `5<=m<=18`, the slack is
`(m-5)(18-m)/2>=0`. Summation gives

`g_y<=11*252-45*52-45*8-12C(18,2)=-1764`.

For `r_y=19`, its link is precisely a pair cover of the type in step 3,
so all `m_yz<=15`. For `5<=m<=15`,

`f(m)<=(19m-75)/2`,

with slack `(m-5)(15-m)/2>=0`; at m=4 the inequality also holds since
`-46<=1/2`. Thus

`g_y<=(19*266-75*52)/2-12C(19,2)=-1475=-1764+289`.

For `r_y=18+d`, `2<=d<=21`, put r=r_y. For `5<=m<=r`,

`f(m)<=((r+4)m-5r)/2`,

with slack `(m-5)(r-m)/2>=0`. At m=4, its slack is `(108-r)/2>0`
because r<=39. Summing the 52 terms of total load 14r gives

`g_y<=r^2-96r=-1404-60d+d^2`.

The difference from `-1764+289d` is

`(d-2)(347-d)+334>0` for `2<=d<=21`.

Therefore every permitted degree satisfies

`g_y<=-1764+289d_y`.                                       (D)

## 6. Contradiction and lifting

From (B)–(D) and `sum d_y=21`,

`0<=H<=42*2080-1764*53+289*21
      =87360-93492+6069=-63`.

This is impossible. Padding therefore excludes every triple covering of
size at most 65, proving the first statement.

For a complete quadruple covering on 54 points with B occurrences of
16-blocks, its link at every point covers all triples on the remaining
53 points: adjoining that point to any triple produces a covered
quadruple. Each point degree is at least 66. Consequently

`16B>=54*66=3564`, so `B>=ceil(3564/16)=223`.

This proves only the stated lower bound. It supplies no construction,
sharpness, novelty, or maintained-table status.
