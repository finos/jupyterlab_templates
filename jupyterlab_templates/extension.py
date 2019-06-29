import os
import os.path
import fnmatch
import json
from io import open
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join


class TemplatesHandler(IPythonHandler):
    def initialize(self, templates=None):
        self.templates = templates

    def get(self):
        temp = self.get_argument('template', '')
        if temp:
            self.finish(self.templates[temp])
        else:
            self.set_status(404)


class TemplateNamesHandler(IPythonHandler):
    def initialize(self, templates=None):
        self.templates = templates

    def get(self, template=None):
        self.finish(json.dumps(sorted(self.templates.keys())))


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

    # TODO
    # template_dirs.append('STANDARD INSTALL DIR')

    templates = {}
    for path in template_dirs:
        abspath = os.path.abspath(os.path.realpath(path))
        files = []
        # get all files in subdirectories
        for dirname, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.ipynb'):
                files.append((os.path.join(dirname, filename), dirname.replace(path, ''), filename))

        # pull contents and push into templates list
        for f, dirname, filename in files:
            with open(os.path.join(abspath, f), 'r', encoding='utf8') as fp:
                content = fp.read()
            templates[os.path.join(dirname, filename)] = {'path': f, 'dirname': dirname, 'filename': filename, 'content': content}

    print('Available templates:\n\t%s' % '\n\t'.join(t for t in templates))
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, 'templates/names'), TemplateNamesHandler, {'templates': templates})])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, 'templates/get'), TemplatesHandler, {'templates': templates})])
