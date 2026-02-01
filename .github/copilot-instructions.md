# Copilot project instructions

Purpose: enable AI coding agents to work productively in this repository while staying aligned with its current state and constraints.

## Big picture
- Project: Efficient Frontier (finance) — repository currently minimal and course-oriented.
- Current contents: `README.md`, two PDFs with course material, and the VS Code workspace file `E_f_Workspace.code-workspace`.
- No code, build system, tests, or package manifests are present yet.

## Repository layout and constraints
- Keep PDFs (`maths doc I.pdf`, `prog_finance.pdf`) unchanged; treat them as reference materials.
- Maintain the workspace file `E_f_Workspace.code-workspace` and avoid disruptive renames.
- Default documentation language can be EN (README is EN). If writing course notes, FR is acceptable — be consistent within a file.

## How to work in this repo
- Confirm the requested deliverable with the user before scaffolding new code.
- When asked to create code, prefer small, runnable scripts with a clear entry point and a short usage section in `README.md`.
- Add only the minimum structure needed for the task (avoid heavy frameworks unless explicitly requested).

## Suggested scaffold (use only when asked)
- Python first: typical finance tooling and Linux environment fit well.
- Minimal structure:
  - `src/` for library code
  - `scripts/` for runnable CLIs
  - `notebooks/` for exploration (optional)
  - `data/` for small sample CSVs (keep under VCS if tiny)
- Add `requirements.txt` only when external packages are actually used.

## Developer workflows (when code exists)
- Environment: Python 3.10+ on Linux.
- Create a venv and install deps only as needed:
  - `python -m venv .venv`
  - `. .venv/bin/activate`
  - `pip install -r requirements.txt`
- Put quick-run instructions in the README and provide one tiny dataset if relevant.

## Conventions
- Keep code and docs concise and reproducible; include a small example invocation for every new script.
- Prefer deterministic computations and fixed seeds in examples where randomness is involved.
- If plotting, save figures under `outputs/` and mention the path in README.
- Cite data sources (e.g., if fetching market data) in comments and README.

## Safe changes and review
- Do not overwrite or recreate the PDFs; link to them from README if needed.
- Keep new files focused on the requested task; avoid broad refactors in a single PR.
- When uncertainty exists (e.g., language, package choice), propose 1–2 options and ask the user to choose.

## Examples
- Add a single script under `scripts/compute_efficient_frontier.py` that reads a small CSV from `data/`, prints portfolio stats, and optionally saves a plot under `outputs/`. Document how to run it in README.
- If asked for notebooks, create `notebooks/efficient_frontier.ipynb` with a minimal, reproducible workflow and pinned package versions in `requirements.txt`.
