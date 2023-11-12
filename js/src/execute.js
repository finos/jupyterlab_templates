/******************************************************************************
 *
 * Copyright (c) 2020, the jupyterlab_templates authors.
 *
 * This file is part of the jupyterlab_templates library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
import {Dialog, showDialog} from "@jupyterlab/apputils";
import {PageConfig} from "@jupyterlab/coreutils";
import {request} from "requests-helper";
import {OpenTemplateWidget} from "./widget";

export const execute = (templates, app, browser) => {
  const gobutton = Dialog.okButton({label: "GO"});
  showDialog({
    body: new OpenTemplateWidget(templates, gobutton),
    buttons: [Dialog.cancelButton(), gobutton],
    focusNodeSelector: "input",
    title: "Template",
  }).then((result) => {
    if (result.button.label === "Cancel") {
      return;
    }
    if (result.value) {
      request("get", `${PageConfig.getBaseUrl()}templates/get`, {
        template: result.value,
      }).then((res2) => {
        const data = res2.json();
        const {path} = browser.tracker.currentWidget.model;

        return new Promise((resolve) => {
          const ext = data.filename.split(".").pop().toLowerCase();
          const isNotebook = ext === "ipynb";
          app.commands
            .execute("docmanager:new-untitled", {
              ext,
              path,
              type: isNotebook ? "notebook" : "file",
            })
            .then((model) => {
              app.commands
                .execute("docmanager:open", {
                  factory: isNotebook ? "Notebook" : null,
                  path: model.path,
                })
                .then((widget) => {
                  // eslint-disable-next-line no-param-reassign
                  widget.isUntitled = true;
                  widget.context.ready.then(() => {
                    if (isNotebook) {
                      widget.model.fromString(data.content);
                    } else {
                      widget.content.editor._editor.setValue(data.content);
                    }
                    resolve(widget);
                  });
                });
            });
        });
      });
    }
  });
};
