# jupyterlab_templates
Support for jupyter notebook templates in jupyterlab

[![Build Status](https://travis-ci.org/timkpaine/jupyterlab_templates.svg?branch=master)](https://travis-ci.org/timkpaine/jupyterlab_templates)
[![GitHub issues](https://img.shields.io/github/issues/timkpaine/jupyterlab_templates.svg)]()
[![codecov](https://codecov.io/gh/timkpaine/jupyterlab_templates/branch/master/graph/badge.svg)](https://codecov.io/gh/timkpaine/jupyterlab_templates)
[![PyPI](https://img.shields.io/pypi/l/jupyterlab_templates.svg)](https://pypi.python.org/pypi/jupyterlab_templates)
[![PyPI](https://img.shields.io/pypi/v/jupyterlab_templates.svg)](https://pypi.python.org/pypi/jupyterlab_templates)
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
c.JupyterLabTemplates.include_default = True
```

## Templates for libraries
If you have tutorials or guides you'd like to install for users, simply copy them into your jupyter data folder inside the `notebook_templates` directory, e.g. `/usr/local/share/jupyter/notebook_templates/bqplot` for `bqplot`.

Templates will be looked for in a subdirectory of one of the `template_dirs` specified above.

### Flags
- `template_dirs`: a list of directories. all `.ipynb` files in these directories will be listed as templates
- `include_default`: include the default Sample template (default True)
- `include_core_paths`: include jupyter core paths (see: jupyter --paths) (default True)
