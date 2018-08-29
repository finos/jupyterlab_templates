# jupyterlab_templates
Support for jupyter notebook templates in jupyterlab

[![Build Status](https://travis-ci.org/timkpaine/jupyterlab_templates.svg?branch=master)](https://travis-ci.org/timkpaine/jupyterlab_templates)
[![GitHub issues](https://img.shields.io/github/issues/timkpaine/jupyterlab_templates.svg)]()
[![codecov](https://codecov.io/gh/timkpaine/jupyterlab_templates/branch/master/graph/badge.svg)](https://codecov.io/gh/timkpaine/jupyterlab_templates)
[![PyPI](https://img.shields.io/pypi/l/jupyterlab_iframe.svg)](https://pypi.python.org/pypi/jupyterlab_templates)
[![PyPI](https://img.shields.io/pypi/v/jupyterlab_iframe.svg)](https://pypi.python.org/pypi/jupyterlab_templates)
[![npm](https://img.shields.io/npm/v/jupyterlab_templates.svg)](https://www.npmjs.com/package/jupyterlab_templates)

![](https://raw.githubusercontent.com/timkpaine/jupyterlab_templates/master/docs/example1.gif)


## Install
```bash
pip install jupyterlab_templates
jupyter labextension install jupyterlab_templates
jupyter serverextension enable --py jupyterlab_templates
```

## Adding templates
install the server extension, and add the following to `jupyter_notebook_config.py`

```python3
c.JupyterLabTemplates.template_dirs = ['list', 'of', 'template', 'directories']
```
