/******************************************************************************
 *
 * Copyright (c) 2020, the jupyterlab_templates authors.
 *
 * This file is part of the jupyterlab_templates library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
import {Widget} from "@lumino/widgets";
import "@tree-finder/base/dist/tree-finder.css";
import "@tree-finder/base/style/theme/material.css";

function templatesToRoot(templates) {
  // Build a nested tree structure from the flat templates dict
  // templates is { dirName: [{name: "/dir/file.ipynb"}, ...], ... }
  const tree = {dirs: {}, files: []};

  Object.entries(templates).forEach(([dirName, fileEntries]) => {
    const parts = dirName.split("/").filter((p) => p);
    let node = tree;
    parts.forEach((part) => {
      if (!node.dirs[part]) {
        node.dirs[part] = {dirs: {}, files: []};
      }
      node = node.dirs[part];
    });
    node.files.push(...fileEntries);
  });

  // Convert tree node to IContentRow format for tree-finder
  function toContentRow(node, pathSegments) {
    return {
      kind: "dir",
      path: pathSegments,
      getChildren: async () => {
        const dirs = Object.entries(node.dirs).map(([name, subNode]) => toContentRow(subNode, [...pathSegments, name]));

        const files = node.files.map((file) => ({
          kind: "text",
          path: [...pathSegments, file.name.split("/").pop()],
        }));

        return [...dirs, ...files];
      },
    };
  }

  return toContentRow(tree, []);
}

export class OpenTemplateWidget extends Widget {
  constructor(templates) {
    const body = document.createElement("div");
    body.classList.add("jp-Template-Browser");
    super({node: body});
    // Handle both {templates: {...}, template_label: ...} and direct dict formats
    this.templates = templates.templates || templates;
  }

  onAfterAttach(msg) {
    super.onAfterAttach(msg);
    this.setButtonDisabled();
    this.treeFinder = document.createElement("tree-finder-panel");
    this.treeFinder.classList.add("jp-Template-Browser");
    this.node.appendChild(this.treeFinder);
    this.init();
  }

  getButton = () => this.node.parentNode.querySelectorAll("button")[1];

  setButtonDisabled = () => {
    const button = this.getButton();
    button.style.display = "none";
  };

  setButtonEnabled = () => {
    const button = this.getButton();
    button.style.display = "";
  };

  updateButtonState = () => {
    const selected = this.treeFinder.model?.selectedLast;
    if (selected && selected.row.kind !== "dir") {
      this.setButtonEnabled();
    } else {
      this.setButtonDisabled();
    }
  };

  init = async () => {
    const root = templatesToRoot(this.templates);
    await this.treeFinder.init({
      root,
      gridOptions: {
        doWindowResize: true,
        showFilter: true,
      },
    });

    // Monitor clicks to update button state based on selection
    this.treeFinder.addEventListener("click", () => {
      setTimeout(() => this.updateButtonState(), 0);
    });
  };

  getValue = () => {
    const selected = this.treeFinder.model?.selectedLast;
    if (selected && selected.row.kind !== "dir") {
      // Reconstruct the template name from path (e.g. "/dirname/filename.ipynb")
      return `/${selected.row.path.join("/")}`;
    }
    return null;
  };
}
