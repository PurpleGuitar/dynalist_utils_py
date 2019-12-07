""" Utilities for Dynalist apps """

# Python
import argparse
import sys


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
    raise Exception("ERROR: Please pass in a Dynalist URL "
                    "or set DYNALIST_URL environment variable.")


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


def eprint(*args, **kwargs): # pragma: no cover
    """ Print to stderr """
    print(*args, file=sys.stderr, **kwargs)

# vim: foldmethod=indent
