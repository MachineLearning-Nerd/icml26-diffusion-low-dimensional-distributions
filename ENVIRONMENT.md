# Environment and reproduction boundary

## Runtime policy

The repository’s trusted evidence policy is local CPU or local GTX 1050 only.
No Hugging Face Jobs, cpu-upgrade, paid compute, or remote GPU run is claimed
as part of the retained scientific evidence. Full neural diffusion-model
training is outside the demonstrated local feasibility boundary.

The official Trackio Space and its rejudge are recorded for publication and
evaluation provenance. They are not described as a local training run.

## Recorded environments

| Route | Recorded runtime | Device | Scale |
| --- | --- | --- | --- |
| C1 literal reverse sampler | Python and NumPy clean-room route | Local CPU | d=48, M=128, k=3; N through 50,000 |
| C1 stability fixture | Python 3.14.5, local CPU NumPy | Local CPU | d=k=M=1; n=512; 64 particles |
| C2 proof dependency | Python and NumPy analytic fixture | Local CPU | d=6, M=3, k=2; three shared seeds |
| C3 full dependency audit | Python 3.14.5, NumPy 2.5.1 | Local CPU | d=48, M=128, k=3; 100,000-trial controls |
| C3 literal estimator | Python and NumPy finite estimator | Local CPU | d=12, M=3, k=2; n=6,000 |
| C4 weak regularity | NumPy float32 streaming | Local CPU | d=48, M=128, k=3; N=50,000; 10,000 evaluation points |
| C5 direct comparator | Python 3.14.5, NumPy 2.5.1 | Local CPU | d=1; n=250; three seeds; K=5,990 |

The exact per-run metadata remains in the output summaries and logs. The
table is a navigation aid, not a replacement for those artifacts.

## Reproduction commands

The README lists the bootstrap, test, release-validation, and checksum
commands. The smallest integrity-only check is:

~~~bash
python3 verify_final.py
~~~

The verifier does not rerun scientific experiments. It checks the published
GitHub branch topology, attribution, required files, summary invariants, and
the hashes of retained evidence.

## Interpretation

Finite synthetic experiments can check implementation routes, algebra,
controls, and selected proof dependencies. They cannot by themselves certify
the paper’s universal expected-rate theorems. The claim verdicts therefore
remain deliberately scoped: C1--C4 inconclusive and C5 toy locally, with the
official rejudge reporting C1--C3 inconclusive and C4--C5 toy.
