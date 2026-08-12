# Branch and attribution audit

Former repository name: `icml26-repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions`

Target repository name: `icml26-diffusion-low-dimensional-distributions`

The original remote exposed 31 branches: `main`, 27 `orx/*` branches, two
quarantine branches, and one `work/*` branch. The table below gives every
branch a descriptive name while preserving its checkpoint tip and purpose.
These branches are historical evidence snapshots; they are not all ancestors
of the final `main` release.

## Complete branch mapping

| Former branch | Clean branch | What it records |
| --- | --- | --- |
| `main` | `main` | Trusted local-only release and current official 2/10 status. |
| `orx/baseline-judged-0-10-reproduction` | `audit/baseline-reproduction` | Baseline judged reproduction and runtime/report cleanup. |
| `orx/claim-1-route-1-proof-chain-and-external-converg` | `audit/claim-1-proof-chain` | Claim 1 conditional proof-chain audit. |
| `orx/claim-1-route-2-faithful-one-dimensional-reverse` | `audit/claim-1-reverse-sde` | Claim 1 one-dimensional faithful reverse-SDE study. |
| `orx/claim-1-route-2-threshold-escape-falsification-c` | `audit/claim-1-threshold-escape` | Claim 1 threshold-escape stability/falsification diagnostic. |
| `orx/claim-2-conditional-intrinsic-score-proof-certif` | `audit/claim-2-proof-certificate` | Claim 2 conditional intrinsic-score proof certificate. |
| `orx/claim-2-evaluator-visible-combined-evidence` | `release/claim-2-combined-evidence` | Claim 2 evidence assembled for evaluator visibility. |
| `orx/claim-2-faithful-component-scaling-study` | `audit/claim-2-component-scaling` | Claim 2 source-faithful component-scaling study. |
| `orx/claim-3-evaluator-visible-evidence` | `release/claim-3-evidence` | Claim 3 assumption evidence assembled for evaluator visibility. |
| `orx/claim-3-exact-recovery-identifiability-counterex` | `audit/claim-3-identifiability-counterexample` | Claim 3 exact-recovery/identifiability counterexample route. |
| `orx/claim-4-evaluator-visible-evidence` | `release/claim-4-evidence` | Claim 4 weak-regularity evidence assembled for evaluator visibility. |
| `orx/claim-4-paper-scale-atomic-weak-regularity-study` | `audit/claim-4-atomic-weak-regularity` | Claim 4 paper-scale atomic weak-regularity study. |
| `orx/claim-5-evaluator-visible-evidence` | `release/claim-5-evidence` | Claim 5 prior-work evidence assembled for evaluator visibility. |
| `orx/claim-5-primary-proof-chain-certificate` | `audit/claim-5-proof-chain` | Claim 5 primary cited-rate proof-chain certificate. |
| `orx/claims-1-and-4-threshold-escape-evaluator-eviden` | `audit/claims-1-4-threshold-escape` | Combined Claim 1/4 threshold-escape evidence package. |
| `orx/concise-current-poster-layout` | `release/poster-concise-layout` | Concise current poster layout checkpoint. |
| `orx/current-poster-checksum-and-full-gate-run` | `release/poster-checksum-gates` | Current poster checksums and full gate run. |
| `orx/evaluator-blind-candidate-review-round-1` | `audit/evaluator-blind-review-round-1` | First evaluator-blind candidate review. |
| `orx/evaluator-blind-candidate-review-round-1-2` | `audit/evaluator-blind-review-round-1-2` | Follow-up evaluator-blind candidate review. |
| `orx/evaluator-blind-review-harness-fix` | `audit/review-harness-fix` | Scope fix for the blind-review harness. |
| `orx/evaluator-visible-candidate-fixes` | `release/evaluator-visible-candidate-fixes` | Candidate fixes exposed for evaluator review. |
| `orx/exact-published-revision-verification` | `release/exact-published-revision` | Exact published Space revision verification. |
| `orx/final-release-candidate-and-recorded-red-team` | `release/final-release-red-team` | Final release candidate and recorded red-team review. |
| `orx/linux-poster-dependencies-and-current-evidence-p` | `release/linux-poster-dependencies` | Linux poster dependencies and current evidence. |
| `orx/poster-gate-diagnostic-after-scientific-acceptan` | `release/poster-gate-diagnostics` | Poster-gate diagnostic after scientific acceptance. |
| `orx/zero-advisory-current-poster` | `release/poster-advisory-current` | Current-poster advisory cleanup. |
| `orx/zero-advisory-current-poster-final-phrase` | `release/poster-advisory-final-phrase` | Final phrase advisory cleanup. |
| `orx/zero-advisory-current-poster-final-wording` | `release/poster-advisory-final-wording` | Final wording advisory cleanup. |
| `quarantine/remote-1e41143` | `quarantine/remote-1e41143` | Rejected remote candidate retained for provenance; never publish. |
| `quarantine/remote-57cc883` | `quarantine/remote-57cc883` | Rejected remote candidate retained for provenance; never publish. |
| `work/l5-c2-local-proof-dependency-522a14f` | `audit/claim-2-proof-dependency-mixture` | Local Claim 2 conditional proof-dependency mixture audit. |

The 31-branch count includes `main`. The remote symbolic `origin/HEAD` is not a
branch. After publication, only the clean names above should be visible; no
`orx/*` branch should remain on GitHub.

## Attribution policy

Every reachable commit from `main`, the descriptive audit/release branches,
and the retained quarantine branches is normalized to:

```text
MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>
```

The repository rename and branch cleanup do not change scientific evidence.
Quarantine branches remain explicitly excluded from publication, and the
current `publication_allowed` state remains false for future scientific claim
changes.
