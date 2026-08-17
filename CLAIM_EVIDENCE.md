# Claim-to-evidence dossier

This dossier explains how each of the five paper claims is produced in this
repository, which source and program paths are involved, which controls were
run, and what the evidence can actually support.

The frozen challenge input is contract/live_claims.json. Every official input
claim remains marked unverified there. The local verdicts below are scoped
reproduction labels, not theorem proofs. The official rejudge of the exact
published Space revision 47dad2b9bfe645cb59775632bc894efa9d65a546 is
authoritative for the competition score: 2/10, with Claims 1--3
inconclusive and Claims 4--5 toy.

## Claim map

| ID | Paper statement | Production path | Local scope | Official outcome |
| --- | --- | --- | --- | --- |
| C1 | Theorem 2 gives an intrinsic-dimension W1 sampling rate. | Literal d=48, M=128, k=3 reverse-OU/Euler route; independent d=k=M=1 hard-threshold stability route. | Inconclusive. | Inconclusive. |
| C2 | Theorem 1 gives an intrinsic-dimension smoothed-score L2 rate. | Full d=48 score grid and controls; conditional d=6, M=3, k=2 analytic proof-dependency fixture. | Inconclusive. | Inconclusive. |
| C3 | Assumption 1 describes a union of subspaces with zero intersection mass and subgaussian within-subspace tails. | d=48 dependency audit; literal d=12, M=3, k=2 UoS estimator with controls. | Inconclusive. | Inconclusive. |
| C4 | The analysis does not require several ambient regularity assumptions. | Full d=48, M=128, k=3, N=50,000 uniform-cube UoS score experiment. | Inconclusive locally. | Toy. |
| C5 | Prior smooth-density work has ambient-dimensional sample complexity. | Pinned primary-source rate extraction and reduced direct Cai--Li probability-flow toy. | Toy. | Toy. |

## C1 — intrinsic-dimension sampling rate

### What the paper claim is

Theorem 2 combines the score-estimation result with reverse-SDE sampling
error and selects a sample-dependent stopping time and horizon. The claimed
Wasserstein rate depends on the maximum of the intrinsic dimension k and 2,
rather than directly on the ambient dimension d.

### How the repository produces evidence

1. Source mapping and the clean-room implementation are in
   src/claim1_reverse_diffusion.py. The retained literal protocol uses
   d=48, M=128, k=3, N in {6250, 12500, 25000, 50000}, T=log N,
   tau=N^(-2/k), the Eq. (8)--(14) KDE score, and Euler--Maruyama reverse
   OU integration.
2. The sampler produces 128 generated samples and is scored with a
   64-projection sliced-W1 metric plus a held-out target-split floor.
3. At N=50,000 and 16 steps, the three-seed mean sliced-W1 is
   1818.1228434244792, while the target-split floors are approximately
   0.07--0.08. The wrong-basis and step-count controls are retained.
4. Because a poor finite discretization does not test the idealized
   continuous-time theorem, a separate source-independent diagnostic is in
   src/claim1_threshold_stability_1d.py. It uses a theorem-domain
   d=k=M=1 Gaussian fixture, n=512, 64 coupled particles, a 2048-step
   Euler reference, and 256-step Euler and stochastic-Heun paths.
5. The preregistered W1 tolerances are all failed:
   Euler-to-fine 1.9316850232061964, Heun-to-fine 1.0337012009501216,
   and Euler-to-Heun 2.752747938118488, against a maximum tolerance of
   0.15. The hard threshold makes the drift discontinuous at the gate.

### Evidence and boundary

Primary artifacts are outputs/claim1_reverse_full/summary.json and its
SHA256SUMS, plus outputs/claim1_threshold_stability_1d_toy/PROTOCOL.json,
DERIVATION.md, summary.json, and SHA256SUMS.

The result is inconclusive. The literal sampler is unstable and the
independent finite stability fixture fails its numerical tolerances, but
neither observation is a defensible counterexample to an idealized
expected-rate theorem with separate discretization qualifications.

## C2 — intrinsic smoothed-score error

### What the paper claim is

Theorem 1 bounds the smoothed-score L2 error using intrinsic dimension k.
Its proof combines component-count events, KDE and tail terms, mixture
weights, and tangent/normal score decomposition.

### How the repository produces evidence

1. src/claim2_fullscale_cleanroom.py and the
   outputs/claim2_fullscale_grid/ artifacts retain the literal d=48,
   M=128, k=3 estimator grid. Reduced-N, wrong-basis, and ambient-basis
   controls are retained under outputs/claim2_controls/.
2. The independent conditional route is
   src/claim2_proof_dependency_mixture.py. It maps the source proof to
   Results.tex and pf-of-theorems.tex, checks the displayed algebra, and
   uses an analytic d=6, M=3, k=2 Gaussian-mixture fixture.
3. The fixture compares exact recovered bases with deliberately cyclically
   wrong bases on shared seeds. The mean MSE is 0.017759518195334726 for
   recovered bases and 0.7330441197259617 for the wrong-basis control.
4. The proof checks pass, including algebra absolute error
   8.881784197001252e-16 and the component-count bound. This is evidence
   about conditional dependencies, not evidence that the theorem expectation
   and hidden constants hold globally.

### Evidence and boundary

The independent dossier is
outputs/claim2_proof_dependency_mixture/DERIVATION.md,
proof_checks.json, results.csv, summary.json, and SHA256SUMS. The literal
grid and controls are preserved for context.

The result is inconclusive. Known labels, three seeds, finite MSE, and
source-algebra checks cannot verify or falsify the theorem-level expectation
bound.

## C3 — union-of-subspaces assumptions

### What the paper claim is

Assumption 1 describes support on a union of M low-dimensional linear
subspaces, zero probability on their intersections, nontrivial component
mass, and subgaussian tails inside each component.

### How the repository produces evidence

1. src/claim3_non_toy_dependency_audit.py checks the component-count
   Chernoff/union-bound dependency, the normal/tangent score identity,
   generic intersection dimension, and explicit assumption-removal controls
   at d=48, M=128, k=3.
2. The analytic identity has maximum absolute error
   1.1238240792670481e-14 over 4,096 held-out evaluation points.
3. The positive-intersection control inserts an atom at the origin and
   produces 10,112 ambiguous labels out of 100,000 draws. The Student-t
   heavy-tail control fails the subgaussian diagnostic. These controls
   intentionally violate assumptions and are not counterexamples to C3.
4. src/claim3_literal_uos_estimator.py is the literal finite route:
   d=12, M=3, k=2, n=6000, n_eval=512, t=0.35. It runs the source hard
   psi gate, clips only the low-dimensional score before adding the
   normal-space term, uses ambient q/p weights, and sweeps the
   source-unspecified C_R over {0.5, 1, 2}.
5. At C_R=1, the nominal regularized MSE is
   0.0013136629952398033. The raw arrays include nominal, intersection-atom,
   and low-mass controls.

### Evidence and boundary

The d=48 dependency evidence is in outputs/claim3_fullscale/. The literal
route is in outputs/claim3_literal_uos_estimator/ with config.json,
results.csv, summary.json, raw_arrays.npz, and SHA256SUMS.

The result is inconclusive. The finite constructions support individual
assumption and proof dependencies, but they do not prove a universal
theorem and do not falsify the literal statement of C3.

## C4 — weak regularity assumptions

### What the paper claim is

The paper is intended to cover singular, multimodal UoS targets without
ambient density, density lower bounds, Holder smoothness, uniform density
bounds, or global log-concavity assumptions used by comparator analyses.

### How the repository produces evidence

src/claim4_fullscale_weak_regularities.py runs a literal-scale local CPU
experiment with d=48, M=128, k=3, N=50,000 and 10,000 smoothed evaluation
points. The target is an equal-weight mixture of bounded intrinsic uniform
cubes. It has bounded-support subgaussian tails and generic zero-dimensional
intersections, while the recorded diagnostics report no ambient density,
no density lower bound, boundary discontinuity, no Holder continuity, and
no global log-concavity.

The analytic-score MSE is 1.8611300606057062. The experiment is classified
as non-toy literal paper-scale synthetic evidence, but one finite MSE cannot
establish the universal result.

### Evidence and boundary

The result and protocol are in outputs/claim4_fullscale/result.json,
config.json, run.log, and SHA256SUMS.

The local result is inconclusive. The official rejudge assigns C4 toy for
the competition score; that official score label does not convert the
finite local experiment into a theorem proof.

## C5 — prior ambient-dimensional comparator

### What the paper claim is

The paper contrasts its intrinsic rate with prior smooth-density diffusion
results whose sample complexity has exponent (d+2 beta)/beta.

### How the repository produces evidence

1. src/claim5_prior_work_comparator.py and
   outputs/claim5_attempt1/ retain primary-source files and the
   algebraic inversion of n^(-beta/(d+2 beta)) = epsilon.
2. The direct cited-method route is
   src/claim5_cai_premise_1d_toy.py. It uses Cai--Li Algorithm 1 at
   d=1, n=250, beta=2, and K=5990, satisfying the cited K premise.
3. Three seeds are run with a normalized full-real-line Gaussian-KDE TV
   proxy interval, a target-tail bound, common-initialization controls,
   permutation checks, and normalized KDE target-A versus target-B
   calibration.
4. The mean TV-proxy lower and upper values are both
   0.9999999930833573. The maximum target-tail bound is
   2.0386675117424833e-29 and maximum permutation error is zero.

### Evidence and boundary

Primary-source provenance is under evidence/claim5_attempt1/prior_sources/.
The scoreable reduced experiment is under
outputs/claim5_cai_premise_1d_toy/ with PROTOCOL.json, results.csv,
summary.json, and SHA256SUMS.

The result is toy locally and officially. It is a reviewed direct-method
toy, not exact-TV theorem verification or falsification. The official
rejudge assigns one point to C5.

## Official-score provenance

The exact published Space was
DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions at
revision 47dad2b9bfe645cb59775632bc894efa9d65a546. The rejudge was recorded
at 2026-08-02T10:58:24Z with model zai-org/GLM-5.2 and score 2/10. The
post-publication readback and score plan are retained in
outputs/final_anonymous_readback_complete_20260802T104812Z.log and
outputs/official_rejudge_score_plan_20260802.md.

The older JSON file outputs/final_verdict_fetch_20260802T104812Z.json
describes an earlier Space revision and is retained as historical provenance;
it is not used as the current official score source.
