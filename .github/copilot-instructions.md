# Copilot project instructions

Purpose: enable AI coding agents to work productively in this multi-module finance education repository while respecting established patterns and constraints.

## Big picture
- **Project scope**: Efficient Frontier (portfolio optimization) — course-oriented education repository with multiple sub-projects.
- **Main structure**: 
  - [Efficient_Frontier_Fr/](Efficient_Frontier_Fr/): Active sub-project generating French LaTeX course document with embedded Python-computed frontier figures and CSV tables.
  - `Seance1/`, `Seance2_prof2/`, `Projet/`: Course sessions with Jupyter notebooks and Python scripts for exercises.
- **Key architectural insight**: Each module (especially `Efficient_Frontier_Fr/`) treats computation (Python scripts) and documentation (LaTeX/Jupyter) as co-equal first-class citizens. Scripts *must* generate artifacts that are then embedded in docs.

## Established workflows and tools
- **Build system**: [Efficient_Frontier_Fr/](Efficient_Frontier_Fr/) uses `Make` to orchestrate:
  1. Python asset generation (`scripts/compute_frontier.py` → CSV + PDF plots)
  2. LaTeX compilation (pdflatex or xelatex via latexmk)
  - Run: `cd Efficient_Frontier_Fr && make pdf` (handles Python deps gracefully if missing)
- **Python environment**: Python 3.10+, venv-based, minimal deps (`numpy`, `matplotlib`).
- **Language convention**:
  - French (FR) for course content, documentation, and LaTeX files
  - Comments in Python scripts may use FR or EN; be consistent per-file
  - README files can use EN or FR; track which language in commit messages

## Repository layout and constraints
- **Read-only PDFs**: [prog_finance.pdf](../prog_finance.pdf), [maths doc I.pdf](../maths%20doc%20I.pdf) — do not overwrite; cite as reference sources in comments.
- **Workspace**: [E_f_Workspace.code-workspace](E_f_Workspace.code-workspace) — maintain intact; all modules visible.
- **Efficient_Frontier_Fr/**: This is the active development focus:
  - [scripts/compute_frontier.py](scripts/compute_frontier.py): Generates frontier (min-variance to max-return) for a 3-asset synthetic portfolio. Outputs CSV (selected rows) and LaTeX table rows, plus PDF plot.
  - [tex/prog_finance_fr.tex](tex/prog_finance_fr.tex): Main document; embeds computed CSV and LaTeX table via `\input{../build/frontier_table.tex}` or includes figures from `../build/frontier_plot.pdf`.
  - [build/](build/): Output directory (CSV, PDF, TeX artefacts); gitignored.

## Critical developer patterns
1. **Python → LaTeX data flow**: When modifying [compute_frontier.py](scripts/compute_frontier.py):
   - Always output both CSV (`frontier_table.csv` for external ref) and LaTeX rows (`frontier_table.tex` for `\input{}`).
   - Use deterministic synthetic data (fixed seed or algebraic—no randomness) to ensure reproducible PDF builds.
   - Example: See lines in [compute_frontier.py](scripts/compute_frontier.py) where rows are written as `"{r_star:.4f} & {ret:.4f} & ... \\"`.

2. **Makefile resilience**: The Makefile must gracefully handle:
   - Missing Python 3 (warn, skip asset generation, compile LaTeX from existing artefacts).
   - Missing `latexmk` (fall back to repeated `pdflatex`).
   - Missing Python deps in [requirements.txt](requirements.txt) (catch exception, inform user).

3. **Jupyter notebooks** (in `Seance1/`, etc.):
   - Keep them minimal and reproducible.
   - If adding new deps, update [requirements.txt](requirements.txt) at repo root *and* any local `requirements.txt` in subdirs.

## How to work in this repo
- **Confirm intent first**: Ask user whether changes target course docs, exercise notebooks, or build infrastructure before scaffolding.
- **Preserve existing workflows**: If modifying [compute_frontier.py](scripts/compute_frontier.py), ensure `make pdf` still produces valid output.
- **Keep modules isolated**: Changes in one session (e.g., `Seance1/`) should not break `Efficient_Frontier_Fr/` build.
- **Document why**: Comments in scripts and commit messages should explain portfolio or algorithm choices (e.g., "3-asset example matches Sec. 2 of source PDF").

## Conventions specific to this repo
- **Asset paths**: Scripts write to `build/` relative to their module dir. Refer to assets from LaTeX using relative paths: `./build/frontier_plot.pdf` or `\input{../build/frontier_table.tex}`.
- **French naming in code**: Variable names may be FR (e.g., `risque`, `rendement`) if consistent with pedagogical LaTeX docs. Keep function/module names EN for cross-team clarity.
- **Reproducible examples**: Any new script should include a small hardcoded example (e.g., synthetic 3-asset vector) to validate logic without external data.

## Examples of correct patterns
- Modify [compute_frontier.py](scripts/compute_frontier.py) to add a Sharpe ratio calculation: compute it, append to LaTeX rows (e.g., `f"{sharpe:.4f} \\"`), document the formula in a comment referencing [prog_finance_fr.tex](tex/prog_finance_fr.tex) line number.
- Add a new exercise notebook in `Seance2/`: use same Python 3.10+ environment, import from common [requirements.txt](requirements.txt), and run `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Fix LaTeX compilation error in [prog_finance_fr.tex](tex/prog_finance_fr.tex): test locally with `make pdf`, then verify both `build/prog_finance_fr.pdf` and `build/frontier_table.tex` exist before committing.
