# Case JSON Schema

Each case is a single UTF-8 JSON file under `cases/PK{20,21,23}/`. This document
describes every field. The schema is shared by all 50 cases (one PK20 case,
CoffeePodProducer, uses a slightly reduced `source` block — see note below).

## Top-level fields

| Field | Type | Description |
|---|---|---|
| `case_id` | string | Numeric id within its casebook (e.g., `"001"`). |
| `version` | string | Annotation version of the case (e.g., `"v3"`). |
| `source` | object | Provenance: `title`, `inspired_by` (firm), `year`, `author`, `reference`, `casebook_abbr` (`PK20`/`PK21`/`PK23`). |
| `case_type` | string | Always `"interviewer_driven"` in this release. |
| `case_arch` | object | `primary` archetype (e.g., Profitability, Market Entry) plus `tags`. |
| `difficulty` | string | Easy / Medium / Hard (and intermediate labels). |
| `industry` | string | Industry of the client. |
| `topic` | string | One-line topic description. |
| `expected_duration_minutes` | number | Nominal interview length. |
| `opening_prompt` | string | The verbatim prompt that opens the case (instructions + question list + client context). |
| `structure_1_client_basic_context` | object | Information given to the analyst upfront. |
| `structure_2_information_upon_request` | object | Facts released only when the analyst asks (see below). |
| `structure_3_case_questions` | object | The 4–5 questions, keyed `Q1`…`Q5` (see below). |
| `structure_4_ground_truth` | object | Scoring ground truth, keyed `Q{n}_ground_truth` (see below). |
| `state_machine_global` | object | Global progression rules across questions. |
| `scoring_summary` | object | Per-question keypoint counts and scoring method. |

## `structure_2_information_upon_request`

A set of `item_N` objects. Each item is a fact the interviewer reveals **only
when the analyst's response semantically engages its trigger** — not on a mere
keyword match. Each item has four fields:

| Field | Description |
|---|---|
| `trigger` | What the analyst must ask/engage for the item to be released. |
| `core_dimensional_concept` | The single atomic concept the release decision turns on. |
| `release_conditions` | `structural_position` (forms the analyst's engagement can take) and `alternative_phrasings`. |
| `disqualifying` | "Do-not-release" borderline examples: passing mentions (F pattern) and adjacent-dimension references (G pattern) that look related but should NOT trigger release. |
| `info` | The fact to reveal once triggered. |

The **F / G patterns** in `disqualifying` are the two ways an analyst can appear
to touch a concept without genuinely engaging it: **F = passing mention** (the
concept appears only as an adjective or aside) and **G = adjacent-dimension
modifier** (a neighboring concept is raised, e.g., a "risk" framing instead of
the underlying dimension). Both are explicitly *not* releases.

## `structure_3_case_questions`

Each `Q{n}` object:

| Field | Description |
|---|---|
| `q_id` | `"Q1"`…`"Q5"`. |
| `type` | `framework`, `qualitative`, or `quantitative`. |
| `question_text` | The verbatim question. |
| `information_to_share_upfront` | Data given with the question (or `null`). |
| `information_upon_request` | Either a pointer to `structure_2` items, or a list of question-specific release items in the same 4-field schema. |
| `state_machine` | `next_question`, `skip_logic`, transition conditions. |

## `structure_4_ground_truth`

Keyed `Q{n}_ground_truth`. **This is the scoring key** — in a live run it is
withheld from the analyst, but it is part of the released benchmark so results
are reproducible.

For **framework / qualitative** questions:

| Field | Description |
|---|---|
| `type` | `framework` / `qualitative`. |
| `scoring_method` | 3-level: covered (1.0) / false-partial (0.5) / false-not-covered (0.0). |
| `pillars` | Named pillars, each with a `keypoints` list (and optionally nested sub-categories). |
| `total_keypoints` | Count of keypoints across pillars. |
| `minimum_expected` | Threshold for a passing answer. |
| `outstanding_threshold` | Threshold for an excellent answer. |

For **quantitative** questions:

| Field | Description |
|---|---|
| `type` | `quantitative`. |
| `quantitative_part` | `correct_final_answer`, accepted values, tolerance, and calculation steps. |
| `qualitative_part` | Keypoints for the reasoning/commentary portion (Tier 1 / Tier 2), if any. |

## Scoring at a glance

- **Framework & Qualitative**: each ground-truth keypoint scores covered (1.0),
  false-partial (0.5), or false-not-covered (0.0); the per-question score is the
  mean over keypoints.
- **Quantitative**: exact-match against `correct_final_answer` with the stated
  tolerance; the reasoning commentary (if present) is scored on its own keypoints.

## Notes

- One PK20 case (`Case_008_CoffeePodProducer_PK20_v3.json`) carries a reduced
  `source` block (`casebook` / `firm` / `year`) instead of the full one; its
  PK20 membership is recoverable from the filename and folder.
- Internal annotation scaffolding (working notes, version cross-references) was
  removed for this release; the substantive benchmark content is unchanged. The
  release pipeline is in `scripts/clean_cases.py` in the paper repository.
