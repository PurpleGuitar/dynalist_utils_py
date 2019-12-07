#!/usr/bin/env python3

"""
Convert a Dynalist doc to a Markdown file.
"""

# Python
import argparse
import os
import sys

# Project
import app_utils
import dynalist
import markdown


def main():
    """ Check args and download doc """
    try:
        args = get_arguments()
        token = app_utils.get_token(args, os.environ)
        url = app_utils.get_url(args, os.environ)
        parsed_url = dynalist.parse_url(url)
        zoom_node_id = parsed_url["zoom_node_id"] if parsed_url["zoom_node_id"] else "root"
        doc = dynalist.Document.from_url(url, token)
        args.outfile.write(markdown.convert(doc, zoom_node_id))
    except Exception as exception: # pylint: disable=broad-except
        app_utils.eprint(exception)
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Convert a Dynalist doc to a Markdown file.")
    app_utils.add_argument_url(parser)
    app_utils.add_argument_token(parser)
    app_utils.add_argument_outfile(parser)
    return parser.parse_args()


if __name__ == "__main__":
    main()

# vim: foldmethod=indent
