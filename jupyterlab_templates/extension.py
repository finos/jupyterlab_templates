# *****************************************************************************
#
# Copyright (c) 2020, the jupyterlab_templates authors.
#
# This file is part of the jupyterlab_templates library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
import fnmatch
import json
import os
import os.path
import jupyter_core.paths
import tornado.web

from io import open
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join


class TemplatesLoader:
    def __init__(self, template_dirs):
        self.template_dirs = template_dirs

    def get_templates(self):
        templates = {}
        template_by_path = {}

        for path in self.template_dirs:
            # in order to produce correct filenames, abspath should point to the parent directory of path
            abspath = os.path.abspath(os.path.join(os.path.realpath(path), os.pardir))
            files = []
            # get all files in subdirectories
            for dirname, _, filenames in os.walk(path, followlinks=True):
                if dirname == path:
                    # Skip top level
                    continue

                for filename in fnmatch.filter(filenames, "*.ipynb"):
                    if ".ipynb_checkpoints" not in dirname:
                        files.append(
                            (
                                os.path.join(dirname, filename),
                                dirname.replace(path, ""),
                                filename,
                            )
                        )
            # pull contents and push into templates list
            for f, dirname, filename in files:
                # skips over faild attempts to read content
                try:
                    with open(os.path.join(abspath, f), "r", encoding="utf8") as fp:
                        content = fp.read()
                except (FileNotFoundError, PermissionError):
                    # Can't read file, skip
                    continue

                data = {
                    "path": f,
                    "name": os.path.join(dirname, filename),
                    "dirname": dirname,
                    "filename": filename,
                    "content": content,
                }

                # remove leading slash for select
                if dirname.strip(os.path.sep) not in templates:
                    templates[dirname.strip(os.path.sep)] = []

                # don't include content unless necessary
                templates[dirname.strip(os.path.sep)].append({"name": data["name"]})

                # full data
                template_by_path[data["name"]] = data

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


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    template_dirs = nb_server_app.config.get("JupyterLabTemplates", {}).get(
        "template_dirs", []
    )

    if nb_server_app.config.get("JupyterLabTemplates", {}).get("include_default", True):
        template_dirs.insert(0, os.path.join(os.path.dirname(__file__), "templates"))

    base_url = web_app.settings["base_url"]

    host_pattern = ".*$"
    print(
        "Installing jupyterlab_templates handler on path %s"
        % url_path_join(base_url, "templates")
    )

    if nb_server_app.config.get("JupyterLabTemplates", {}).get(
        "include_core_paths", True
    ):
        template_dirs.extend(
            [
                os.path.join(x, "notebook_templates")
                for x in jupyter_core.paths.jupyter_path()
            ]
        )
    print("Search paths:\n\t%s" % "\n\t".join(template_dirs))

    loader = TemplatesLoader(template_dirs)
    print(
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
