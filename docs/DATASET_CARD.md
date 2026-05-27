# BACasebook Dataset Card

Follows the NeurIPS Datasets & Benchmarks documentation convention.

## Summary

BACasebook is a benchmark for multi-step, mixed-verifiability reasoning in
business analytics: **50 verbatim MBB casebook cases** with **248 questions**,
with ground truth extracted directly from source PDFs. Each question is typed
(framework / qualitative / quantitative) and scored on a comprehensive rubric
(keypoint partial-credit for the non-verifiable axes; exact-match with tolerance
for the quantitative axis).

## Composition

| | |
|---|---|
| Cases | 50 |
| Questions | 248 |
| Source casebooks | 3 (PK20: 11, PK21: 24, PK23: 15) |
| Keypoints (audited subset of 48 cases) | 2,374 (~49/case, ~9–10/question) |
| Languages | English |

**Question types:** qualitative 139, quantitative 58, framework 51.

**Primary archetypes** (as tagged per case): Profitability, Revenue Growth,
Market Entry, Comparison, Growth Strategy, Wild Card, Impact of Trend,
Implementation, plus a few single-case archetypes (M&A / Investment Decision,
Organizational Performance, New Business / Make-or-Buy, Digital Transformation).

**Difficulty:** Hard 25, Medium 15, Medium-Hard 4, Easy 4, Easy-Medium 2.

## Intended use

Academic evaluation of LLM reasoning in structured business-analytics domains:
benchmarking frontier models, failure-mode attribution, and judge-protocol
research. Also a template for transferring verbatim-ground-truth methodology to
adjacent professional domains.

## Out-of-scope use

BACasebook must **not** be used to make hiring or educational-admissions
decisions, nor to characterize the consulting aptitude of real individuals.
Scores reflect performance on a specific evaluation protocol and are not a
measure of general consulting competence.

## Provenance & licensing

The cases come from a dual provenance: institutional casebooks compiled by
university consulting clubs, and practitioner collections (the PK series)
released for educational use. All sources are publicly distributed for
educational use and permit non-commercial academic redistribution.

- No proprietary or confidential consulting materials are included.
- The release contains **no personally identifiable information**.
- Reproduction of original casebook text is limited to **verbatim keypoint
  extracts**; full casebook PDFs are **not** redistributed.

See [`../LICENSE`](../LICENSE) for the full non-commercial research license.

## Annotation & quality

Annotation was performed by project authors and compensated team members at or
above local living-wage rates; no crowdsourced unpaid labor was used. Quality is
underwritten by a three-leg validation pipeline (source-fidelity audit, AI
cross-check, schema check). A four-reviewer audit of 48 of the 50 cases (2,374
keypoints) found a keypoint-level annotation accuracy of **96.5%** after
correction. See [`ANNOTATION_PROTOCOL.md`](ANNOTATION_PROTOCOL.md).

## Maintenance

- **v1** — this release: 50 annotated cases.
- **v2 (planned)** — open-weights models in the baseline suite; multilingual
  extension beyond English.
- **v3 (roadmap)** — a candidate-led extension surfacing agenda-control failure
  modes.

## Citation

A citation will be provided upon publication.
