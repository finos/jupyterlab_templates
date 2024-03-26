/******************************************************************************
 *
 * Copyright (c) 2021, the jupyterlab_templates authors.
 *
 * This file is part of the jupyterlab_templates library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
const esModules = [
  "@finos",
  "@jupyter",
  "@jupyterlab",
  "@jupyter-widgets",
  "@microsoft",
  "@rjsf",
  "delaunator",
  "exenv-es6",
  "internmap",
  "lib0",
  "lodash-es",
  "nanoid",
  "robust-predicates",
  "y-protocols",
].join("|");

module.exports = {
  moduleDirectories: ["node_modules", "src", "tests"],
  moduleNameMapper: {
    "\\.(css|less|sass|scss)$": "<rootDir>/tests/styleMock.js",
    "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$": "<rootDir>/tests/fileMock.js",
  },
  reporters: [ "default", "jest-junit" ],
  setupFiles: ["<rootDir>/tests/setup.js"],
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.jsx?$": "babel-jest",
    ".+\\.(css|styl|less|sass|scss)$": "jest-transform-css",
  },
  transformIgnorePatterns: [`/node_modules/(?!(${esModules}))`],
};
