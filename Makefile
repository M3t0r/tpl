DistFolder := ./dist
BuildFolder := ./build
SourceFiles := setup.py ./tpl/*.py

test:
	-flake8 tpl/
	#pytest

all: test $(DistFolder)/tpl

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
