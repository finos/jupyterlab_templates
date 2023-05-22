# *****************************************************************************
#
# Copyright (c) 2020, the jupyterlab_templates authors.
#
# This file is part of the jupyterlab_templates library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
import json
import os
import os.path
from collections import defaultdict

import jupyter_core.paths
import tornado.web

from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join

from distutils.util import strtobool

from pyarrow import fs


class TemplatesLoader:
    def __init__(self, template_dirs, log):
        self.template_dirs = template_dirs
        self.log = log

    def get_templates(self):
        templates = defaultdict(list)
        template_by_path = {}

        for uri in self.template_dirs:
            try:
                client, path = fs.FileSystem.from_uri(uri)
            except Exception as e:
                self.log.error("Failed to load template directory %s. \n%s", uri, e)
                continue

            try:
                for file in client.get_file_info(fs.FileSelector(path, recursive=True)):
                    if file.extension == "ipynb":
                        with client.open_input_file(file.path) as f:
                            content = f.read().decode("utf-8")
                        data = {
                            "path": file.path,
                            "name": file.base_name,
                            "dirname": os.path.dirname(file.path),
                            "filename": file.base_name,
                            "content": content,
                        }

                        # don't include content unless necessary
                        templates[data["dirname"]].append({"name": data["name"]})
                        # full data
                        template_by_path[data["name"]] = data
            except FileNotFoundError as e:
                self.log.warning("Failed to load template directory %s. \n%s", uri, e)
                continue

        return templates, template_by_path


class TemplatesHandler(IPythonHandler):
    def initialize(self, loader):
        self.loader = loader

    @tornado.web.authenticated
    def get(self):
        temp = self.get_argument("template", "")
        if temp:
            self.finish(self.loader.get_templates()[1][temp])
        else:
            self.set_status(404)


class TemplateNamesHandler(IPythonHandler):
    def initialize(self, loader):
        self.loader = loader

    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps(self.loader.get_templates()[0]))


def get_bool_config(config, key, default_value=True):
    value = config.get(key, default_value)
    return strtobool(value) if isinstance(value, str) else value


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    jupyterlab_templates_config = nb_server_app.config.get("JupyterLabTemplates", {})
    nb_server_app.log.info("jupyterlab_templates config: %s" % jupyterlab_templates_config)

    template_dirs = jupyterlab_templates_config.get("template_dirs", [])
    if isinstance(template_dirs, str):
        template_dirs = template_dirs.split(",")

    if get_bool_config(jupyterlab_templates_config, "include_default"):
        template_dirs.insert(0, os.path.join(os.path.dirname(__file__), "templates"))

    base_url = web_app.settings["base_url"]

    host_pattern = ".*$"
    nb_server_app.log.info(
        "Installing jupyterlab_templates handler on path %s"
        % url_path_join(base_url, "templates")
    )

    if get_bool_config(jupyterlab_templates_config, "include_core_paths"):
        template_dirs.extend([os.path.join(x, "notebook_templates") for x in jupyter_core.paths.jupyter_path()])
    nb_server_app.log.info("Search paths:\n\t%s" % "\n\t".join(template_dirs))

    loader = TemplatesLoader(template_dirs, nb_server_app.log)
    nb_server_app.log.info(
        "Available templates:\n\t%s"
        % "\n\t".join(t for t in loader.get_templates()[1].keys())
    )

    web_app.add_handlers(
        host_pattern,
        [
            (
                url_path_join(base_url, "templates/names"),
                TemplateNamesHandler,
                {"loader": loader},
            )
        ],
    )
    web_app.add_handlers(
        host_pattern,
        [
            (
                url_path_join(base_url, "templates/get"),
                TemplatesHandler,
                {"loader": loader},
            )
        ],
    )
