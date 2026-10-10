.PHONY: install dev test lint format doctor build check-dist monitor monitor-slack publishing

PYTHON ?= python3

install:
	$(PYTHON) -m pip install -e .

dev:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check src tests

format:
	$(PYTHON) -m ruff format src tests

doctor:
	pypi-space doctor

build:
	pypi-space build

check-dist: build
	pypi-space check-dist dist

monitor:
	pypi-space monitor run --json

monitor-slack:
	pypi-space monitor slack

publishing:
	pypi-space publishing
