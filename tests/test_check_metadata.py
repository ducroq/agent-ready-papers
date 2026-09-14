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


def test_parse_registry_keeps_every_occurrence_not_just_the_first():
    """OVERRULES the previous assertion, deliberately and with a reason.

    This test used to pin a file-global dedup: `[("10.1000/x", 1),
    ("10.2000/y", 2)]`, with the third line discarded. That dedup silently
    dropped every later citation of a DOI — so a source captioned correctly on
    one line and MISCAPTIONED on another was never checked on the second, and
    whether the miscaption surfaced depended on row order. Registry mode exists
    to catch exactly that, so the pinned behaviour defeated the mode's purpose.

    Measured 2026-09-14 before changing it: a registry citing 10.2196/52935 as
    "Mugaanyi et al. 2024" on one row and "Smith et al. 2019" on the next
    reported `3 checked` with the miscaptioned row absent from the report
    entirely; it now reports 2 entries, the second a year MISMATCH, exit 1.

    The cost the dedup was paying for is preserved: the CALLER caches the fetch
    per DOI, so the run above makes one network call for two entries.
    """
    content = "a 10.1000/x here\nb 10.2000/y there\nc 10.1000/x again\n"
    entries = _parse_registry(content)
    assert [(e.doi, e.line_number) for e in entries] == [
        ("10.1000/x", 1),
        ("10.2000/y", 2),
        ("10.1000/x", 3),
    ]


def test_registry_mode_makes_one_fetch_per_distinct_doi(tmp_path, monkeypatch):
    """The dedup moved from parsing to fetching; prove the saving survived."""
    import tools.check_metadata as m

    calls: list[str] = []

    def fake_fetch(doi, timeout, mailto):
        calls.append(doi)
        return ({"title": "T", "years": ("2024",), "surnames": ("x",), "venue": ""}, "stub", "found")

    monkeypatch.setattr(m, "_fetch_record", fake_fetch)
    reg = tmp_path / "r.md"
    reg.write_text("a 10.1000/x\nb 10.1000/x\nc 10.2000/y\n", encoding="utf-8")
    report = m.check_metadata(reg)
    assert len(report.results) == 3, "every occurrence must be checked"
    assert sorted(calls) == ["10.1000/x", "10.2000/y"], "one fetch per distinct DOI"


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
    # ⚠️ Assert the VENUE check, not the aggregate. `_worst(...) != "mismatch"`
    # cannot fail here: the venue branch only ever emits "ok" or "warn", so
    # the assertion passed against an implementation with NO venue check at
    # all — verified 2026-09-14 by deleting the whole venue block from
    # _compare_bib, which left the suite green.
    venue = [c for c in checks if c.field_name == "venue"]
    assert venue, "no venue check was produced at all"
    assert venue[0].verdict == "warn", f"expected the benign abbreviation case: {venue[0]}"
    assert "abbreviation is normal" in venue[0].note


def test_title_subtitle_truncation_does_not_fail():
    record = {**WHETTEN, "title": "What Constitutes a Theoretical Contribution? A Review"}
    checks = _compare_bib(
        _bib_entry(author="Whetten, David A.", title="What Constitutes a Theoretical Contribution?", year="1989"),
        record,
    )
    # Same reasoning as the venue test above: name the field under test.
    title = [c for c in checks if c.field_name == "title"]
    assert title, "no title check was produced at all"
    assert title[0].verdict == "ok", f"subtitle truncation should match: {title[0]}"


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


# --- the network layer: a DOI we could not check is not a DOI that is absent --
#
# Seeded 2026-09-14. The caller decided the verdict with `"404" in note`, and
# the note for "Crossref said 404, DataCite was unreachable" is
# `"Crossref 404; DataCite: <error>"` — which contains "404". So an arXiv DOI on
# any DataCite outage or proxied network rendered as NO RECORD: a real paper
# reported as fabricated, in a tool whose purpose is catching fabrication.
# Before this there was NO test of the network layer at all.


def _stub_get_json(monkeypatch, crossref, datacite):
    import tools.check_metadata as m

    def fake(host, path, timeout):
        return crossref if host == m.CROSSREF_HOST else datacite

    monkeypatch.setattr(m, "_get_json", fake)


@pytest.mark.parametrize(
    "crossref,datacite,expected_outcome",
    [
        ((None, 404, "404"), (None, 404, "404"), "absent"),
        ((None, 404, "404"), (None, None, "gaierror"), "unreachable"),
        ((None, None, "timeout"), (None, 404, "404"), "unreachable"),
        (({"message": {}}, 200, "Crossref"), (None, 404, "404"), "found"),
    ],
)
def test_fetch_record_reports_absent_and_unreachable_distinctly(monkeypatch, crossref, datacite, expected_outcome):
    """Only BOTH agencies answering 404 licenses 'absent'. Anything else is
    'unreachable', which must not render as NO RECORD."""
    import tools.check_metadata as m

    _stub_get_json(monkeypatch, crossref, datacite)
    _record, _note, outcome = m._fetch_record("10.1234/abcd", 5.0, None)
    assert outcome == expected_outcome


def test_unreachable_datacite_is_not_reported_as_no_record(monkeypatch):
    """The exact regression: Crossref 404 + DataCite unreachable must NOT
    produce the 'unresolved' verdict that renders as NO RECORD."""
    import tools.check_metadata as m

    _stub_get_json(monkeypatch, (None, 404, "404"), (None, None, "gaierror: no name"))
    record, note, outcome = m._fetch_record("10.48550/arXiv.2601.00828", 5.0, None)
    assert record is None
    assert outcome == "unreachable"
    verdict = "unresolved" if outcome == "absent" else "error"
    assert verdict == "error", "an unreachable DOI must not be called NO RECORD"
    assert "unreachable" in note


# --- an entry where nothing was compared is not an entry that passed ---------
#
# Seeded 2026-09-14. `_worst` ranked only mismatch/warn, so a bib entry whose
# every field check came back "absent" fell through to "ok" — and to_markdown
# suppresses the detail block for "ok", so the word "absent" never reached the
# reader. A bare `@article{k, doi = {...}}` reported OK and passed --strict.
# Zero fields compared was indistinguishable from all fields matching.


def test_worst_returns_unchecked_when_nothing_was_comparable():
    from tools.check_metadata import FieldCheck, _worst

    absent_only = (
        FieldCheck("title", "", "remote title", "absent", "no local title"),
        FieldCheck("author", "", "remote authors", "absent", "no local author field"),
    )
    assert _worst(absent_only) == "unchecked"


def test_worst_still_ranks_normally_when_something_was_compared():
    """The guard must not fire when any real comparison happened."""
    from tools.check_metadata import FieldCheck, _worst

    assert _worst((FieldCheck("title", "a", "a", "ok", ""),)) == "ok"
    assert (
        _worst(
            (
                FieldCheck("title", "a", "a", "ok", ""),
                FieldCheck("author", "", "x", "absent", "no local author field"),
            )
        )
        == "ok"
    )
    assert _worst((FieldCheck("t", "a", "b", "warn", ""),)) == "warn"
    assert _worst((FieldCheck("t", "a", "b", "mismatch", ""),)) == "mismatch"


def test_offline_with_strict_is_refused_not_silently_passed(tmp_path, capsys):
    """Seeded 2026-09-14: `if args.offline: return 0` sat ABOVE the --strict
    branch, so --offline --strict exited 0 unconditionally. A CI step that
    inherited --offline could never fail — the exact hazard tools/README.md
    documents for the sibling tool while asserting the flag is check_dois only.
    """
    from tools.check_metadata import main

    bib = tmp_path / "r.bib"
    bib.write_text("@article{k,\n  doi = {10.2196/52935},\n  title = {T}\n}\n", encoding="utf-8")
    assert main([str(bib), "--offline", "--strict"]) == 2
    assert "Drop one of them" in capsys.readouterr().err
    # offline alone still succeeds: it is a legitimate parse-only mode
    assert main([str(bib), "--offline"]) == 0
