# for Coverage
from mock import patch, MagicMock
from jupyterlab_templates.extension import load_jupyter_server_extension


class TestExtension:
    def test_load_jupyter_server_extension(self):

        m = MagicMock()

        m.web_app.settings = {}
        m.web_app.settings['base_url'] = '/test'
        load_jupyter_server_extension(m)
