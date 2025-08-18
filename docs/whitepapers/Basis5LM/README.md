# Basis5LM — Toroidal Phase Space (Lower Math)

Purpose: entry-level development of LEE’s toroidal phase space and counterfactual dynamics with minimal formalism.

## Build
- Requires LaTeX + BibTeX (MiKTeX or TeX Live).
- Figures in `figs/`. Bibliography in `../refs/LEE_refs.bib`.

### Windows (PowerShell)
latexmk -pdf -jobname=build/Basis5LM main.tex

### Linux/macOS
latexmk -pdf -jobname=build/Basis5LM main.tex
