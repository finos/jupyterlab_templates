testjs: ## Clean and Make js tests
	yarn test

testpy: ## Clean and Make unit tests
	python3 -m pytest -v tests --cov=jupyterlab_templates

test: lint ## run the tests for travis CI
	@ python3 -m pytest -v tests --cov=jupyterlab_templates
	yarn test

lint: ## run linter
	flake8 jupyterlab_templates 
	yarn lint

annotate: ## MyPy type annotation check
	mypy -s jupyterlab_templates

annotate_l: ## MyPy type annotation check - count only
	mypy -s jupyterlab_templates | wc -l 

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf 
	find . -name "*.pyc" | xargs rm -rf 
	find . -name ".ipynb_checkpoints" | xargs  rm -rf 
	rm -rf .coverage cover htmlcov logs build dist *.egg-info lib node_modules

install:  ## install to site-packages
	pip3 install .

serverextension: install ## enable serverextension
	jupyter serverextension enable --py jupyterlab_templates

js:  ## build javascript
	yarn
	yarn build

labextension: js ## enable labextension
	jupyter labextension install .

dist:  js  ## dist to pypi
	rm -rf dist build
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	twine check dist/* && twine upload dist/*

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean install serverextension labextension test tests help docs dist
