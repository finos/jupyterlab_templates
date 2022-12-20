<img src="https://github.com/finos/jupyterlab_templates/raw/main/docs/logo.png" width=400></img>

Support for jupyter notebook templates in jupyterlab

[![Build Status](https://github.com/finos/jupyterlab_templates/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/finos/jupyterlab_templates/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/finos/jupyterlab_templates/branch/main/graph/badge.svg)](https://codecov.io/gh/finos/jupyterlab_templates)
[![PyPI](https://img.shields.io/pypi/l/jupyterlab_templates.svg)](https://pypi.python.org/pypi/jupyterlab_templates)
[![PyPI](https://img.shields.io/pypi/v/jupyterlab_templates.svg)](https://pypi.python.org/pypi/jupyterlab_templates)
[![npm](https://img.shields.io/npm/v/jupyterlab_templates.svg)](https://www.npmjs.com/package/jupyterlab_templates)

![](https://raw.githubusercontent.com/finos/jupyterlab_templates/main/docs/example1.gif)


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
**Note!** Templates in the parent directories will be ignored. You must put the templates in *subdirectories*, in order to keep everything organized.  

If `include_default = True` the `notebook_templates` directory under the [jupyter data folder](https://jupyter.readthedocs.io/en/latest/use/jupyter-directories.html) is one of the default parent directories. Thus, if you have tutorials or guides you'd like to install for users, simply copy them into your jupyter data folder inside the `notebook_templates` directory, e.g. `/usr/local/share/jupyter/notebook_templates/bqplot` for `bqplot`.


### Flags
- `template_dirs`: a list of absolute directory paths. All `.ipynb` files in any *subdirectories* of these paths will be listed as templates
- `include_default`: include the default Sample template (default True)
- `include_core_paths`: include jupyter core paths (see: jupyter --paths) (default True)


## Contributing
For any questions, bugs or feature requests please open an [issue](https://github.com/finos/jupyterlab_templates/issues)

To submit a contribution:
1. Fork it (<https://github.com/finos/jupyterlab_templates/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Read our [contribution guidelines](./CONTRIBUTING.md) and [Community Code of Conduct](https://www.finos.org/code-of-conduct)
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request

_NOTE:_ Commits and pull requests to FINOS repositories will only be accepted from those contributors with an active, executed Individual Contributor License Agreement (ICLA) with FINOS OR who are covered under an existing and active Corporate Contribution License Agreement (CCLA) executed with FINOS. Commits from individuals not covered under an ICLA or CCLA will be flagged and blocked by the FINOS Clabot tool (or [EasyCLA](https://community.finos.org/docs/governance/Software-Projects/easycla)). Please note that some CCLAs require individuals/employees to be explicitly named on the CCLA.


*Need an ICLA? Unsure if you are covered under an existing CCLA? Email [help@finos.org](mailto:help@finos.org)*

## License

Copyright 2020 JP Morgan Chase

Distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

SPDX-License-Identifier: [Apache-2.0](https://spdx.org/licenses/Apache-2.0)