Dynalist Utils
==============

A collection of Python libraries and command-line utilities for working
with Dynalist documents.

[Dynalist](https://dynalist.io/) is a web-based outliner that has a
variety of powerful features, including folding, linking, hoisting,
image support, and Markdown support. It also has an API allowing for
programmatic access, which these tools use.

Using the tools requires your Dynalist developer API token, which you
can get from the [Dynalist developer
page](https://dynalist.io/developer).

Scripts
=======

This repo provides Python libraries for working with Dynalist documents
as well as a few scripts for performing common actions. Please note that
the libraries and scripts **only provide read access** to the Dynalist
API for now -- they cannot be used to make changes to your online
documents.

These scripts are:

dl2md.py
--------

Converts a node of a Dynalist document to a Markdown file, converting
nodes to headers or bullet lists depending on their current folding
state. Also includes a Bash shell script for downloading the Dynalist
URL on the clipboard and automatically converting it to Markdown and
PDF.

dllint.py
---------

Checks a Dynalist document for problems, such as internal links that no
longer point to valid nodes.

dlget.py
--------

Downloads the JSON for a given Dynalist document.

Installation
============

These instructions are for Linux or WSL.

-   Install python3, e.g. `sudo apt install python3`
-   Clone this repo.
-   Use pip3 to install the Python libraries in requirements.txt, for
    example: `pip3 install -r requirements.txt`.
-   Optional: In your bashrc, set the `DYNALIST_TOKEN` environment
    variable to your Dynalist API key. The scripts will detect this and
    use it to talk to the Dynalist API. If you prefer not to do this,
    you can specify a `--token` parameter at the command line of most of
    the tools.
