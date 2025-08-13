import os
import sys
import django

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('..'))  # Path to myStore root folder
os.environ['DJANGO_SETTINGS_MODULE'] = 'myStore.settings'
django.setup()

# -- Project information -----------------------------------------------------
project = 'MyStore'
author = 'Lerato Malebyoe'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',   # Pulls in docstrings
    'sphinx.ext.viewcode',  # Links to highlighted source code
    'sphinx.ext.napoleon',  # Supports Google & NumPy docstring styles
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

# Master document
master_doc = 'index'
