#!/usr/bin/env python3
"""Validation tests for the BACasebook release.

Run standalone:   python3 tests/test_dataset.py
Or with pytest:   pytest tests/

Checks structural integrity, schema conformance, and the headline counts that
the paper reports (50 cases, 248 questions, casebook split).
"""
import json
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASE_GLOB = os.path.join(ROOT, "cases", "*", "*.json")
CJK = re.compile(r"[一-鿿]")
QTYPES = {"framework", "qualitative", "quantitative"}

EXPECTED_CASES = 50
EXPECTED_QUESTIONS = 248
EXPECTED_BY_BOOK = {"PK20": 11, "PK21": 24, "PK23": 15}

REQUIRED_TOPLEVEL = [
    "case_id", "source", "case_type", "opening_prompt",
    "structure_1_client_basic_context", "structure_2_information_upon_request",
    "structure_3_case_questions", "structure_4_ground_truth",
]


def _cases():
    return sorted(glob.glob(CASE_GLOB))


def load(f):
    with open(f, encoding="utf-8") as fh:
        return json.load(fh)


def test_case_count():
    assert len(_cases()) == EXPECTED_CASES, \
        f"expected {EXPECTED_CASES} cases, found {len(_cases())}"


def test_valid_json_and_required_keys():
    for f in _cases():
        d = load(f)  # raises on invalid JSON
        for k in REQUIRED_TOPLEVEL:
            assert k in d, f"{os.path.basename(f)} missing top-level key '{k}'"


def test_no_cjk():
    for f in _cases():
        blob = json.dumps(load(f), ensure_ascii=False)
        m = CJK.search(blob)
        assert m is None, \
            f"{os.path.basename(f)} contains CJK char {m.group()!r}"


def test_casebook_split():
    counts = {"PK20": 0, "PK21": 0, "PK23": 0}
    for f in _cases():
        book = re.search(r"PK2[013]", f).group()
        counts[book] += 1
    assert counts == EXPECTED_BY_BOOK, f"casebook split is {counts}"


def test_question_count_and_types():
    total = 0
    for f in _cases():
        d = load(f)
        for qid, q in d["structure_3_case_questions"].items():
            if not isinstance(q, dict) or "type" not in q:
                continue
            total += 1
            assert q["type"] in QTYPES, \
                f"{os.path.basename(f)} {qid}: bad type {q['type']!r}"
            assert q.get("question_text"), \
                f"{os.path.basename(f)} {qid}: empty question_text"
    assert total == EXPECTED_QUESTIONS, \
        f"expected {EXPECTED_QUESTIONS} questions, found {total}"


def test_every_question_has_ground_truth():
    for f in _cases():
        d = load(f)
        gt = d["structure_4_ground_truth"]
        for qid, q in d["structure_3_case_questions"].items():
            if not isinstance(q, dict) or "type" not in q:
                continue
            # A split question like "Q4_qualitative" shares the base
            # question's ground truth (its qualitative_part).
            base = qid.split("_")[0]
            key = f"{qid}_ground_truth"
            base_key = f"{base}_ground_truth"
            assert key in gt or base_key in gt, \
                f"{os.path.basename(f)}: no ground truth for {qid}"


def test_info_request_schema():
    """Each structure_2 item carries the four release-schema fields."""
    fields = {"trigger", "core_dimensional_concept", "release_conditions",
              "disqualifying", "info"}
    for f in _cases():
        d = load(f)
        s2 = d["structure_2_information_upon_request"]
        for k, item in s2.items():
            if not isinstance(item, dict) or "trigger" not in item:
                continue
            missing = fields - set(item.keys())
            # `disqualifying` may legitimately be absent on a few items;
            # the other four are required.
            hard = missing - {"disqualifying"}
            assert not hard, \
                f"{os.path.basename(f)} {k}: missing release fields {hard}"


def test_quant_questions_have_answer():
    for f in _cases():
        d = load(f)
        gt = d["structure_4_ground_truth"]
        for qid, q in d["structure_3_case_questions"].items():
            if not isinstance(q, dict) or q.get("type") != "quantitative":
                continue
            block = gt.get(f"{qid}_ground_truth", {})
            qp = block.get("quantitative_part", {})
            assert qp.get("correct_final_answer") is not None, \
                f"{os.path.basename(f)} {qid}: quant question without answer"


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
    return passed == len(tests)


if __name__ == "__main__":
    import sys
    sys.exit(0 if _run() else 1)
