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
import logging
import sys
from typing import List

# Project
from dynalist_utils import app_utils
from dynalist_utils import dynalist
from dynalist_utils import markdown

MIRROR_LINK_TEXT = "mirror"

class MirrorNode: # pylint: disable=too-few-public-methods
    """ Composes a node with the id of the node it's to be a mirror of """
    def __init__(self, node, target_id: str):
        self.node = node
        self.target_id = target_id

def main():
    """ Check args and download doc """
    try:
        args = get_arguments()
        logging.basicConfig(format=app_utils.LOGGING_FORMAT,
                            level=logging.DEBUG if args.trace else logging.WARNING)
        doc = app_utils.read_doc(args)
        mirror_nodes: List[MirrorNode] = find_mirror_nodes(doc)
        change_nodes = create_change_nodes(doc, mirror_nodes)
        print(change_nodes)
        # Send list to API
    except Exception: # pylint: disable=broad-except
        logging.exception("An error occured.")
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Mirror nodes in a Dynalist document")
    app_utils.add_standard_arguments(parser)
    return parser.parse_args()

def find_mirror_nodes(doc) -> List[MirrorNode]:
    """ Return a list of nodes that contain mirror links. """
    mirror_nodes: List[MirrorNode] = []
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
            mirror_node = MirrorNode(node, url["zoom_node_id"])
            mirror_nodes.append(mirror_node)
    return mirror_nodes

def create_change_nodes(doc, mirror_nodes: List[MirrorNode]):
    change_nodes = []
    for mirror_node in mirror_nodes:
        change_node = { "action": "edit", "node_id": mirror_node["id"] }
        source_node = doc.get_node(mirror_node.target_id)
        print(source_node)
    return change_nodes




if __name__ == "__main__":
    main()

# vim: foldmethod=indent
