# Contributing

Thank you for your interest in contributing to `jupyterlab_templates`!

`jupyterlab_templates` is built on open source and hosted by the Fintech Open Source Foundation (FINOS). We invite you to participate in our community by adding and commenting on [issues](https://github.com/finos/jupyterlab_templates/issues) (e.g., bug reports; new feature suggestions) or contributing code enhancements through a pull request.

Note that commits and pull requests to FINOS repositories such as `jupyterlab_templates` may only be accepted from those contributors with a [Contributor License Agreement (CLA)](https://community.finos.org/docs/governance/Software-Projects/contribution-compliance-requirements) with FINOS. This may take the form of either:
* an active, executed Individual Contributor License Agreement (ICLA) with FINOS, OR
* coverage under an existing, active Corporate Contribution License Agreement (CCLA) executed with FINOS (most likely by the developer's employer). Please note that some, though not all, CCLAs require individuals/employees to be explicitly named on the CCLA.

Commits from individuals not covered under an CLA can not be merged by `jupyterlab_templates`'s committers. We encourage you to check that you have a CLA in place well in advance of making your first pull request.

Need an ICLA? Unsure if you are covered under an existing CCLA? Confused? Email [help@finos.org](mailto:help@finos.org) and the foundation team will help get it sorted out for you.

If you have any general questions about contributing to `jupyterlab_templates`, please feel free to open an issue on [github](https://github.com/finos/jupyterlab_templates/issues/new), or email [help@finos.org](mailto:finos.org).

## Reporting bugs, feature requests, etc.

To report bugs, request new features or similar, please open an issue on the Github
repository.

A good bug report includes:

- Expected behavior
- Actual behavior
- Steps to reproduce (preferably as minimal as possible)
- Possibly any output from the browser console (typically available via Ctrl + Shift + J or via F12).

## Minor changes, typos etc.

Minor changes can be contributed by navigating to the relevant files on the Github repository,
and clicking the "edit file" icon. By following the instructions on the page you should be able to
create a pull-request proposing your changes. A repository maintainer will then review your changes,
and either merge them, propose some modifications to your changes, or reject them (with a reason for
the rejection).

## Setting up a development environment

If you want to help resolve an issue by making some changes that are larger than that covered by the above paragraph, it is recommended that you:

- Fork the repository on Github
- Clone your fork to your computer
- Run the following commands inside the cloned repository:
  - `pip install -e .[dev]` - This will install the Python package in development
    mode.
  - `jupyter labextension install .` - This will add the lab extension development
    mode.
- Validate the install by running the tests:
  - `py.test` - This command will run the Python tests.
  - `yarn test` - This command will run the JS tests.

Once you have such a development setup, you should:

- Make the changes you consider necessary
- Run the tests to ensure that your changes does not break anything
- If you add new code, preferably write one or more tests for checking that your code works as expected.
- Commit your changes and publish the branch to your github repo.
- Open a pull-request (PR) back to the main repo on Github.

## Project Governance
See [GOVERNANCE.md](./GOVERNANCE.md)
