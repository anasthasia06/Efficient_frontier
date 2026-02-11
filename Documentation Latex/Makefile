# Makefile to build the French LaTeX PDF

TEX=tex/prog_finance_fr.tex
OUTDIR=build
PDF=$(OUTDIR)/prog_finance_fr_v2.pdf
ENGINE?=pdflatex
ASSETS_SCRIPT=scripts/compute_frontier.py

# Try latexmk if available for robust builds
LATEXMK:=$(shell command -v latexmk 2>/dev/null)

.PHONY: all pdf clean distclean

all: pdf

pdf: $(PDF)

$(OUTDIR):
	mkdir -p $(OUTDIR)

$(PDF): $(TEX) | $(OUTDIR)
ifeq (,$(wildcard $(ASSETS_SCRIPT)))
		$(info [warn] $(ASSETS_SCRIPT) not found; skipping asset generation)
else
		@if command -v python3 >/dev/null 2>&1; then \
			echo "[info] Generating assets via Python..."; \
			python3 $(ASSETS_SCRIPT) || echo "[warn] Asset generation failed (missing deps?)"; \
		else \
			echo "[warn] python3 not found; skipping asset generation"; \
		fi
endif
ifdef LATEXMK
	latexmk -$(ENGINE) -halt-on-error -interaction=nonstopmode -file-line-error -outdir=$(OUTDIR) $(TEX)
else
	$(ENGINE) -halt-on-error -interaction=nonstopmode -file-line-error -output-directory=$(OUTDIR) $(TEX)
	$(ENGINE) -halt-on-error -interaction=nonstopmode -file-line-error -output-directory=$(OUTDIR) $(TEX)
endif

clean:
ifdef LATEXMK
	latexmk -C -outdir=$(OUTDIR) || true
endif
	rm -f $(OUTDIR)/*.aux $(OUTDIR)/*.log $(OUTDIR)/*.toc $(OUTDIR)/*.out $(OUTDIR)/*.fls $(OUTDIR)/*.fdb_latexmk $(OUTDIR)/*.synctex.gz

distclean: clean
	rm -f $(PDF)
	rmdir $(OUTDIR) 2>/dev/null || true
