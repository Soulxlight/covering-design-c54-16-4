# Proposed lower-bound proofs for C(54,16,4)

The [reviewer entry point](audit224/REVIEWER_START.md) presents an internally
audited proposed proof **C(54,16,4)>=224**. Qualified external review,
formal-kernel verification and literature priority remain pending. Research,
proof drafting and release preparation used AI assistance under Perry Kern's
direction. No exact covering number or335-block construction is claimed.

The public base commit `946f7ee8931ca9a3b64ef3f1c0f4b0a9fe803c35` already
contains the222 proof. Its frozen numerical data, original verifier, tests
and proofs are unchanged. The [retained222/223 audit](audit/README.md)
adds full semantic exposition and two proposed223 routes. The new224 proof
excludes all five223-occurrence point-degree profiles with independent
coefficient reconstructions and exact signed certificates.

`C(v,k,t)` minimizes k-subsets covering every t-subset of a v-point set.
The proofs allow repeated whole blocks as indexed occurrences, a larger
domain; points within each block remain distinct. There are316251 target
quadruples. The target theorem is an ordinary mathematical implication
with exact arithmetic support, not a proof-assistant result or human
endorsement. Arithmetic checks cannot alone prove the cover-to-model maps.

The previously recorded upper336 and **Franco Atzeni** credit are retained
as historical [Covering Repository](https://coveringrepository.com/systems.aspx?li=2)
context. The filtered target table was inaccessible during fresh checking.
This packet contains no upper-bound witness and does not certify its current
table status. The [citations](CITATIONS.md) and [dated search](audit224/prior_art/SEARCH_REPORT.md)
state exact attribution and access limits. General rank, intersection-polynomial,
moment and LP/IP methods have prior art; parameter-specific priority is unresolved.

Use standard-library Python 3.10+ and the commands in [REPRODUCE.md](REPRODUCE.md).
The complete [publication manifest](PUBLIC_MANIFEST.json) and
[checksum index](PUBLIC_SHA256SUMS) identify the reviewed whitelist.
The earlier audit's manifest/checksum index covers its fixed historical
subset; the48-file scout224 packet retains its own byte-identical manifest.

Project-owned code and documentation use the unchanged [MIT license](LICENSE),
copyright2026 Perry Kern. Third-party sources retain their rights. No private
correspondence is reproduced or treated as validation. “Pētā Method/Proof”
is a working label, not a claim of priority.
