###############
# Build Tools #
###############
build:  ## build python/javascript
	python -m build .

develop:  ## install to site-packages in editable mode
	python -m pip install --upgrade build pip setuptools twine wheel
	cd js; yarn
	python -m pip install -e .[develop]

install:  ## install to site-packages
	python -m pip install .

###########
# Testing #
###########
testpy: ## Clean and Make unit tests
	python -m pytest -v jupyterlab_templates/tests --junitxml=junit.xml --cov=jupyterlab_templates --cov-report=xml:.coverage.xml --cov-branch --cov-fail-under=20 --cov-report term-missing

testjs: ## Clean and Make js tests
	cd js; yarn test

test: tests
tests: testpy testjs ## run the tests

###########
# Linting #
###########
lintpy:  ## Black/flake8 python
	python -m ruff jupyterlab_templates setup.py
	python -m black --check jupyterlab_templates setup.py

lintjs:  ## ESlint javascript
	cd js; yarn lint

lint: lintpy lintjs  ## run linter

fixpy:  ## Black python
	python -m ruff jupyterlab_templates setup.py --fix
	python -m black jupyterlab_templates/ setup.py

fixjs:  ## ESlint Autofix JS
	cd js; yarn fix

fix: fixpy fixjs  ## run black/tslint fix
format: fix

#################
# Other Checks #
#################
check: checks

checks: check-manifest  ## run security, packaging, and other checks

check-manifest:  ## run manifest checker for sdist
	check-manifest -v

semgrep:  ## run semgrep
	semgrep ci --config auto

################
# Distribution #
################
dist: clean build  ## create dists
	python -m twine check dist/*

publishpy:  ## dist to pypi
	python -m twine upload dist/* --skip-existing

publishjs:  ## dist to npm
	cd js; npm publish || echo "can't publish - might already exist"

publish: dist publishpy publishjs  ## dist to pypi and npm

############
# Cleaning #
############
clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf
	find . -name "*.pyc" | xargs rm -rf
	find . -name ".ipynb_checkpoints" | xargs  rm -rf
	rm -rf .coverage coverage *.xml build dist *.egg-info lib node_modules .pytest_cache *.egg-info
	rm -rf jupyterlab_templates/labextension
	cd js && yarn clean
	git clean -fd

###########
# Helpers #
###########
# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: testjs testpy tests test lintpy lintjs lint fixpy fixjs fix format checks check check-manifest semgrep build develop install labextension dist publishpy publishjs publish docs clean
