.PHONY: test lint format check coverage check-dois

test:  ## Run tests
	pytest tests/ -x -q

lint:  ## Run linter
	ruff check tools/ tests/

format:  ## Auto-format code
	ruff format tools/ tests/
	ruff check --fix tools/ tests/

check:  ## Run all checks (lint + test)
	ruff check tools/ tests/
	pytest tests/ -x -q

coverage:  ## Coverage report against Paper 1 registry
	python -m tools.coverage papers/perspective/vv/claims/claim_registry.md

check-dois:  ## DOI verification against Paper 1 registry
	python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md
