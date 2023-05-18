<img src="https://github.com/finos/jupyterlab_templates/raw/main/docs/logo.png" width=400></img>

Support for jupyter notebook templates in jupyterlab

[![Build Status](https://github.com/finos/jupyterlab_templates/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/finos/jupyterlab_templates/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/finos/jupyterlab_templates/branch/main/graph/badge.svg)](https://codecov.io/gh/finos/jupyterlab_templates)
[![PyPI](https://img.shields.io/pypi/l/jupyterlab_templates.svg)](https://pypi.python.org/pypi/jupyterlab_templates)
[![PyPI](https://img.shields.io/pypi/v/jupyterlab_templates.svg)](https://pypi.python.org/pypi/jupyterlab_templates)
[![npm](https://img.shields.io/npm/v/jupyterlab_templates.svg)](https://www.npmjs.com/package/jupyterlab_templates)
[![FINOS Active](https://cdn.jsdelivr.net/gh/finos/contrib-toolbox@master/images/badge-active.svg)](https://community.finos.org/docs/governance/software-projects/stages/active/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/finos/jupyterlab_templates/main?urlpath=lab)

![](https://raw.githubusercontent.com/finos/jupyterlab_templates/main/docs/example1.gif)


## Install

### PyPI
`jupyterlab_templates` is available on [PyPI](https://pypi.org/project/jupyterlab-templates/):

```bash
pip install jupyterlab_templates
```

### Conda
`jupyterlab_templates` is also available on [conda-forge](https://github.com/conda-forge/jupyterlab_templates-feedstock):

```bash
conda install -c conda-forge jupyterlab_templates
```

### Jupyter Server/JupyterLab Extension
```
jupyter labextension install jupyterlab_templates
jupyter server extension enable --py jupyterlab_templates
```

## Adding templates
install the server extension, and add the following to `jupyter_notebook_config.py`

```python3
c.JupyterLabTemplates.template_dirs = ['list', 'of', 'template', 'directories']
c.JupyterLabTemplates.include_default = True
c.JupyterLabTemplates.include_core_paths = True
```

## HDFS path

HDFS paths are supported by setting the hdfs:// prefix in the template_dirs list and can be used with local paths. 
The 
For example:

```python3
c.JupyterLabTemplates.template_dirs = ['hdfs://path/to/template/directory', '/local/path']
```

> Note: The `fs.defaultFS` from `core-site.xml` will be used to define the connection to HDFS.

```python3

## Templates for libraries
The extension will search *subdirectories* of each parent directory specified in `template_dirs` for templates.
**Note!** Templates in the parent directories will be ignored. You must put the templates in *subdirectories*, in order to keep everything organized.  

If `include_default = True` the `notebook_templates` directory under the [jupyter data folder](https://jupyter.readthedocs.io/en/latest/use/jupyter-directories.html) is one of the default parent directories. Thus, if you have tutorials or guides you'd like to install for users, simply copy them into your jupyter data folder inside the `notebook_templates` directory, e.g. `/usr/local/share/jupyter/notebook_templates/bqplot` for `bqplot`.


### Flags
- `template_dirs`: a list of absolute directory paths. All `.ipynb` files in any *subdirectories* of these paths will be listed as templates
- `include_default`: include the default Sample template (default True)
- `include_core_paths`: include jupyter core paths (see: jupyter --paths) (default True)


## Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.


## License

This software is licensed under the Apache 2.0 license. See the
[LICENSE](LICENSE) and [AUTHORS](AUTHORS) files for details.
