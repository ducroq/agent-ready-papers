.PHONY: test lint format check coverage check-dois check-metadata verify-bib check-registry formula-scan preservation-check drift dr-status gotcha-stats check-counts read-surface

test:  ## Run tests
	pytest tests/ -x -q

lint:  ## Run linter
	ruff check tools/ tests/ extensions/

format:  ## Auto-format code
	ruff format tools/ tests/ extensions/
	ruff check --fix tools/ tests/ extensions/

check:  ## Run all checks (lint + test)
	ruff check tools/ tests/ extensions/
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

formula-scan:  ## Advisory formula/readability locator (PROPOSED, DR-022); FILE=<path>, default Paper 1
	python extensions/formula_scan.py "$(or $(FILE),papers/perspective/manuscript.tex)"

preservation-check:  ## Did a translation keep numbers and certainty? (PROPOSED, DR-023); SRC=<source> TRN=<translation> [LINK=<source link>]
	@[ -n "$(SRC)" ] && [ -n "$(TRN)" ] || { echo "usage: make preservation-check SRC=<source> TRN=<translation> [LINK=<source link>]"; exit 2; }
	python extensions/preservation_check.py "$(SRC)" "$(TRN)" $(if $(LINK),--link "$(LINK)")

drift:  ## Session-start drift check: companion pin, global skills, self and paper stamps
	bash scripts/drift.sh

dr-status:  ## Decision records grouped by status (only Accepted binds)
	bash scripts/dr-status.sh

gotcha-stats:  ## Gotcha-log entry count and sizes (maintainer-local memory/)
	bash scripts/gotcha-stats.sh

check-counts:  ## Character and test counts stated in the top CHANGELOG section vs the repo (run before /release)
	bash scripts/check-counts.sh

read-surface:  ## Characters in memory/ and docs/work-items/ outside archive/ vs a budget (maintainer-local)
	bash scripts/read-surface.sh
