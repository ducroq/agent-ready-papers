"""DR-027 tools prototype, review round 2: a seeded positive per defect.

Each test fails on the round-1 commit (cc2f191) and passes with the fix. The
alias-parity class rule has its own file, `test_v5_parity.py`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.test_v5_registry import CLAIMS_HEADER, OLD_REGISTRY, claim_row, contrib_row, registry, write
from tools import check_registry as cr
from tools.check_registry import GLOSSARY_PLACEHOLDERS, check_registry
from tools.coverage import check_coverage
from tools.coverage import main as coverage_main

REPO_ROOT = Path(__file__).resolve().parents[1]


# 3. effective tier ------------------------------------------------------------


@pytest.mark.parametrize(
    "rests",
    [
        "claim: S1-1, S1-2",
        "claim: S1-1 (the count)",
        "claim: [S1-1](#s1-1)",
        "claim: D1",
        "claim: S1-2; claim: S1-1 and S1-2",
    ],
)
def test_contribution_with_an_unparseable_claim_item_fails_the_floor(tmp_path, rests):
    text = registry(
        claims=claim_row("S1-1", priority="P1", tier="ESTABLISHED") + claim_row("S1-2", priority="P1", tier="ESTABLISHED"),
        contribs=contrib_row(rests=rests, tier="SUPPORTED"),
    )
    path = write(tmp_path, text)
    report = check_coverage(path)
    assert report.p0_below_floor == ("C1",)
    assert dict(report.effective_tiers)["C1"].startswith("UNREADABLE (Rests-on item")
    assert coverage_main([str(path), "--strict"]) == 1


def test_contribution_resting_on_a_claim_with_an_unreadable_tier_fails_the_floor(tmp_path):
    text = registry(claims=claim_row("S1-1", priority="P1", tier="TBD"), contribs=contrib_row(tier="SUPPORTED"))
    report = check_coverage(write(tmp_path, text))
    assert report.p0_below_floor == ("C1",)
    assert "whose tier is unreadable" in dict(report.effective_tiers)["C1"]


def test_contribution_resting_on_a_contribution_is_one_id(tmp_path):
    text = registry(
        claims=claim_row("S1-1", priority="P1", tier="ESTABLISHED"),
        contribs=contrib_row("C1", rests="claim: C2", tier="SUPPORTED") + contrib_row("C2", tier="ESTABLISHED"),
    )
    assert check_coverage(write(tmp_path, text)).meets_tier_floor


def test_effective_tier_reason_is_in_markdown_and_json(tmp_path, capsys):
    text = registry(claims=claim_row(priority="P1", tier="EMERGING"), contribs=contrib_row(tier="SUPPORTED"))
    path = write(tmp_path, text)
    assert "C1: effective EMERGING (weakest claim S1-1; own SUPPORTED)" in check_coverage(path).to_markdown()
    coverage_main([str(path), "--json"])
    data = json.loads(capsys.readouterr().out)
    assert data["contribution_effective_tiers"] == {"C1": "EMERGING (weakest claim S1-1; own SUPPORTED)"}


# 4. glossary placeholders are exact strings -----------------------------------------


def test_every_glossary_placeholder_occurs_in_the_template():
    template = (REPO_ROOT / "templates" / "glossary.md").read_text(encoding="utf-8")
    assert [p for p in GLOSSARY_PLACEHOLDERS if p not in template] == []


def test_filled_glossary_citing_vim_and_using_n_passes(tmp_path):
    gloss = write(
        tmp_path,
        "# Glossary\n\n**Paper:** Measurement\n\n| Term | Definition | Source | Plain |\n|---|---|---|---|\n"
        "| measurand | quantity intended to be measured [VIM 2.3] | VIM | thing measured |\n"
        "| DFT length | the transform size [N] samples | DSP | size |\n\n*Version: 2*\n",
        "glossary.md",
    )
    reg = write(tmp_path, registry(claims=claim_row()))
    assert not [f for f in check_registry(reg, glossary_path=gloss).findings if f.check == "glossary"]


@pytest.mark.parametrize("token", ["*Version: [N]*", "| [term] |", "[VIM / GUM / ISO / etc.]"])
def test_one_leftover_template_placeholder_fails(tmp_path, token):
    gloss = write(tmp_path, f"# Glossary\n\n**Paper:** Measurement\n\n{token}\n", "glossary.md")
    reg = write(tmp_path, registry(claims=claim_row()))
    assert [f.check for f in check_registry(reg, glossary_path=gloss).findings] == ["glossary"]


# 5. near-miss markers need a table; DR-004 registries get a note ---------------------


def test_near_miss_label_without_a_table_is_not_reported(tmp_path):
    text = "**Arguments**\n\nThe arguments are discussed in prose.\n\n" + registry(claims=claim_row())
    path = write(tmp_path, text)
    assert check_coverage(path).rows
    assert not any("near-miss" in f.message for f in check_registry(path).findings)


def test_near_miss_in_an_indented_code_block_is_not_reported(tmp_path):
    text = "Example:\n\n    **CLAIMS:**\n\n    | ID | Statement |\n\n" + registry(claims=claim_row())
    assert check_coverage(write(tmp_path, text)).rows


def test_near_miss_in_an_all_dr004_registry_is_a_note(tmp_path):
    # A heading first: without it master's stray-row rule fires on S5-1, a finding on master too.
    text = OLD_REGISTRY + "\n## More\n\n**arguments:**\n\n" + CLAIMS_HEADER + claim_row("S5-1")
    path = write(tmp_path, text)
    assert coverage_main([str(path), "--strict"]) == 0
    assert any("near-miss" in n for n in check_coverage(path).notes)
    report = check_registry(path)
    assert report.ok
    assert [f.severity for f in report.findings if "near-miss" in f.message] == ["note"]
    assert cr.main([str(path)]) == 0
