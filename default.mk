# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

# Run “make build” by default
.DEFAULT_GOAL = build

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifneq (,$(findstring xterm,${TERM}))
	GREEN := $(shell tput -Txterm setaf 2)
	RESET := $(shell tput -Txterm sgr0)
	CS = "${GREEN}~~~ "
	CE = " ~~~${RESET}"
else
	CS = "~~~ "
	CE = " ~~~"
endif

COV          =
HEADER_EXTRA =

REQUIREMENTS     = requirements.txt
REQUIREMENTS_DEV = requirements-dev.txt

PYTEST_FLAGS ?= --color=yes -v
FLAKE8_FLAGS ?= --show-source --statistics

VENV_ROOT = .venv

# PYTHON will used to create venv
ifeq ($(OS),Windows_NT)
	PYTHON  ?= python
	VENV_BIN = $(VENV_ROOT)/Scripts
else
	PYTHON  ?= python3
	VENV_BIN = $(VENV_ROOT)/bin
endif

VENV_PIP    = $(VENV_BIN)/pip
VENV_PYTHON = $(VENV_BIN)/python

# Program availability
ifndef PYTHON
$(error "Python is not available please install Python")
else
ifneq ($(OS),Windows_NT)
HAVE_PYTHON := $(shell sh -c "command -v $(PYTHON)")
ifndef HAVE_PYTHON
$(error "Python is not available please install Python")
endif
endif
endif

#define CHECK_AIRSLATE
#import pkgutil
#print(1 if pkgutil.find_loader('airslate') else 0)
#endef
#export CHECK_AIRSLATE
#
#HAVE_AIRSLATE=$(shell sh -c "$(VENV_PYTHON) -c \"$$CHECK_AIRSLATE\"")
#$(error "HAVE_AIRSLATE=$(HAVE_AIRSLATE)")
