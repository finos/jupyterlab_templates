# jupyterlab_templates
Support for jupyter notebook templates in jupyterlab

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
