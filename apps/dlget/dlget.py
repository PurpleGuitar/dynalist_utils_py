#!/usr/bin/env python3

"""
Download a Dynalist document to a JSON file.
"""

# Python
import argparse
import os
import logging
import sys

# Project
from dynalist_utils import app_utils
from dynalist_utils import dynalist


def main():
    """ Check args and download doc """
    try:
        args = get_arguments()
        token = app_utils.get_token(args, os.environ)
        url = app_utils.get_url(args, os.environ)
        doc = dynalist.Document.from_url(url, token)
        args.outfile.write(doc.to_json())
    except Exception: # pylint: disable=broad-except
        logging.exception("An error occured.")
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Download a Dynalist document to a JSON file.")
    app_utils.add_argument_url(parser)
    app_utils.add_argument_token(parser)
    app_utils.add_argument_outfile(parser)
    return parser.parse_args()


if __name__ == "__main__":
    main()

# vim: foldmethod=indent
