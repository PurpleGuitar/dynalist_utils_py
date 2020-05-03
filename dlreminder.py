#!/usr/bin/env python3

"""
Emails a reminder of due tasks.
"""

# Python
import argparse
import logging
import re
import sys
from datetime import datetime
from typing import Any, Dict
from operator import attrgetter

# Project
import app_utils

DATE_REGEX = re.compile(r"!\((\d\d\d\d-\d\d\-\d\d).*\)")

class DatedNode:
    def __init__(self):
        self.date: str = ""
        self.node: Dict[str, Any] = None

def main():
    """ Check args and download doc """
    try:
        # Get arguments
        args = get_arguments()
        logging.basicConfig(format=app_utils.LOGGING_FORMAT,
                            level=logging.DEBUG if args.trace else logging.WARNING)

        # Get doc
        doc = app_utils.read_doc(args)

        # Find all dated nodes
        dated_nodes: List[DatedNode] = []
        for node in doc.get_nodes():
            date: str = ""
            # Look in content
            match = DATE_REGEX.search(node["content"])
            # If not in content, look in note
            if not match:
                match = DATE_REGEX.search(node["note"])
            # If found, add to list
            if match:
                dated_node: DatedNode = DatedNode()
                dated_node.date = match[1]
                dated_node.node = node
                dated_nodes.append(dated_node)

        # Sort nodes by date
        dated_nodes = sorted(dated_nodes, key=attrgetter("date"))

        # Due today
        today = datetime.today().strftime('%Y-%m-%d')
        logging.debug("Today: %s", today)
        due_today = [dated_node for dated_node in dated_nodes if dated_node.date == today]
        for item in due_today:
            logging.debug("Due today: %s", item.node["content"])


                






    except Exception: # pylint: disable=broad-except
        logging.exception("An error occured.")
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Populate a template from a Dynalist node")
    app_utils.add_standard_arguments(parser)
    return parser.parse_args()



if __name__ == "__main__":
    main()

# vim: foldmethod=indent
