#!/usr/bin/env make

# Change this to match the name of the highest level python package
PROJECT		:= weather_ai
RM			:= rm -rf
PYTHON		:= python3
COVERAGE	:= 90

.DEFAULT_GOAL	:= test

.PHONY: all badge clean cleanall doc format help lint preen report test lint_unsafe

all: test report

help:
	@echo
	@echo "Default goal: ${.DEFAULT_GOAL}"
	@echo
	@echo "  all:    style and test"
	@echo "  badge:  generate project badges"
	@echo "  clean:  delete all generated files"
	@echo "  doc:    generate html reports and pdoc"
	@echo "  format: format code, sort imports and requirements"
	@echo "  lint:   check code"
	@echo "  preen:  format and lint"
	@echo "  report: doc and badge"
	@echo "  test:   preen and run unit tests"
	@echo
	@echo "Initialise virtual environment (.venv) with:"
	@echo
	@echo "  pip3 install virtualenv"
	@echo "  python3 -m virtualenv .venv"
	@echo "  source .venv/bin/activate          (*nix)"
	@echo "  source .venv/Scripts/activate      (windows)"
	@echo "  pip3 install -Ur requirements.txt"
	@echo
	@echo "Start virtual environment (.venv) with:"
	@echo
	@echo "  source .venv/bin/activate          (*nix)"
	@echo "  source .venv/Scripts/activate      (windows)"
	@echo
	@echo Deactivate with:
	@echo
	@echo "  deactivate"
	@echo

format:
	ruff format
	sort-requirements requirements.txt

lint:
	ruff check --output-format grouped --fix

lint_unsafe:
	ruff check --unsafe-fixes --fix --show-fixes

preen:	format lint

test:	preen
	pytest --verbose --cov-fail-under=$(COVERAGE) $(PROJECT)

report:	doc badge

doc:
	pdoc $(PROJECT) !$(PROJECT).tests -o public

	pytest --cov --cov-report=html:public/coverage \
	  --html=public/pytest_report.html --self-contained-html

badge:
	# pytest
	pytest --junitxml=public/pytest_report.xml
	genbadge tests --input-file public/pytest_report.xml --output-file public/tests.svg

clean:
	# clean generated artefacts
	$(RM) $(PROJECT)/__pycache__/ $(PROJECT)/*/__pycache__/
	$(RM) .coverage
	$(RM) .hypothesis/
	$(RM) .pytest_cache/
	$(RM) public/

cleanall: clean
	# clean development environment
	$(RM) .venv/
	$(RM) .idea/
