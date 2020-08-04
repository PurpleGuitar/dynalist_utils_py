#!/usr/bin/env python3

"""
Convert a Dynalist doc to a Markdown file.
"""

# Python
import argparse
import logging
import sys

# Project
from dynalist_utils import app_utils
from dynalist_utils import markdown


def main():
    """ Check args and download doc """
    try:
        args = get_arguments()
        doc = app_utils.read_doc(args)
        zoom_node_id = doc.get_metadata()["zoom_node_id"]
        if not zoom_node_id:
            zoom_node_id = "root"
        args.outfile.write(markdown.convert(doc, zoom_node_id))
    except Exception: # pylint: disable=broad-except
        logging.exception("An error occured.")
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Convert a Dynalist doc to a Markdown file.")
    app_utils.add_argument_url(parser)
    app_utils.add_argument_infile(parser)
    app_utils.add_argument_token(parser)
    app_utils.add_argument_outfile(parser)
    app_utils.add_argument_cached(parser)
    return parser.parse_args()


if __name__ == "__main__":
    main()

# vim: foldmethod=indent
