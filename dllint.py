#!/usr/bin/env python3

"""
Simple linter for Dynalist docs.
"""

# Python
import argparse
import collections
import enum
import os
import sys

# Project
import app_utils
import dynalist
import markdown

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
        token = app_utils.get_token(args, os.environ)
        url = app_utils.get_url(args, os.environ)
        doc = dynalist.Document.from_url(url, token)
        messages = []
        messages.extend(check_bad_internal_links(doc))
        if not messages:
            app_utils.eprint("No warnings or errors.")
            sys.exit(0)
        for message in messages:
            app_utils.eprint("{}: {}\n{}".format(message.level, message.summary, message.details))
        sys.exit(1)
    except Exception as exception: # pylint: disable=broad-except
        app_utils.eprint("Unexpected exception!  Details follow.")
        raise exception


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Run some checks on a Dynalist document")
    app_utils.add_argument_url(parser)
    app_utils.add_argument_token(parser)
    return parser.parse_args()

def check_bad_internal_links(doc):
    """ Check for internal links that don't point to a valid node. """
    messages = []
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
            messages.append(Message(
                level=Level.ERROR,
                summary="Bad internal link (target node does not exist)",
                details="Node id: {}\nContent: {}\nBad link: {}".format(
                    node["id"], node["content"], link["url"])))
    return messages


if __name__ == "__main__":
    main()

# vim: foldmethod=indent
