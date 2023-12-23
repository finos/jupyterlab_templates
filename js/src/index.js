/******************************************************************************
 *
 * Copyright (c) 2020, the jupyterlab_templates authors.
 *
 * This file is part of the jupyterlab_templates library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
import {IFileBrowserFactory} from "@jupyterlab/filebrowser";
import {ILauncher} from "@jupyterlab/launcher";
import {IMainMenu} from "@jupyterlab/mainmenu";
import {activate} from "./activate";

import "../style/index.css";

const extension = {
  activate,
  autoStart: true,
  id: "jupyterlab_templates",
  optional: [ILauncher],
  requires: [IMainMenu, IFileBrowserFactory],
};

export default extension;
export {activate as _activate};
