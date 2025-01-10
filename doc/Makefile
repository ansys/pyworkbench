# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
STATICDIR	  = "$(SOURCEDIR)/_static"
ARTIFACTSDIR  = "$(STATICDIR)/artifacts"

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

artifacts:
	python -m pip install build && python -m build .. -o $(ARTIFACTSDIR)

.PHONY: help Makefile artifacts

# Catch-all target
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# customized clean due to api examples
clean:
	rm -rf $(BUILDDIR)
	find . -type d -name "_autosummary" -exec rm -rf {} +

# customized pdf due to svg issue
pdf: artifacts
	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cd $(BUILDDIR)/latex && latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode || true
	(test -f $(BUILDDIR)/latex/ansys-workbench-core.pdf && echo pdf exists) || exit 1
