#!/usr/bin/env python3

"""

Update "mirror nodes" in a Dynalist document.  A "mirror node" is a node
that contins a specially formatted Markdown link with the following properties:

- The title of the link is "mirror" (or some other constant)
- it links to another node in the same document.

This script will find mirror nodes in a document and update their title,
note, etc. to be an exact duplicate of the source node, plus a mirror link
at the end of the note.

This script is idempotent -- if there are no mirror nodes, or if the nodes
are already up-to-date, the document will be unchanged.

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

def main():
    """ Check args and download doc """
    try:
        args = get_arguments()
        logging.basicConfig(format=app_utils.LOGGING_FORMAT,
                            level=logging.DEBUG if args.trace else logging.WARNING)
        doc = app_utils.read_doc(args)
        mirror_nodes = find_mirror_nodes(doc)
        print(mirror_nodes)
        # Create list of update nodes to send to API
        # Send list to API
    except Exception: # pylint: disable=broad-except
        logging.exception("An error occured.")
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Mirror nodes in a Dynalist document")
    app_utils.add_standard_arguments(parser)
    return parser.parse_args()

def find_mirror_nodes(doc):
    """ Return a list of nodes that contain mirror links. """
    mirror_nodes = []
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
            if not doc.has_node(url["zoom_node_id"]):
                continue
            mirror_nodes.append(node)
    return mirror_nodes


if __name__ == "__main__":
    main()

# vim: foldmethod=indent
