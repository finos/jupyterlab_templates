import os
import os.path
import json
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join


class TemplatesHandler(IPythonHandler):
    def initialize(self, templates=None):
        self.templates = templates

    def get(self, template=None):
        self.finish(json.dumps({'templates': self.templates}))


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    template_dirs = nb_server_app.config.get('JupyterLabTemplates', {}).get('template_dirs', [])

    if nb_server_app.config.get('JupyterLabTemplates', {}).get('include_default', True):
        template_dirs.append(os.path.join(os.path.dirname(__file__), 'templates'))

    base_url = web_app.settings['base_url']

    host_pattern = '.*$'
    print('Installing jupyterlab_templates handler on path %s' % url_path_join(base_url, 'templates'))

    template_dirs = nb_server_app.config.get('JupyterLabTemplates', {}).get('template_dirs', [])

    templates = []
    for path in template_dirs:
        abspath = os.path.abspath(os.path.realpath(path))
        files = [f for f in os.listdir(abspath) if os.path.isfile(os.path.join(abspath, f)) and f.endswith('.ipynb')]
        for f in files:
            with open(os.path.join(abspath, f), 'r') as fp:
                content = fp.read()
            templates.append((f, abspath, content))

    print('Available templates: %s' % ','.join(t[0] for t in templates))
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, 'templates/get'), TemplatesHandler, {'templates': templates})])
