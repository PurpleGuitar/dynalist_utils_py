#!/usr/bin/env python3

"""
Generates text from templates in Dynalist.
"""

# Python
import argparse
import logging
import random
import re
import sys

# Project
from dynalist_utils import app_utils

FIELD_REGEX = re.compile(r"{{([^}]+)}}")
WHITESPACE_REGEX = re.compile(r"\s\s+")

def main():
    """ Check args and download doc """
    try:
        # Get arguments
        args = get_arguments()
        logging.basicConfig(format=app_utils.LOGGING_FORMAT,
                            level=logging.DEBUG if args.trace else logging.WARNING)

        # Get doc
        doc = app_utils.read_doc(args)

        # Get zoom node
        zoom_node_id = doc.get_metadata()["zoom_node_id"]
        if not zoom_node_id:
            zoom_node_id = "root"

        # Process text
        for _ in range(args.num):
            text = process_template(doc, zoom_node_id)
            print(text)

    except Exception: # pylint: disable=broad-except
        logging.exception("An error occured.")
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Populate a template from a Dynalist node")
    app_utils.add_standard_arguments(parser)
    parser.add_argument("--num",
                        type=int,
                        default=1,
                        help="Number of results to generate")
    return parser.parse_args()

def process_template(doc, zoom_node_id):
    """ Read template and fill in values from doc """

    # Read template
    template = doc.get_node(zoom_node_id)["content"]
    logging.debug("Template: %s", template)

    # Index children
    children = doc.get_children(zoom_node_id)
    children_by_content = {}
    for child in children:
        children_by_content[child["content"]] = child
    logging.debug("Found keys: %s", children_by_content.keys())

    # Process template
    text = template
    while True:
        match = FIELD_REGEX.search(text)
        if not match:
            break
        key = match.group(1)
        if key in children_by_content:
            data = children_by_content[key]
            values = doc.get_children(data["id"])
            random_value = random.choice(values)["content"]
            logging.debug("{{%s}} -> %s", key, random_value)
            text = text[:match.start()] + random_value + text[match.end():]
        else:
            logging.warning("No child found for key '%s'", key)
            text = text[:match.start()] + f"MISS({key})" + text[match.end():]

    # Clean up whitespace
    text = WHITESPACE_REGEX.sub(" ", text)
    logging.debug("Output: %s", text)

    # Done
    return text

if __name__ == "__main__":
    main()

# vim: foldmethod=indent
