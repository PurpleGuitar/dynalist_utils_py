#!/usr/bin/env python3

"""
Simple linter for Dynalist docs.
"""

# Python
import argparse
import collections
import enum
import logging
import sys

# Project
from dynalist_utils import app_utils
from dynalist_utils import dynalist
from dynalist_utils import markdown

class Level(enum.Enum):
    """ Enumerates message levels """
    DEBUG = enum.auto()
    INFO = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()

Message = collections.namedtuple(
    "Message",
    ["level", "summary", "details"])

def main():
    """ Check args and download doc """
    try:
        args = get_arguments()
        logging.basicConfig(format=app_utils.LOGGING_FORMAT,
                            level=logging.DEBUG if args.trace else logging.WARNING)
        doc = app_utils.read_doc(args)
        check_bad_internal_links(doc)
    except Exception: # pylint: disable=broad-except
        logging.exception("An error occured.")
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Run some checks on a Dynalist document")
    app_utils.add_standard_arguments(parser)
    return parser.parse_args()

def check_bad_internal_links(doc):
    """ Check for internal links that don't point to a valid node. """
    for node in doc.get_nodes():
        links = markdown.find_links(node["content"])
        if "note" in node:
            links.extend(markdown.find_links(node["note"]))
        for link in links:
            try:
                url = dynalist.parse_url(link["url"])
            except dynalist.ParseException:
                continue
            if not url:
                continue
            if url["doc_id"] != doc.get_metadata()["file_id"]:
                continue
            if "zoom_node_id" not in url:
                continue
            if doc.has_node(url["zoom_node_id"]):
                continue
            logging.warning("Target node does not exist:\nNode id: %s\nContent: %s\nBad link: %s",
                            node["id"], node["content"], link["url"])


if __name__ == "__main__":
    main()

# vim: foldmethod=indent
