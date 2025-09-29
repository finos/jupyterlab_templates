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
import jupyter_core.paths
import tornado.web

from io import open
from fnmatch import fnmatch
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join

TEMPLATES_IGNORE_FILE = ".jupyterlab_templates_ignore"


class TemplatesLoader:
    def __init__(self, template_dirs, allowed_extensions=None, template_label=None):
        self.template_dirs = template_dirs
        self.template_label = template_label or "Template"
        self.allowed_extensions = allowed_extensions or ["*.ipynb"]

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

                if TEMPLATES_IGNORE_FILE in filenames:
                    # skip this very directory (subdirectories will still be considered)
                    continue

                _files = [x for x in filenames if any(fnmatch(x, y) for y in self.allowed_extensions)]
                for filename in _files:
                    if ".ipynb_checkpoints" not in dirname:
                        files.append(
                            (
                                os.path.join(dirname, filename),
                                dirname.replace(path, ""),
                                filename,
                            )
                        )
            # pull contents and push into templates list
            for f, dirname, filename in sorted(files):
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


class TemplatesHandler(JupyterHandler):
    def initialize(self, loader):
        self.loader = loader

    @tornado.web.authenticated
    def get(self):
        temp = self.get_argument("template", "")
        if temp:
            self.finish(self.loader.get_templates()[1][temp])
        self.set_status(404)


class TemplateNamesHandler(JupyterHandler):
    def initialize(self, loader):
        self.loader = loader

    @tornado.web.authenticated
    def get(self):
        templates, _ = self.loader.get_templates()
        response = {"templates": templates, "template_label": self.loader.template_label}
        self.finish(json.dumps(response))


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    template_dirs = nb_server_app.config.get("JupyterLabTemplates", {}).get("template_dirs", [])

    allowed_extensions = nb_server_app.config.get("JupyterLabTemplates", {}).get("allowed_extensions", ["*.ipynb"])

    if nb_server_app.config.get("JupyterLabTemplates", {}).get("include_default", True):
        template_dirs.insert(0, os.path.join(os.path.dirname(__file__), "templates"))

    base_url = web_app.settings["base_url"]

    host_pattern = ".*$"
    nb_server_app.log.info("Installing jupyterlab_templates handler on path %s" % url_path_join(base_url, "templates"))

    if nb_server_app.config.get("JupyterLabTemplates", {}).get("include_core_paths", True):
        template_dirs.extend([os.path.join(x, "notebook_templates") for x in jupyter_core.paths.jupyter_path()])
    nb_server_app.log.info("Search paths:\n\t%s" % "\n\t".join(template_dirs))

    template_label = nb_server_app.config.get("JupyterLabTemplates", {}).get("template_label", "Template")
    nb_server_app.log.info("Template label: %s" % template_label)

    loader = TemplatesLoader(template_dirs, allowed_extensions=allowed_extensions, template_label=template_label)
    nb_server_app.log.info("Available templates:\n\t%s" % "\n\t".join(t for t in loader.get_templates()[1].keys()))

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
