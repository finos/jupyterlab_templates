from codecs import open
from os import path

from jupyter_packaging import (
    combine_commands,
    create_cmdclass,
    ensure_python,
    ensure_targets,
    get_version,
    install_npm,
)
from setuptools import find_packages, setup

pjoin = path.join

ensure_python(("2.7", ">=3.6"))

name = "jupyterlab_templates"
here = path.abspath(path.dirname(__file__))
jshere = path.abspath(path.join(path.dirname(__file__), "js"))
version = get_version(pjoin(here, name, "_version.py"))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read().replace("\r\n", "\n")

requires = ["jupyterlab>=3.0.0"]

dev_requires = requires + [
    "black>=20.",
    "bump2version>=1.0.0",
    "flake8>=3.7.8",
    "flake8-black>=0.2.1",
    "mock",
    "pytest",
    "pytest-cov>=2.6.1",
    "Sphinx>=1.8.4",
    "sphinx-markdown-builder>=0.5.2",
]

data_spec = [
    # Lab extension installed by default:
    ("share/jupyter/lab/extensions", "lab-dist", "jupyterlab_templates-*.tgz"),
    # Config to enable server extension by default:
    ("etc/jupyter", "jupyter-config", "**/*.json"),
]


cmdclass = create_cmdclass("js", data_files_spec=data_spec)
cmdclass["js"] = combine_commands(
    install_npm(jshere, build_cmd="build:all"),
    ensure_targets(
        [pjoin(jshere, "lib", "index.js"), pjoin(jshere, "style", "index.css")]
    ),
)


setup(
    name=name,
    version=version,
    description="Notebook templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timkpaine/jupyterlab_templates",
    author="the jupyterlab_templates authors",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
    cmdclass=cmdclass,
    keywords="jupyter jupyterlab",
    packages=find_packages(
        exclude=[
            "tests",
        ]
    ),
    install_requires=requires,
    extras_require={"dev": dev_requires},
    include_package_data=True,
    zip_safe=False,
)
