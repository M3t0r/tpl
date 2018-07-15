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
