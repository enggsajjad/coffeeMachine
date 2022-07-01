# A Universal Makefile for LaTeX
# Version 0.2

# Copyright 2013 Christoph Reller (christoph.reller@gmail.com)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.

# Note that using this makefile to build your documents does NOT place them
# under the GPL unless you, the author, specifically does so.

#Vorgehen:
#	0. Mit make die Vektorgrafiken erstellen (vorher das Dokument scannen?)
#	1. pdflatex ausfüheren => man erhält durch tikzexternalize die Makedateien für tikz
#	2. Mit make tikz dateien erstellen
#	3. Mit pdflatex/latexmk fertiges Dokument erstellen

# ToDo:
# global Makedatei
SHELL := '/bin/bash'

#SHELL := /usr/bin/env zsh


maintex := $(shell grep -l '^[^%]*\\documentclass' [^_]*.tex)


subdirs := $(sort $(dir $(wildcard ./*/Makefile)))

sed_pre := -e '/\\begin{document}/Q'  # quit when preamble finished
sed_com := -e '/^\s*%/d' -e 's/%.*//' # delete comments
sed_jnl := -e ':a;N;$$!ba;s/\n/ /g'   # join several lines
sed_tmo := -e 's/.*\\usepackage\s*\[\(.*\)\]\s*{MakeSupport}.*/\1/' # extract options given to tikzmake
sed_tmo_exd := -e 's/.*extdir\s*=\s*\([A-Za-z0-9_/\.]*\).*/\1/p' # extract the directory name used for externalized tikzpictures
sed_tmo_vector_exd := -e 's/.*vectoroutdir\s*=\s*\([A-Za-z0-9_/\.]*\).*/\1/p' # extract the directory name used for all externalized tikzpictures
sed_tmo_build := -e 's/.*builddir\s*=\s*\([A-Za-z0-9_/\.]*\).*/\1/p' # extract the directory name used the build files
sed_tmo_eps_pref := -e 's/.*buildepsprefix\s*=\s*\([A-Za-z0-9_/\.]*\).*/\1/p' # extract the prefix of eps-files
sed_tmo_svg_pref := -e 's/.*buildsvgprefix\s*=\s*\([A-Za-z0-9_/\.]*\).*/\1/p' # extract the prefix of svg-files
sed_tmo_eps_dir := -e 's/.*epsdir\s*=\s*\([A-Za-z0-9_/\.]*\).*/\1/p' # extract the directory of eps-files
sed_tmo_svg_dir := -e 's/.*svgdir\s*=\s*\([A-Za-z0-9_/\.]*\).*/\1/p' # extract the directory of svg-files


sed_tmp := $(shell \
	dirname=$$(sed $(sed_pre) $(sed_com) $(maintex) | \
		sed $(sed_jnl) | sed $(sed_tmo) );\
	echo "$$dirname")

extdir := $(shell \
	dirname=$$(echo "$(sed_tmp)" | sed -n $(sed_tmo_exd));\
	if [ ! "$$dirname" ]; then \
		dirname='tikzext';\
	fi;\
	echo "$$dirname")

vectoroutdir := $(shell \
	dirname=$$(echo "$(sed_tmp)" | sed -n $(sed_tmo_vector_exd));\
	if [ ! "$$dirname" ]; then \
		dirname='BuildGraphics';\
	fi;\
	echo "$$dirname")

buildsvgpref := $(shell \
	prefix=$$(echo "$(sed_tmp)" | sed -n $(sed_tmo_svg_pref));\
	if [ ! "$$prefix" ]; then \
		prefix='svg';\
	fi;\
	echo "$$prefix")

buildepspref := $(shell \
	prefix=$$(echo "$(sed_tmp)" | sed -n $(sed_tmo_eps_pref));\
	if [ ! "$$prefix" ]; then \
		prefix='eps';\
	fi;\
	echo "$$prefix")

svgdir := $(shell \
	dirname=$$(echo "$(sed_tmp)" | sed -n $(sed_tmo_svg_dir));\
	if [ ! "$$dirname" ]; then \
		dirname='VectorGraphics';\
	fi;\
	echo "$$dirname")

epsdir := $(shell \
	dirname=$$(echo "$(sed_tmp)" | sed -n $(sed_tmo_eps_dir));\
	if [ ! "$$dirname" ]; then \
		dirname='VectorGraphics';\
	fi;\
	echo "$$dirname")

builddir := $(shell \
	dirname=$$(echo "$(sed_tmp)" | sed -n $(sed_tmo_build));\
	if [ ! "$$dirname" ]; then \
		dirname='build';\
	fi;\
	echo "$$dirname")

svg_files =$(call rwildcard ,$(svgdir),*.svg)
eps_files =$(call rwildcard ,$(epsdir),*.eps)

build_svg :=$(svg_files:$(svgdir)/%.svg=$(vectoroutdir)/$(buildsvgpref)%.pdf)
build_svg_tex :=$(build_svg:%.pdf=%.pdf_tex)
build_eps :=$(eps_files:$(epsdir)/%.eps=$(vectoroutdir)/$(buildepspref)%.pdf)


#(call DISPLAYERROR file.tex, jobname)
define DISPLAYERROR
	($(call echo-error,Errors encountered:) && $(call colorize-latex-errors,$(1)))
endef

ERROR_SEDSCRIPT := colorize-latex-errors.sed

# $(call colorize-latex-errors,<log file>)
define colorize-latex-errors
	sed -f "$(ERROR_SEDSCRIPT)" "$1"
endef

# Terminal color definitions
tput	=
ifneq ($(TERM),)
ifndef NO_COLOR
tput	= $(shell tput $1)
endif
endif

black	:= $(call tput,setaf 0)
red		:= $(call tput,setaf 1)
green	:= $(call tput,setaf 2)
yellow	:= $(call tput,setaf 3)
blue	:= $(call tput,setaf 4)
magenta	:= $(call tput,setaf 5)
cyan	:= $(call tput,setaf 6)
white	:= $(call tput,setaf 7)
bold	:= $(call tput,bold)
uline	:= $(call tput,smul)
reset	:= $(call tput,sgr0)
#
#
# User-settable definitions
#
LATEX_COLOR_WARNING	?= magenta
LATEX_COLOR_ERROR	?= red
LATEX_COLOR_INFO	?= green
LATEX_COLOR_UNDERFULL	?= magenta
LATEX_COLOR_OVERFULL	?= red bold
LATEX_COLOR_PAGES	?= bold
LATEX_COLOR_BUILD	?= blue
LATEX_COLOR_GRAPHIC	?= yellow
LATEX_COLOR_DEP		?= green
LATEX_COLOR_SUCCESS	?= green bold
LATEX_COLOR_FAILURE	?= red bold
LATEX_COLOR_FILENAME?= black bold
LATEX_COLOR_PROGNAME?= black bold

# Gets the real color from a simple textual definition like those above
# $(call get-color,ALL_CAPS_COLOR_NAME)
# e.g., $(call get-color,WARNING)
get-color	= $(subst $(space),,$(foreach c,$(LATEX_COLOR_$1),$($c)))

#
# STANDARD COLORS
#
C_WARNING	:= $(call get-color,WARNING)
C_ERROR		:= $(call get-color,ERROR)
C_INFO		:= $(call get-color,INFO)
C_UNDERFULL	:= $(call get-color,UNDERFULL)
C_OVERFULL	:= $(call get-color,OVERFULL)
C_PAGES		:= $(call get-color,PAGES)
C_BUILD		:= $(call get-color,BUILD)
C_GRAPHIC	:= $(call get-color,GRAPHIC)
C_DEP		:= $(call get-color,DEP)
C_SUCCESS	:= $(call get-color,SUCCESS)
C_FAILURE	:= $(call get-color,FAILURE)
C_FILENAME  := $(call get-color,FILENAME)
C_PROGNAME  := $(call get-color,PROGNAME)
C_RESET		:= $(reset)

echo-img      = echo "$(C_BUILD)====> $(C_INFO)Generating figure $(C_FILENAME)$1$(C_RESET)$(if $2, | $(red)Step $2$(C_RESET),)"
echo-cpy      = echo "$(C_BUILD)====> $(C_INFO)Copying figure $(C_FILENAME)$1$(C_RESET)$(if $2, | $(red)Step $2$(C_RESET),)"
echo-tex-step = echo "$(C_BUILD)====> $(C_INFO)$1 $(C_PROGNAME)$2 $(C_RESET)"
echo-gen      = echo "$(C_BUILD)====> $(C_INFO)Generating $1 $(C_RESET)"
echo-do       = echo "$(C_BUILD)====> $(C_INFO)$1 $(C_FILENAME)$(if $2,$2,)$(C_RESET)"
echo-error    = echo "$(C_BUILD)====> $(C_ERROR)$1 $(C_FILENAME)$(if $2,$2,)$(C_RESET)"
echo-warning  = echo "$(C_BUILD)====> $(C_WARNING)$1 $(C_FILENAME)$(if $2,$2,)$(C_RESET)"
echo-finish   = echo "$(C_BUILD)====> $(blue)Finished $(C_RESET)$1$(C_INFO)$(if $2, in $(red)$2$(blue) runs,)$(C_RESET)"
echo-debug    = echo "$(C_BUILD)====> $(C_INFO)DEBUG $1 $(C_RESET)"

#
#
#


mainpdf :=
$(foreach file,$(maintex),$(eval mainpdf +=$(shell dirname $(file) )/$(builddir)/$(shell basename --suffix=.tex $(file)).pdf)) # the pdf-files

draftpdf := $(filter %_draft.pdf,$(mainpdf))

DRAFTpdf := $(filter %_DRAFT.pdf,$(mainpdf))

WithoutDraftpdf := $(filter-out %_draft.pdf %_DRAFT.pdf,$(mainpdf))

.PHONY: all clean clean_vector clean_all allimages allvectorgraphics draft DRAFT handout handnotes nonotes allBeamer normal


allBeamer: allimages allvectorgraphics normal handout handnotes nonotes

normal: allimages allvectorgraphics $(filter-out %_draft.pdf %_DRAFT.pdf %_handnotes.pdf %_handout.pdf %_nonotes.pdf,$(mainpdf))

draft: $(draftpdf)

DRAFT: $(DRAFTpdf)

handout: allimages allvectorgraphics $(filter %_handout.pdf,$(mainpdf))

handnotes: allimages allvectorgraphics $(filter %_handnotes.pdf,$(mainpdf))

nonotes: allimages allvectorgraphics $(filter %_nonotes.pdf,$(mainpdf))

all: allimages allvectorgraphics $(mainpdf)

allvectorgraphics: $(build_svg) $(build_svg_tex) $(build_eps)
	@$(call echo-finish,Creating vectorgraphics);

# the makefile created from scanning for includes
-include $(mainpdf:.pdf=.tex-dep)

# the makefile created by tikz
-include $(mainpdf:.pdf=.makefile)


$(build_svg): $(vectoroutdir)/$(buildsvgpref)%.pdf: $(svgdir)/%.svg
	mkdir -p $(shell dirname $@)
	@$(call echo-img,$@);
	inkscape -z -D --file=$< --export-pdf='$@' --export-latex

$(build_svg_tex): $(vectoroutdir)/$(buildsvgpref)%.pdf_tex: $(svgdir)/%.svg
	mkdir -p $(shell dirname $@)
	@$(call echo-img,$@);
	inkscape -z -D --file=$< --export-pdf='$@' --export-latex

$(build_eps): $(vectoroutdir)/$(buildepspref)%.pdf: $(epsdir)/%.svg
	mkdir -p $(shell dirname $@)
	@$(call echo-img,$@);
	epstopdf --outfile=$@ $<


$(subdirs):
	@$(MAKE) -C $@ 
	# make in the subdir



# clean up all build files, except vector-graphics
clean: 
	@$(call echo-do,Cleaning up build files)
	-@for dir in $(subdirs); do $(MAKE) -C $$dir clean; done
	-@rm -f *.glo
	-@rm -f *.ist
	-@rm -rf $(builddir)

# clean up all build vector-graphics
clean_vector:
	@$(call echo-do,Cleaning up generated vectorgraphics)
	-@for dir in $(subdirs); do $(MAKE) -C $$dir clean_vector; done
	-@rm -rf $(vectoroutdir)

# clean up all build files
clean_all: clean clean_vector
	-@rm -rf $(extdir)

%.md5: 
	@cp  $(builddir)/$@ $(extdir)
	

.PHONY: test 

test: 
	@$(call create-tikz,build/main.makefile,build/main.pdf)

# main pdf targets
.SECONDEXPANSION:
$(WithoutDraftpdf) : %.pdf : $$(subst $$(builddir)/,,$$*).tex  allimages allvectorgraphics
	@$(call echo-do,Creating folders);
	@if [ $(extdir) ]; then mkdir -p $(extdir); fi	
	@if [ $(vectoroutdir) ]; then mkdir -p $(vectoroutdir); fi	
	@if [ $(builddir) ]; then mkdir -p $(builddir); fi
	@if [ $(builddir)/$(extdir) ]; then mkdir -p $(builddir)/$(extdir); fi
	@$(call echo-tex-step,Start to compile,$*.pdf);
	@$(call echo-tex-step,Running,LaTexMk);
	@$(call run-latex-and-dep,$<)
	@$(call create-tikz,$*.makefile,$<)
	@$(call parse-log,$*.log)
	@rm -f $(subst .tex,.ist,$<)
	@rm -f $(subst .tex,.glo,$<)
	@if [[ "$(extdir)" && ! "$$(ls -A $(extdir))" ]]; then rmdir $(extdir); fi
	@if [[ "$(vectoroutdir)" && ! "$$(ls -A $(vectorourdir))" ]]; then rmdir $(vectoroutdir); fi

.SECONDEXPANSION:
$(draftpdf) : %.pdf : $$(subst $$(builddir)/,,$$*).tex
	@$(call echo-do,Creating folders);	
	@if [ $(builddir) ]; then mkdir -p $(builddir); fi
	@$(call echo-tex-step,Start to compile,$*.pdf);
	@$(call echo-tex-step,Running,LaTexMk);
	@$(call run-latex-and-dep,$<)
	@$(call parse-log,$*.log)
	@rm -f $(subst .tex,.ist,$<)
	@rm -f $(subst .tex,.glo,$<)

.SECONDEXPANSION:
$(DRAFTpdf) : %.pdf : $$(subst $$(builddir)/,,$$*).tex
	@$(call echo-do,Creating folders);	
	@if [ $(builddir) ]; then mkdir -p $(builddir); fi
	@$(call echo-tex-step,Start to compile,$*.pdf);
	@$(call echo-tex-step,Running,LaTexMk);
	@$(call run-latex-and-dep,$<)
	@$(call parse-log,$*.log)
	@rm -f $(subst .tex,.ist,$<)
	@rm -f $(subst .tex,.glo,$<)

#$(call create-tikz, makefile, pdffile)
define create-tikz
	$(eval TMP= $(shell $(MAKE) -f $(1) allimages))
	if [ -e $(1) ]; then if [ "$(TMP)" == "All images exist now. Use make -B to re-generate them." ]; then $(call echo-tex-step,Tikz-Images are up to date,=> pdfLaTeX is skipped.); else make -f $(1) allimages; $(call echo-tex-step,Running,pdfLaTeX); $(call run-pdflatex, $(2)); fi else $(call echo-warning,No '$*.makefile' found.); fi
endef

#$(call parse-log, logfile)
define parse-log
	$(call DISPLAYERROR ,$(1));
	$(call echo-warning,Undefined references and citations:);\
	echo -n "$(C_WARNING)" && egrep -i "(Reference|Citation).*undefined" $(1) && echo "$(C_RESET)" || echo "$(C_INFO)None.$(C_RESET)";
endef

#$(call parse-log-with-pplatex, logfile)
define parse-log-with-pplatex
	pplatex -i $(1)
endef

define DEFAULT_LATEX_OPTIONS
	-synctex=1 -interaction=batchmode -file-line-error-style -shell-escape
endef

define run-latex
	latexmk -pdf    \
			-use-make \
			-cd \
			-r latexmkrc \
	        -pdflatex="pdflatex $(DEFAULT_LATEX_OPTIONS) %O %S"  \
					-output-directory=$(builddir) $(1) ||  $(call echo-error,An error occured while running LaTexMk);
endef

define run-pdflatex
	pdflatex $(DEFAULT_LATEX_OPTIONS) -output-directory=$(builddir) $(1) || $(call echo-error,An error occured while running pdfLaTex)
endef

define run-latex-and-dep
	latexmk -pdf    \
			-use-make \
			-cd \
			-r latexmkrc \
			-deps-out='$(builddir)/$(1)-dep' \
	        -pdflatex="pdflatex $(DEFAULT_LATEX_OPTIONS) %O %S"  \
					-output-directory=$(builddir) $(1) || $(call echo-error,An error occured while running LaTexMk)
endef

