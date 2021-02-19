# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

include default.mk

define mk-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		echo $(ROOT_DIR) >  $(VENV_ROOT)/.project; \
		if [ ! -d $(WORKON_HOME)/$(PKG_NAME) -a ! -L $(WORKON_HOME)/$(PKG_NAME) ]; \
		then \
			ln -s $(ROOT_DIR)/$(VENV_ROOT) $(WORKON_HOME)/$(PKG_NAME); \
			echo ; \
			echo Since you use virtualenvwrapper, we created a symlink; \
			echo "so you can also use "workon $(PKG_NAME)" to activate the venv."; \
			echo ; \
		fi; \
	fi
endef

define rm-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		if [ -L "$(WORKON_HOME)/$(PKG_NAME)" -a -f "$(WORKON_HOME)/$(PKG_NAME)" ]; \
		then \
			$(RM) $(WORKON_HOME)/$(PKG_NAME); \
		fi; \
	fi
endef

## Public targets

$(VENV_PYTHON): $(VENV_ROOT)
	@echo

$(VENV_ROOT):
	@echo $(CS)Creating a Python environment $(VENV_ROOT)$(CE)
	$(PYTHON) -m venv --prompt $(PKG_NAME) $(VENV_ROOT)
	@echo
	@echo Done.
	@echo
	@echo To active it manually, run:
	@echo
	@echo "    source $(VENV_BIN)/activate"
	@echo
	@echo See https://docs.python.org/3/library/venv.html for more.
	@echo
	$(call mk-venv-link)

.PHONY: init
init: $(VENV_PYTHON)
	@echo $(CS)Installing dev requirements$(CE)
	$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
	$(VENV_PIP) install --upgrade -r $(REQUIREMENTS)

.PHONY: install
install: init
	@echo $(CS)Installing $(PKG_NAME)$(CE)
	$(VENV_PIP) install --upgrade --editable .


.PHONY: uninstall
uninstall:
	@echo $(CS)Uninstalling $(PKG_NAME)$(CE)
	- $(VENV_PIP) uninstall --yes $(PKG_NAME) &2>/dev/null
	@echo Done.
	@echo

.PHONY: clean
clean:
	@echo $(CS)Remove build and tests artefacts and directories$(CE)

	$(RM) -r $(VENV_ROOT)
	$(call rm-venv-link)
	find ./ -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r ./build ./dist ./*.egg-info
	$(RM) -r ./.cache ./.pytest_cache
	$(RM) -r ./htmlcov
	$(RM) ./.coverage ./coverage.xml

.PHONY: check-dist
check-dist: $(VENV_PYTHON)
	@echo $(CS)Check distribution files$(HEADER_EXTRA)$(CE)
	$(VENV_BIN)/twine check ./dist/*
	$(VENV_BIN)/check-wheel-contents ./dist/*.whl
	@echo

.PHONY: test-ccov
test-ccov: COV=--cov=./$(PKG_NAME) --cov=./tests --cov-report=xml --cov-report=html
test-ccov: HEADER_EXTRA=' (with coverage)'
test-ccov: test

.PHONY: test-all
test-all: uninstall clean install test test-dist lint

.PHONY: test-dist
test-dist: test-sdist test-wheel
	@echo

.PHONY: sdist
sdist:
	@echo $(CS)Creating source distribution$(CE)
	$(VENV_PYTHON) setup.py sdist

.PHONY: test-sdist
test-sdist: $(VENV_PYTHON) sdist
	@echo $(CS)Testing source distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.gz
	@echo
	$(VENV_PYTHON) -c "import $(PKG_NAME); print($(PKG_NAME).__version__)"
	@echo

.PHONY: wheel
wheel: $(VENV_PYTHON)
	@echo $(CS)Creating wheel distribution$(CE)
	$(VENV_PYTHON) setup.py bdist_wheel

.PHONY: test-wheel
test-wheel: $(VENV_PYTHON) wheel
	@echo $(CS)Testing built distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.whl
	@echo
	$(VENV_PYTHON) -c "import $(PKG_NAME); print($(PKG_NAME).__version__)"
	@echo

.PHONY: test
test: $(VENV_PYTHON)
	@echo $(CS)Running tests$(HEADER_EXTRA)$(CE)
	export PYTHONDONTWRITEBYTECODE=1
	$(VENV_BIN)/py.test $(PYTEST_FLAGS) $(COV) ./$(PKG_NAME) ./tests
	@echo

.PHONY: lint
lint: $(VENV_PYTHON)
	@echo $(CS)Running linters$(CE)
	$(VENV_BIN)/flake8 $(FLAKE8_FLAGS) ./
	$(VENV_BIN)/pylint ./$(PKG_NAME)

.PHONY: publish
publish: test-all upload

.PHONY: upload
upload: $(VENV_PYTHON)
	@echo $(CS)Upload built distribution$(CE)
	@$(VENV_PYTHON) setup.py --version | grep -q "dev" && echo '!!! Not publishing dev version !!!' && exit 1 || echo ok
	$(MAKE) build
	$(MAKE) check-dist
	$(VENV_BIN)/twine upload ./dist/*
	@echo

.PHONY: build
build: sdist wheel
	@echo

.PHONY: help
help:
	@echo $(PKG_NAME)
	@echo
	@echo 'Run "make init" first to install and update all dev dependencies.'
	@echo 'See "default.mk" for variables you might want to set.'
	@echo
	@echo 'Available targets:'
	@echo
	@echo '  help:         Show this help and exit'
	@echo '  init:         Installing dev requirements (has to be launched first)'
	@echo '  install:      Install development version of $(PKG_NAME)'
	@echo '  uninstall:    Uninstall local version of $(PKG_NAME)'
	@echo '  build:        Build $(PKG_NAME) distribution (sdist and wheel)'
	@echo '  sdist:        Create a source distribution'
	@echo '  wheel:        Create a wheel distribution'
	@echo '  publish:      Publish $(PKG_NAME) distribution to the repository'
	@echo '  upload:       Upload $(PKG_NAME) distribution to the repository (w/o tests)'
	@echo '  clean:        Remove build and tests artefacts and directories'
	@echo '  check-dist:   Check integrity of the distribution files and validate package'
	@echo '  test:         Run unit tests'
	@echo '  test-dist:    Testing package distribution and installation'
	@echo '  test-sdist:   Testing source distribution and installation'
	@echo '  test-wheel:   Testing built distribution and installation'
	@echo '  test-all:     Test everything'
	@echo '  test-ccov:    Run unit tests with coverage'
	@echo '  lint:         Lint the code'
	@echo
	@echo 'Virtualenv:'
	@echo
	@echo '  Python:       $(VENV_PYTHON)'
	@echo '  pip:          $(VENV_PIP)'
	@echo
	@echo 'Flags:'
	@echo
	@echo '  FLAKE8_FLAGS: $(FLAKE8_FLAGS)'
	@echo '  PYTEST_FLAGS: $(PYTEST_FLAGS)'
	@echo
	@echo 'Environment variables:'
	@echo
	@echo '  PYTHON:       $(PYTHON)'
	@echo '  WORKON_HOME:  ${WORKON_HOME}'
	@echo '  SHELL:        $(shell echo $$SHELL)'
	@echo '  TERM:         $(shell echo $$TERM)'
	@echo
