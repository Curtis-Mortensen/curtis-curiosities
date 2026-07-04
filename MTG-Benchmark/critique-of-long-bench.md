## 🛠 About Short-LongBench

**Short-LongBench** is a fork of [THUDM/LongBench](https://github.com/THUDM/LongBench) (LongBench v2). The goal is to make the benchmark more useful for evaluating models on **specific task types** and, eventually, as **open-ended generative tasks** rather than multiple-choice.

This README documents what is actually implemented in this repo versus what was planned but never built.

## ⚠️ The multiple-choice problem in LongBench v2

LongBench v2 deliberately uses a multiple-choice format (A/B/C/D) for "reliable evaluation." Every item in the dataset includes `choice_A` through `choice_D`, and the official `pred.py` pipeline asks the model to pick a letter and scores via exact match.

That design has a real limitation: **models are guided by the provided options** rather than having to extract and synthesize an answer from the long context on their own. A model can often eliminate distractors or pattern-match against choices without demonstrating genuine long-context comprehension. This makes scores harder to interpret as a measure of real-world long-context ability.

Short-LongBench was started to address that by moving toward open-ended answers. **That conversion has not been implemented yet** (see [Planned but not implemented](#-planned-but-not-implemented) below). The evaluation code in this repo still runs the original multiple-choice pipeline unchanged.

## ✅ What this fork actually changes

Compared to the official [THUDM/LongBench](https://github.com/THUDM/LongBench) repo, the only committed change so far is this README. The inference and scoring code (`pred.py`, `prompts/`, `config/`, `result.py`) and the bundled LongBench v1 code under `LongBench/` are **identical to upstream**.

What *is* useful in this fork is the documented approach to **filtering the dataset by category** so you can evaluate on a subset of tasks rather than all 503 questions at once.

## 📂 Where question categorization lives

Categorization is **not defined in this repo**. It comes from metadata fields on each row in the [LongBench v2 HuggingFace dataset](https://huggingface.co/datasets/THUDM/LongBench-v2):

| Field | Description | Values |
| :--- | :--- | :--- |
| `domain` | High-level task category (6 types) | See table below |
| `sub_domain` | Finer-grained category within a domain | 16 values (e.g. `Academic`, `Legal`, `Code repo QA`) |
| `difficulty` | Human-annotated difficulty | `easy`, `hard` |
| `length` | Context length bucket | `short`, `medium`, `long` |

### Domain categories (503 questions total)

| Domain | Count |
| :--- | ---: |
| Single-Document QA | 175 |
| Multi-Document QA | 125 |
| Long In-context Learning | 81 |
| Code Repository Understanding | 50 |
| Long-dialogue History Understanding | 39 |
| Long Structured Data Understanding | 33 |

`pred.py` already loads these fields when building the evaluation set:

```python
data_all = [{
    "_id": item["_id"],
    "domain": item["domain"],
    "sub_domain": item["sub_domain"],
    "difficulty": item["difficulty"],
    "length": item["length"],
    # ... question, choices, answer, context
} for item in dataset]
```

`result.py` only breaks down scores by `difficulty` and `length` — not by `domain` or `sub_domain`.

## 🔍 Filtering questions by category

You can load only the questions you care about by filtering on the dataset metadata after loading from HuggingFace:

```python
from datasets import load_dataset

dataset = load_dataset("THUDM/LongBench-v2", split="train")

# Example: only Single-Document QA, hard difficulty, short context
filtered = [
    item for item in dataset
    if item["domain"] == "Single-Document QA"
    and item["difficulty"] == "hard"
    and item["length"] == "short"
]

# Example: only code-related tasks
code_tasks = [
    item for item in dataset
    if item["domain"] == "Code Repository Understanding"
]

# Example: filter by sub-domain
legal_qa = [
    item for item in dataset
    if item["sub_domain"] == "Legal"
]
```

To use a filtered subset with the existing `pred.py` pipeline, pass your filtered list into `get_pred()` instead of the full `data_all` list, or add a filter step in `main()` before inference runs.

This lets you run targeted evaluations — for example, only multi-document QA or only long-context items — without loading the full benchmark every time.

## 🚧 Planned but not implemented

The following was described in earlier versions of this README but **does not exist in the codebase**:

| Planned change | Status |
| :--- | :--- |
| Remove A/B/C/D choices from prompts | ❌ Not done — `prompts/0shot.txt` still presents all four choices |
| Open-ended answer generation | ❌ Not done — models are still asked to pick a letter |
| Map `answer: "B"` → text from `choice_B` as ground truth | ❌ Not done |
| Promptfoo config and test cases | ❌ No `promptfoo.yaml` or transformation script in repo |
| Semantic similarity scoring (embeddings) | ❌ Not done — scoring is still exact letter match |
| OpenRouter integration | ❌ Not done |

The intended pipeline was:

1. Strip multiple-choice options from prompts so models must generate answers from context alone.
2. Convert each item's correct choice letter to its full text (e.g. `"B"` → `choice_B`) as the reference answer.
3. Export to [Promptfoo](https://www.promptfoo.dev/) test cases for side-by-side model comparison.
4. Score responses with embedding-based semantic similarity instead of exact string or letter matching.

If you want to contribute, that pipeline is the main missing piece.

## ⚙️ Running the current (multiple-choice) evaluation

The repo still uses the official LongBench v2 MCQ pipeline via vLLM.

