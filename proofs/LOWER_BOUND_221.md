# Global counting proof: C(54,16,4) >= 221

This proof concerns every complete covering, with no finite block pool,
specified parent, pairing or search neighborhood. Repeated blocks do not
invalidate the argument. It does not exclude any size from221 through335.
Its mathematical novelty in the literature has not been established.

The use of block-intersection polynomials and moment counts builds on
[Cameron--Soicher (preprint dated 2006)](https://maths.qmul.ac.uk/~leonard/bip.pdf) and
[Soicher (2010)](https://webspace.maths.qmul.ac.uk/l.h.soicher/nbip2_v2.pdf).
The latter also treats binomial moment identities and LP/IP methods.
This proof claims only the stated parameter-specific inequality; see
[the citation notes](../CITATIONS.md).

## Established local floors

[Horsley's Theorem1](https://arxiv.org/html/1409.0485v3) states that a pair
covering has at least ceil(v*(r+1)/(k+1)) blocks if
v-1=r*(k-1)-d and0<=d<k-1 and d<r-1. At(v,k)=(52,14), r=4,d=1 satisfy
the hypotheses; the bound is ceil(260/15)=18.

Let B be a complete (54,16,4) covering with b blocks. Denote point degrees
by r_x, pair degrees by lambda_xy, and triple degrees by mu_T. Every pair
link is a (52,14,2) covering, so lambda_xy>=18. Counting pairs through x
then gives15*r_x>=53*18=954, hence r_x>=64. Thus b>=216.
Every triple needs four blocks because it has51 outside points and each
block covers13 of them; hence mu_T>=4.

## Tight triples force exact block intersections

Let t4 count the triples with degree exactly4, and let n_s count unordered
pairs of block occurrences whose intersection has size s.

For a degree4 triple T, the four blocks through it cover all51 outside
points using52 outside incidences. Exactly one outside point occurs twice
and every other outside point once. Of the six unordered block pairs,
exactly five intersect in T alone and exactly one intersects in T plus
that repeated point. An intersection3 pair determines a unique T, while
an intersection4 pair has only four common triples. Therefore

```text
n_3 >= 5*t4,                 4*n_4 >= t4.                  (1)
```

Let p0 count the point pairs with degree exactly18. Through such a pair,
the52 triple extensions have degrees>=4 and sum18*14=252. If z have
degree4, the sum is at least4*z+5*(52-z)=260-z; hence z>=8. Each degree4
triple contains only three point pairs, so

```text
3*t4 >= 8*p0.                                                (2)
```

The polynomial P(s)=(s-6)*(s-7) is nonnegative at every integer s. Since
P(3)=12 and P(4)=6, equations(1) and(2) give

```text
sum_s P(s)*n_s >= 12*n_3+6*n_4
                   >= (123/2)*t4 >= 164*p0.                 (3)
```

## Point and pair moments contradict small b

Suppose216<=b<=220 and put j=b-216. Write r_x=64+delta_x and
lambda_xy=18+e_xy. These excesses are nonnegative integers. Set
D=sum_x delta_x and E=sum_{x<y} e_xy. Exact incidence counts give

```text
D = 16*j,                  E = 162+120*j.
```

Because lambda_xy<=min(r_x,r_y) and delta_x+delta_y<=D,

```text
0 <= e_xy <= 46+floor(D/2) = 46+8*j <= 78 < 164.              (4)
```

For each integer e in this range,

```text
e^2 + 164*1[e>0] <= 165*e.                                   (5)
```

For e=0 this is equality; for e>0 it is equivalent to
(e-1)*(e-164)<=0. Thus, if m counts pairs with positive excess,
sum e^2+164*m<=165*E, and p0=1431-m.

Let N=binom(b,2), S1=sum_s s*n_s and M2=sum_s binom(s,2)*n_s.
Double counting and r_x>=64 imply

```text
S1 = sum_x binom(r_x,2)
   = 108864+64*D+sum_x binom(delta_x,2) >= 108864+1024*j.
2*M2 = sum_{x<y} lambda_xy*(lambda_xy-1)
     = 437886+35*E+sum e^2.
sum_s P(s)*n_s = 2*M2-12*S1+42*N.
```

Combining these identities with(5) yields

```text
sum_s P(s)*n_s - 164*p0
  <= 203202+200*E-12*S1+42*N
  <= -95526+20763*j+21*j^2.                                  (6)
```

For j=0,1,2,3,4, the last expression is respectively

```text
-95526, -74742, -53916, -33048, -12138.
```

Every value is negative, contradicting(3). No complete covering can have
216 through220 blocks; the established point floor excludes smaller b.
Consequently C(54,16,4)>=221. QED.

The proof uses only the cited pair-covering theorem, integrality and explicit
counting. The accompanying independent audits verify the arithmetic and
exercise the tight-triple lemma on raw inputs and complete link fixtures.
They are reproducibility checks, not a substitute for the semantic proof.
