# Source audit

## Paper identity

- Title: Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions
- Authors: Jingda Wu and Changxiao Cai
- arXiv: 2605.30153
- OpenReview: L5JTAPUdbQ
- ICML 2026 submission: 2510
- Repository: https://github.com/MachineLearning-Nerd/icml26-diffusion-low-dimensional-distributions
- Previous repository name: icml26-repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions

## Pinned source material

The source audit pinned the arXiv source archive and PDF as Git-tracked
objects. Their expected content hashes are recorded in
evidence/source/SHA256SUMS:

| Object | SHA-256 |
| --- | --- |
| evidence/source/arxiv_source.tar | 07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7 |
| evidence/source/paper.pdf | fca4eed2739dc7b9f202d6e22e1c08ae0a80d08401f79595ccb9b9515477e506 |

The source inventory is in evidence/source/source_inventory.txt. It lists
the paper TeX files, bibliography/style files, and the numerical-results
figure used by the source audit.

This checkout uses sparse-checkout rules that omit binary source objects from
the materialized worktree. The objects are still present in the Git tree;
git cat-file -e and git show can retrieve them. verify_final.py checks the
manifest through the worktree when available and through the tracked Git
object when sparse-checkout has skipped a file.

## Executable and data boundary

The initial source audit found no official executable, dataset, or checkpoint
in the pinned source package. The repository therefore implements clean-room
claim-specific audits and finite synthetic protocols; it does not present
an author-maintained training implementation.

The source package is evidence for paper text and proof mapping. It does not
by itself prove the claims. Each claim dossier identifies the code, controls,
raw outputs, and limitations needed to interpret its result.

## Integrity checks

- The source manifest is evidence/source/SHA256SUMS.
- The source file inventory is evidence/source/source_inventory.txt.
- Selected output directories each carry their own SHA256SUMS.
- EVIDENCE_MANIFEST.json aggregates the documentation, source metadata,
  selected claim summaries, official-score provenance, and nested manifest
  hashes.
- verify_final.py checks both aggregate and nested hashes.

## Reproduction boundary

The trusted release uses local CPU or the locally available GTX 1050 policy.
It contains no claim that Hugging Face Jobs, paid compute, or remote GPU
compute produced the retained evidence. The public Trackio Space is an
evaluation and readback artifact, not a substitute for the source audit or
for a full neural diffusion-model training reproduction.
