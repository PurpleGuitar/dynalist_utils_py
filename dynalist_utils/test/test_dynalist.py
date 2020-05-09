""" Tests for dynalist """

# Python
import json
import os
import unittest

# Project
import dynalist

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestParseURL(unittest.TestCase):
    """ Tests for dlget.get_url() """

    def test_empty_url(self):
        """ No url provided -- throw exception """
        with self.assertRaises(Exception):
            dynalist.parse_url("")
        with self.assertRaises(Exception):
            dynalist.parse_url(None)

    def test_non_dynalist_url(self):
        """ Some non-Dynalist URL """
        with self.assertRaises(Exception):
            dynalist.parse_url("https://www.example.com")

    def test_dynalist_url(self):
        """ Plain Dynalist URL """
        result = dynalist.parse_url(
            "https://dynalist.io/d/5_zeWJ0rbUeWXOu_svUrFd3h")
        expected = {
            "doc_id": "5_zeWJ0rbUeWXOu_svUrFd3h",
            "zoom_node_id": "",
            "query": ""
        }
        self.assertEqual(expected, result)

    def test_dynalist_zoom_url(self):
        """ Dynalist URL with zoom """
        result = dynalist.parse_url(
            "https://dynalist.io/d/5_zeWJ0rbUeWXOu_svUrFd3h#z=bdBGyB8FtmnVL2JLPWIePLdf")
        expected = {
            "doc_id": "5_zeWJ0rbUeWXOu_svUrFd3h",
            "zoom_node_id": "bdBGyB8FtmnVL2JLPWIePLdf",
            "query": ""
        }
        self.assertEqual(expected, result)

    def test_dynalist_query_url(self):
        """ Dynalist URL with query """
        result = dynalist.parse_url(
            "https://dynalist.io/d/5_zeWJ0rbUeWXOu_svUrFd3h#q=pylint")
        expected = {
            "doc_id": "5_zeWJ0rbUeWXOu_svUrFd3h",
            "zoom_node_id": "",
            "query": "pylint"
        }
        self.assertEqual(expected, result)

    def test_dynalist_zoom_query_url(self):
        """ Dynalist URL with zoom and query """
        result = dynalist.parse_url(
            "https://dynalist.io/d/5_zeWJ0rbUeWXOu_svUrFd3h#z=bdBGyB8FtmnVL2JLPWIePLdf&q=pylint")
        expected = {
            "doc_id": "5_zeWJ0rbUeWXOu_svUrFd3h",
            "zoom_node_id": "bdBGyB8FtmnVL2JLPWIePLdf",
            "query": "pylint"
        }
        self.assertEqual(expected, result)


class TestGetIndexByNodeId(unittest.TestCase):
    """ Tests for dynalist.get_index_by_node_id() """

    def test_simple_doc(self):
        """ Test a simple document """
        data = dynalist.load_json_from_file(
            os.path.join(TEST_DIR, "test_colors.json"))
        index = dynalist.get_index_by_node_id(data)
        self.assertEqual(7, len(index))
        root = index["root"]
        self.assertEqual("test", root["content"])
        self.assertEqual(6, len(root["children"]))


class TestDocument(unittest.TestCase):
    """ Tests for Dyanlist Document """

    def test_from_data(self):
        """ Test a simple document """
        data = dynalist.load_json_from_file(
            os.path.join(TEST_DIR, "test_colors.json"))
        doc = dynalist.Document.from_dict(data)
        root = doc.get_root()
        self.assertEqual("test", root["content"])
        children = doc.get_children(root["id"])
        self.assertEqual(6, len(children))


    def test_from_json_file(self):
        """ Test a simple document """
        doc = dynalist.Document.from_json_file(
            os.path.join(TEST_DIR, "test_colors.json"))
        root = doc.get_root()
        self.assertEqual("test", root["content"])
        children = doc.get_children(root["id"])
        self.assertEqual(6, len(children))


    def test_from_json_stream(self):
        """ Test a simple document """
        with open(os.path.join(TEST_DIR, "test_colors.json")) as stream:
            doc = dynalist.Document.from_json_stream(stream)
        root = doc.get_root()
        self.assertEqual("test", root["content"])
        children = doc.get_children(root["id"])
        self.assertEqual(6, len(children))


    def test_to_json(self):
        """ Test a simple document """
        filename = os.path.join(TEST_DIR, "test_colors.json")
        data_from_json = dynalist.load_json_from_file(filename)
        doc = dynalist.Document.from_json_file(filename)
        data_from_doc = json.loads(doc.to_json())
        self.assertEqual(data_from_json, data_from_doc)


    def test_get_nodes_api_order(self):
        """ Test getting all nodes in the document. """
        doc = dynalist.Document.from_json_file(
            os.path.join(TEST_DIR, "test_colors_reversed.json"))
        nodes = doc.get_nodes(order="api")
        self.assertEqual(7, len(nodes))
        self.assertEqual("test", nodes[0]["content"])
        self.assertEqual("color 1", nodes[1]["content"])
        self.assertEqual("color 6", nodes[6]["content"])


    def test_get_nodes_tree_order(self):
        """ Test getting all nodes in the document. """
        doc = dynalist.Document.from_json_file(
            os.path.join(TEST_DIR, "test_colors_reversed.json"))
        nodes = doc.get_nodes(order="tree")
        self.assertEqual(7, len(nodes))
        self.assertEqual("test", nodes[0]["content"])
        self.assertEqual("color 6", nodes[1]["content"])
        self.assertEqual("color 1", nodes[6]["content"])


    def test_get_nodes_makes_copy(self):
        """ Test getting all nodes in the document. """
        doc = dynalist.Document.from_json_file(
            os.path.join(TEST_DIR, "test_colors_reversed.json"))
        nodes = doc.get_nodes()
        nodes_copy = doc.get_nodes()
        self.assertIsNot(nodes, nodes_copy)


    def test_get_nodes_error(self):
        """ Test getting all nodes in the document. """
        doc = dynalist.Document.from_json_file(os.path.join(TEST_DIR, "test_colors_reversed.json"))
        with self.assertRaises(Exception):
            doc.get_nodes(order="invalid_order")

    def test_get_metadata(self):
        """ Test getting metadata of the document. """
        doc = dynalist.Document.from_json_file(os.path.join(TEST_DIR, "test_collapsed.json"))
        metadata = doc.get_metadata()
        self.assertEqual("QVAyujPE0w9uj0Vd1VykS7QP", metadata["file_id"])

    def test_has_node(self):
        """ Test checking if a node exists. """
        doc = dynalist.Document.from_json_file(os.path.join(TEST_DIR, "test_collapsed.json"))
        self.assertTrue(doc.has_node("1zsUGsZAwJUQE90HFBpYmKpS"))

    def test_collapsed_nodes(self):
        """ Test getting all nodes in the document. """
        doc = dynalist.Document.from_json_file(
            os.path.join(TEST_DIR, "test_collapsed.json"))
        nodes = doc.get_nodes(order="tree")
        self.assertEqual(11, len(nodes))
        attendees = doc.get_node("1zsUGsZAwJUQE90HFBpYmKpS")
        self.assertTrue(attendees["collapsed"])

# vim: foldmethod=indent
