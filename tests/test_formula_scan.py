"""Tests for extensions/formula_scan.py (PROPOSED under DR-022).

Each signal is exercised against seeded input it must flag and against input
it must not. A signal that only ever sees clean input cannot be told apart
from an absent one (docs/verification-hooks.md). The varied fixture clears
every minimum (sentences, paragraphs, lists, sections), so its "no flags"
result is a measurement, not a gate that never opened.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "formula_scan", Path(__file__).resolve().parent.parent / "extensions" / "formula_scan.py"
)
fs = importlib.util.module_from_spec(_SPEC)
sys.modules["formula_scan"] = fs  # dataclasses resolve types through sys.modules
_SPEC.loader.exec_module(fs)


def _write(tmp_path: Path, text: str, name: str = "doc.md") -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def _signals(report) -> set[str]:
    return {f.signal for f in report.flags}


def _messages(report, signal: str) -> list[str]:
    return [f.message for f in report.flags if f.signal == signal]


# Seven sections built on one template: same opener, a negation-contrast
# turn, a triad, uniform short sentences, and a "Takeaway:" closer.
SECTION = """## Part {n}

Here is the thing about {topic}. It is not a rule. It is a habit. You use it, you trust it, and you forget it.

The pattern is simple. The pattern is old. The pattern is everywhere. The pattern is quiet. The pattern is yours.

*Takeaway:* When did you last notice {topic}?
"""
TOPICS = ["habits", "maps", "clocks", "ledgers", "rituals", "forms", "badges"]
FORMULAIC = "# Title\n\n" + "\n".join(SECTION.format(n=i, topic=t) for i, t in enumerate(TOPICS, 1))

# Clears every minimum: 20+ sentences, 6+ prose paragraphs, 5+ lists of mixed
# length, 3+ sections with different openings and endings.
VARIED = """# A varied piece

## Winter

The river froze early that year, and nobody in the village could remember a December so hard.

Why? Nobody knew. The miller blamed the moon, which was absurd, though he said it with such conviction that two of his neighbours, both otherwise sensible people, repeated it at the market for a week.

They stocked flour and salt before the roads closed.

## Ice

By February the ice had grown thick enough to carry a cart loaded with barrels, planks, rope, nails and a stubborn goat. Children skated. Old men argued about whether the fish below were sleeping or dead, a question that mattered to exactly one of them, the one who sold fish.

Spring came late and all at once, bringing mud and geese.

The baker, the smith, the priest and the schoolteacher met to discuss the bridge, and agreed on nothing whatsoever, which surprised no one who had lived there longer than a season.

## Thaw

In the end the thaw took the bridge. It had stood for ninety years, longer than anyone alive, and it went in an afternoon while the whole village watched from the bank and said very little.

A ferry was improvised from two doors and a tabletop. It sank. The second one, built by the smith with more care and considerably more swearing, held for the rest of the summer and carried sheep, pigs, hens, a piano, a bishop and, on one memorable occasion, a wedding.

Somebody kept a list of everything it carried. Nobody ever found it.

## Summer

The ferryman charged a penny, an egg, a song or a story, depending on his mood. Most people paid in stories. Some of them were even true.

By August the new bridge had a design, a budget, a committee, a quarrel and a plaque, but no stones. It has none still.
"""


def test_formulaic_text_flags_every_structural_signal(tmp_path):
    r = fs.scan(_write(tmp_path, FORMULAIC))
    assert {"rhythm", "contrast", "lists", "phrases", "openers", "template"} <= _signals(r)
    msgs = _messages(r, "template")
    assert any('label "Takeaway:"' in m for m in msgs)
    assert any("close on a question" in m for m in msgs)
    assert any('open with "here is"' in m for m in msgs)


def test_varied_text_clears_every_minimum_and_raises_no_structural_flags(tmp_path):
    r = fs.scan(_write(tmp_path, VARIED))
    assert r.not_evaluated == {}, r.not_evaluated  # every gate open: the result below is a measurement
    assert not ({"rhythm", "paragraphs", "contrast", "lists", "template"} & _signals(r)), r.flags


def test_low_sentence_cv_flag_fires(tmp_path):
    # 24 sentences of 7 or 9 words: CV about 0.13, alternating so no long monotone run is needed.
    s7, s9 = "The cat sat by the warm stove.", "The old dog slept on the rug all day."
    text = " ".join([s7, s9] * 12)
    r = fs.scan(_write(tmp_path, text))
    assert any("sentence-length variation is low" in m for m in _messages(r, "rhythm"))


def test_uniform_paragraphs_flag_fires_and_list_items_are_excluded(tmp_path):
    para = "One two three four five six seven eight nine ten.\n\n"
    r = fs.scan(_write(tmp_path, para * 6))
    assert "paragraphs" in _signals(r)
    # Six uniform prose paragraphs plus wildly uneven list items: the items must not
    # count, or the CV would rise above the threshold and the flag would vanish.
    listy = para * 6 + "- a b\n- c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g h\n"
    r2 = fs.scan(_write(tmp_path, listy, "b.md"))
    assert "paragraphs" in _signals(r2) and r2.metrics["paragraph_length_cv"] == 0.0


def test_gated_metrics_are_marked_not_evaluated(tmp_path):
    r = fs.scan(_write(tmp_path, "One short line. Another one here. A third.\n"))
    assert set(r.not_evaluated) >= {"sentence_length_cv", "paragraph_length_cv", "triad_share", "template_features"}
    assert "not evaluated" in r.to_markdown()


def test_negation_contrast_forms(tmp_path):
    text = (
        "It is not a bug. It is a feature.\n\n"
        "This is not just a tool but a habit.\n\n"
        "They were not only late but also rude.\n\n"
        "The work isn't finished, it's abandoned.\n"
    )
    r = fs.scan(_write(tmp_path, text))
    assert r.metrics["negation_contrast"] == 4


def test_plain_negation_is_not_a_contrast(tmp_path):
    text = "The results do not support the hypothesis. The sample was small and the effect was weak.\n"
    assert fs.scan(_write(tmp_path, text)).metrics["negation_contrast"] == 0


def test_contrast_does_not_cross_paragraphs(tmp_path):
    assert fs.scan(_write(tmp_path, "That was not the plan.\n\nIt is late now.\n")).metrics["negation_contrast"] == 0


def test_list_sizes_and_triad_share(tmp_path):
    triads = "\n\n".join(f"We bought apples, pears, and plums on day {d}." for d in "abcde")
    r = fs.scan(_write(tmp_path, triads))
    assert r.metrics["lists"] == 5 and r.metrics["triad_share"] == 1.0
    assert "lists" in _signals(r)
    mixed = "We bought apples, pears, plums, and figs. We saw red, green, blue, cyan, and grey.\n"
    assert fs.scan(_write(tmp_path, mixed, "b.md")).metrics["triad_share"] == 0.0


@pytest.mark.parametrize(
    "sentence",
    [
        "It happened in 2023, 2024, and 2025 again.",
        "As argued by Smith, Jones, and Lee (2020) at length.",
        "Work by Smith, Jones, and Lee et al. was cited.",
    ],
)
def test_dates_and_author_lists_are_not_triads(tmp_path, sentence):
    assert fs.scan(_write(tmp_path, sentence + "\n")).metrics["lists"] == 0


def test_monotone_run_detected_and_broken(tmp_path):
    r = fs.scan(_write(tmp_path, " ".join(["The cat sat on the mat today."] * 6)))
    assert r.metrics["monotone_runs"] == 1
    broken = (
        "The cat sat on the mat today. " * 2
        + "Then, without any warning at all, the whole house shook and the cat ran. "
        + "The cat sat on the mat today. " * 2
    )
    assert fs.scan(_write(tmp_path, broken, "b.md")).metrics["monotone_runs"] == 0


def test_style_vocabulary_with_provenance_and_inflections(tmp_path, monkeypatch):
    monkeypatch.setattr(fs, "STYLE_WORDS", {"delve": "K", "tapestry": "R", "intricate": "K"})
    text = "We delve into it. She delves deeper. A rich tapestry. The delivery was late. It was intricately made.\n"
    r = fs.scan(_write(tmp_path, text))
    assert len(r.vocabulary["delve"]) == 2  # "delivery" must not match
    assert len(r.vocabulary["tapestry"]) == 1
    assert len(r.vocabulary["intricate"]) == 1  # e-drop stem + "ely"
    assert "vocabulary" in _signals(r)
    assert "| delve | K | 2 |" in r.to_markdown()


def test_style_phrase_does_not_double_count_its_words(tmp_path, monkeypatch):
    monkeypatch.setattr(fs, "STYLE_WORDS", {"crucial": "K", "plays a crucial role": "W"})
    r = fs.scan(_write(tmp_path, "Salt plays a crucial role here. Water is crucial too.\n"))
    assert r.metrics["style_words"] == 2
    assert len(r.vocabulary["plays a crucial role"]) == 1 and len(r.vocabulary["crucial"]) == 1


def test_every_default_style_word_has_a_source():
    assert fs.STYLE_WORDS
    assert all(src and set(src) <= set("KRW,") for src in fs.STYLE_WORDS.values())


def test_line_numbers_point_at_the_hit_not_the_paragraph(tmp_path):
    text = "First line of the paragraph here.\nIt is not a bug.\nIt is a feature.\n"
    r = fs.scan(_write(tmp_path, text))
    assert r.metrics["negation_contrast"] == 1
    assert [s.line for p in fs.parse(text)[0].paragraphs for s in p.sentences] == [1, 2, 3]


def test_skips_tables_code_comments_and_front_matter(tmp_path):
    text = (
        "---\ntitle: x\n---\n\n"
        "| a | b |\n|---|---|\n| It is not x. It is y. | z |\n\n"
        "```\nIt is not x. It is y.\n```\n\n"
        "~~~\nIt is not x. It is y.\n~~~\n\n"
        "<!-- It is not x.\nIt is y. -->\n\n"
        "A plain sentence stands here alone.\n"
    )
    r = fs.scan(_write(tmp_path, text))
    assert r.sentences == 1 and r.metrics["negation_contrast"] == 0


def test_leading_horizontal_rule_is_not_front_matter(tmp_path):
    r = fs.scan(_write(tmp_path, "---\n\nBody para here with words.\n\n---\n\nMore body.\n"))
    assert r.sentences == 2


def test_blockquote_paragraphs_and_setext_headings(tmp_path):
    r = fs.scan(_write(tmp_path, "> Para one here.\n>\n> Para two here.\n"))
    assert r.paragraphs == 2
    setext = "One\n===\n\nText a.\n\nTwo\n---\n\nText b.\n\nThree\n=====\n\nText c.\n"
    assert fs.scan(_write(tmp_path, setext, "s.md")).sections == 3


def test_latex_preamble_tables_and_math_are_skipped(tmp_path):
    tex = (  # sections: the abstract's preamble section, One, Two
        "\\documentclass{article}\n\\usepackage{amsmath}\n\\begin{document}\n"
        "\\begin{abstract} The abstract body is prose.\n\\end{abstract}\n"
        "\\section{One}\nIt is not x. It is y. % It is not z. It is w.\n\n"
        "\\begin{tabular}{ll}\nID & Type & Priority & Tier \\\\\n\\end{tabular}\n\n"
        "\\begin{equation}\nE = mc^2 \\label{eq:1}\n\\end{equation}\n\n"
        "\\section{Two}\nPlain text with \\emph{emphasis} here \\cite{x}.\n"
        "\\end{document}\n"
    )
    r = fs.scan(_write(tmp_path, tex, "m.tex"))
    texts = [s.text for sec in fs.parse(tex, latex=True) for p in sec.paragraphs for s in p.sentences]
    assert any("abstract body" in t for t in texts)
    assert not any("article" in t or "Priority" in t or "mc" in t or "amsmath" in t for t in texts)
    assert r.sections == 3 and r.metrics["negation_contrast"] == 1


def test_abbreviations_do_not_split_but_no_does(tmp_path):
    r = fs.scan(_write(tmp_path, "Some tools, e.g. Pangram, are opaque (Emi et al. 2024). See Eq. 2 there.\n"))
    assert r.sentences == 2
    assert fs.scan(_write(tmp_path, "Is it hard? No. It is simple.\n", "b.md")).sentences == 3


def test_non_english_text_is_flagged(tmp_path):
    dutch = "Het regent al de hele week en de rivier staat hoog. Wij blijven binnen en lezen een boek.\n"
    assert "language" in _signals(fs.scan(_write(tmp_path, dutch)))
    assert "language" not in _signals(fs.scan(_write(tmp_path, VARIED, "en.md")))


def test_cli_exit_codes(tmp_path, capsys):
    assert fs.main([str(tmp_path / "missing.md")]) == 2
    assert fs.main([str(tmp_path)]) == 2  # a directory: OSError, not a traceback
    assert fs.main([str(_write(tmp_path, "| only | a table |\n", "t.md"))]) == 2
    (tmp_path / "latin1.md").write_bytes("caf\xe9 au lait.".encode("latin-1"))
    assert fs.main([str(tmp_path / "latin1.md")]) == 2
    capsys.readouterr()
    assert fs.main([str(_write(tmp_path, FORMULAIC)), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["flags"] and "metrics" in out and "not_evaluated" in out


@pytest.mark.parametrize("text", [FORMULAIC, VARIED])
def test_advisory_report_exits_zero(tmp_path, text):
    assert fs.main([str(_write(tmp_path, text))]) == 0


def test_one_sentence_closing_paragraph_template(tmp_path):
    sec = "## S{n}\n\nOpening words number {n} vary here, {w}.\n\nA longer middle paragraph sits here. It has two sentences.\n\nThen the {w} lands.\n"
    words = ["apple", "river", "stone", "cloud"]
    r = fs.scan(_write(tmp_path, "\n".join(sec.format(n=i, w=w) for i, w in enumerate(words))))
    assert any("close with a one-sentence paragraph" in m for m in _messages(r, "template"))


def test_blockquote_marker_is_stripped_before_matching(tmp_path):
    assert fs.scan(_write(tmp_path, "> It is not a bug.\n> It is a feature.\n")).metrics["negation_contrast"] == 1


def test_latex_commands_do_not_become_words(tmp_path):
    tex = "\\section{One}\n\\noindent Plain \\textsc{text} here \\LaTeX\\ now.\n"
    texts = [s.text for sec in fs.parse(tex, latex=True) for p in sec.paragraphs for s in p.sentences]
    assert texts and not any("noindent" in t or "LaTeX" in t for t in texts)


def test_phrase_and_vocabulary_hits_report_their_own_line(tmp_path, monkeypatch):
    monkeypatch.setattr(fs, "STYLE_WORDS", {"tapestry": "R"})
    para = "A {a} opening sentence begins on this line\nand {b} says, to our knowledge,\nthat a {c} tapestry exists.\n\n"
    fills = [("long", "only here", "rich"), ("short", "the author", "woven"), ("plain", "the reader", "bright")]
    r = fs.scan(_write(tmp_path, "".join(para.format(a=a, b=b, c=c) for a, b, c in fills)))
    phrase = dict((p, ln) for p, _, ln in r.phrases)["to our knowledge"]
    assert phrase == [2, 6, 10]
    assert r.vocabulary["tapestry"] == [3, 7, 11]


def test_markdown_that_mentions_latex_keeps_its_prose(tmp_path):
    md = (
        "# Doc\n\nIntro para one.\n\n```\n\\section{Foo}\n```\n\n"
        "See \\begin{table} and \\end{table} usage here.\n\n"
        "Inline `\\begin{document}` is mentioned.\n\n\\begin{figure} is how you start.\n\nFinal para.\n"
    )
    r = fs.scan(_write(tmp_path, md))
    assert r.sentences == 5 and "parse" not in _signals(r)


def test_unclosed_latex_environment_is_reported(tmp_path):
    tex = "\\section{A}\nProse before.\n\\begin{table}\nhidden\n\\section{B}\nLost prose.\n"
    r = fs.scan(_write(tmp_path, tex, "m.tex"))
    assert any("never closed" in m for m in _messages(r, "parse"))


def test_text_around_one_line_environments_is_kept(tmp_path):
    tex = (
        "\\section{A}\nText \\begin{equation} x \\end{equation} after it.\n\n"
        "\\begin{center}\\begin{tabular}{l} x & y \\end{tabular}\\end{center}\n\nClosing words here.\n"
    )
    texts = [s.text for sec in fs.parse(tex, latex=True) for p in sec.paragraphs for s in p.sentences]
    joined = " ".join(texts)
    assert "Text" in joined and "after it" in joined and "Closing words" in joined
    assert "x & y" not in joined and " y " not in f" {joined} "


def test_percent_is_prose_in_markdown_but_a_comment_in_latex(tmp_path):
    md = fs.parse("Sales rose 50% last year and kept rising.\n")
    assert "kept rising" in md[0].paragraphs[0].text
    tex = fs.parse("Sales rose. % a comment\n", latex=True)
    assert "comment" not in tex[0].paragraphs[0].text


def test_wrapped_number_line_is_not_a_list_item(tmp_path):
    secs = fs.parse("The war ended in\n1945. That year was hard.\n")
    paras = secs[0].paragraphs
    assert len(paras) == 1 and not paras[0].is_list_item and "1945" in paras[0].text
    secs2 = fs.parse("Some text here.\n1. first item\n2. second item\n")
    assert [p.is_list_item for p in secs2[0].paragraphs] == [False, True, True]


def test_each_bullet_is_its_own_list_paragraph():
    paras = fs.parse("- alpha one\n- beta two\n- gamma three\n")[0].paragraphs
    assert len(paras) == 3 and all(p.is_list_item for p in paras)


def test_setext_only_for_a_single_buffered_line():
    secs = fs.parse("Line one\nline two\n---\n\nBody.\n")  # two lines, then a rule: prose, not a heading
    assert [sec.title for sec in secs] == ["(preamble)"]
    assert "line two" in secs[0].paragraphs[0].text


def test_html_tags_are_not_words(tmp_path):
    r = fs.scan(_write(tmp_path, "<div class='x'>Plain <b>bold</b> words here.</div>\n"))
    assert r.words == 4


def test_list_without_serial_comma_counts(tmp_path):
    r = fs.scan(_write(tmp_path, "The flag was red, green and blue.\n"))
    assert r.metrics["lists"] == 1 and r.metrics["triad_share"] == 1.0


def test_language_gate_needs_length_for_english_but_catches_short_dutch(tmp_path):
    bullets = "- Alpha Beta Gamma\n- Delta Epsilon Zeta\n- Eta Theta Iota\n"
    assert "language" not in _signals(fs.scan(_write(tmp_path, bullets)))
    dutch = "Het is een mooie dag en de zon schijnt.\n"
    assert "language" in _signals(fs.scan(_write(tmp_path, dutch, "nl.md")))


def test_long_comma_run_stays_fast(tmp_path):
    import time

    text = "We listed " + ", ".join(f"item{i}" for i in range(4000)) + ".\n"  # no conjunction: worst case
    t0 = time.perf_counter()
    fs.scan(_write(tmp_path, text))
    assert time.perf_counter() - t0 < 5


def test_style_phrase_matches_across_extra_whitespace(tmp_path, monkeypatch):
    monkeypatch.setattr(fs, "STYLE_WORDS", {"in summary": "W"})
    assert fs.scan(_write(tmp_path, "In  summary, it works.\n")).metrics["style_words"] == 1


def test_not_x_but_rather_y_is_a_contrast(tmp_path):
    text = "The challenge may not be the data but rather the argument.\n"
    assert fs.scan(_write(tmp_path, text)).metrics["negation_contrast"] == 1


def test_rather_than_is_counted_apart_and_flagged_only_by_rate(tmp_path):
    one = "We chose words rather than numbers, and the long report went on for many pages without it. "
    filler = "The committee met on a Tuesday and read every page of the draft with care. " * 40  # ~600 words
    r = fs.scan(_write(tmp_path, one + filler))
    assert r.metrics["rather_than"] == 1 and r.metrics["negation_contrast"] == 0
    assert "rather" not in _signals(r)  # below the rate
    dense = "Words rather than numbers. Ideas rather than data. Speed rather than care.\n"
    r2 = fs.scan(_write(tmp_path, dense, "b.md"))
    assert r2.metrics["rather_than"] == 3
    assert "rather" in _signals(r2) and "contrast" not in _signals(r2)


def test_em_dashes_counted_in_markdown_and_latex(tmp_path):
    md = "The tool\u2014which is new\u2014works. A hyphen-word and a range 3\u20135 are not dashes.\n"
    r = fs.scan(_write(tmp_path, md))
    assert r.metrics["em_dashes"] == 2 and "dashes" in _signals(r)
    tex = "\\section{A}\nThe tool---which is new---works, pages 3--5.\n"
    assert fs.scan(_write(tmp_path, tex, "m.tex")).metrics["em_dashes"] == 2
    calm = "The tool\u2014new\u2014works. " + "Plain words follow here in a long and quiet sentence. " * 60
    r3 = fs.scan(_write(tmp_path, calm, "c.md"))
    assert r3.metrics["em_dashes"] == 2 and "dashes" not in _signals(r3)  # below the rate


def test_house_words_are_reported_as_source_h(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fs, "STYLE_WORDS", {"crucial": "K"})
    house = _write(tmp_path, "\ufeff# house list\n\nload-bearing\nQuietly   # trailing note\ncrucial\n", "house.txt")
    words = fs.load_house_words(house)
    assert words == {"load-bearing": "H", "quietly": "H", "crucial": "H"}  # BOM, case, comment handled
    doc = _write(tmp_path, "This load-bearing step quietly matters. It is crucial.\n")
    r = fs.scan(doc, words)
    assert r.sources == {"load-bearing": "H", "quietly": "H", "crucial": "K"}  # evidence source wins
    assert r.metrics["style_words"] == 1 and r.metrics["house_words"] == 2  # counted apart
    assert r.metrics["house_list_entries"] == 3 and "house" in _signals(r)
    md = r.to_markdown()
    assert "| load-bearing | H | 1 |" in md and "| crucial | K | 1 |" in md
    plain = fs.scan(doc)
    assert "load-bearing" not in plain.vocabulary and "house_words" not in plain.metrics  # off unless asked for
    assert fs.main([str(doc), "--house-words", str(house)]) == 0
    assert "| quietly | H |" in capsys.readouterr().out
    assert fs.main([str(doc), "--house-words", str(tmp_path / "missing.txt")]) == 2
    assert "house list" in capsys.readouterr().err
    assert fs.main([str(doc), "--house-words", ""]) == 2  # an empty path is an error, not ignored


def test_house_phrase_cannot_take_an_evidence_hit(tmp_path, monkeypatch):
    monkeypatch.setattr(fs, "STYLE_WORDS", {"pivotal": "K", "in summary": "W"})
    house = fs.load_house_words(_write(tmp_path, "a pivotal role\nIn  Summary\n", "h.txt"))
    assert house == {"a pivotal role": "H", "in summary": "H"}  # whitespace normalised
    r = fs.scan(_write(tmp_path, "It plays a pivotal role. In summary, it works.\n"), house)
    assert r.sources == {"pivotal": "K", "in summary": "W"}
    assert r.metrics["style_words"] == 2 and r.metrics["house_words"] == 0


def test_empty_house_list_is_visible(tmp_path):
    r = fs.scan(_write(tmp_path, "Plain words here.\n"), fs.load_house_words(_write(tmp_path, "# only\n", "h.txt")))
    assert r.metrics["house_list_entries"] == 0


def test_latex_urls_and_verb_dashes_are_not_counted_but_textemdash_is(tmp_path):
    tex = "\\section{A}\nSee \\url{http://x.org/a---b} and \\verb|a---b| and the tool\\textemdash here---works.\n"
    assert fs.scan(_write(tmp_path, tex, "m.tex")).metrics["em_dashes"] == 2


def test_markdown_ascii_dashes_are_noted_not_counted(tmp_path):
    r = fs.scan(_write(tmp_path, "The tool -- which is new -- works.\n"))
    assert r.metrics["em_dashes"] == 0 and "em_dashes" in r.not_evaluated
    calm = "Pages 10 - 12 are fine. Run `make -- check` now.\n"  # a hyphen and code are not dashes
    assert "em_dashes" not in fs.scan(_write(tmp_path, calm, "c.md")).not_evaluated


@pytest.mark.parametrize("sentence", ["This cannot be data but rather argument.", "It isn't data but rather argument."])
def test_contracted_negation_but_rather(tmp_path, sentence):
    assert fs.scan(_write(tmp_path, sentence + "\n")).metrics["negation_contrast"] == 1


def test_hash_inside_a_word_is_not_a_comment(tmp_path):
    words = fs.load_house_words(_write(tmp_path, "c#\n# whole-line note\nquietly # trailing note\n", "h.txt"))
    assert words == {"c#": "H", "quietly": "H"}


def test_latex_url_with_nested_braces_is_dropped_whole(tmp_path):
    tex = "\\section{A}\nSee \\url{http://a.b/{x}---c} for the tool---here.\n"
    assert fs.scan(_write(tmp_path, tex, "m.tex")).metrics["em_dashes"] == 1
