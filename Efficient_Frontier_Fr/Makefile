# Makefile to build the French LaTeX PDF

TEX=tex/prog_finance_fr.tex
OUTDIR=build
PDF=$(OUTDIR)/prog_finance_fr.pdf
ENGINE?=pdflatex

# Try latexmk if available for robust builds
LATEXMK:=$(shell command -v latexmk 2>/dev/null)

.PHONY: all pdf clean distclean

all: pdf

pdf: $(PDF)

$(OUTDIR):
	mkdir -p $(OUTDIR)

$(PDF): $(TEX) | $(OUTDIR)
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
