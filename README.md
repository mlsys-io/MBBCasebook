# BACasebook

**A Benchmark for LLM-Based Business Analytics**

BACasebook is a benchmark for **multi-step, mixed-verifiability reasoning** in
business analytics. It instantiates the regime in which a single reasoning chain
interleaves qualitative judgment with exact quantitative derivation — the regime
a professional analyst actually works in, and one that neither fully verifiable
math suites nor open-ended judge benchmarks capture.

The corpus is **50 verbatim MBB (McKinsey / Bain / BCG) casebook cases** with
**248 questions**, drawn from three consulting-casebook collections. Ground truth
is extracted **directly from the source PDFs** — keypoint phrasings, numerical
answers, and framework decompositions are reproduced verbatim, so source fidelity
replaces annotator subjectivity.

## What's in this repo

```
cases/            50 case files in JSON, grouped by source casebook
  PK20/           11 cases
  PK21/           24 cases
  PK23/           15 cases
docs/
  SCHEMA.md       the case-JSON schema, field by field
  DATASET_CARD.md intended use, provenance, licensing, maintenance
  ANNOTATION_PROTOCOL.md  how cases were extracted and validated
tests/
  test_dataset.py validation suite (counts, schema, no-CJK)
LICENSE           non-commercial research license
```

## The case schema in brief

Each case is one JSON file with these top-level sections (full detail in
[`docs/SCHEMA.md`](docs/SCHEMA.md)):

| Section | What it holds |
|---|---|
| `source`, `case_arch`, `difficulty`, `industry`, `topic` | Case metadata |
| `opening_prompt` | The verbatim prompt that opens the case |
| `structure_1_client_basic_context` | Information given upfront |
| `structure_2_information_upon_request` | Facts released only when the analyst asks (trigger / concept / release-conditions / info) |
| `structure_3_case_questions` | The 4–5 questions, each typed framework / qualitative / quantitative, with a state machine |
| `structure_4_ground_truth` | The scoring ground truth: keypoints per pillar, plus quantitative exact-match answers |
| `scoring_summary` | Per-question keypoint counts and scoring method |

Questions are scored on a **comprehensive rubric**: framework and qualitative
turns use a 3-level keypoint rubric (covered 1.0 / false-partial 0.5 /
false-not-covered 0.0); quantitative turns use exact-match with tolerance bands.

## Quick start

```python
import json, glob

cases = [json.load(open(f)) for f in glob.glob("cases/*/*.json")]
print(len(cases), "cases")

c = cases[0]
print(c["source"]["title"] if "title" in c["source"] else c["source"])
for qid, q in c["structure_3_case_questions"].items():
    if isinstance(q, dict) and "type" in q:
        print(qid, q["type"], "—", q["question_text"][:80])
```

## Dataset statistics

| | |
|---|---|
| Cases | 50 |
| Questions | 248 |
| Source casebooks | 3 (PK20, PK21, PK23) |
| Question types | framework, qualitative, quantitative |
| Languages | English |

See [`docs/DATASET_CARD.md`](docs/DATASET_CARD.md) for the full breakdown,
provenance, and intended/out-of-scope use.

## Validate

```bash
python3 tests/test_dataset.py     # or: pytest tests/
```

Checks the case count (50), question count (248), casebook split, schema
conformance, and that no internal annotation text remains.

## License

Released under a **non-commercial research license** (see [`LICENSE`](LICENSE)).
The source casebook copyrights remain with their respective authors and
consulting clubs; BACasebook redistributes verbatim keypoint extracts only — the
**full casebook PDFs are not redistributed**.

## Citation

A citation will be provided upon publication.
