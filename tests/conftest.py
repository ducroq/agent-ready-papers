"""Shared fixtures for tools/ test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PAPER1_REGISTRY = REPO_ROOT / "papers" / "perspective" / "vv" / "claims" / "claim_registry.md"


@pytest.fixture(scope="session")
def paper1_registry() -> Path:
    """Path to the known-good Paper 1 registry fixture.

    19 entries: 16 CLAIMs, 2 ARGUMENTs, 1 PROPOSITION.
    Priority breakdown: P0=8, P1=10, P2=1. All status [x] (100% verified).
    Contains 9 DOIs (verified independently in DR-011 Pass 1 review).
    """
    assert PAPER1_REGISTRY.is_file(), f"fixture missing: {PAPER1_REGISTRY}"
    return PAPER1_REGISTRY
