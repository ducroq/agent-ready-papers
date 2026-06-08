"""Shape-pin tests for tools.check_dois.

These tests assert the DOI extraction contract against the Paper 1
fixture. The xfail tests become PASS once the extractor lands. The
DOI set was independently verified in DR-011 Pass 1 review (Haiku,
2026-06-08) against the regex `10\\.\\d{4,9}/[^\\s\\]\\)\\\"<>]+`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.check_dois import DOIReport, DOIResult, _clean_doi, check_dois

EXPECTED_DOIS = {
    "10.2196/52935",
    "10.2307/25148742",
    "10.18653/v1/2024.acl-long.552",
    "10.5465/amr.1989.4308371",
    "10.1056/AIoa2400196",
    "10.1038/s41562-025-02273-8",
    "10.1002/14651858.MR000030.pub2",
    "10.1016/S0140-6736(13)62228-X",
    "10.2753/MIS0742-1222240302",
}


def test_dataclass_shape_is_stable():
    result = DOIResult(
        doi="10.2196/52935",
        line_number=87,
        http_status=200,
        parseable=True,
        resolved=True,
        note="",
    )
    assert result.resolved is True
    with pytest.raises((AttributeError, TypeError)):
        result.resolved = False  # type: ignore[misc]


def test_check_dois_raises_filenotfound_on_missing_path():
    with pytest.raises(FileNotFoundError):
        check_dois(Path("does-not-exist.md"))


def test_paper1_registry_doi_extraction(paper1_registry):
    """--offline must surface exactly the 9 known DOIs from the Paper 1 fixture."""
    report = check_dois(paper1_registry, offline=True)

    assert isinstance(report, DOIReport)
    assert report.offline is True

    extracted = {r.doi for r in report.results}
    assert extracted == EXPECTED_DOIS

    # Offline mode: parseable=True, resolved=False, by design.
    assert all(r.parseable for r in report.results)
    assert not any(r.resolved for r in report.results)
    assert report.all_parseable is True
    assert report.all_resolved is False

    # Line numbers must be populated (≥1, never zero).
    assert all(r.line_number >= 1 for r in report.results)


def test_paper1_doi_extraction_is_deterministic(paper1_registry):
    """Same input → byte-identical output across runs (#8 from DR-011 review)."""
    r1 = check_dois(paper1_registry, offline=True)
    r2 = check_dois(paper1_registry, offline=True)
    assert r1.to_markdown() == r2.to_markdown()
    assert r1.to_dict() == r2.to_dict()


def test_clean_doi_strips_trailing_punctuation():
    assert _clean_doi("10.2196/52935.") == "10.2196/52935"
    assert _clean_doi("10.2196/52935,") == "10.2196/52935"
    assert _clean_doi("10.2196/52935:") == "10.2196/52935"
    assert _clean_doi("10.2196/52935;") == "10.2196/52935"


def test_clean_doi_strips_unbalanced_closing_paren():
    """Markdown wraps DOIs: `(DOI: 10.xxx/abc)` → regex captures 'abc)' → strip."""
    assert _clean_doi("10.2196/52935)") == "10.2196/52935"
    assert _clean_doi("10.2196/52935):") == "10.2196/52935"


def test_clean_doi_preserves_balanced_parens():
    """Lancet DOIs carry '(13)' mid-string — must not be stripped (the fix
    that caused DR-011 Pass 2 to remark this needed an explicit test).
    """
    assert (
        _clean_doi("10.1016/S0140-6736(13)62228-X")
        == "10.1016/S0140-6736(13)62228-X"
    )


def test_clean_doi_handles_wrapped_lancet_doi():
    """The real edge case: a balanced-paren DOI wrapped in prose parens."""
    assert (
        _clean_doi("10.1016/S0140-6736(13)62228-X)")
        == "10.1016/S0140-6736(13)62228-X"
    )
