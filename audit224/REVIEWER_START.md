# Reviewer entry point: internally audited proposed lower bound 224

Prepared 8 October 2026 under Perry Kern's direction, with AI assistance by
Mopî, Pētā, the scout and the independent internal reviewer. The proposed
statement is **C(54,16,4) >= 224**. Qualified external mathematical review,
formal-kernel verification and priority remain pending. No upper-bound
construction or exact covering number is established here.

The public base commit `946f7ee8931ca9a3b64ef3f1c0f4b0a9fe803c35` contains
the 222 proof. The [older 222/223 audit](../audit/README.md) is retained;
223 is an internally audited intermediate result. The new 224 route first
proves C(53,15,3)>=66, lifts it to point degrees >=66, and rules out every
223-occurrence point-degree profile using five separately reconstructed
necessary-condition models and exact signed certificates.

1. Read [the numbered proof](STEP_BY_STEP_224.md), especially the repeated
   occurrence domain, avoidance cap, five-case exhaustion and cover-to-model
   implications. The compact child proof and every case source are included.
2. Inspect [dependencies and the assumption-to-code map](ASSUMPTION_CODE_MAP.md).
   Arithmetic replay checks the specified matrices; it does not by itself
   prove that their rows are necessary for every cover.
3. Check [enumeration universes and limits](ENUMERATIONS.md), then use the
   commands in [REPRODUCE.md](../REPRODUCE.md). Standard-library Python 3.10+
   suffices; no network, solver, package installation or account is needed.
4. Inspect the [frozen case ledger](package/CASE_LEDGER.json),
   [source transformations](package/PROVENANCE.json),
   [completed internal review](package/review/REVIEW_STATUS.md),
   [new test receipts](receipts/TEST_RECEIPT.json) and
   [dated prior-art search](prior_art/SEARCH_REPORT.md).
5. Check [changes and preservation](CHANGELOG.md) and the exact
   [publication manifest](../PUBLIC_MANIFEST.json). Pin its digest from the
   independent handoff; hashes are not signatures or mathematical acceptance.

The complete 48-file scout package is byte-preserved inside `package/`.
Its manifest SHA-256 is
`d5ebe7dba35a94b99675c670616a99c5d669760732b8f3e7cf9a935555a78308`.
Historical case drafts still say review was pending when written. The
included completed global review supersedes those historical status lines;
the drafts themselves were not rewritten. Its source verdict SHA-256 is
`52fa7ea04706173898c24d087df9d10ceb2a820bb93297d2ddf28a54329085b7`.

No prior 224-or-stronger result was identified in the recorded bounded
search. Table-access failures and unsearched representations prevent a
priority conclusion. General intersection-polynomial, moment, rank and
LP/IP methods are established prior art. “Pētā Method/Proof” is a working
label. Private correspondence is excluded and supplies no endorsement.

This packet is prepared for a separate final editorial review. It contains
no GitHub publication authorization or claim that publication occurred.
