"""Sphinx documentation configuration file."""

from datetime import datetime
import fnmatch
import hashlib
import os
import pathlib
import zipfile

from ansys_sphinx_theme import (
    ansys_favicon,
    ansys_logo_white,
    ansys_logo_white_cropped,
    get_version_match,
    latex,
    watermark,
)
from sphinx.builders.latex import LaTeXBuilder

from ansys.workbench.core import __version__

LaTeXBuilder.supported_image_types = ["image/png", "image/pdf", "image/svg+xml"]


# Project information
project = "ansys-workbench-core"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", default="workbench.docs.pyansys.com")
switcher_version = get_version_match(__version__)

# Select desired logo, theme, and declare the html title
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PyWorkbench"
html_static_path = ["_static"]

# specify the location of your github repo
html_context = {
    "github_user": "ansys",
    "github_repo": "pyworkbench",
    "github_version": "main",
    "doc_path": "doc/source",
    "pyansys_tags": ["Multiphysics", "Platform"],
}
html_theme_options = {
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": switcher_version,
    },
    "github_url": "https://github.com/ansys/pyworkbench",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "icon_links": [
        {
            "name": "Support",
            "url": "https://github.com/ansys/pyworkbench/discussions",
            "icon": "fa fa-comment fa-fw",
        },
    ],
    "ansys_sphinx_theme_autoapi": {
        "project": project,
    },
    "logo": "pyansys",
}

# Sphinx extensions
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "ansys_sphinx_theme.extension.autoapi",
    "numpydoc",
    "sphinx_design",
    "sphinx_jinja",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    # "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

html_favicon = ansys_favicon

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".mystnb": "jupyter_notebook",
    ".md": "markdown",
}

# The master toctree document.
master_doc = "index"

# Configuration for Sphinx autoapi
suppress_warnings = ["autoapi.python_import_resolution", "config.cache"]
exclude_patterns = [
    "**/ExampleData*",
    "**/LaunchWorkbench*",
    "**/ClientWrapper*",
]

# additional logos for the latex coverpage
latex_additional_files = [watermark, ansys_logo_white, ansys_logo_white_cropped]

# change the preamble of latex with customized title page
# variables are the title of pdf, watermark
latex_elements = {"preamble": latex.generate_preamble(html_title)}

# disable cheatsheet for now until the issue with doc build is fixed
BUILD_CHEATSHEET = True if os.environ.get("BUILD_CHEATSHEET", "true") == "true" else False

linkcheck_ignore = [
    "https://github.com/ansys/pyworkbench-examples",
    "https://github.com/ansys/pyworkbench/issues",
    "https://github.com/ansys/example-data/raw/master/pyworkbench",
    "https://workbench.docs.pyansys.com",
    "workbench.docs.pyansys.com",
    "https://www.ansys.com/*",
]

# -- Declare the Jinja context -----------------------------------------------
BUILD_API = True if os.environ.get("BUILD_API", "true") == "true" else False
if not BUILD_API:
    exclude_patterns.extend(["api.rst", "api/**"])

BUILD_EXAMPLES = True if os.environ.get("BUILD_EXAMPLES", "true") == "true" else False
if not BUILD_EXAMPLES:
    exclude_patterns.extend(["examples.rst", "examples/**"])

if BUILD_CHEATSHEET:
    html_theme_options["cheatsheet"] = {
        "file": "cheatsheet/cheatsheet.qmd",
        "title": "PyWorkbench cheat sheet",
    }

# -- Jinja context configuration ---------------------------------------------


def zip_directory(directory_path: pathlib.Path, zip_filename: pathlib.Path, ignore_patterns=None):
    """Compress a directory using the Zip app.

    Parameters
    ----------
    directory_path : ~pathlib.Path
        Directory to compress.
    zip_filename : ~pathlib.Path
        Path and file name for creating the ZIP file.
    ignore_patterns : list
        List of Unix-like patterns to ignore.

    """
    if ignore_patterns is None:
        ignore_patterns = []

    if not zip_filename.suffix == ".zip":
        zip_filename = zip_filename.with_suffix(".zip")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in directory_path.rglob("*"):
            if file_path.is_file():
                if any(
                    fnmatch.fnmatch(file_path.relative_to(directory_path), pattern)
                    for pattern in ignore_patterns
                ):
                    continue

                relative_path = file_path.relative_to(directory_path)
                zipf.write(file_path, relative_path)


def get_sha256_from_file(filepath: pathlib.Path):
    """Compute the SHA-256 hash for a file.

    Parameters
    ----------
    filepath : ~pathlib.Path
        Path to the file.

    Returns
    -------
    str
        String representing the SHA-256 hash.

    """
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as file:
        while chunk := file.read(8192):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def get_file_size_in_mb(file_path):
    """
    Compute the size of a file in megabytes.

    Parameters
    ----------
    file_path : str or Path
        Path to the file.

    Returns
    -------
    float
        Size of the file in megabytes.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    OSError
        If an OS-related error occurs while accessing the file.

    """
    path = pathlib.Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"The file at {file_path} does not exist.")

    file_size_bytes = path.stat().st_size
    return file_size_bytes / (1024 * 1024)


STATIC_PATH = pathlib.Path(__file__).parent / "_static"
ARTIFACTS_PATH = STATIC_PATH / "artifacts"
ARTIFACTS_WHEEL = ARTIFACTS_PATH / f"{project.replace('-', '_')}-{version}-py3-none-any.whl"
ARTIFACTS_SDIST = ARTIFACTS_PATH / f"{project.replace('-', '_')}-{version}.tar.gz"

jinja_globals = {
    "SUPPORTED_PYTHON_VERSIONS": ["3.11", "3.12", "3.13"],
    "SUPPORTED_PLATFORMS": ["windows", "ubuntu"],
}

jinja_contexts = {
    "install_guide": {
        "version": f"v{version}" if not version.endswith("dev0") else "main",
    },
    "main_toctree": {
        "build_api": BUILD_API,
        "build_examples": BUILD_EXAMPLES,
    },
    "artifacts": {
        "wheels": ARTIFACTS_WHEEL.name,
        "wheels_size": f"{get_file_size_in_mb(ARTIFACTS_WHEEL):.2f} MB",
        "wheels_hash": get_sha256_from_file(ARTIFACTS_WHEEL),
        "source": ARTIFACTS_SDIST.name,
        "source_size": f"{get_file_size_in_mb(ARTIFACTS_SDIST):.2f} MB",
        "source_hash": get_sha256_from_file(ARTIFACTS_SDIST),
    },
}
