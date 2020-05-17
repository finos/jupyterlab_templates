# jupyterlab_templates
Support for jupyter notebook templates in jupyterlab

[![Build Status](https://dev.azure.com/tpaine154/jupyter/_apis/build/status/jpmorganchase.jupyterlab_templates?branchName=master)](https://dev.azure.com/tpaine154/jupyter/_build/latest?definitionId=26&branchName=master)
[![GitHub issues](https://img.shields.io/github/issues/jpmorganchase/jupyterlab_templates.svg)]()
[![Coverage](https://img.shields.io/azure-devops/coverage/tpaine154/jupyter/26/master)](https://dev.azure.com/tpaine154/jupyter/_build?definitionId=26&_a=summary)
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
c.JupyterLabTemplates.include_core_paths = True
```

## Templates for libraries
The extension will search *subdirectories* of each parent directory specified in `template_dirs` for templates.

The `notebook_templates` directory under the jupyter data folder is one of the default parent directory. Thus, if you have tutorials or guides you'd like to install for users, simply copy them into your jupyter data folder inside the `notebook_templates` directory, e.g. `/usr/local/share/jupyter/notebook_templates/bqplot` for `bqplot`.


### Flags
- `template_dirs`: a list of absolute directory paths. All `.ipynb` files in any *subdirectories* of these paths will be listed as templates
- `include_default`: include the default Sample template (default True)
- `include_core_paths`: include jupyter core paths (see: jupyter --paths) (default True)


## Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.


## License

This software is licensed under the Apache 2.0 license. See the
[LICENSE](LICENSE) and [AUTHORS](AUTHORS) files for details.
