"""Tests for tools/registry_edit.py: edits only claim-table rows, and only on exactly one match."""

from __future__ import annotations

from tools.registry_edit import main

REGISTRY = """## Priority Guide

| S7-3 | Butlin et al. 2023 method and conclusion | § 7 misreports its anchor source |

### Section 7

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S7-3 | Butlin et al. derive indicator properties | P0 | ESTABLISHED | Butlin et al. 2023 | D | [ ] |
| S7-4 | Another claim | P2 | ESTABLISHED | Someone 2023 | D | [ ] |
"""


def _reg(tmp_path):
    p = tmp_path / "claim_registry.md"
    p.write_text(REGISTRY, encoding="utf-8")
    return p


def test_append_edits_the_claim_row_not_the_priority_guide(tmp_path):
    p = _reg(tmp_path)
    assert main([str(p), "S7-3", "--append", "Full text read 2026-10-08."]) == 0
    text = p.read_text(encoding="utf-8")
    assert "| S7-3 | Butlin et al. 2023 method and conclusion | § 7 misreports" in text
    assert "derive indicator properties. Full text read 2026-10-08. | P0 |" in text


def test_status_and_replace(tmp_path):
    p = _reg(tmp_path)
    assert main([str(p), "S7-4", "--status", "x", "--replace", "Another", "A verified"]) == 0
    assert "| S7-4 | A verified claim | P2 | ESTABLISHED | Someone 2023 | D | [x] |" in p.read_text(encoding="utf-8")


def test_refuses_zero_or_several_matches(tmp_path):
    p = _reg(tmp_path)
    assert main([str(p), "S9-9", "--append", "x"]) == 1
    p.write_text(REGISTRY + "| S7-4 | Duplicate | P2 | ESTABLISHED | X | D | [ ] |\n", encoding="utf-8")
    before = p.read_text(encoding="utf-8")
    assert main([str(p), "S7-4", "--append", "x"]) == 1
    assert p.read_text(encoding="utf-8") == before


def test_refuses_missing_replace_text_and_dry_run_writes_nothing(tmp_path):
    p = _reg(tmp_path)
    assert main([str(p), "S7-3", "--replace", "not there", "y"]) == 1
    assert main([str(p), "S7-3", "--append", "z", "--dry-run"]) == 0
    assert p.read_text(encoding="utf-8") == REGISTRY


def test_refuses_unescaped_pipe_and_reports_unreadable_registry(tmp_path):
    p = _reg(tmp_path)
    assert main([str(p), "S7-3", "--append", "a | b"]) == 1
    assert p.read_text(encoding="utf-8") == REGISTRY
    assert main([str(p), "S7-3", "--append", r"a \| b"]) == 0
    assert main([str(tmp_path / "missing.md"), "S7-3", "--append", "x"]) == 2


def test_keeps_crlf_line_endings(tmp_path):
    p = tmp_path / "claim_registry.md"
    p.write_bytes(REGISTRY.replace("\n", "\r\n").encode())
    assert main([str(p), "S7-4", "--status", "x"]) == 0
    assert b"| [x] |\r\n" in p.read_bytes()


def test_refuses_line_breaks_keeps_ellipsis_and_skips_code_fences(tmp_path):
    p = _reg(tmp_path)
    assert main([str(p), "S7-3", "--append", "line1\nline2"]) == 1
    p.write_text(REGISTRY.replace("Another claim", "Another claim...")
                 + "\n```\n| S7-4 | Example in a fence | P2 | X | Y | D | [ ] |\n```\n", encoding="utf-8")
    assert main([str(p), "S7-4", "--append", "Read."]) == 0
    text = p.read_text(encoding="utf-8")
    assert "Another claim.... Read. | P2 |" in text
    assert "| S7-4 | Example in a fence | P2 |" in text


def test_round2_registry_cases(tmp_path):
    p = tmp_path / "claim_registry.md"
    base = ("| ID | Statement | Priority | Confidence | Source | Source Tier | Status |\n"
            "|----|-----------|----------|------------|--------|-------------|--------|\n"
            "| S2-1 | a claim \\| b | P1 | ESTABLISHED | X | A | [ ] |\n")
    p.write_text(base, encoding="utf-8")
    assert main([str(p), "S2-1", "--replace", "\\", ""]) == 1  # would un-escape a pipe
    assert main([str(p), "S2-1", "--append", "one\u2028two"]) == 1  # splitlines would break the row
    assert p.read_text(encoding="utf-8") == base
    fenced = base + "````\n```python\n| S2-1 | example | P1 | E | X | A | [ ] |\n```\n````\n"
    p.write_text(fenced, encoding="utf-8")
    assert main([str(p), "S2-1", "--status", "x"]) == 0  # the example inside the 4-tick fence is skipped
    assert "| example | P1 | E | X | A | [ ] |" in p.read_text(encoding="utf-8")


def test_replace_needs_a_unique_nonempty_old(tmp_path):
    p = _reg(tmp_path)
    p.write_text(REGISTRY.replace("Another claim", "Another claim about a claim"), encoding="utf-8")
    assert main([str(p), "S7-4", "--replace", "claim", "x"]) == 1  # "claim" occurs twice
    assert main([str(p), "S7-4", "--replace", "", "Note: "]) == 1
    assert not (tmp_path / "claim_registry.md.tmp").exists()


def test_non_utf8_registry_is_a_tooling_error(tmp_path):
    p = tmp_path / "reg.md"
    p.write_bytes(b"| S1-1 | caf\xe9 | P1 | E | X | A | [ ] |\n")
    assert main([str(p), "S1-1", "--status", "x"]) == 2
