# Annotation Protocol

How BACasebook cases were extracted from source casebooks and validated.

## Verbatim ground truth

The central principle: ground truth is **extracted verbatim** from the source
casebook PDFs — keypoint phrasings, numerical answers, and framework
decompositions are reproduced as written, with no rewriting. This places
subjectivity with the casebook authors who define the professional standard,
makes extraction mechanical and auditable, and gives every grader the same
reliability floor.

Each case is produced in three parallel forms sharing one file stem: the source
PDF, an image folder at ≥200 DPI, and the structured JSON released here.

## Three-leg validation

The pipeline has three independent validation legs, staffed by trained reviewers
rather than crowdsourced annotators:

1. **Source-fidelity leg** — a four-reviewer audit comparing every JSON field
   against the source PDF. Across 48 of the 50 cases (2,374 keypoints),
   reviewers flagged 171 issues; 82 were functional errors (corrected before
   release) and 89 were non-functional (formatting differences or items already
   self-corrected in earlier iterations). Post-correction keypoint-level
   accuracy is **96.5%**.

   | Casebook | Cases | Keypoints | Accuracy |
   |---|---:|---:|---:|
   | PK20 | 11 | 663 | 97.0% |
   | PK21 | 23 | 1,060 | 96.6% |
   | PK23 | 14 | 651 | 96.0% |
   | **Total** | **48** | **2,374** | **96.5%** |

2. **AI cross-check leg** — keypoints are re-extracted automatically and must
   reach ≥75% agreement with the human annotations.

3. **Schema-check leg** — a 16-rule schema validator runs against every JSON
   file (keypoint atomicity, pillar MECE-ness, quantitative-tuple completeness,
   handling of disqualifying examples).

## The 16 schema checks

Distilled from real annotation failures, applied to every case JSON:

| # | Category | Rule |
|---|---|---|
| 1 | Structure | Sub-category headers are JSON containers, not scoreable keypoints. |
| 2 | Structure | Column-internal titles in casebook tables trigger the container check, not main–sub combos. |
| 3 | Pillar consistency | Every pillar within a question exposes a flat keypoint list for uniform traversal. |
| 4 | Counting | Each pillar's subtotal equals its actual keypoint count. |
| 5 | Counting | The question total equals the sum of pillar subtotals and matches the scoring summary. |
| 6 | Versioning | Notes and rubric references cite the current principles version. |
| 7 | Extraction | All sub-items under a parent bullet are extracted; none dropped. |
| 8 | Extraction | Parent-bullet bridge phrases do not contaminate child keypoints. |
| 9 | Format | Sub-group labels become "parent – child" prefixes, not bare JSON keys. |
| 10 | Hierarchy | Container vs content is decided by function (MECE vs elaboration), not indent depth. |
| 11 | Image fidelity | Multi-line bullets are neither split nor merged against the source page. |
| 12 | Scoring | Sub-items are always scored independently; "examples not counted" is disallowed. |
| 13 | Cross-reference | "See question N" references are followed and their keypoints reproduced. |
| 14 | Completeness | Tips/guidance pages are scanned end-to-end for additional question references. |
| 15 | Quantitative | Where the casebook authorizes variable assumptions, the anchor value used for scoring is documented. |
| 16 | Cross-reference | When a "See question N" reference would leave a single unscoreable keypoint, the reference is expanded inline. |

## Scoring conventions

- **Framework & qualitative**: 3-level keypoint rubric — covered (1.0),
  false-partial (0.5), false-not-covered (0.0); per-question score is the mean
  over keypoints, with multi-path tolerance at the conclusion level.
- **Quantitative**: exact-match against the stated answer with a tolerance band;
  reasoning commentary, when present, is scored on its own keypoints.

## Information-release discipline

Facts in `structure_2_information_upon_request` are released only when the
analyst **semantically engages** the item's trigger, not on keyword presence.
The `disqualifying` field enumerates the two failure patterns that must NOT
trigger a release: **F (passing mention)** and **G (adjacent-dimension
modifier)**. This keeps the benchmark testing reasoning rather than keyword
spotting, and makes the release decision reproducible.
