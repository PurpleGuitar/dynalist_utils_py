""" Utilities for Dynalist apps """

# Python
import argparse
import hashlib
import logging
import os
import sys

from dynalist_utils import dynalist

LOGGING_FORMAT = "%(asctime)s %(levelname)s %(module)s/%(funcName)s:%(lineno)d\n%(message)s"

def add_standard_arguments(parser): # pragma: no cover
    """ Convenience function to add arguments typical apps want. """
    add_argument_url(parser)
    add_argument_infile(parser)
    add_argument_token(parser)
    add_argument_trace(parser)
    add_argument_cached(parser)


def add_argument_url(parser): # pragma: no cover
    """ Add --url to parser arguments """
    parser.add_argument("--url",
                        action="store",
                        help="Dynalist URL, or set DYNALIST_URL env var")


def get_url(args, env):
    """ Get URL from args or environment """
    if args.url:
        return args.url
    if "DYNALIST_URL" in env:
        return env["DYNALIST_URL"]
    return None


def add_argument_infile(parser): # pragma: no cover
    """ Add --infile to parser arguments """
    parser.add_argument("--infile",
                        nargs="?",
                        type=argparse.FileType("r"),
                        default=sys.stdin,
                        help="Local file to load, defaults to stdin")


def add_argument_token(parser): # pragma: no cover
    """ Add --token to parser arguments """
    parser.add_argument("--token",
                        action="store",
                        help="Dynalist token, or set DYNALIST_TOKEN env var")


def get_token(args, env):
    """ Get token from args or environment """
    if args.token:
        return args.token
    if "DYNALIST_TOKEN" in env:
        return env["DYNALIST_TOKEN"]
    raise Exception("ERROR: Please pass in a Dynalist token "
                    "or set DYNALIST_TOKEN environment variable.")


def add_argument_outfile(parser): # pragma: no cover
    """ Add --outfile to parser arguments """
    parser.add_argument("--outfile",
                        nargs="?",
                        type=argparse.FileType("w"),
                        default=sys.stdout,
                        help="Output file, defaults to stdout")


def add_argument_trace(parser): # pragma: no cover
    """ Add --trace to parser arguments """
    parser.add_argument("--trace",
                        action="store_true",
                        help="Enable tracing output")


def add_argument_cached(parser): # pragma: no cover
    """ Add --cached to parser arguments """
    parser.add_argument("--cached",
                        action="store_true",
                        help="Create and reuse cached copy of document")


def read_doc(args): #pragma: no cover
    """ Convenience method to read the doc based on the given args """
    token = get_token(args, os.environ)
    url = get_url(args, os.environ)
    if args.cached:
        hasher = hashlib.md5()
        hasher.update(str.encode(url))
        cache_filename = hasher.hexdigest() + ".json"
        if os.path.exists(cache_filename):
            logging.info("Reusing cached document at: %s", cache_filename)
            return dynalist.Document.from_json_file(cache_filename)
    if url:
        logging.info("Loading doc from url: %s", url)
        doc = dynalist.Document.from_url(url, token)
    else:
        logging.info("Loading doc from file stream: %s", args.infile)
        doc = dynalist.Document.from_json_stream(args.infile)
    if args.cached:
        with open(cache_filename, "w") as cache_file:
            logging.info("Created cached document at: %s", cache_filename)
            cache_file.write(doc.to_json())
    return doc

# vim: foldmethod=indent
