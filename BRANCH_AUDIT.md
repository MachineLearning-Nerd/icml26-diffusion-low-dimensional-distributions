# Branch audit

The live GitHub repository has exactly 31 branches. The names below are the
clean public names; the complete former-to-clean mapping is preserved in
branch-audit.md.

## Trusted release

| Branch | Role |
| --- | --- |
| main | Trusted local-only release and current official 2/10 status. |

## Audit branches

| Branch | What it records |
| --- | --- |
| audit/baseline-reproduction | Baseline judged reproduction and runtime/report cleanup. |
| audit/claim-1-proof-chain | Claim 1 conditional proof-chain audit. |
| audit/claim-1-reverse-sde | Claim 1 one-dimensional faithful reverse-SDE study. |
| audit/claim-1-threshold-escape | Claim 1 threshold-escape stability diagnostic. |
| audit/claim-2-proof-certificate | Claim 2 conditional intrinsic-score proof certificate. |
| audit/claim-2-component-scaling | Claim 2 source-faithful component-scaling study. |
| audit/claim-3-identifiability-counterexample | Claim 3 exact-recovery and identifiability route. |
| audit/claim-4-atomic-weak-regularity | Claim 4 paper-scale atomic weak-regularity study. |
| audit/claim-5-proof-chain | Claim 5 primary cited-rate proof-chain certificate. |
| audit/claims-1-4-threshold-escape | Combined Claim 1 and Claim 4 threshold-escape package. |
| audit/evaluator-blind-review-round-1 | First evaluator-blind candidate review. |
| audit/evaluator-blind-review-round-1-2 | Follow-up evaluator-blind candidate review. |
| audit/review-harness-fix | Blind-review harness scope fix. |
| audit/claim-2-proof-dependency-mixture | Local Claim 2 conditional proof-dependency mixture audit. |

## Release and presentation branches

| Branch | What it records |
| --- | --- |
| release/claim-2-combined-evidence | Claim 2 evidence assembled for evaluator visibility. |
| release/claim-3-evidence | Claim 3 evidence assembled for evaluator visibility. |
| release/claim-4-evidence | Claim 4 evidence assembled for evaluator visibility. |
| release/claim-5-evidence | Claim 5 evidence assembled for evaluator visibility. |
| release/poster-concise-layout | Concise current poster layout checkpoint. |
| release/poster-checksum-gates | Current poster checksums and full gate run. |
| release/evaluator-visible-candidate-fixes | Candidate fixes exposed for evaluator review. |
| release/exact-published-revision | Exact published Space revision verification. |
| release/final-release-red-team | Final release candidate and recorded red-team review. |
| release/linux-poster-dependencies | Linux poster dependencies and current evidence. |
| release/poster-gate-diagnostics | Poster-gate diagnostic after scientific acceptance. |
| release/poster-advisory-current | Current-poster advisory cleanup. |
| release/poster-advisory-final-phrase | Final phrase advisory cleanup. |
| release/poster-advisory-final-wording | Final wording advisory cleanup. |

## Provenance-only quarantine branches

| Branch | Purpose |
| --- | --- |
| quarantine/remote-1e41143 | Rejected remote candidate retained for provenance; never publish. |
| quarantine/remote-57cc883 | Rejected remote candidate retained for provenance; never publish. |

The quarantine branches are intentionally retained and are not evidence
release candidates. Their histories are included in attribution checks, but
their candidate verdicts cannot override main.

## Topology invariants

- Expected live branch count: 31, including main.
- No old orx/* branch remains.
- No old work/* branch remains.
- Exactly two quarantine/* branches remain.
- main is the GitHub default branch.
- Reachable author and committer identity is
  MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>.

verify_final.py checks these invariants against the live origin, not only
against local branch names.
