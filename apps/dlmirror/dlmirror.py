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
import requests
import os
from collections import namedtuple
from typing import List

# Project
from dynalist_utils import app_utils
from dynalist_utils import dynalist
from dynalist_utils import markdown

MIRROR_LINK_TEXT = "mirror"

MirrorNode = namedtuple("MirrorNode", ["source_node", "target_node", "link"])

def main():
    """ Check args and download doc """
    try:
        args = get_arguments()
        logging.basicConfig(format=app_utils.LOGGING_FORMAT,
                            level=logging.DEBUG if args.trace else logging.WARNING)
        doc = app_utils.read_doc(args)
        mirror_nodes = find_mirror_nodes(doc)
        token = app_utils.get_token(args, os.environ)
        update_dynalist(doc, token, mirror_nodes)
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
            source_node = doc.get_node(url["zoom_node_id"])
            target_node = node
            mirror_nodes.append(MirrorNode(source_node, target_node, link))
            break # for link in links
    return mirror_nodes

def update_dynalist(doc, token, mirror_nodes: List[MirrorNode]):
    changes = []
    data = { "file_id": doc.get_metadata()["file_id"], 
             "token": token,
             "changes": changes }
    for mirror_node in mirror_nodes:
        change_needed = False
        link_text = f"[{mirror_node.link['title']}]({mirror_node.link['url']})"
        change = { "action": "edit" }
        change["node_id"] = mirror_node.target_node["id"]
        if mirror_node.source_node["content"] != mirror_node.target_node["content"]:
            change_needed = True
            change["content"] = mirror_node.source_node["content"]
        if "note" not in mirror_node.source_node:
            change_needed = True
            change["note"] = link_text
        elif mirror_node.source_node["note"] == "":
            target_note = link_text
            if mirror_node.target_node["note"] != target_note:
                change_needed = True
                change["note"] = target_note
        else:
            target_note = mirror_node.source_node["note"] + "\n" + link_text
            if mirror_node.target_node["note"] != target_note:
                change_needed = True
                change["note"] = target_note
        if change_needed:
            changes.append(change)
    if len(changes) == 0:
        logging.info("No changes required.")
    else:
        response = requests.post("https://dynalist.io/api/v1/doc/edit", json=data)

if __name__ == "__main__":
    main()

# vim: foldmethod=indent
