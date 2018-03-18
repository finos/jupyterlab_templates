# jupyterlab_templates
Support for jupyter notebook templates in jupyterlab

![](https://raw.githubusercontent.com/timkpaine/jupyterlab_iframe/master/docs/example1.gif)

## Adding templates
install the server extension, and add the following to `jupyter_notebook_config.py`

```python3
c.JupyterLabTemplate.template_dirs = ['list', 'of', 'template', 'directories']
```
