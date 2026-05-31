# DEVELOPMENT.md

Developer/agent orientation for this repository (build commands, architecture, conventions).

> **Why this isn't `CLAUDE.md`:** `CLAUDE.md` and `AGENTS.md` are in `.gitignore` — the autoresearch launchers generate per-session agent prompt files at those paths, so anything written there is uncommitted and gets overwritten. This file lives at a non-ignored path so it's version-controlled and durable. The canonical agent *run* instructions are still **`program.md`** (and `program_wuphf_enhanced.md`); this file is the broader codebase guide.

## What This Repo Is

A fork of Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) — an autonomous overnight LLM-pretraining research loop — that has been extended with two additional workstreams. There are effectively **three concerns** in this directory, and they barely share code:

1. **Core autoresearch** (`prepare.py`, `train.py`, `program.md`) — the original: an AI agent edits `train.py`, trains for a fixed 5-minute budget, and minimizes `val_bpb`.
2. **WUPHF Learning System bridge** (`autoresearch_wuphf_bridge.py` + `*_manager.py`) — wraps experiment results so an external learning system at `~/.wuphf/` can do pattern recognition / hyperparameter suggestions across runs. Degrades to standalone mode if `~/.wuphf/` is absent.
3. **WUPHF Agile Agent Network + pitch-deck fine-tuning** (`agents/`, `config.json`, `wuphf_*`, `*pitch_deck*`, `create_*`, `merge_*`, `validate_*`) — a multi-agent orchestration system plus a dataset/fine-tuning pipeline for a German pitch-deck assistant model. This is the bulk of the `autoresearch/may27` branch work and is unrelated to GPT pretraining.

When asked to "run an experiment," that almost always means concern #1.

## Commands

```bash
# Setup (Python 3.10+, uv). torch is pinned to a CUDA 12.8 index.
uv sync

# One-time: download data shards + train BPE tokenizer into ~/.cache/autoresearch/ (~2 min)
uv run prepare.py

# Run a single training experiment (~5 min wall-clock training budget)
uv run train.py

# Tests (dev extras provide pytest). testpaths=["tests"] is set in pyproject.
uv run --extra dev pytest tests/
uv run --extra dev pytest tests/test_ceo_agent.py -v          # single file
uv run --extra dev pytest tests/test_ceo_agent.py::TestTaskDataclass::test_task_creation -v   # single test
```

The agent-network tests (`tests/test_*`) import from `agents/` and the bridge/manager modules — they run without a GPU. Only `prepare.py`/`train.py` require an NVIDIA GPU (this fork uses `flash-attn3` via the `kernels` package and selects a Hopper vs. non-Hopper kernel at import time).

## Concern #1: The autoresearch experiment loop

Read `program.md` for the full agent protocol. The essentials:

- **Edit only `train.py`.** `prepare.py` is read-only ground truth (fixed constants, data prep, tokenizer, dataloader, and the `evaluate_bpb` metric). Do not modify it, do not add dependencies, do not touch the eval harness.
- **Fixed 5-minute budget** (`TIME_BUDGET = 300` in `prepare.py`, wall-clock training time excluding startup/compile). You never tune for speed — only for quality within the budget.
- **Metric: `val_bpb`** (validation bits-per-byte), lower is better, vocab-size-independent so architecture changes compare fairly.
- **Per-run branch**: each research run lives on its own `autoresearch/<tag>` branch cut from `master` (current branch is `autoresearch/may27`).
- **`results.tsv`** is the experiment log: one row per experiment with `commit / val_bpb / memory_gb / status / description`, where `status` is `keep` or `discard`. It is **gitignored** — it's local run state. Each kept experiment is a commit; the description column mirrors the commit message.
- **Simplicity criterion**: prefer simpler code; a tiny `val_bpb` gain that adds hacky complexity is not worth it, and a simplification that holds `val_bpb` flat is a win.
- **VRAM is a soft constraint** — modest increases are fine for real gains, but don't blow it up.

### This fork is tuned for an RTX 3070 Ti (8 GB), not an H100

`GPTConfig` in `train.py` ships with deliberately reduced defaults vs. upstream (e.g. `n_layer=4`, `n_head=4`, `n_embd=256`, `window_pattern="SSSL"`). `sequence_len`/`vocab_size` must stay in sync with `MAX_SEQ_LEN`/`VOCAB_SIZE` in `prepare.py` (2048 / 8192). Recent kept experiments hover around `val_bpb ≈ 1.19` at ~3.6 GB — see `results.tsv` for the live baseline before proposing changes.

## Concern #2: WUPHF Learning System bridge

`autoresearch_wuphf_bridge.py` is the integration layer. It prepends `~/.wuphf/providers` to `sys.path` and tries to import `agent_learning_system`; if unavailable it sets `WUPHF_AVAILABLE = False` and runs standalone. It composes two local managers:

- `model_knowledge_manager.py` — stores/retrieves model checkpoints + episodic memory, `get_best_model()`, search.
- `hyperparameter_pattern_manager.py` — builds success patterns from good runs and anti-patterns (with mitigations) from failures, persists to JSON, emits optimization suggestions.

Config defaults live in `autoresearch_wuphf_config.py` and may be overridden by `autoresearch_wuphf_config.json`. The two-level idea: autoresearch optimizes individual models (micro), WUPHF optimizes the research process across runs (macro). See `README_WUPHF_INTEGRATION.md` and `program_wuphf_enhanced.md`.

## Concern #3: Agile Agent Network & pitch-deck fine-tuning

Driven by `config.json` and planned in `docs/plans/2026-05-27-wuphf-agile-agent-network.md`.

- **`agents/ceo_orchestrator_agent.py`** — the only implemented agent. A `CEOOrchestratorAgent` (calls `nvidia/nemotron-120b` via OpenRouter, key from `OPENROUTER_API_KEY`) that analyzes requests, delegates to specialized agents, and scores output against **"True North"** QA principles (release gate is ~80%+). The other specialized agents in `config.json` are `pending_implementation`.
- **Dataset pipeline** — German-language pitch-deck training data as JSONL (`wuphf_*.jsonl`, `*pitch_deck*.jsonl`). Records use a `role`/`input`/`output` shape (e.g. `role == "content"`). `create_*.py` generate example sets, `merge_*.py` combine them into progressively larger datasets (`..._combined` → `..._ultimate` → `..._final_2026`), and `validate_*.py` + `*_validation.md` check them. `update_config_*.py` point the model config at the chosen dataset.
- **Fine-tuning targets** — three interchangeable backends, all aiming at an Ollama model (`gemma4:e4b`, packaged as `pitchdeck-2026`): `train_wuphf_ollama.py` (few-shot/in-context via the local Ollama API at `localhost:11434`), `train_wuphf_lora.py` / `setup_unsloth_training.py` (LoRA/QLoRA), and `train_wuphf_tasks.py`. `wuphf_model_config.json` records the active model + German system prompt.
- **PDF output** — `create_pitch_deck_pdf.py` renders decks; QA artifacts land in `test_qa_reports/` and `test_pitch_deck_output/`.

## Conventions

- Per the workspace root rules: this is a `uv` project — use `uv sync` / `uv run`, not bare `pip`. Use `trash`, not `rm`.
- Don't switch branches, stash, or touch worktrees unless asked (multi-agent workstation).
- Agent-network and dataset code is German-first (comments, prompts, docs). Match the surrounding language when editing it.
- "No simulation" rule (from the agent-network plan): agents do real work, not mocked/demo output; ship only at the True North quality gate.
