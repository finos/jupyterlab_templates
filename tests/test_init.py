# for Coverage
from mock import patch, MagicMock
from jupyterlab_templates import _jupyter_server_extension_paths


class TestInit:
    def setup(self):
        pass
        # setup() before each test method

    def teardown(self):
        pass
        # teardown() after each test method

    @classmethod
    def setup_class(cls):
        pass
        # setup_class() before any methods in this class

    @classmethod
    def teardown_class(cls):
        pass
        # teardown_class() after any methods in this class

    def test__jupyter_server_extension_paths(self):
        assert _jupyter_server_extension_paths() == [{"module": "jupyterlab_templates.extension"}]
