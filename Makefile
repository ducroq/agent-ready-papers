.PHONY: test lint format check coverage check-dois check-metadata verify-bib check-registry drift dr-status gotcha-stats

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

check-metadata:  ## Bibliographic field verification against Paper 1 registry
	python -m tools.check_metadata papers/perspective/vv/claims/claim_registry.md

verify-bib:  ## Field-level verification of Paper 1 references.bib (the stronger check)
	python -m tools.check_metadata papers/perspective/references.bib

check-registry:  ## Registry/manuscript internal consistency for Paper 1
	python -m tools.check_registry papers/perspective/vv/claims/claim_registry.md \
		--manuscript papers/perspective/manuscript.tex --budget 5000

drift:  ## Session-start drift check: companion pin, global skills, self and paper stamps
	bash scripts/drift.sh

dr-status:  ## Decision records grouped by status (only Accepted binds)
	bash scripts/dr-status.sh

gotcha-stats:  ## Gotcha-log entry count and sizes (maintainer-local memory/)
	bash scripts/gotcha-stats.sh
