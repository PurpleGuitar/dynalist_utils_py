""" Tests for markdown """

# Python
import json
import os
import pathlib
import unittest

# Project
from dynalist_utils import dynalist
from dynalist_utils import markdown


# pylint: disable=line-too-long
CONVERT_TESTS = [
    {"title": "Simple List",
     "source": r'''{"_code":"Ok","title":"root","nodes":[
           {"id":"root","content":"root","note":"","children":["EhYNY6ULjIEF0xFg65USFLlW"],"created":1554216514019,"modified":1554216524784}, 
           {"id":"EhYNY6ULjIEF0xFg65USFLlW","content":"header","note":"","collapsed":true,"children":["SPhwaj_3zX2hGgZHLTZ9LI0p"],"created":1554216517391,"modified":1554216540818},{"id":"SPhwaj_3zX2hGgZHLTZ9LI0p","content":"list-root","note":"","children":["iUxAdTERIqo5WOzDLOC_fzcl","Rf_gJtC-7OeWwmmKfJyCUw2W","BLyQ8GQqMSZTPkz_tup9gg0R"],"created":1554216540818,"modified":1554216546745},
           {"id":"iUxAdTERIqo5WOzDLOC_fzcl","content":"item-1","note":"","created":1554216546745,"modified":1554216546745},
           {"id":"Rf_gJtC-7OeWwmmKfJyCUw2W","content":"item-2","note":"","created":1554216546745,"modified":1554216546745},
           {"id":"BLyQ8GQqMSZTPkz_tup9gg0R","content":"item-3","note":"","created":1554216546745,"modified":1554216624702}]}''',
     "expected": "# root\n\n## header\n\n- list-root\n    - item-1\n    - item-2\n    - item-3\n\n"},
    {"title": "Simple List with italics",
     "source": r'''{"_code":"Ok","title":"root","nodes":[
           {"id":"root","content":"root","note":"","children":["EhYNY6ULjIEF0xFg65USFLlW"],"created":1554216514019,"modified":1554216524784}, 
           {"id":"EhYNY6ULjIEF0xFg65USFLlW","content":"header","note":"","collapsed":true,"children":["SPhwaj_3zX2hGgZHLTZ9LI0p"],"created":1554216517391,"modified":1554216540818},{"id":"SPhwaj_3zX2hGgZHLTZ9LI0p","content":"list-root","note":"","children":["iUxAdTERIqo5WOzDLOC_fzcl","Rf_gJtC-7OeWwmmKfJyCUw2W","BLyQ8GQqMSZTPkz_tup9gg0R"],"created":1554216540818,"modified":1554216546745},
           {"id":"iUxAdTERIqo5WOzDLOC_fzcl","content":"item-1","note":"","created":1554216546745,"modified":1554216546745},
           {"id":"Rf_gJtC-7OeWwmmKfJyCUw2W","content":"item-2","note":"This is how __Dynalist__ formats italics","created":1554216546745,"modified":1554216546745},
           {"id":"BLyQ8GQqMSZTPkz_tup9gg0R","content":"item-3","note":"","created":1554216546745,"modified":1554216624702}]}''',
     "expected": "# root\n\n## header\n\n- list-root\n    - item-1\n    - item-2\n        \n        This is how *Dynalist* formats italics\n        \n    - item-3\n\n"},
    {"title": "List with Note",
     "source": r'''{"_code":"Ok","title":"root","nodes":[
         {"id":"root","content":"root","note":"root note text","children":["EhYNY6ULjIEF0xFg65USFLlW"],"created":1554216514019,"modified":1554217026764},
         {"id":"EhYNY6ULjIEF0xFg65USFLlW","content":"header","note":"","collapsed":true,"children":["SPhwaj_3zX2hGgZHLTZ9LI0p"],"created":1554216517391,"modified":1554216540818},
         {"id":"SPhwaj_3zX2hGgZHLTZ9LI0p","content":"list-root","note":"","children":["iUxAdTERIqo5WOzDLOC_fzcl","Rf_gJtC-7OeWwmmKfJyCUw2W","BLyQ8GQqMSZTPkz_tup9gg0R"],"created":1554216540818,"modified":1554216546745},
         {"id":"iUxAdTERIqo5WOzDLOC_fzcl","content":"item-1","note":"","created":1554216546745,"modified":1554216546745},
         {"id":"Rf_gJtC-7OeWwmmKfJyCUw2W","content":"item-2","note":"note for item 2","created":1554216546745,"modified":1554217032672},
         {"id":"BLyQ8GQqMSZTPkz_tup9gg0R","content":"item-3","note":"","created":1554216546745,"modified":1554216624702}]}''',
     "expected": "# root\n\nroot note text\n\n## header\n\n- list-root\n    - item-1\n    - item-2\n        \n        note for item 2\n        \n    - item-3\n\n"}]

LINK_TESTS = [
    {"title": "No Links",
     "source": "",
     "expected": []},
    {"title": "Simple Markdown Link",
     "source": "This is an [Example](https://www.example.com).",
     "expected": [{"title": "Example", "url": "https://www.example.com"}]},
    {"title": "Two Markdown Links",
     "source": "Here are two links: [Example1](https://www.example.com) and [Example2](https://www.github.com).",
     "expected": [{"title": "Example1", "url": "https://www.example.com"},
                  {"title": "Example2", "url": "https://www.github.com"}]},
    {"title": "Bare link",
     "source": "You can find it here: https://www.example.com",
     "expected": [{"title": "", "url": "https://www.example.com"}]},
    {"title": "Two bare links",
     "source": "You can find it here: https://www.example.com or here: https://www.example.org",
     "expected": [{"title": "", "url": "https://www.example.com"},
                  {"title": "", "url": "https://www.example.org"}]},
    {"title": "Bare followed by Markdown link",
     "source": "You can find it here: https://www.example.com or here: [Example](https://www.example.org)",
     "expected": [{"title": "", "url": "https://www.example.com"},
                  {"title": "Example", "url": "https://www.example.org"}]},
    {"title": "Markdown followed by bare link",
     "source": "You can find it here: [Example](https://www.example.com) or here: https://www.example.org",
     "expected": [{"title": "Example", "url": "https://www.example.com"},
                  {"title": "", "url": "https://www.example.org"}]}
    ]

TEST_DIR = os.path.dirname(os.path.realpath(__file__))

class TestConvert(unittest.TestCase):
    """ tests for markdown.convert() """

    def test_examples(self):
        """ Run through examples and make sure they all match """
        for test in CONVERT_TESTS:
            data = json.loads(test["source"])
            doc = dynalist.Document.from_dict(data)
            actual = markdown.convert(doc, "root")
            self.assertEqual(test["expected"], actual, test["title"])

    def test_collapsed_nodes(self):
        """ Test that collapsed nodes render as headers """
        doc = dynalist.Document.from_json_file(os.path.join(TEST_DIR, "test_markdown_collapsed.json"))
        expected = pathlib.Path(os.path.join(TEST_DIR, "test_markdown_collapsed.md")).read_text()
        actual = markdown.convert(doc, "root")
        self.assertEqual(expected, actual)

class TestMarkdown(unittest.TestCase):
    """ Test other markdown functions """
    def test_find_links(self):
        """ Test finding links in Markdown text """
        for test in LINK_TESTS:
            actual = markdown.find_links(test["source"])
            self.assertEqual(test["expected"], actual, test["title"])
