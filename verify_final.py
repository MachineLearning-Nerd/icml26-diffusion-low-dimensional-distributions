#!/usr/bin/env python3
"""Verify the published diffusion-reproduction dossier and live GitHub state."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANONICAL = (
    "MachineLearning-Nerd",
    "MachineLearning-Nerd@users.noreply.github.com",
)
EXPECTED_REPOSITORY = "MachineLearning-Nerd/icml26-diffusion-low-dimensional-distributions"
EXPECTED_OVERALL_VERDICT = "SCOPED_CLAIMS_1_TO_4_INCONCLUSIVE_CLAIM_5_TOY_OFFICIAL_2_OF_10"
EXPECTED_PUBLICATION_BOUNDARY = "OFFICIAL_2_OF_10_SCOPED_NO_FULL_REPRODUCTION"
EXPECTED_BRANCHES = {
    "main",
    "audit/baseline-reproduction",
    "audit/claim-1-proof-chain",
    "audit/claim-1-reverse-sde",
    "audit/claim-1-threshold-escape",
    "audit/claim-2-proof-certificate",
    "audit/claim-2-component-scaling",
    "audit/claim-3-identifiability-counterexample",
    "audit/claim-4-atomic-weak-regularity",
    "audit/claim-5-proof-chain",
    "audit/claims-1-4-threshold-escape",
    "audit/evaluator-blind-review-round-1",
    "audit/evaluator-blind-review-round-1-2",
    "audit/review-harness-fix",
    "audit/claim-2-proof-dependency-mixture",
    "release/claim-2-combined-evidence",
    "release/claim-3-evidence",
    "release/claim-4-evidence",
    "release/claim-5-evidence",
    "release/poster-concise-layout",
    "release/poster-checksum-gates",
    "release/evaluator-visible-candidate-fixes",
    "release/exact-published-revision",
    "release/final-release-red-team",
    "release/linux-poster-dependencies",
    "release/poster-gate-diagnostics",
    "release/poster-advisory-current",
    "release/poster-advisory-final-phrase",
    "release/poster-advisory-final-wording",
    "quarantine/remote-1e41143",
    "quarantine/remote-57cc883",
}
REQUIRED_PATHS = [
    "README.md",
    "STATUS.md",
    "branch-audit.md",
    "BRANCH_AUDIT.md",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "claims.json",
    "reproduction_verdicts.json",
    "AUTONOMOUS_STATE.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
    "contract/contract_manifest.json",
    "contract/live_claims.json",
    "contract/metadata.json",
    "evidence/source/SHA256SUMS",
    "evidence/source/source_inventory.txt",
    "outputs/final_anonymous_readback_complete_20260802T104812Z.log",
    "outputs/final_published_space_api_20260802T104701Z.json",
    "outputs/official_rejudge_score_plan_20260802.md",
    "outputs/claim1_reverse_full/summary.json",
    "outputs/claim1_threshold_stability_1d_toy/summary.json",
    "outputs/claim2_proof_dependency_mixture/summary.json",
    "outputs/claim3_fullscale/result.json",
    "outputs/claim3_literal_uos_estimator/summary.json",
    "outputs/claim4_fullscale/result.json",
    "outputs/claim5_cai_premise_1d_toy/summary.json",
]
NESTED_MANIFESTS = [
    "evidence/source/SHA256SUMS",
    "outputs/claim1_reverse_full/SHA256SUMS",
    "outputs/claim1_threshold_stability_1d_toy/SHA256SUMS",
    "outputs/claim2_proof_dependency_mixture/SHA256SUMS",
    "outputs/claim3_fullscale/SHA256SUMS",
    "outputs/claim3_literal_uos_estimator/SHA256SUMS",
    "outputs/claim4_fullscale/SHA256SUMS",
    "outputs/claim5_cai_premise_1d_toy/SHA256SUMS",
    "outputs/claim5_attempt1/SHA256SUMS",
]


def run(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"command failed: {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout


def fail(message: str) -> None:
    print(f"FINAL_AUDIT=FAILED {message}", file=sys.stderr)
    raise SystemExit(1)


def git_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        fail(f"tracked file is unavailable: {path}")
    return result.stdout


def file_bytes(path: str) -> bytes:
    local = ROOT / path
    return local.read_bytes() if local.exists() else git_bytes(path)


def sha256(path: str) -> str:
    return hashlib.sha256(file_bytes(path)).hexdigest()


def tracked_exists(path: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    return result.returncode == 0


def json_file(path: str) -> object:
    try:
        return json.loads(file_bytes(path))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON in {path}: {exc}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def verify_hash_manifest(path: str) -> None:
    text = file_bytes(path).decode("utf-8")
    base = Path(path).parent
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        require(len(parts) == 2, f"malformed hash line in {path}: {line}")
        expected, name = parts
        name = name.lstrip("*")
        candidates = [name, str(base / name)]
        target = next(
            (
                candidate
                for candidate in candidates
                if (ROOT / candidate).exists() or tracked_exists(candidate)
            ),
            None,
        )
        if target is None:
            target = name if name.startswith("/") else str(Path(base) / name)
        require(
            sha256(target) == expected,
            f"hash mismatch in {path}: {name}",
        )


def main() -> None:
    origin = run("git", "config", "--get", "remote.origin.url").strip()
    require(
        origin in {
            "https://github.com/MachineLearning-Nerd/icml26-diffusion-low-dimensional-distributions.git",
            "git@github.com:MachineLearning-Nerd/icml26-diffusion-low-dimensional-distributions.git",
        },
        f"unexpected origin: {origin}",
    )

    symref = run("git", "ls-remote", "--symref", "origin", "HEAD")
    require("ref: refs/heads/main\tHEAD" in symref, "origin/HEAD is not main")

    remote_lines = run("git", "ls-remote", "--heads", "origin").splitlines()
    remote_heads = {}
    for line in remote_lines:
        commit, ref = line.split("\t", 1)
        require(ref.startswith("refs/heads/"), f"unexpected remote ref: {ref}")
        remote_heads[ref.removeprefix("refs/heads/")] = commit
    require(
        set(remote_heads) == EXPECTED_BRANCHES,
        f"branch set mismatch: {sorted(set(remote_heads) ^ EXPECTED_BRANCHES)}",
    )
    require(
        len(remote_heads) == 31,
        f"expected 31 branches, found {len(remote_heads)}",
    )
    require(
        not any(name.startswith(("orx/", "work/")) for name in remote_heads),
        "old orx/work branch remains",
    )
    require(
        sum(name.startswith("quarantine/") for name in remote_heads) == 2,
        "quarantine branch count changed",
    )
    require(
        remote_heads["main"] == run("git", "rev-parse", "origin/main").strip(),
        "local origin/main disagrees with live origin",
    )

    local_heads = set(
        run("git", "for-each-ref", "--format=%(refname:strip=2)", "refs/heads")
        .splitlines()
    )
    require(local_heads <= EXPECTED_BRANCHES, "unexpected local branch name")
    refs = run("git", "for-each-ref", "--format=%(refname)", "refs").splitlines()
    require(not any("refs/original/" in ref for ref in refs), "refs/original remains")

    identities = set()
    for line in run("git", "log", "--all", "--format=%an\t%ae\t%cn\t%ce").splitlines():
        if line.strip():
            identities.add(tuple(line.split("\t")))
    require(
        identities == {(CANONICAL[0], CANONICAL[1], CANONICAL[0], CANONICAL[1])},
        f"non-canonical reachable identity: {sorted(identities)}",
    )
    require(
        "co-authored-by:" not in run("git", "log", "--all", "--format=%B").lower(),
        "co-author trailer found",
    )
    commit_count = int(run("git", "rev-list", "--count", "--all").strip())
    require(commit_count >= 85, f"unexpectedly short history: {commit_count}")

    for path in REQUIRED_PATHS:
        if not (ROOT / path).exists():
            git_bytes(path)

    claims = json_file("claims.json")
    require(isinstance(claims, dict), "claims.json must be an object")
    claim_rows = claims.get("claims", [])
    require(len(claim_rows) == 5, "claims.json must contain five claims")
    require(
        [row.get("status") for row in claim_rows] == [
            "inconclusive",
            "inconclusive",
            "inconclusive",
            "inconclusive",
            "toy",
        ],
        "unexpected local claim statuses",
    )
    official = claims.get("official_rejudge", {})
    require(
        claims.get("repository") == EXPECTED_REPOSITORY
        and claims.get("overall_verdict") == EXPECTED_OVERALL_VERDICT
        and claims.get("publication_allowed") is False
        and claims.get("publication_boundary") == EXPECTED_PUBLICATION_BOUNDARY
        and claims.get("score_claim") is False
        and claims.get("official_author_endorsement") is False,
        "claims publication boundary mismatch",
    )
    require(official.get("score") == 2, "official score is not 2")
    require(
        official.get("space_sha")
        == "47dad2b9bfe645cb59775632bc894efa9d65a546",
        "official Space SHA mismatch",
    )

    reproduction = json_file("reproduction_verdicts.json")
    require(
        reproduction.get("repository") == EXPECTED_REPOSITORY
        and reproduction.get("overall_verdict") == EXPECTED_OVERALL_VERDICT
        and reproduction.get("publication_allowed") is False
        and reproduction.get("publication_boundary") == EXPECTED_PUBLICATION_BOUNDARY
        and reproduction.get("score_claim") is False
        and reproduction.get("official_author_endorsement") is False,
        "reproduction verdict boundary mismatch",
    )
    require(
        {
            key: value.get("verdict")
            for key, value in reproduction.get("verdicts", {}).items()
        }
        == {
            "1": "inconclusive",
            "2": "inconclusive",
            "3": "inconclusive",
            "4": "inconclusive",
            "5": "toy",
        },
        "unexpected reproduction verdicts",
    )

    state = json_file("AUTONOMOUS_STATE.json")
    require(
        state.get("github_repository") == f"https://github.com/{EXPECTED_REPOSITORY}"
        and state.get("phase") == "published_scoped_partial_audit_official_2_of_10"
        and state.get("publication_allowed") is False
        and state.get("overall_verdict") == EXPECTED_OVERALL_VERDICT
        and state.get("publication_boundary") == EXPECTED_PUBLICATION_BOUNDARY
        and state.get("score_claim") is False
        and state.get("official_author_endorsement") is False
        and state.get("live_verification", {}).get("branch_count") == 31
        and state.get("live_verification", {}).get("default_branch") == "main"
        and state.get("verified_reachable_commits") == 88,
        "state publication boundary mismatch",
    )
    require(
        state.get("attribution", {}).get("email") == CANONICAL[1],
        "state attribution mismatch",
    )

    live_claims = json_file("contract/live_claims.json")
    require(
        isinstance(live_claims, list)
        and len(live_claims) == 5
        and all(row.get("status") == "unverified" for row in live_claims),
        "immutable live claim metadata changed",
    )

    status = file_bytes("STATUS.md").decode("utf-8")
    readme = file_bytes("README.md").decode("utf-8")
    require("2/10" in status and "2/10" in readme, "official score missing")
    require(
        "47dad2b9bfe645cb59775632bc894efa9d65a546" in status,
        "official Space SHA missing",
    )
    for marker in (
        EXPECTED_OVERALL_VERDICT,
        "reproduction_verdicts.json",
        "publication_allowed=false",
        "score_claim=false",
        "official_author_endorsement=false",
    ):
        require(marker in readme, f"README marker missing: {marker}")
    for marker in (
        EXPECTED_OVERALL_VERDICT,
        EXPECTED_PUBLICATION_BOUNDARY,
        "reproduction_verdicts.json",
        "publication_allowed=false",
        "score_claim=false",
        "official_author_endorsement=false",
    ):
        require(marker in status, f"STATUS marker missing: {marker}")
    report = file_bytes("REPORT.md").decode("utf-8")
    for marker in (
        EXPECTED_OVERALL_VERDICT,
        "publication_allowed=false",
        "official_author_endorsement=false",
    ):
        require(marker in report, f"REPORT marker missing: {marker}")

    c1 = json_file("outputs/claim1_reverse_full/summary.json")
    require(c1["protocol"]["d"] == 48 and c1["protocol"]["M"] == 128, "C1 scale mismatch")
    require(c1["protocol"]["k"] == 3, "C1 intrinsic dimension mismatch")
    require(c1["full_N50000_steps16_mean_sliced_w1"] > 1000, "C1 result changed")
    require("unstable" in c1["interpretation"].lower(), "C1 interpretation changed")

    c1_stability = json_file("outputs/claim1_threshold_stability_1d_toy/summary.json")
    require(c1_stability["verdict"] == "inconclusive", "C1 stability verdict changed")
    require(not c1_stability["passes_fixture_tolerances"], "C1 fixture unexpectedly passes")
    require(c1_stability["metrics"]["euler_to_fine_w1"] > 0.15, "C1 control changed")

    c2 = json_file("outputs/claim2_proof_dependency_mixture/summary.json")
    require(c2["verdict"] == "inconclusive", "C2 verdict changed")
    require(c2["proof_checks"]["checks_pass"], "C2 proof checks failed")
    require(c2["recovered_mse_mean"] < c2["wrong_basis_mse_mean"], "C2 control changed")

    c3 = json_file("outputs/claim3_fullscale/result.json")
    require(c3["verdict"] == "inconclusive", "C3 verdict changed")
    require(
        c3["score_identity"]["max_abs_score_identity_error"] < 1e-10,
        "C3 identity error changed",
    )
    c3_literal = json_file("outputs/claim3_literal_uos_estimator/summary.json")
    require(
        c3_literal["config"]["d"] == 12
        and c3_literal["config"]["M"] == 3
        and c3_literal["config"]["k"] == 2,
        "C3 literal scale changed",
    )
    require(
        c3_literal["config"]["C_R_sweep"] == [0.5, 1.0, 2.0],
        "C3 sensitivity sweep changed",
    )

    c4 = json_file("outputs/claim4_fullscale/result.json")
    require(
        (c4["d"], c4["M"], c4["k"], c4["N"]) == (48, 128, 3, 50000),
        "C4 scale changed",
    )
    require(abs(c4["mse"] - 1.8611300606057062) < 1e-12, "C4 MSE changed")

    c5 = json_file("outputs/claim5_cai_premise_1d_toy/summary.json")
    require(c5["verdict"] == "toy" and c5["n"] == 250, "C5 verdict or n changed")
    require(c5["mean_tv_proxy_lower"] > 0.99, "C5 toy result changed")
    require(c5["max_permutation_error"] == 0.0, "C5 permutation control changed")

    aggregate = json_file("EVIDENCE_MANIFEST.json")
    require(isinstance(aggregate, dict), "EVIDENCE_MANIFEST must be an object")
    for entry in aggregate.get("entries", []):
        expected = entry.get("sha256", "")
        require(len(expected) == 64 and expected != "PENDING", f"pending hash: {entry}")
        require(sha256(entry["path"]) == expected, f"aggregate hash mismatch: {entry['path']}")
    require(aggregate.get("entries"), "aggregate manifest is empty")

    for manifest in NESTED_MANIFESTS:
        verify_hash_manifest(manifest)

    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={len(remote_heads)} commits={commit_count} "
        "claims1-4=inconclusive claims5=toy official=2/10"
    )


if __name__ == "__main__":
    main()
