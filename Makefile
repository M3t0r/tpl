DistFolder := ./dist
BuildFolder := ./build
SourceFiles := setup.py ./tpl/*.py

.PHONY: zipapp
zipapp: $(DistFolder)/tpl

.PHONY: docker
docker: zipapp Dockerfile
	docker build -t "tpl:v`./setup.py -V`" ./
	@echo " ==>" `tput setaf 2`Succesfully`tput sgr0` build `tput setaf 4`$@`tput sgr0`.

.PHONY: wheel
wheel: $(DistFolder)/tpl.1
	python3 ./setup.py sdist bdist_wheel
	@echo " ==>" `tput setaf 2`Succesfully`tput sgr0` build `tput setaf 4`$@`tput sgr0`.

.PHONY: docs documentation
docs documentation: $(DistFolder)/tpl.1 $(BuildFolder)
	@echo " ==>" `tput setaf 3`Building`tput sgr0` HTML documentation for `tput setaf 4;./setup.py -V;tput sgr0`
	sphinx-build -j auto -d $(BuildFolder)/sphinx -b html docs $(DistFolder)/docs

$(DistFolder)/tpl.1: docs/manpage.rst
	@# calling `./setup.py -V` makes sure that tpl.__version__ exists and docs/conf.py can import it
	@echo " ==>" `tput setaf 3`Building`tput sgr0` manpage for `tput setaf 4;./setup.py -V;tput sgr0`
	sphinx-build -d $(BuildFolder)/sphinx -b man -E docs $(DistFolder)

.PHONY: test
test: TEST_SELECTOR ?= ""
test: codestyle
	pytest -k ${TEST_SELECTOR} ./tests

.PHONY: codestyle
codestyle:
	flake8 --max-line-length=88 tpl/
	@# we have to ingore 401 and 811 because of the way that pytest
	@# fixtures work
	-flake8 --ignore=F401,F811 --max-line-length=88 tests/ && echo " ==>" Codestyle is `tput setaf 2`conforming`tput sgr0`.

.PHONY: all
all: test zipapp documentation # this is not all but the ones we recommend

.PHONY: check-releasable-git-state
check-releasable-git-state:
	# check if there are changes staged to be commited
	git diff --cached --stat --exit-code
	# check if there are any changes to tracked files
	git diff --stat --exit-code
	# check if there are untracked files in tpl/ and tests/
	! git status --porcelain=2 | grep -E "\\? [\"']?(tpl|tests)/"
	# check if the current state is tagged in git
	git describe --tags --exact
	@echo " ==>" git state is `tput setaf 2`releasable`tput sgr0`

.PHONY: release
release: check-releasable-git-state test zipapp wheel
	@# check if there are no further changes not commited to git in $(SourceFiles)
	@echo " ==>" `tput setaf 3`Releasing`tput sgr0` tag `tput setaf 4;./setup.py -V;tput sgr0` to PyPI.
	twine upload dist/tpl-`./setup.py -V`*
	@echo " ==>" `tput setaf 2`Released`tput sgr0` version `tput setaf 4;./setup.py -V;tput sgr0` to PyPI.

.PHONY: install
install: $(SourceFiles)
	python -m pip install ./

$(DistFolder)/tpl: $(DistFolder) $(BuildFolder) $(SourceFiles)
	python -m pip install ./ -t $(BuildFolder)
	python -m zipapp --python "/usr/bin/env python3" --main tpl.__main__:_argv_wrapper --output $@ $(BuildFolder)
	@echo " ==>" `tput setaf 2`Succesfully`tput sgr0` build `tput setaf 4`$@`tput sgr0`, you can now copy it somewhere into your `tput setaf 3`\$$PATH`tput sgr0`.

$(DistFolder):
	mkdir -p $@
$(BuildFolder):
	mkdir -p $@

.PHONY: clean
clean:
	rm -rf $(BuildFolder)

.PHONY: distclean
distclean: clean
	rm -rf $(DistFolder)
