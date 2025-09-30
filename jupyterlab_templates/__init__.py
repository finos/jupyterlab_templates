# *****************************************************************************
#
# Copyright (c) 2020, the jupyterlab_templates authors.
#
# This file is part of the jupyterlab_templates library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.

__version__ = "0.1.0"


def _jupyter_server_extension_paths():
    return [{"module": "jupyterlab_templates"}]


def _jupyter_server_extension_points():
    return [{"module": "jupyterlab_templates"}]


def _load_jupyter_server_extension(nb_server_app, nb6_entrypoint=False):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    # web_app = nb_server_app.web_app


def _jupyter_nbextension_paths():
    return [
        {
            "section": "tree",
            "src": "nbextension/static",
            "dest": "jupyterlab_templates",
            "require": "jupyterlab_templates/notebook",
        }
    ]
