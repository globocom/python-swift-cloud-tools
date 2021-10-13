.PHONY: help clean setup pycodestyle tests tests-ci dist release

# Version package
VERSION=$(shell python -c 'import swift-cloud-tools; print(swift-cloud-tools.__version__)')

CWD="`pwd`"
PROJECT_HOME = $(CWD)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Project cleaning up for any extra files created during execution
	@echo "Cleaning up"
	@rm -rf build dist *.egg-info
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@find . -name "**/*.pyc" -delete
	@find . -name "*.~" -delete
	@rm -rf .pytest_cache

setup:
	@pip install -r $(PROJECT_HOME)/requirements_test.txt

pycodestyle: ## Check source-code for pycodestyle compliance
	@echo "Checking source-code pycodestyle compliance"
	@-pycodestyle $(PROJECT_HOME) --ignore=E501,E126,E127,E128,W605

tests: clean pycodestyle ## Run tests (with coverage)
	@echo "Running all tests with coverage"
	@py.test --cov-config .coveragerc --cov $(PROJECT_HOME) --cov-report term-missing

tests-ci: clean pycodestyle ## Run tests
	@echo "Running the tests"
	@py.test

dist: clean ## Make dist
	@python setup.py sdist

release: clean dist ## Publish a new release
	@echo 'Releasing version ${VERSION}'
	twine upload dist/*
	@git tag ${VERSION}
	@git push --tags
