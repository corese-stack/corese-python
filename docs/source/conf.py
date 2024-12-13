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
import shutil

# -- Path to the Python source code ------------------------------------------------
sys.path.insert(0, pathlib.Path(__file__).parents[2].joinpath('src').resolve().as_posix())

# -- Copy files for docs --------------------------------------------------
#
# To avoid duplicating the information and symlinks
shutil.copyfile(pathlib.Path(__file__).parents[2].joinpath('INSTALL.md'), "dev_install.md")
shutil.copyfile(pathlib.Path(__file__).parents[2].joinpath('examples/example1.ipynb'), "user_guide.ipynb")

# -- Project information -----------------------------------------------------
project = 'corese-python'
copyright = '2024, WIMMICS'
author = 'Corese Team'

# The suffix(es) of source filenames.
source_suffix = ['.rst', '.md']
#exclude_patterns = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Add any paths that contain data files here, relative to this directory.
html_static_path = ['_static']

# Define the css files to include in the documentation
html_css_files = [
    "css/custom.css",
]

# Define the js files to include in the documentation
html_js_files = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_sidebars = {
  #"corese": [], # syntax for hiding the sidebar
}

# Tell sphinx what the pygments highlight language should be.
highlight_language = 'python'

# Project logo, to place at the top of the sidebar.
html_logo = "_static/corese.svg"

# Icon to put in the browser tab.
html_favicon = "_static/Corese-square-logo-transparent.svg"

# Modify the title to get good social-media links
#html_title = "CORESE-PYTHON"
#html_short_title = "CORESE-PYTHON"

# -- Theme Options -----------------------------------------------------------
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation. https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'pydata_sphinx_theme'
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


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx.ext.duration', # to display the duration of Sphinx processing
    'sphinx.ext.todo', # to include todo items in the documentation
    #'sphinx.ext.githubpages', # to deploy the documentation on GitHub pages ???
    'sphinx.ext.viewcode', # to add links to the source code
    'sphinx.ext.doctest', # to test code snippets in the documentation
    'sphinx.ext.autodoc', # to automatically generate documentation from docstrings
    'sphinx.ext.autosummary', # this extension generates function/method/attribute summary lists
    'sphinx.ext.autosectionlabel', # to automatically generate section labels
    'sphinx.ext.napoleon', # to parse Google-style docstrings
    'sphinx_design', # to render panels
    #'myst_parser', # to parse markdown
    "myst_nb", # to parse jupyter notebooks and markdown files
    #'sphinxcontrib.mermaid', # to render mermaid diagrams
    # Alternative ways to include markdown files, cannot be used together with myst_parser
    # advantages of sphynx_mdinclude/m2r3: it can include partial markdown files
    #
    #'sphinx_mdinclude', # to include partial markdown files
    #'m2r3', # to include markdown files
    'sphinx_copybutton', # to add copy buttons to code blocks
    'sphinx_multiversion', # to build documentation for multiple versions
    ]

# -- Options for sphinx.ext.autodoc / sphinx.ext.autosummary-----------------------------
# generate autosummary even if no references
#autodoc_default_flags = ["members", "inherited-members"]
autosummary_generate = True

autodoc_default_options = {
    #"member-order": "bysource",
    #"special-members": "__init__",
    # "undoc-members": True,
    # "show-inheritance": True,
    # "template": "_templates/base.rst",  # Path to your template
}

# -- Options for sphinx.ext.napoleon----------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_use_admonition_for_notes = True
napoleon_use_rtype = False

# -- Setup the sphinx.ext.todo extension ------------------------------------
# TODO: Set to false in the final version
todo_include_todos = True

# -- sphinx-multiversion extension configuration -----------------------------------
# Optional: Exclude certain branches or tags from multi-versioning
#smv_branch_whitelist = r'develop'  # TODO Build documentation only for feature/retrieve-doc, must be replaced with "main" for production
smv_tag_whitelist = r'^v\d+\.\d+.*$'  # Only build tags that match version pattern like v1.0

# -- MyST-NB configuration ---------------------------------------------------
# https://myst-nb.readthedocs.io/en/latest/
# Take the example notebook as-is, without executing it
nb_execution_mode = "off"

# Suppress warnings
suppress_warnings = [
    "myst.xref_missing",  # Suppress warnings about missing references after fixing the one you can fix
    "mystnb.unknown_mime_type"  # Suppress warnings about Google Colab button in the notebook
]

# Substitute the relative path in the markdown file for the GitHub repo root URL
def preprocess_markdown(app, docname, source):
    base_url = "https://github.com/corese-stack/corese-python/blob/main/"
    if docname == "dev_install":  # Replace with the actual document using the Markdown file
        content = source[0]
        # Replace relative paths with appropriate links
        source[0] = content.replace("./" ,  base_url)

def setup(app):
    app.connect("source-read", preprocess_markdown)