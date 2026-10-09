# Proposed Pētā point-link proof: C(54,16,4) >= 223

2026-10-08 UTC. Complete analytic proof for parent semantic review.
“Pētā” is a working name. Literature priority and outside correctness review
are unresolved. The canonical/public bounds are not edited by this packet.

We prove the stronger local statement **C(53,15,3)>=66**, then use point
counting. Block occurrences may repeat throughout the argument, so the
statement also applies to distinct blocks. No finite pool, parent, pairing,
symmetry or search-neighborhood restriction is used.

## 1. Published dependency and elementary local floors

[Horsley, Theorem 1](https://arxiv.org/html/1409.0485v3), at v=52,k=14,
lambda=1, uses 51=4*13-1, r=4,d=1, with d<r-lambda. It gives

    C(52,14,2) >= ceil(52*5/15) = 18.                       (1)

In any complete C(53,15,3) covering, deleting a point from its containing
blocks gives C(52,14,2). Hence every point degree r_y is at least 18.
Every pair degree m_yz is at least ceil(51/13)=4, by covering its 51 outside
extensions. Point counting already gives b>=ceil(53*18/15)=64.
It therefore suffices to exclude b=64 and b=65.

## 2. A tight point has exactly one repeated partner

Consider a complete C(52,14,2) covering. If a point q has degree four,
its four containing blocks have 4*13=52 outside incidences covering 51
other points. Exactly one other point occurs twice, and every other point
occurs once. Thus its codegree with another point is at most two, and
exactly one other point has codegree two. Call that point its repeated
partner. This argument remains valid with repeated block occurrences.

## 3. Avoidance lemma: a 19-block pair link has point degree at most 15

Assume the pair covering in section 2 has 19 blocks, and a point p has
degree m>=16. Necessarily m<=19. Let a be the number of degree-four
points other than p. All other point degrees are at least four, and all
non-tight points have degree at least five. The incidence total gives

    19*14 - m >= 4*a + 5*(51-a) = 255-a,
    a >= m-11 >= 5.                                         (2)

There are s=19-m<=3 blocks avoiding p. Each tight point q has codegree
with p at most two, so it occurs in at least two of those avoiding blocks.

If s<=1 this is impossible. If s=2, every tight point occurs in both
avoiding blocks and twice with p. Its repeated partner is therefore p.
Two such tight points would share both avoiding blocks, giving another
repeated partner. Thus there can be at most one, contradicting a>=5.

Now let s=3. If a tight point q occurs in all three avoiding blocks, it
shares at least two of them with every other tight point. Each of those
other points would have codegree at least two with q. Since q has only one
repeated partner, a<=2, again contradicting a>=5.

Consequently every tight point occurs in exactly two avoiding blocks and
exactly two blocks containing p, and has repeated partner p. Two tight
points cannot occupy the same two avoiding blocks. There are only
C(3,2)=3 such supports, so a<=3, contradicting (2). This proves

    every point in a complete 19-block C(52,14,2) link
    has degree at most 15.                                 (3)

Scope: (3) concerns an arbitrary complete 19-block pair covering, not a
selected link in an incumbent. No assertion of sharpness or existence
at degree 15 is needed.

## 4. Tight pairs force exact block intersections in C(53,15,3)

Suppose a complete C(53,15,3) covering has b in {64,65} blocks. Let n_s
count unordered pairs of distinct block occurrences whose intersection
has size s, for s=0,...,15. Let p4 count point pairs of degree four.

Four blocks through such a pair cover all 51 outside points in 52
incidences. Exactly one outside point occurs twice. Five block pairs
therefore intersect in exactly the given two points, and one intersects
in a three-set. A size-two intersection can be assigned to only one
tight pair; a size-three intersection to at most three. Hence

    n_2 >= 5*p4,             3*n_3 >= p4.                  (4)

The integer polynomial P(s)=(s-6)(s-7) is nonnegative at every integer
s. Since P(2)=20 and P(3)=12, (4) implies

    H := sum_s P(s)*n_s - 104*p4 >= 0.                     (5)

This is the established intersection-polynomial framework, with the local
tight-pair assignments supplying the particular coefficient 104.

## 5. Express H as a sum of point contributions

Write r_y=18+d_y, d_y>=0. Point incidence counting gives

    D := sum_y d_y = 15*b-954 = 6 or 21,
    0<=d_y<=D,              18<=r_y<=39.                   (6)

For each point y let a_y count the pairs yz of degree four. Define

    f(m) = C(m,2) - 52*1[m=4],
    g_y = sum_{z!=y} f(m_yz) - 12*C(r_y,2).                (7)

The pair-degree load at y is

    sum_{z!=y} m_yz = 14*r_y,                              (8)

because each containing 15-block supplies fourteen pairs through y.
Also m_yz<=r_y by containment. Double-counting a point or a pair in two
block occurrences gives

    sum_s s*n_s = sum_y C(r_y,2),
    sum_s C(s,2)*n_s = sum_{y<z} C(m_yz,2).

As P(s)=2*C(s,2)-12*s+42 and sum_y a_y=2*p4, these identities imply

    H = 42*C(b,2) + sum_y g_y.                             (9)

The identities hold even for incomplete or repeated-block families.
Completeness was used for the floors and tight-link implications.

## 6. Three complete degree cases

**Case r_y=18.** There are 52 extensions with sum 252 and minimum degree
four. If a_y of them have degree four, then
252>=4*a_y+5*(52-a_y), so a_y>=8. For each integer 4<=m<=18,

    f(m) <= 11*m - 45 - 45*1[m=4].                       (10)

At m=4 this is equality. For 5<=m<=18, it is the chord inequality
C(m,2)<=11*m-45, with equality at the two endpoints. Thus

    sum f(m_yz) <= 11*252 - 45*52 - 45*8 = 72,
    g_y <= 72 - 12*C(18,2) = -1764.                     (11)

**Case r_y=19.** The link at y is a complete 19-block C(52,14,2)
covering. By (3), every m_yz<=15. For 4<=m<=15,

    f(m) <= (19*m-75)/2.                                 (12)

For 5<=m<=15 this is the chord of C(m,2) at 5 and 15. At m=4,
f(4)=-46<=1/2. Using (8),

    sum f(m_yz) <= (19*266 - 75*52)/2 = 577,
    g_y <= 577 - 12*C(19,2) = -1475
         = -1764 + 289.                                  (13)

**Case r_y=18+d, 2<=d<=21.** Put r=r_y. For 5<=m<=r the chord gives

    C(m,2) <= ((r+4)*m-5*r)/2.

At m=4, f(4)=-46 and the right side is (16-r)/2>=-23/2 since r<=39.
Therefore the same inequality holds for f at every permitted m. Summing
52 extensions with load 14*r yields

    sum f(m_yz) <= 7*r^2-102*r,
    g_y <= r^2-96*r = -1404-60*d+d^2.                    (14)

For every 2<=d<=21,

    (-1764+289*d)-(-1404-60*d+d^2)
      = (d-2)*(347-d)+334 > 0.                            (15)

Combining (11), (13) and (14)–(15) gives the universal envelope

    g_y <= -1764+289*d_y.                                 (16)

No degree case is omitted, and no real-valued empirical cap enters this
integer-degree argument.

## 7. Exact contradictions and the target recurrence

Summing (16), using 53 points and (6), and substituting into (9) gives

    0 <= H <= 42*C(b,2)-1764*53+289*(15*b-954).            (17)

For the only remaining two sizes:

| b | D | exact right side of (17) |
|---:|---:|---:|
| 64 | 6 | -7086 |
| 65 | 21 | -63 |

Both contradict H>=0. Consequently C(53,15,3)>=66.

Now let a complete C(54,16,4) covering have B block occurrences. Its
link at every point is a complete C(53,15,3) covering, so every point
degree is at least 66. Thus

    16*B >= 54*66 = 3564,
    B >= ceil(3564/16) = 223.                              (18)

This proves the stated proposed lower bound, conditional only on the
published dependency (1) and the complete elementary arguments above.
There is no 335 construction in this packet. No size >=223 is excluded.

## Provenance and verification limits

The local stage-01 LP led to the point-link attack but is not a dependency
of this short proof. The determinant obstruction is also unnecessary for
(17); it is preserved as a separate lemma. The essential new project
ingredient here is the avoidance proof (3), followed by the particular
local star envelopes and parameter substitution. These derivation facts
do not establish literature priority.

The underlying Gram/rank methods have Bose/Fisher/Horsley background;
intersection polynomials and moment identities have
[Cameron–Soicher](https://webspace.maths.qmul.ac.uk/l.h.soicher/designtheory.org/library/preprints/bip.pdf)
and [Soicher](https://webspace.maths.qmul.ac.uk/l.h.soicher/nbip2_v2.pdf)
prior art, including LP/IP formulations. No new framework is claimed.

Two separate implementations check all declared integer chord cases,
the complete small outside-support census, theorem-substitution arithmetic
and final contradictions. Those checks exercise calculations and coding;
the arbitrary-cover mapping and avoidance proof above require semantic
review. Outside human validation and novelty review remain outstanding.
