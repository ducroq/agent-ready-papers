"""Tests for tools.check_metadata.

Offline by design. Every test here exercises parsing, normalisation, or
comparison against a hand-built record — nothing contacts Crossref or
DataCite, so the suite stays deterministic and runnable without network.

The comparison tests are regression pins for the three bugs the first
real run against `papers/perspective/references.bib` exposed:
LaTeX-accented surnames reading as author mismatches, a Crossref 301
reading as an error, and arXiv DOIs (DataCite-registered) reading as
having no record.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.check_metadata import (
    FieldCheck,
    MetadataResult,
    _clean_doi,
    _compare_bib,
    _compare_registry,
    _containment,
    _LocalEntry,
    _normalise,
    _parse_bib,
    _parse_registry,
    _record_from_crossref,
    _record_from_datacite,
    _split_authors,
    _worst,
    check_metadata,
)

WHETTEN = {
    "title": "What Constitutes a Theoretical Contribution?",
    "years": {1989},
    "surnames": ("whetten",),
    "venue": "The Academy of Management Review",
    "agency": "Crossref",
}


def _bib_entry(**fields) -> _LocalEntry:
    return _LocalEntry(key="k", line_number=1, doi="10.5465/amr.1989.4308371", fields=fields)


# --------------------------------------------------------------------------
# normalisation
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (r"Schl{\"u}ssel", "schlussel"),
        (r"Hr{\o}bjartsson", "hrobjartsson"),
        (r"Mu{\~n}oz", "munoz"),
        (r"{\c{C}}elik", "celik"),
        (r"Stra{\ss}e", "strasse"),
        (r"G{\"o}del", "godel"),
        ("Mayo-Wilson", "mayo wilson"),
    ],
)
def test_normalise_folds_latex_accents_to_base_letters(raw, expected):
    """Regression: a naive `\\[a-z]+ -> space` rule split these into two words,
    which then read as author mismatches against Crossref."""
    assert _normalise(raw) == expected


def test_split_authors_handles_both_bibtex_name_orders():
    assert _split_authors("Whetten, David A. and Toulmin, Stephen") == ("whetten", "toulmin")
    assert _split_authors("David A. Whetten and Stephen Toulmin") == ("whetten", "toulmin")


def test_split_authors_survives_accented_surnames():
    assert _split_authors(r"Schl{\"u}ssel, Michael and Hr{\o}bjartsson, Asbj{\o}rn") == (
        "schlussel",
        "hrobjartsson",
    )


def test_containment_is_relative_to_the_shorter_side():
    # A truncated subtitle must not read as a different paper.
    assert _containment("The Nature of Theory", "The Nature of Theory in Information Systems") == 1.0
    assert _containment("something else entirely", "The Nature of Theory") < 0.3


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("10.2196/52935", "10.2196/52935"),
        ("10.2196/52935.", "10.2196/52935"),
        ("10.1016/S0140-6736(13)62228-X", "10.1016/S0140-6736(13)62228-X"),
        ("10.2196/52935)", "10.2196/52935"),
    ],
)
def test_clean_doi_balances_parens(raw, expected):
    assert _clean_doi(raw) == expected


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------


def test_parse_bib_extracts_key_doi_and_fields():
    content = (
        "@article{whetten1989,\n"
        "  author  = {Whetten, David A.},\n"
        '  title   = "What Constitutes a Theoretical Contribution?",\n'
        "  year    = {1989},\n"
        "  doi     = {10.5465/amr.1989.4308371}\n"
        "}\n"
    )
    (entry,) = _parse_bib(content)
    assert entry.key == "whetten1989"
    assert entry.doi == "10.5465/amr.1989.4308371"
    assert entry.fields["year"] == "1989"
    assert entry.fields["title"] == "What Constitutes a Theoretical Contribution?"


def test_parse_bib_honours_nested_braces_in_titles():
    content = "@article{k,\n  title = {A {Nested} Title},\n  doi = {10.1/x}\n}\n"
    (entry,) = _parse_bib(content)
    assert entry.fields["title"] == "A {Nested} Title"


def test_parse_bib_finds_a_doi_hidden_in_a_url_field():
    content = "@misc{k,\n  title = {T},\n  url = {https://doi.org/10.48550/arXiv.2409.16813}\n}\n"
    (entry,) = _parse_bib(content)
    assert entry.doi == "10.48550/arXiv.2409.16813"


def test_parse_bib_records_entries_without_a_doi():
    content = "@book{toulmin2003,\n  title = {The Uses of Argument},\n  year = {2003}\n}\n"
    (entry,) = _parse_bib(content)
    assert entry.doi == ""


def test_parse_registry_dedupes_and_keeps_first_line_number():
    content = "a 10.1000/x here\nb 10.2000/y there\nc 10.1000/x again\n"
    entries = _parse_registry(content)
    assert [(e.doi, e.line_number) for e in entries] == [("10.1000/x", 1), ("10.2000/y", 2)]


# --------------------------------------------------------------------------
# record normalisation
# --------------------------------------------------------------------------


def test_record_from_crossref_collects_every_associated_year():
    """Online-first publishing gives issued and published-print different
    years; accepting any of them avoids flagging a correct entry."""
    record = _record_from_crossref(
        {
            "title": ["T"],
            "issued": {"date-parts": [[2025]]},
            "published-print": {"date-parts": [[2026, 3]]},
            "author": [{"family": "Song"}, {"family": "Hu"}],
            "container-title": ["AI & SOCIETY"],
        }
    )
    assert record["years"] == {2025, 2026}
    assert record["surnames"] == ("song", "hu")
    assert record["agency"] == "Crossref"


def test_record_from_datacite_maps_arxiv_shape():
    record = _record_from_datacite(
        {
            "data": {
                "attributes": {
                    "titles": [{"title": "PeerArg"}],
                    "publicationYear": 2024,
                    "creators": [{"familyName": "Sukpanichnant"}],
                    "publisher": "arXiv",
                }
            }
        }
    )
    assert record["title"] == "PeerArg"
    assert record["years"] == {2024}
    assert record["surnames"] == ("sukpanichnant",)
    assert record["agency"] == "DataCite"


# --------------------------------------------------------------------------
# comparison — the two failure shapes from Rao & Callison-Burch (COLM 2026)
# --------------------------------------------------------------------------


def test_correct_entry_passes_every_field():
    checks = _compare_bib(
        _bib_entry(
            author="Whetten, David A.",
            title="What Constitutes a Theoretical Contribution?",
            year="1989",
            journal="Academy of Management Review",
        ),
        WHETTEN,
    )
    assert _worst(checks) == "ok"


def test_isolated_field_error_is_a_mismatch_on_that_field_alone():
    checks = _compare_bib(
        _bib_entry(
            author="Whetten, David A.",
            title="What Constitutes a Theoretical Contribution?",
            year="1991",
            journal="Academy of Management Review",
        ),
        WHETTEN,
    )
    assert _worst(checks) == "mismatch"
    assert [c.field_name for c in checks if c.verdict == "mismatch"] == ["year"]


def test_wholesale_substitution_trips_title_year_and_author():
    checks = _compare_bib(
        _bib_entry(
            author="Fleming, Alexander",
            title="On the Antibacterial Action of Cultures of a Penicillium",
            year="1929",
            journal="British Journal of Experimental Pathology",
        ),
        WHETTEN,
    )
    failed = {c.field_name for c in checks if c.verdict == "mismatch"}
    assert failed == {"title", "year", "author"}


def test_first_author_present_but_coauthor_missing_is_only_a_warning():
    checks = _compare_bib(
        _bib_entry(
            author="Whetten, David A. and Ghost, A.", title="What Constitutes a Theoretical Contribution?", year="1989"
        ),
        WHETTEN,
    )
    assert _worst(checks) == "warn"


def test_venue_abbreviation_does_not_fail():
    checks = _compare_bib(
        _bib_entry(
            author="Whetten, David A.",
            title="What Constitutes a Theoretical Contribution?",
            year="1989",
            journal="Acad. Manage. Rev.",
        ),
        WHETTEN,
    )
    assert _worst(checks) != "mismatch"


def test_title_subtitle_truncation_does_not_fail():
    record = {**WHETTEN, "title": "What Constitutes a Theoretical Contribution? A Review"}
    checks = _compare_bib(
        _bib_entry(author="Whetten, David A.", title="What Constitutes a Theoretical Contribution?", year="1989"),
        record,
    )
    assert _worst(checks) != "mismatch"


# --------------------------------------------------------------------------
# registry mode
# --------------------------------------------------------------------------


def test_registry_mode_flags_a_wrong_year_in_prose():
    entry = _LocalEntry(
        key="",
        line_number=3,
        doi="10.5465/amr.1989.4308371",
        fields={"_context": "Whetten 1991 (AMR, DOI: 10.5465/amr.1989.4308371): four components"},
    )
    checks = _compare_registry(entry, WHETTEN)
    assert _worst(checks) == "mismatch"


def test_registry_mode_accepts_correct_prose():
    entry = _LocalEntry(
        key="",
        line_number=3,
        doi="10.5465/amr.1989.4308371",
        fields={"_context": "Whetten 1989 (AMR, DOI: 10.5465/amr.1989.4308371): four components"},
    )
    assert _worst(_compare_registry(entry, WHETTEN)) == "ok"


def test_registry_mode_does_not_check_titles():
    """Regression: the title check warned on 8 of 9 correct rows in this
    repo's own registry, because registry prose cites sources rather than
    quoting their titles."""
    entry = _LocalEntry(
        key="",
        line_number=3,
        doi="10.5465/amr.1989.4308371",
        fields={"_context": "Whetten 1989 (AMR): four components"},
    )
    assert "title" not in {c.field_name for c in _compare_registry(entry, WHETTEN)}


# --------------------------------------------------------------------------
# contract
# --------------------------------------------------------------------------


def test_dataclasses_are_frozen():
    check = FieldCheck("year", "1989", "1989", "ok")
    with pytest.raises((AttributeError, TypeError)):
        check.verdict = "mismatch"  # type: ignore[misc]


def test_failed_fields_lists_only_mismatches():
    result = MetadataResult(
        doi="10.1/x",
        line_number=1,
        entry_key="k",
        verdict="mismatch",
        checks=(
            FieldCheck("year", "1991", "1989", "mismatch"),
            FieldCheck("venue", "a", "b", "warn"),
            FieldCheck("title", "t", "t", "ok"),
        ),
    )
    assert result.failed_fields == ("year",)


def test_check_metadata_raises_filenotfound_on_missing_path():
    with pytest.raises(FileNotFoundError):
        check_metadata(Path("no/such/file.bib"))


def test_check_metadata_raises_valueerror_when_no_dois_present(tmp_path):
    path = tmp_path / "empty.bib"
    path.write_text("@book{k,\n  title = {No DOI Here}\n}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        check_metadata(path)


def test_offline_mode_parses_without_network(tmp_path):
    path = tmp_path / "x.bib"
    path.write_text(
        "@article{k,\n  title = {T},\n  year = {1989},\n  doi = {10.5465/amr.1989.4308371}\n}\n",
        encoding="utf-8",
    )
    report = check_metadata(path, offline=True)
    assert report.offline is True
    assert [r.verdict for r in report.results] == ["skipped"]
    assert report.to_markdown().startswith("# Metadata report")


def test_mode_is_chosen_by_suffix(tmp_path):
    bib = tmp_path / "a.bib"
    bib.write_text("@article{k,\n  doi = {10.1000/x}\n}\n", encoding="utf-8")
    md = tmp_path / "a.md"
    md.write_text("see DOI: 10.1000/x\n", encoding="utf-8")
    assert check_metadata(bib, offline=True).mode == "bib"
    assert check_metadata(md, offline=True).mode == "registry"
