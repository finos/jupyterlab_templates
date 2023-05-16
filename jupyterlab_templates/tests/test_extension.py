# *****************************************************************************
#
# Copyright (c) 2020, the jupyterlab_templates authors.
#
# This file is part of the jupyterlab_templates library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
# for Coverage
from unittest.mock import MagicMock
from jupyterlab_templates.extension import load_jupyter_server_extension


class TestExtension:
    def get_mock_config(self, file_system):
        m = MagicMock()
        m.web_app.settings = {}
        m.web_app.settings["base_url"] = "/test"
        m.config = {'file_system': file_system}
        return m

    def test_load_jupyter_server_extension(self):
        load_jupyter_server_extension(self.get_mock_config('local'))

    def test_load_jupyter_server_extension_hdfs(self):
        load_jupyter_server_extension(self.get_mock_config('hdfs'))
