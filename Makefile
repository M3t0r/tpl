DistFolder := ./dist
BuildFolder := ./build
SourceFiles := setup.py ./tpl/*.py

zipapp: $(DistFolder)/tpl

docker: zipapp Dockerfile
	docker build -t "tpl:v`./setup.py -V`" ./
	@echo " ==>" `tput setaf 2`Succesfully`tput sgr0` build `tput setaf 4`$@`tput sgr0`.

wheel:
	python3 ./setup.py sdist bdist_wheel
	@echo " ==>" `tput setaf 2`Succesfully`tput sgr0` build `tput setaf 4`$@`tput sgr0`.

test: codestyle
	pytest ./tests

codestyle:
	flake8 --max-line-length=88 tpl/
	@# we have to ingore 401 and 811 because of the way that pytest
	@# fixtures work
	-flake8 --ignore=F401,F811 --max-line-length=88 tests/ && echo " ==>" Codestyle is `tput setaf 2`conforming`tput sgr0`.

all: test zipapp # this is not all but the ones we recommend

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

release: check-releasable-git-state test zipapp docker wheel
	@# check if there are no further changes not commited to git in $(SourceFiles)
	@echo " ==>" `tput setaf 3`Releasing`tput sgr0` tag `tput setaf 4;./setup.py -V;tput sgr0` to PyPI and DockerHub.
	twine upload dist/tpl-`./setup.py -V`*
	docker push "tpl:v`./setup.py -V`"
	@echo " ==>" `tput setaf 2`Released`tput sgr0` version `tput setaf 4;./setup.py -V;tput sgr0` to PyPI and DockerHub.

install: $(SourceFiles)
	python -m pip install ./

$(DistFolder)/tpl: $(DistFolder) $(BuildFolder) $(SourceFiles)
	python -m pip install ./ -t $(BuildFolder)
	python -m zipapp --python "/usr/bin/env python3" --main tpl:main --output $@ $(BuildFolder)
	@echo " ==>" `tput setaf 2`Succesfully`tput sgr0` build `tput setaf 4`$@`tput sgr0`, you can now copy it somewhere into your `tput setaf 3`\$$PATH`tput sgr0`.

$(DistFolder):
	mkdir -p $@
$(BuildFolder):
	mkdir -p $@

clean:
	rm -rf $(BuildFolder)

distclean: clean
	rm -rf $(DistFolder)
