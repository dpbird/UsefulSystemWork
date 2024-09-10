# Matt Gormley
# 
# Makefile for LaTeX and Bibtex.  Change the NAME and BIB parameters
# to be the name of the .tex and .bib files respectively.

NAME=main
BIB=references

# All the pdfs in the fig directory.
figures=$(wildcard fig/*.pdf)

all: serve
se: serve-errors

# ========================================
# Build individual lecture note PDFs
# ========================================
.SECONDARY:

note_%.tex : chp_%.tex template_note.tex
	cp template_note.tex $@
	perl -i -pe 's/CHPFILE/chp_$*/g' $@

build/note_%.pdf : note_%.tex
	latexmk -outdir=build -auxdir=build -pdf -pvc $<

# Run latexmk and contiuously rebuild.
serve: $(NAME).tex $(figures)
	latexmk -outdir=build -auxdir=build -pdf -pvc -xelatex -interaction=nonstopmode $(NAME).tex

# Run latexmk and continuously rebuild -- stop on error.
serve-errors:$(NAME).tex $(figures)
	latexmk -outdir=build -auxdir=build -pdf -pvc $(NAME).tex

$(NAME).pdf: $(NAME).tex $(figures)
	latexmk -outdir=build -auxdir=build -pdf $(NAME).tex

# Clean up the various extra files created by pdflatex
# and by AucTex in Aquamacs.
clean:
	rm -f $(NAME).aux $(NAME).bbl $(NAME).blg $(NAME).log \
		$(NAME).rel $(NAME).toc $(NAME).synctex.gz \
		$(NAME).out $(NAME).pdf \
		$(NAME).fls $(NAME).fdb_latexmk \
		$(NAME).loa $(NAME).lof $(NAME).lot \
		 _region_.* *~
	rm -rf auto/
	rm -rf build/

clean-biber:
	rm -rf `biber --cache`

# The phony targets ensure that this will run even if a file named
# clean or all is accidently created.
.PHONY: all
.PHONY: clean
.PHONY: clean-biber
.PHONY: serve
