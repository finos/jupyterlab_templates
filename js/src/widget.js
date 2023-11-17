/******************************************************************************
 *
 * Copyright (c) 2020, the jupyterlab_templates authors.
 *
 * This file is part of the jupyterlab_templates library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
import {Widget} from "@lumino/widgets";
import {IContentRow, Path} from "@tree-finder/base";
import "@tree-finder/base/dist/tree-finder.css";
import "@tree-finder/base/style/theme/material.css";

export function bool() {
  return Math.random() < 0.5;
}

// randomize array in-place using Durstenfeld shuffle algorithm
// ref: https://stackoverflow.com/a/12646864
export function shuffle(arr, inPlace = false) {
  arr = inPlace ? arr : [...arr];

  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }

  return arr;
}
export const ALLIED_PHONETIC = [
  "able",
  "baker",
  "charlie",
  "dog",
  "easy",
  "fox",
  "george",
  "how",
  "item",
  "jig",
  "king",
  "love",
  "mike",
  "nan",
  "oboe",
  "peter",
  "queen",
  "roger",
  "sugar",
  "tare",
  "uncle",
  "victor",
  "william",
  "xray",
  "yoke",
  "zebra",
];

const _mockCache = {};
let mockFileIx = 0;
let modDaysIx = -1;

function mockContent(props) {
  // infinite recursive mock contents
  const {path, kind, modDays = modDaysIx++, nchildren = 100, ndirectories = 10, randomize = false} = props;
  const modified = new Date(modDays * 24 * 60 * 60 * 1000);
  const writable = randomize && bool();

  if (kind === "dir") {
    // is a dir
    return {
      kind,
      path,
      modified,
      writable,
      getChildren: async () => {
        const pathstr = path.join("/");

        if (pathstr in _mockCache) {
          return _mockCache[pathstr];
        }

        const children = [];
        const dirNames = randomize ? shuffle(ALLIED_PHONETIC) : ALLIED_PHONETIC;

        for (let i = 0; i < nchildren; i++) {
          children.push(
            mockContent({
              kind: i < ndirectories ? "dir" : "text",
              path: [...path, i < ndirectories ? `${dirNames[i]}` : `file_${`${mockFileIx++}`.padStart(7, "0")}.txt`],
              nchildren,
              ndirectories,
              randomize,
            }),
          );
        }

        _mockCache[pathstr] = children;
        return children;
      },
    };
  }
  // is a file
  return {
    kind,
    path,
    modified,
    writable,
  };
}

const root = mockContent({
  kind: "dir",
  path: [],
  randomize: true,
});

export class OpenTemplateWidget extends Widget {
  constructor(templates) {
    const body = document.createElement("div");
    body.classList.add("jp-Template-Browser");

    const label = document.createElement("label");
    label.textContent = "Template:";

    // const package_input = document.createElement("select");
    // const notebook_input = document.createElement("select");

    // Object.keys(templates).forEach((package_name) => {
    //   const package_option = document.createElement("option");
    //   package_option.label = package_name;
    //   package_option.text = package_name;
    //   package_option.value = package_name;
    //   package_input.appendChild(package_option);
    // });

    // const fill = (package_name) => {
    //   while (notebook_input.lastChild) {
    //     notebook_input.removeChild(notebook_input.lastChild);
    //   }

    //   templates[package_name].forEach((notebook) => {
    //     const notebook_option = document.createElement("option");
    //     notebook_option.label = notebook.name;
    //     notebook_option.text = notebook.name;
    //     notebook_option.value = notebook.name;
    //     notebook_input.appendChild(notebook_option);
    //   });
    // };

    // package_input.addEventListener("change", (event) => {
    //   const package_name = event.target.value;
    //   fill(package_name);
    // });

    // if (Object.keys(templates).length > 0) {
    //   fill(Object.keys(templates)[0]);
    // }

    // body.appendChild(label);
    // body.appendChild(package_input);
    // body.appendChild(notebook_input);
    super({node: body});
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

  init = async () => {
    await this.treeFinder.init({
      root,
      gridOptions: {
        doWindowResize: true,
        showFilter: true,
      },
    });
  };

  getValue = () => this.node.getElementsByTagName("select")[1].value;
}
