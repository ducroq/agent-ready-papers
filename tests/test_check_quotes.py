"""Tests for tools/check_quotes.py (issue #48).

The normalisation cases are the extraction faults that produced false misses in practice:
ligatures, OCR substitutions, curly quotes, hyphenation, a decimal read as a colon, and a quote
running across a page break. PDF extraction is not exercised here (it needs poppler); the PDF path
is covered through `has_text_layer` on synthetic pages.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

from tools.check_quotes import Page, _attach_overlays, columns_text, find, has_text_layer, load, main, normalise


def test_normalise_folds_extraction_noise():
    assert normalise("signi®cant") == normalise("significant")
    assert normalise("the ﬁrst") == normalise("the first")
    assert normalise("“it all comes together”") == normalise('"it all comes together"')
    assert normalise("predict-\ning") == normalise("predicting")
    assert normalise("48:5 ± 1:3%") != normalise("48.5 ± 1.3%")  # strict: a colon is not a decimal
    assert normalise("48:5 ± 1:3%", lenient=True) == normalise("48.5 ± 1.3%", lenient=True)


def test_find_reports_printed_page_and_crosses_page_breaks():
    pages = [Page("p. 141", "There was not a lot known"), Page("p. 142", "about the neocortex in 1980.")]
    r = find("there was not a lot known about the neocortex", [pages])
    assert r.found and r.page == "p. 141"


def test_find_tries_every_reading():
    scrambled = [Page("pdf p. 1", "column A line one column B line one")]
    ordered = [Page("pdf p. 1", "column A line one column A line two")]
    assert find("column A line one column A line two", [scrambled, ordered]).found


def test_missing_quote_is_reported():
    assert not find("words that are not there", [[Page("text", "other words entirely")]]).found


def test_no_text_layer_detected():
    assert not has_text_layer([[Page("pdf p. 1", "© 1986"), Page("pdf p. 2", "")]])
    assert has_text_layer([[Page("pdf p. 1", "word " * 100)]])


def _epub(tmp: Path) -> Path:
    path = tmp / "book.epub"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("OEBPS/content.opf",
                   '<package><manifest><item id="c1" href="c1.xhtml"/></manifest>'
                   '<spine><itemref idref="c1"/></spine></package>')
        z.writestr("OEBPS/c1.xhtml",
                   '<html><body><span epub:type="pagebreak" id="page_6"/>Earlier text.'
                   '<span epub:type="pagebreak" id="page_7"/>forms of brain-based prediction – '
                   "‘controlled hallucinations’ – that arise</body></html>")
    return path


def test_epub_page_markers(tmp_path):
    r = find("forms of brain-based prediction - 'controlled hallucinations' - that arise", load(_epub(tmp_path)))
    assert r.found and r.page == "p. 7"


def test_cli_exit_codes(tmp_path, capsys):
    src = tmp_path / "s.txt"
    src.write_text("The procedure repeatedly adjusts the weights of the connections.", encoding="utf-8")
    assert main([str(src), "repeatedly adjusts the weights"]) == 0
    assert main([str(src), "repeatedly adjusts the weights", "not in the source"]) == 1
    assert main([str(tmp_path / "absent.txt"), "x"]) == 2


def test_columns_text_reads_column_by_column():
    # Two columns, the left ending mid-sentence on each line; a gutter between x=100 and x=120.
    words = [(10, 60, 10, "a"), (61, 95, 10, "difference"), (125, 160, 10, "dren."),
             (10, 40, 20, "of"), (41, 70, 20, "up"), (71, 95, 20, "to"), (125, 170, 20, "What"),
             (10, 60, 30, "five"), (61, 95, 30, "orders"), (125, 170, 30, "accounts")]
    text = columns_text(words, 200)
    assert find("a difference of up to five orders", [[Page("pdf p. 1", text)]]).found
    assert " ".join(text.split()).startswith("a difference of up to five orders")


def test_no_false_found_on_numbers_or_word_boundaries():
    src = [[Page("text", "The best model explains 48:5 ± 1:3% of the variance, said the therapist.")]]
    hit = find("explains 48.5 ± 1.3% of the variance", src)
    assert hit.found and hit.note and "lenient" in hit.note  # found only by the labelled lenient pass
    assert not find("explains 4.85 ± 1.3% of the variance", src).found
    assert not find("said the the rapist", src).found
    assert not find("explains 48 5 of", src).found  # a decimal is one token, not two numbers


def test_short_quotes_and_unreadable_quotes_file_are_tooling_errors(tmp_path):
    src = tmp_path / "s.txt"
    src.write_text("one two three four", encoding="utf-8")
    assert main([str(src), "two"]) == 2
    assert main([str(src), "--quotes-file", str(tmp_path / "missing.txt")]) == 2


def test_comparison_signs_and_minus_are_kept():
    src = [[Page("text", "We found p > 0.05 for the effect, and a change of −3 points overall.")]]
    assert find("We found p > 0.05", src).found
    assert not find("We found p < 0.05", src).found
    assert not find("a change of 3 points overall", src).found


def test_partial_scan_is_no_text_layer():
    pages = [Page("pdf p. 1", "word " * 100)] + [Page(f"pdf p. {i}", "") for i in range(2, 5)]
    assert not has_text_layer([pages])
    figures = [Page(f"pdf p. {i}", "word " * 100) for i in range(4)] + [Page("fig", "Figure 1 caption")] * 5
    assert has_text_layer([figures])  # 5 of 9 pages are figures: still a text PDF


def test_unsupported_file_type_is_a_tooling_error(tmp_path):
    src = tmp_path / "book.mobi"
    src.write_bytes(b"binary")
    assert main([str(src), "three word quote"]) == 2


def test_epub_label_does_not_carry_over_between_files(tmp_path):
    path = tmp_path / "b.epub"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("content.opf", '<package><manifest><item id="a" href="a.xhtml"/><item id="b" href="b.xhtml"/>'
                   '</manifest><spine><itemref idref="a"/><itemref idref="b"/></spine></package>')
        z.writestr("a.xhtml", '<p><span epub:type="pagebreak" id="page_285"/>notes text here</p>')
        z.writestr("b.xhtml", "<h1>Measuring Consciousness chapter heading</h1>")
    r = find("Measuring Consciousness chapter heading", load(path))
    assert r.found and r.page == "b.xhtml, before its first page marker"


def test_round2_cases():
    def f(src, q):
        return find(q, [[Page("text", src)]]).found
    # hyphenated words split at a line end match the quote's hyphenated form
    assert f("We are rapidly reverse-\nengineering the information processes", "We are rapidly reverse-engineering the information")
    assert f("both pre- and post-synaptic terminals", "and post-synaptic terminals")
    # signs and minus
    assert not f("so x \u2260 y holds here", "so x = y holds")
    assert not f("with r = -0.45 between the two", "r = 0.45 between")
    assert not f("with r = \u20130.45 between the two", "r = 0.45 between")
    assert f("with r = \u22120.45 between the two", "r = -0.45 between")
    # numbers keep their marks
    assert not f("about 1,000 neurons here", "about 1.000 neurons")
    r = find("a ratio of 3.1", [[Page("text", "a ratio of 3:1 here")]])
    assert not r.found or r.note  # never a plain FOUND; at most a CHECK for a human
    assert not f("about 10\u2076 neurons here", "about 106 neurons")
    assert f("about 10\u2076 neurons here", "about 10^6 neurons")
    assert f("about 10 6 neurons here", "about 10^6 neurons")  # PDF superscript as a separate word
    # a blank page between two text pages is not a gap
    pages = [Page("p. 1", "alpha beta gamma delta"), Page("p. 2", ""), Page("p. 3", "epsilon zeta eta")]
    r = find("gamma delta epsilon", [pages])
    assert r.found and r.page == "p. 1"


def test_ocr_only_match_is_check_and_exits_1(tmp_path, capsys):
    src = tmp_path / "s.txt"
    src.write_text("The best model explains 48:5 percent of the variance.", encoding="utf-8")
    assert main([str(src), "explains 48.5 percent of"]) == 1
    assert "CHECK" in capsys.readouterr().out


def test_round3_cases():
    def r(src, q):
        return find(q, [[Page("text", src)]])
    # LaTeX's overlay "≠" (U+0338 extracted before "=") is a negation, not "="
    assert not r("power and if k ̸= 0 holds", "power and if k = 0").found
    assert r("power and if k ̸= 0 holds", "power and if k ≠ 0").found
    # a minus on a bare decimal and in an exponent
    assert not r("The correlation was r = .45 overall", "correlation was r = -.45 overall").found
    assert not r("A rate of 10^3 per second", "A rate of 10^-3 per second").found
    # any maths symbol is a token
    assert not r("We required p ⩽ 0.05 throughout", "We required p ⩾ 0.05 throughout").found
    assert not r("Mean RT was ~450 ms", "Mean RT was 450 ms").found
    # a range stays a range
    assert r("pages 279 –296 of the volume", "pages 279-296 of").found
    # footnote markers and '11, 000' only leniently: CHECK, never a plain FOUND
    hit = r("the posterior probability12 of your model", "posterior probability of your model")
    assert hit.found and hit.note
    hit = r("more than 11, 000 units here", "more than 11,000 units")
    assert hit.found and hit.note


def test_overlay_glyph_attaches_to_the_sign_it_negates():
    words = [(10, 15, 10, "k"), (20, 26, 10, "="), (21, 25, 10, "\u0338"), (30, 36, 10, "0"), (40, 80, 10, "holds")]
    text = columns_text(_attach_overlays(words), 200)
    assert find("k \u2260 0 holds", [[Page("pdf p. 1", text)]]).found
    assert not find("k = 0 holds", [[Page("pdf p. 1", text)]]).found


def test_zero_width_overlay_attaches():
    words = [(10, 15, 10, "k"), (20, 20, 10, "\u0338"), (20, 26, 10, "="), (30, 36, 10, "0"), (40, 80, 10, "next")]
    text = columns_text(_attach_overlays(words), 200)
    assert not find("k = 0 next", [[Page("pdf p. 1", text)]]).found
    assert find("k \u2260 0 next", [[Page("pdf p. 1", text)]]).found
