# Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions

Independent, source-pinned ICML 2026 audit for **Jingda Wu and Changxiao Cai**, “Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions.”

Paper pages: [arXiv abstract](https://arxiv.org/abs/2605.30153) · [HTML paper](https://arxiv.org/html/2605.30153) · [OpenReview submission L5JTAPUdbQ](https://openreview.net/forum?id=L5JTAPUdbQ) · [ICML 2026 paper page](https://icml.cc/virtual/2026/paper/2510)

This repository is an independent theorem, proof-dependency, and finite CPU audit. It is not an author-maintained implementation and it does not claim a full diffusion-model training reproduction. The source archive and PDF audited here are pinned under `evidence/source/` and verified by `evidence/source/SHA256SUMS`; the initial source audit found no official executable, dataset, or checkpoint.

## Outcome first

The current official rejudge for the published Trackio Space scored **2/10**: Claims 1–3 are **inconclusive**, and Claims 4–5 are **toy** outcomes. The repository’s own scoped evidence reaches the same boundaries: Claims 1–4 are inconclusive, while Claim 5 is a reviewed reduced toy. No claim is verified or falsified, and no full neural diffusion-model training was run under the local-only compute policy.

| Claim | Paper statement | Evidence production path | Current verdict |
| --- | --- | --- | --- |
| 1 | Theorem 2: diffusion sampling reaches (\varepsilon) accuracy in (W_1) with roughly \(\widetilde O(\varepsilon^{-(k\vee2)})\) samples, governed by intrinsic dimension (k). | Literal (d=48,M=128,k=3) reverse-OU/Euler run plus an independent (d=k=M=1) hard-threshold stability fixture. | **Inconclusive.** |
| 2 | Theorem 1: the smoothed-score (L^2) error depends on intrinsic (k), rather than exponentially on ambient (d). | Full (d=48) score grid/controls plus a conditional (d=6,M=3,k=2) analytic Gaussian-mixture proof-dependency fixture. | **Inconclusive.** |
| 3 | Assumption 1: the target is supported on a union of low-dimensional subspaces with zero intersection mass and subgaussian within-subspace tails. | Independent allocation/intersection/tail checks and a literal finite (d=12,M=3,k=2) UoS estimator audit. | **Inconclusive.** |
| 4 | The analysis dispenses with Hölder smoothness, log-concavity, uniform density, and density lower-bound assumptions. | Literal-scale (d=48,M=128,k=3,N=50{,}000) uniform-cube UoS score experiment that violates those comparator regularities. | **Inconclusive locally; official outcome: toy.** |
| 5 | Prior smooth-density work has ambient-dimensional sample complexity \(\varepsilon^{-(d+2\beta)/\beta}\), reflecting the curse of dimensionality. | Primary-source rate extraction plus a direct reduced Cai–Li probability-flow toy satisfying its cited iteration premise. | **Toy locally and officially.** |

The official rejudge is authoritative for the score outcome. The local evidence labels describe what was actually reproduced and must not be read as theorem proofs.

## What the paper is doing

The paper studies score-based diffusion sampling for a target distribution supported on a union of (M) linear subspaces in ambient dimension (d), with maximum intrinsic dimension (k). It smooths the target with an Ornstein–Uhlenbeck/ Gaussian-noise process, estimates the time-dependent score with a kernel-based regularized estimator, and inserts that estimator into a reverse OU sampler. The central claim is that the statistical rate depends on (k), not on the ambient (d), while allowing separated multimodal components and only subgaussian tails within each subspace. The authors also compare this rate with prior smooth-density DDPM/DDIM bounds.

### How each claim is produced

1. **Claim 1 — sampling rate.** Theorem 2 combines the score-estimation bound with reverse-SDE sampling error and chooses the sample-dependent early-stopping time and integration horizon. The result is a (W_1) sampling guarantee with exponent (k\vee2). This repository implements the paper’s Algorithm 1 and Eq. (8)–(14) score path at the literal synthetic geometry, then separately checks a one-dimensional theorem-domain fixture. Both are finite numerical protocols; neither verifies the expected-rate theorem.

2. **Claim 2 — intrinsic score error.** Theorem 1 analyzes the regularized kernel score of the Gaussian-smoothed UoS target. Component counts, KDE tails, mixture weights, and intrinsic/tangent dimensions are combined into an expected (L^2) error bound. The repository tests the algebra and score identity on controlled analytic mixtures, then runs the literal (d=48,M=128,k=3) estimator with controls. Known bases, finite seeds, and unknown constants/polylogarithms are not enough to establish the theorem expectation.

3. **Claim 3 — UoS assumptions.** Assumption 1 supplies the structural event needed by the proof: support on the union, zero probability on subspace intersections, a lower bound on component mass, and subgaussian within-subspace tails. The repository independently checks each dependency, adds positive-intersection, vanishing-mass, and heavy-tail controls, and runs a finite three-subspace estimator in the source’s operation order. Controls are diagnostics, not counterexamples to a theorem whose assumptions they intentionally violate.

4. **Claim 4 — weak regularity.** The paper’s contribution is intended to cover singular, multimodal UoS targets without ambient density, density lower-bound, Hölder, or global log-concavity assumptions. The repository constructs an equal-weight mixture of bounded intrinsic uniform cubes, verifies the UoS conditions, confirms the comparator regularity violations, and computes a closed-form smoothed score against the estimator. One finite MSE cannot establish the universal theorem, so the local verdict remains inconclusive; the official judge marked it toy.

5. **Claim 5 — prior-work comparison.** The paper contrasts its intrinsic exponent with prior smooth-density diffusion analyses. The repository pins the cited Zhang et al. and Cai–Li source/PDF excerpts, algebraically inverts their (n^{-\beta/(d+2\beta)}) TV rate, and runs a reduced direct Cai–Li probability-flow procedure. The direct toy uses (d=1,n=250,\beta=2,K=5{,}990), satisfies the cited (K) premise, and reports a normalized full-line KDE-TV proxy; it is not an exact-TV theorem verification.

## Evidence ledger

### Claim 1 — intrinsic-dimension sampling rate

Primary path: `src/claim1_reverse_diffusion.py` with `outputs/claim1_reverse_full/`. It uses the source geometry (d=48,M=128,k=3), (N\in\{6{,}250,12{,}500,25{,}000,50{,}000\}), (T=\log N), (\tau=N^{-2/k}), the Eq. (8)–(14) KDE score, Euler–Maruyama reverse OU integration, 128 generated samples, and a 64-projection sliced-(W_1) metric with a held-out target-split floor. At (N=50{,}000), 16 steps produced mean sliced (W_1=1818.12), while the corresponding target-split floors were about (0.07)–(0.08); the wrong-basis control was similarly poor. A step sweep was also unstable.

Independent diagnostic: `src/claim1_threshold_stability_1d.py` with `outputs/claim1_threshold_stability_1d_toy/` uses (n=512), 64 particles, (d=k=M=1), coupled Brownian paths, Euler/Heun with 256 steps, and a 2048-step Euler reference. Euler-to-reference (W_1=1.9317), Heun-to-reference (W_1=1.0337), and Euler-to-Heun (W_1=2.7527) all exceed the preregistered 0.15 tolerance. The hard score threshold is discontinuous, so this finite disagreement is neither a theorem counterexample nor a numerical verification.

### Claim 2 — intrinsic score-error rate

The full score path is in `src/claim2_fullscale_cleanroom.py` and `outputs/claim2_fullscale_grid/`. At (t=0.1,0.5,1.0), 20 replicates at (N=50{,}000) gave mean MSEs 10.38185, 1.49812, and 0.58816; the (t=0.25) cell had 21 replicates with mean MSE 3.69597. Required wrong-basis, reduced-(N), and ambient-component controls are in `outputs/claim2_controls/`; they did not produce the expected degradation.

The separate conditional proof-dependency route in `src/claim2_proof_dependency_mixture.py` checks the displayed exponent/algebra with (N=1800,M=3,k=2,t=0.6), then compares exact recovered bases with cyclically wrong bases on three shared seeds. Mean MSE is 0.01776 recovered versus 0.73304 wrong-basis. This supports the conditional fixture’s dependencies, not the theorem’s expectation-level bound.

### Claim 3 — union-of-subspaces assumptions

`src/claim3_non_toy_dependency_audit.py` checks the component-count Chernoff/union-bound dependency, exact normal/tangent score decomposition, generic intersection dimension, and assumption-removal controls. In the (d=48,M=128,k=3) fixture, the analytic score identity has maximum absolute error (1.12\times10^{-14}); a positive-intersection control creates 10,112 ambiguous origin labels in 100,000 draws, while a Student-(t(3)) control fails the subgaussian diagnostic.

`src/claim3_literal_uos_estimator.py` is the remediated finite literal route: (d=12,M=3,k=2,n=6000), source hard-ψ threshold, clipping only the low-dimensional score before normal-space addition, ambient (q/p) mixture weights, and (C_R\in\{0.5,1,2\}) sensitivity because the source leaves (C_R) unspecified. At (C_R=1), the nominal regularized MSE is 0.00131366. Raw arrays and controls are in `outputs/claim3_literal_uos_estimator/`.

### Claim 4 — weak regularity assumptions

`src/claim4_fullscale_weak_regularities.py` evaluates a local CPU (d=48,M=128,k=3,N=50{,}000) equal-weight uniform-intrinsic-cube mixture with 10,000 smoothed evaluation points. It satisfies bounded-support subgaussian tails and zero-dimensional generic intersections while lacking an ambient density, density lower bound, Hölder continuity, and global log-concavity. The analytic-score MSE is 1.86113. This is non-toy finite evidence that the estimator runs on such a target, not a universal proof.

### Claim 5 — prior ambient-dimensional comparator

`src/claim5_prior_work_comparator.py` and `outputs/claim5_attempt1/` retain a reduced full-dimensional KDE-score comparator for provenance. The primary-source excerpts and exact exponent inversion are under `evidence/claim5_attempt1/prior_sources/`. The scoreable direct toy in `src/claim5_cai_premise_1d_toy.py` uses Cai–Li Algorithm 1 at (d=1,n=250,\beta=2,K=5{,}990) over three seeds. Its normalized full-real-line Gaussian-KDE TV proxy is near one because the finite sampler escapes the target scale; the result is intentionally classified toy.

## Reproduce the retained evidence

The repository’s local policy is CPU-only (or local GTX 1050); no Hugging Face Jobs, paid compute, or remote GPU evidence is part of this release.

```bash
./scripts/bootstrap_reproduction.sh
./.venv/bin/python -m pytest -q
./.venv/bin/python scripts/validate_release.py

# Source and release integrity
(cd evidence/source && sha256sum -c SHA256SUMS)
(cd outputs/claim1_threshold_stability_1d_toy && sha256sum -c SHA256SUMS)
(cd outputs/claim2_proof_dependency_mixture && sha256sum -c SHA256SUMS)
(cd outputs/claim3_literal_uos_estimator && sha256sum -c SHA256SUMS)
(cd outputs/claim4_fullscale && sha256sum -c SHA256SUMS)
(cd outputs/claim5_cai_premise_1d_toy && sha256sum -c SHA256SUMS)
```

The literal-scale diffusion experiments are retained as evidence and are not required for a documentation-only checkout. `scripts/run_full_poster_gates.sh` reproduces the published non-waived Posterly release gates.

## Audit dossier and final-state check

The claim-by-claim production routes, evidence boundaries, and official-score
provenance are collected in [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md). The
source and sparse-checkout provenance is in [SOURCE_AUDIT.md](SOURCE_AUDIT.md),
the recorded runtime policy is in [ENVIRONMENT.md](ENVIRONMENT.md), and the
short release report is in [REPORT.md](REPORT.md).

The machine-readable companion files are [claims.json](claims.json),
[CITATION.cff](CITATION.cff), [AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md),
[BRANCH_AUDIT.md](BRANCH_AUDIT.md), and
[EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json). Run

~~~bash
python3 verify_final.py
~~~

to verify the live GitHub branch set, canonical attribution, required files,
claim-specific summary facts, and the nested SHA-256 evidence manifests. The
full branch-by-branch historical mapping remains in
[branch-audit.md](branch-audit.md).

## Repository map

| Path | Purpose |
| --- | --- |
| `contract/` | Frozen ICML 2026 challenge metadata and five live claims. |
| `evidence/source/` | Pinned arXiv source/PDF and SHA-256 manifest. |
| `evidence/claim5_attempt1/prior_sources/` | Pinned source/PDF excerpts for the cited ambient-dimensional comparators. |
| `src/` | Claim-specific source audits and clean-room finite estimators/samplers. |
| `outputs/` | Raw arrays, summaries, controls, logs, and integrity manifests for each claim. |
| `logbook/` and `.trackio/` | Fixed-order Trackio claim pages, poster, and release-gate artifacts. |
| `STATUS.md` | Human-readable claim, official-score, publication, and continuation status. |
| `AUTONOMOUS_STATE.json` | Machine-readable continuation state and evidence boundaries. |
| `branch-audit.md` | Complete old-to-new branch mapping and attribution audit. |

## Branches and attribution

The former repository name was `icml26-repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions`; the clean name is [`icml26-diffusion-low-dimensional-distributions`](https://github.com/MachineLearning-Nerd/icml26-diffusion-low-dimensional-distributions). The final branch set keeps `main` as the trusted release, preserves the two rejected candidate checkpoints under `quarantine/*`, and renames the 27 `orx/*` experiment/release branches plus the one `work/*` branch into descriptive `audit/*` or `release/*` names. The full mapping and purpose of every branch is in `branch-audit.md`.

All reachable commits are normalized to:

```text
MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>
```

The quarantined branches are retained for provenance only and are not publication candidates.

## Existing public logbook

- Trackio Space: https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions
- Rendered logbook: https://dineshai-repro-l5jtapudbq-diffusion-low-dimensio-bc85f6d.static.hf.space/
- Official rejudge: Space SHA `47dad2b9bfe645cb59775632bc894efa9d65a546`, score 2/10, model `zai-org/GLM-5.2`.

No public agent trace is declared or attached. The public logbook is a reproduction record, not an author endorsement or an official paper erratum.

## Citation

```bibtex
@article{wu2026diffusion,
  title         = {Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions},
  author        = {Wu, Jingda and Cai, Changxiao},
  journal       = {arXiv preprint arXiv:2605.30153},
  year          = {2026},
  eprint        = {2605.30153},
  archivePrefix = {arXiv},
  primaryClass  = {stat.ML}
}
```

## Thank you

Thank you to Jingda Wu and Changxiao Cai for developing and sharing this focused theoretical treatment of diffusion models on low-dimensional, multimodal distributions. This independent audit is intended to make the assumptions, proof dependencies, numerical controls, and reproduction limits easier for other researchers to inspect; its scoped verdicts are not author-maintained results.

## Current limitations and next steps

- Claims 1–3 need genuinely new, independently reviewed local evidence before any stronger verdict is appropriate.
- Claim 4 remains a finite experiment outside several comparator regularity classes; it is not a universal theorem proof.
- Claim 5 remains a reduced direct-method toy and not exact-TV theorem verification.
- Full neural diffusion-model training remains outside this repository’s local compute policy and has not been claimed.
- `publication_allowed` remains `false` for future scientific claim changes, even though the current documentation/release artifacts are public.
