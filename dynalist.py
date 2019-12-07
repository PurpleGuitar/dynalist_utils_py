"""
Classes and methods for working with the Dynalist API.
"""

# Python
import json
import re

# Libraries
import requests


class Document:
    """ Encapsulates a Dynalist document. """

    @staticmethod
    def from_url(url, token): # pragma: no cover
        """ Creates a Document object from a JSON file. """
        parsed_url = parse_url(url)
        doc_id = parsed_url["doc_id"]
        return Document.from_api(doc_id, token)


    @staticmethod
    def from_api(doc_id, token): # pragma: no cover
        """ Creates a Document object from a JSON file. """
        return Document(get_data_from_api(doc_id, token))


    @staticmethod
    def from_json_file(filename):
        """ Creates a Document object from a JSON file. """
        return Document(load_json_from_file(filename))


    @staticmethod
    def from_dict(data):
        """ Creates a Document object from a dictionary. """
        return Document(data)


    def __init__(self, data):
        self.__data = data
        self.__index = get_index_by_node_id(data)


    def get_metadata(self):
        """ Returns the document metadata, e.g. file_id, etc. """
        return self.__data


    def get_root(self):
        """ Returns the root node of the document. """
        return self.get_node("root")


    def has_node(self, node_id):
        """ Returns whether or not the given node_id is in the doc. """
        return node_id in self.__index


    def get_node(self, node_id):
        """ Accepts a node id and returns the node object for it. """
        return self.__index[node_id]


    def get_children(self, node_id):
        """ Accepts a node_id and returns a list of children, if any. """
        node = self.get_node(node_id)
        if "children" not in node:
            return []
        return [self.get_node(child_id) for child_id in node["children"]]


    def get_descendents(self, node_id):
        """ Get all descendents of the given node in tree order. """
        nodes = []
        for child in self.get_children(node_id):
            nodes.append(child)
            nodes += self.get_descendents(child["id"])
        return nodes


    def get_nodes(self, order="tree"):
        """ Get all nodes from the doc in a list.  The order parameter
            controls whether the nodes are returned in tree order (default,
            order='tree') or api order (order='api'). """
        if order == "api":
            return list(self.__data["nodes"])
        if order == "tree":
            return [self.get_node("root")] + self.get_descendents("root")
        raise Exception("order must be 'api' or 'tree'")


    def to_json(self):
        """ Returns the document as a JSON-encoded string. """
        return json.dumps(self.__data)


def parse_url(url):
    """ Parses a Dynalist URL and returns the component fields. """

    fields = {"doc_id": "", "zoom_node_id": "", "query": ""}

    # Plain URL
    plain = re.compile(r"^https://dynalist.io/d/([a-zA-Z0-9_-]+)$")
    match = plain.match(url)
    if match:
        fields["doc_id"] = match.group(1)
        return fields

    # URL with zoom
    zoom = re.compile(
        r"^https://dynalist.io/d/([a-zA-Z0-9_-]+)#z=([a-zA-Z0-9_-]+)?$")
    match = zoom.match(url)
    if match:
        fields["doc_id"] = match.group(1)
        fields["zoom_node_id"] = match.group(2)
        return fields

    # URL with query
    query = re.compile(r"^https://dynalist.io/d/([a-zA-Z0-9_-]+)#q=(.*)$")
    match = query.match(url)
    if match:
        fields["doc_id"] = match.group(1)
        fields["query"] = match.group(2)
        return fields

    # URL with both zoom and query
    zoom_and_query = re.compile(
        r"^https://dynalist.io/d/([a-zA-Z0-9_-]+)#z=([a-zA-Z0-9_-]+)&q=(.*)$")
    match = zoom_and_query.match(url)
    if match:
        fields["doc_id"] = match.group(1)
        fields["zoom_node_id"] = match.group(2)
        fields["query"] = match.group(3)
        return fields

    # Not found
    raise ParseException("ERROR: Not a Dynalist URL: " + str(url))


def get_data_from_api(doc_id, token):  # pragma: no cover
    """ Retrieves Dynalist data from Dynalist API as a Python dict """
    args = {"file_id": doc_id, "token": token}
    response = requests.post("https://dynalist.io/api/v1/doc/read", json=args)
    data = response.json()
    if data["_code"] != "Ok":
        raise ApiException("ERROR: API request failed. Code was '" +
                           str(data["_code"] + "'"))
    return response.json()


def load_json_from_file(filename):
    """ Utility method: retrieves JSON-encoded data from file """
    with open(filename) as infile:
        return json.load(infile)


def get_index_by_node_id(data):
    """ Indexes a Dynalist data object by node for easy navigation. """
    index = {}
    for node in data["nodes"]:
        index[node["id"]] = node
    return index


class DynalistException(Exception):
    """ Dynalist library exception. """


class ApiException(DynalistException):
    """ Exception for API errors. """


class ParseException(DynalistException):
    """ Exception for parse errors. """


# vim: foldmethod=indent
