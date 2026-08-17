.PHONY: install lint format typecheck test smoke test-cov report clean

install:        ## Install runtime and dev dependencies
	pip install -r requirements.txt -r requirements-dev.txt

lint:           ## Run ruff lint and format checks
	ruff check .
	ruff format --check .

format:         ## Auto-fix lint issues and reformat
	ruff check --fix .
	ruff format .

typecheck:      ## Run mypy over src and tests
	mypy src tests

test:           ## Run the full suite
	pytest

smoke:          ## Run the smoke subset
	pytest -m smoke

test-cov:       ## Run the suite with a coverage report
	pytest --cov --cov-report=term-missing

report:         ## Serve the Allure report locally
	allure serve allure-results

clean:          ## Remove caches and generated artifacts
	rm -rf allure-results allure-report .pytest_cache .ruff_cache .mypy_cache .coverage
