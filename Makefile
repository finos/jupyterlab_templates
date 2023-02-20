test-js:  ## run js tests
	cd js; yarn test

test-py:  ## run python tests
	python -m pytest -v jupyterlab_templates/tests --junitxml=python_junit.xml --cov=jupyterlab_templates --cov-report=xml:.coverage.xml --cov-report=html:.coverage.html --cov-branch --cov-fail-under=60 --cov-report term-missing

tests: test-py test-js ## run the tests

build-js:  ## build js assets
	cd js; yarn
	cd js; yarn build

build:  ## build python and js
	python setup.py build

lint-py:  ## run python linter
	python -m flake8 jupyterlab_templates setup.py
	python -m black --check jupyterlab_templates setup.py

lint-js:  ## run js linter
	cd js; yarn lint

lint: lint-py lint-js ## run linters

fix-py:  ## run python autofixes
	python -m black jupyterlab_templates setup.py

fix-js:  ## run js autofixes
	cd js; yarn fix

fix: fix-py fix-js  ## run autofixers

check-manifest:  ## check python sdist is complete
	python -m check_manifest

check-security-py:  ## check for security vulnerabilities in python
	python -m safety check --full-report -r jupyterlab_templates.egg-info/requires.txt

checks-py: check-manifest check-security-py  ## run python checks

check-security-js:  ## check for security vulnerabilities in python
	cd js; yarn check-security

checks-js: check-security-js  ## run js checks

checks: checks-py checks-js ## run checks

# Alias
check: checks

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf
	find . -name "*.pyc" | xargs rm -rf
	find . -name ".ipynb_checkpoints" | xargs  rm -rf
	rm -rf .coverage coverage cover htmlcov logs build dist *.egg-info lib node_modules .autoversion .pytest_cache lab-dist coverage.xml python_junit.xml
	# make -C ./docs clean

docs:  ## make documentation
	make -C ./docs html
	open ./docs/_build/html/index.html

install:  ## install to site-packages
	python -m pip install .

serverextension: install ## enable serverextension
	python -m jupyter serverextension enable --py jupyterlab_templates

labextension: build-js ## enable labextension
	cd js; python -m jupyter labextension install .

dist: build-js  ## create dists
	rm -rf dist build js/node_modules
	python setup.py sdist bdist_wheel
	python -m twine check dist/*

publish: dist  ## dist to pypi and npm
	python -m twine upload dist/* --skip-existing
	cd js; npm publish || echo "can't publish - might already exist"

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: test-js test-py tests build-js build lint-py lint-js lint fix-py fix-js fix check-manifest check-security-py check-licenses-py checks-py check-security-js check-licenses-js checks-js checks check clean docs install serverextension labextension dist publish help
