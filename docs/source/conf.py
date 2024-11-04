# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import pathlib
import sys
import os

sys.path.insert(0, pathlib.Path(__file__).parents[1].resolve().as_posix())
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())
#sys.path.insert(0, pathlib.Path(__file__).parents[2].joinpath('code').resolve().as_posix())


project = 'CORESE-PYTHON'
copyright = '2024, WIMMICS'
author = 'WIMMICS'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration', # to display the duration of Sphinx processing
    'sphinx.ext.todo', # to include todo items in the documentation
    # Uncomment the following lines if/when include the python code (not used in this project yet)
    #'sphinx.ext.doctest', # to test code snippets in the documentation
    #'sphinx.ext.autodoc', # to automatically generate documentation from docstrings
    #'sphinx.ext.autosummary', # this extension generates function/method/attribute summary lists
    #'sphinx.ext.autosectionlabel', # to automatically generate section labels
    'sphinx_multiversion',
    'sphinx_design', # to render panels
    'myst_parser', # to parse markdown
    'sphinxcontrib.mermaid', # to render mermaid diagrams
    # Alternative ways to include markdown files, cannot be used together with myst_parser
    # advantages of sphynx_mdinclude/m2r3: it can include partial markdown files
    #
    #'sphinx_mdinclude', # to include partial markdown files
    #'m2r3', # to include markdown files
    'sphinx_copybutton', # to add copy buttons to code blocks
    ]

templates_path = ['_templates']
exclude_patterns = []

# The suffix(es) of source filenames.
source_suffix = ['.rst', '.md']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

html_css_files = [
    "css/custom.css",
]
html_js_files = []

# Project logo, to place at the top of the sidebar.
html_logo = "_static/corese.svg"

# Icon to put in the browser tab.
html_favicon = "_static/Corese-square-logo-transparent.svg"

# Modify the title to get good social-media links
html_title = "CORESE-PYTHON"
html_short_title = "CORESE-PYTHON"

# -- Theme Options -----------------------------------------------------------
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
     "logo": {
         "image_relative": "_static/corese.svg",
         "image_light": "_static/corese.svg",
         "image_dark": "_static/corese.svg"
     },
    "navbar_center": [ "navbar-nav" ],
    "navbar_end": ["navbar-icon-links", "version-switcher"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/corese-stack/corese-python",
            "icon": "fab fa-github-square"
        }
    ],
    "switcher": {"json_url": "https://corese-stack.github.io/corese-python/switcher.json", "version_match": r"v\d+\.\d+\.\d+"}
}

html_sidebars = {
  "install": [],
}

# -- MySt-parcer extension Options -------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/

myst_heading_anchors = 4
myst_fence_as_directive = ["mermaid"]

# Tell sphinx what the primary language being documented is.
primary_domain = 'python'

# Tell sphinx what the pygments highlight language should be.
highlight_language = 'python'

# Setup the sphinx.ext.todo extension

# Set to false in the final version
todo_include_todos = True

# Optional: Exclude certain branches or tags from multi-versioning
#smv_branch_whitelist = r'develop'  # TODO Build documentation only for feature/retrieve-doc, must be replaced with "main" for production
smv_tag_whitelist = r'^v\d+\.\d+.*$'  # Only build tags that match version pattern like v1.0
