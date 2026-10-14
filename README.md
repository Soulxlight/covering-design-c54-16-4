# Bounds and a verified335-block cover for C(54,16,4)

The project records **internally reviewed lower bound230 and verified upper bound335**. The
[reviewer entry point](audit230/REVIEWER_START.md) presents the complete internally
reviewed computer-assisted proof **C(54,16,4)>=230**. Qualified external human
acceptance, proof-assistant verification and literature priority remain pending.
The research, manuscript and independent internal review used AI assistance
under Perry Kern's direction. No exact covering number or optimality is claimed.

## Verified upper bound335

The exact [cover-335.txt](data/cover-335.txt) has335 distinct legal16-subsets of
1..54 and covers all316251 quadruples. Its16415 bytes have SHA256
`f00db8b4253b98fecf412031948e7de4e5c5f78a9cc021ef483bb01ea9d84bc8`.
[Two independent exhaustive verifiers and their results](upper335/README.md)
reproduce C(54,16,4)<=335. Perry Kern directed the AI-assisted work and supplied
the final file; Grok's final two-hole repair is credited according to Perry's
account. Construction ancestry beyond that account remains undocumented.
Curator submission is sent; acceptance is not confirmed at this publication.

## Retained lower-bound work

The proof first excludes every indexed 18-occurrence (52,14,2) pair cover,
permitting repeated whole rows, then proves C(52,14,2)>=19 by padding. Point-link
counting gives C(53,15,3)>=68 and the target230. Its complete 70 macro cases,
574 joint types and 15 binary-containment refinements have independently
reconstructed coefficients and row maxima. The weakest exact rank gap is
686878/1225. No numerical optimizer, target-cover search, previous 224 theorem
or later local research is a premise. Read the [full proof](audit230/PROOF.md),
[case ledger](audit230/CASE_LEDGER.md) and [review scope](audit230/REVIEW_STATUS.json).

The [published 224 release](https://github.com/Soulxlight/covering-design-c54-16-4/commit/5c586365ebba71fcf7aa2adf35ae1b48a82c76f4)
and earlier [222/223 audit](audit/README.md) remain available. Their mathematical
data, proofs and checkers are unchanged. The [224 audit](audit224/REVIEWER_START.md)
retains all five exact certificates. Entry-point documents and integrity indexes
are refreshed for this update, with a [transparent change log](audit230/CHANGELOG.md).

`C(v,k,t)` minimizes k-subsets covering every t-subset of a v-point set. These
proofs permit repeated whole blocks as indexed occurrences, a larger domain;
points inside a block remain distinct. There are 316251 target quadruples.
Exact arithmetic supports ordinary semantic proofs; it is not a proof-assistant
kernel or qualified-human endorsement. Checks cannot alone prove the
cover-to-model implications.

The previous upper336 and **Franco Atzeni** credit are retained as historical
[Covering Repository](https://coveringrepository.com/systems.aspx?li=2) context.
The new335 witness is independently verified here. Repository-curator acceptance
and literature priority remain separate, unconfirmed statuses. [Citations](CITATIONS.md) and the retained
[dated search](audit224/prior_art/SEARCH_REPORT.md) state attribution and access
limits. General rank, projection, moment and point-link methods have prior art;
parameter-specific priority is unresolved.

Use standard-library Python 3.10+ and [REPRODUCE.md](REPRODUCE.md). The complete
[public manifest](PUBLIC_MANIFEST.json) and [checksum index](PUBLIC_SHA256SUMS)
bind the publication whitelist; externally pin the manifest and inspect the code.
The legacy 38-path audit and 48-file scout packet retain their declared subset
domains. Frozen generation-era flags are explained separately from current review.

Project-owned code and documentation use the unchanged [MIT license](LICENSE),
copyright2026 Perry Kern. Third-party sources retain their rights. No private
correspondence, session record or unrelated private investigation is published.
"Peta Method/Proof" is a working label and makes no priority claim.
