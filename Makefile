.PHONY: verify
verify:
	lint test coverage

.PHONY: install
install:
	poetry install --all-extras

.PHONY: format
format:
	poetry run black --safe .

.PHONY: lint
lint:
	make .ruff .format_check .poetry_check

.PHONY: poetry_check
poetry_check:
	poetry check

.PHONY: format_check
format_check:
	poetry run black --safe --check --diff --color .

.PHONY: test
test:
	poetry run pytest tests --asyncio-mode=auto --doctest-modules --junitxml=junit/test-results.xml tests/ --cov=spotipyio --cov-report=xml --cov-report=html

.PHONY: coverage
coverage:
	poetry run coverage report

.PHONY: ruff
.ruff:
	poetry run ruff check .
