# *****************************************************************************
#
# Copyright (c) 2020, the jupyterlab_templates authors.
#
# This file is part of the jupyterlab_templates library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
import fnmatch
import json
import jupyter_core.paths
import os
import os.path
import platform
import tornado.web
from io import open
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join


class TemplatesLoader:
    def __init__(self, template_dirs):
        self.template_dirs = template_dirs

    @staticmethod
    def get_user_templates_dir():
        """Get the user templates directory."""
        detected_os = platform.system()

        if detected_os == "Linux":
            return os.path.join(os.path.expanduser("~"), "Templates")
        if detected_os == "Darwin":  # MacOS
            return os.path.join(os.path.expanduser("~"), "Library", "User Template")
        if detected_os == "Windows":
            return os.path.join(os.path.expandvars("%USERPROFILE%"), "Templates")

        raise OSError("Unsupported operating system: %s" % detected_os)

    @staticmethod
    def get_templates_from_dir(path):
        """Get all templates from a directory and its subdirectories.

        Returns:
            template_paths list[{"name" : path}]: List of dictionarys with a single entry
                "name", which returns the relative path to the template.
            templates_data dict[relative_path, dict]: dictionary of dictionaries
                with the relative path as key that holds the template data.
        """
        template_paths = []
        templates_data = {}

        # in order to produce correct filenames, abspath should point to the parent directory of path
        abspath = os.path.abspath(os.path.join(os.path.realpath(path), os.pardir))
        files = []
        # get all files in subdirectories
        for dirname, _, filenames in os.walk(path, followlinks=True):
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
            template_paths.append({"name": data["name"]})
            templates_data[data["name"]] = data
        return template_paths, templates_data

    def get_templates(self):
        templates = {}
        template_by_path = {}
        # add user templates dir
        user_templates_dir = self.get_user_templates_dir()
        if os.path.isdir(user_templates_dir):
            template_paths, templates_data = self.get_templates_from_dir(
                user_templates_dir
            )
            if template_paths:
                templates[user_templates_dir] = template_paths
                template_by_path.update(templates_data)

        # add builtin templates
        for template_folder in self.template_dirs:
            if not os.path.isdir(template_folder):
                continue

            folder_name = os.path.basename(template_folder)
            for item in os.listdir(template_folder):
                path = os.path.join(template_folder, item)
                if os.path.isdir(path):
                    template_paths, templates_data = self.get_templates_from_dir(path)
                    if template_paths:
                        name = os.path.join(folder_name, item)
                        templates[name] = template_paths
                        template_by_path.update(templates_data)

        return templates, template_by_path


class TemplatesHandler(JupyterHandler):
    def initialize(self, loader):
        self.loader = loader

    @tornado.web.authenticated
    def get(self):
        temp = self.get_argument("template", "")
        if temp:
            self.finish(self.loader.get_templates()[1][temp])
        else:
            self.set_status(404)


class TemplateNamesHandler(JupyterHandler):
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
    nb_server_app.log.info(
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
    nb_server_app.log.info("Search paths:\n\t%s" % "\n\t".join(template_dirs))

    loader = TemplatesLoader(template_dirs)
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
