""" Converts a Dynalist doc to Markdown format """

import re

LINK_REGEX = re.compile(r"\[([^]]+)\]\(([^)]+)\)")

def find_links(source):
    """ Find Markdown links in the given source string. """
    links = []
    matches = LINK_REGEX.findall(source)
    if not matches:
        return links
    for match in matches:
        result = {}
        result["title"] = match[0]
        result["url"] = match[1]
        links.append(result)
    return links

def convert(doc, node_id):
    """ Convert a Dynalist doc to Markdown format """
    return convert_node(doc, node_id, True, 1, 0)

def convert_node(doc, node_id, is_root, header_level, collapsed_level): # pylint: disable=too-many-locals
    """ Convert a node and its children to Markdown format """

    markdown = ""
    node = doc.get_node(node_id)
    content = convert_styling(node["content"])
    note = convert_styling(node["note"]) if node["note"] else None

    # Flags
    is_this_node_collapsed = "collapsed" in node and node["collapsed"] and not is_root
    is_ancestor_node_collapsed = collapsed_level > 0 and not is_root
    is_collapsed = is_this_node_collapsed or is_ancestor_node_collapsed
    is_header = not is_ancestor_node_collapsed

    # Is this a header or bullet point?
    if is_header:
        # Render content as header
        for _ in range(header_level):
            markdown += "#"
        markdown += " {}\n\n".format(content)
        # Render note as body
        if note:
            markdown += "{}\n\n".format(note)
    else:
        # Render content as list
        indent = ""
        for _ in range(collapsed_level - 1):
            indent += "    "
        markdown += "{}- {}\n".format(indent, content)
        if note:
            indent += "    "
            markdown += "{}\n".format(indent)
            for line in iter(note.splitlines()):
                markdown += "{}{}\n".format(indent, line)
            markdown += "{}\n".format(indent)

    # Increment levels
    header_level = header_level + 1 if is_header else header_level
    collapsed_level = collapsed_level + 1 if is_collapsed else collapsed_level

    # Render children
    for child in doc.get_children(node["id"]):
        markdown += convert_node(doc, child["id"], False, header_level, collapsed_level)
    if is_header and is_this_node_collapsed:
        markdown += "\n"

    # All done
    return markdown

def convert_styling(text):
    """ Converts Dynalist's styling to Pandoc-style markdown """
    text = text.replace("__", "*")
    return text
