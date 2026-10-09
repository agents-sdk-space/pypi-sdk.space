.PHONY: install dev test lint format doctor build check-dist monitor monitor-slack publishing

install:
	python -m pip install -e .

dev:
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

lint:
	python -m ruff check src tests

format:
	python -m ruff format src tests

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
