"""Shared fixtures for tools/ test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
# Paper 1's registry as it stood on the DR-004 schema (frozen 2026-10-16, when the live
# registry migrated to DR-027). Tests that pin DR-004 parsing use this copy.
PAPER1_REGISTRY = REPO_ROOT / "tests" / "fixtures" / "dr004" / "paper1-v4-registry.md"
PAPER1_V5_REGISTRY = REPO_ROOT / "papers" / "perspective" / "vv" / "claims" / "claim_registry.md"


@pytest.fixture(scope="session")
def paper1_registry() -> Path:
    """Path to the known-good Paper 1 registry fixture (DR-004 schema, frozen).

    Known-good for PARSING only: its DR-002 P0 tier floor fails (#38).
    Counts are pinned by the tests, not restated here:
    `test_paper1_registry_coverage_shape` (entries),
    `test_paper1_p0_tier_floor_fails` (P0 floor), and
    `test_paper1_registry_doi_extraction` (DOIs).
    """
    assert PAPER1_REGISTRY.is_file(), f"fixture missing: {PAPER1_REGISTRY}"
    return PAPER1_REGISTRY


@pytest.fixture(scope="session")
def paper1_v5_registry() -> Path:
    """Path to Paper 1's live registry (DR-027 schema)."""
    assert PAPER1_V5_REGISTRY.is_file(), f"fixture missing: {PAPER1_V5_REGISTRY}"
    return PAPER1_V5_REGISTRY
