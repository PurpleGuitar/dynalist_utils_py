#!/usr/bin/env python3

"""
Emails a reminder of due tasks.
"""

# Python
from datetime import datetime
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from operator import attrgetter
from typing import Any, Dict, List
import argparse
import logging
import os
import re
import smtplib
import sys

# Project
import app_utils

DATE_REGEX = re.compile(r"!\((\d\d\d\d-\d\d\-\d\d).*\)")

class DatedNode: # pylint: disable=too-few-public-methods
    """ Composite of a node an the first date found in it. """
    def __init__(self):
        self.date: str = ""
        self.node: Dict[str, Any] = None
        self.link: str = ""
        self.checked: bool = False

def main():
    """ Check args and download doc """
    try:
        # Get arguments
        args = get_arguments()
        logging.basicConfig(format=app_utils.LOGGING_FORMAT,
                            level=logging.DEBUG if args.trace else logging.WARNING)

        # Get doc
        doc = app_utils.read_doc(args)

        # Get dated nodes
        dated_nodes: List[DatedNode] = get_dated_nodes(doc)

        # Create email
        message: MIMEMultipart = create_message(dated_nodes)

        # Send email
        send_email(message, args.trace)


    except Exception: # pylint: disable=broad-except
        logging.exception("An error occured.")
        sys.exit(1)


def get_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description="Populate a template from a Dynalist node")
    app_utils.add_standard_arguments(parser)
    return parser.parse_args()

def get_dated_nodes(doc) -> List[DatedNode]:
    """ Returns list of all nodes with dates in the doc. """

    dated_nodes: List[DatedNode] = []

    # Find all dated nodes
    for node in doc.get_nodes():
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
            dated_node.link = ("https://dynalist.io/d/" +
                               doc.get_metadata()["doc_id"] +
                               "#z=" +
                               node["id"])
            dated_node.checked = "checked" in node and node["checked"]
            dated_nodes.append(dated_node)

    # Sort nodes by date
    dated_nodes = sorted(dated_nodes, key=attrgetter("date"))

    return dated_nodes

def create_message(dated_nodes: List[DatedNode]) -> MIMEMultipart:
    """ Send reminder email """

    email_from = os.getenv("EMAIL_FROM")
    if not email_from:
        logging.error("Please provide environment variable EMAIL_FROM.")
        sys.exit(1)

    email_to = os.getenv("EMAIL_TO")
    if not email_to:
        logging.error("Please provide environment variable EMAIL_TO.")
        sys.exit(1)

    msg: MIMEMultipart = MIMEMultipart("alternative")
    msg["From"] = email_from
    msg["To"] = email_to

    msg["Subject"] = "Items due for " +  datetime.today().strftime('%Y-%m-%d')

    html: str = "<html>"
    html += "<body>"
    html += render_due_today(dated_nodes)
    html += render_overdue(dated_nodes)
    html += render_due_soon(dated_nodes)
    html += "</body>"
    html += "</html>"
    logging.debug(html)
    msg.attach(MIMEText(html, "html"))

    return msg


def render_due_today(dated_nodes: List[DatedNode]) -> str:
    """ Render tasks due today. """

    logging.debug("DUE TODAY")
    html: str = ""

    today = datetime.today().strftime('%Y-%m-%d')
    logging.debug("Today: %s", today)
    due_today = [dated_node for dated_node in dated_nodes if dated_node.date == today]
    if not due_today:
        return ""

    html += "<h1>Due Today</h1>"
    html += "<ul>"
    for item in due_today:
        html += render_list_item(item)
    html += "</ul>"

    return html

def render_overdue(dated_nodes: List[DatedNode]) -> str:
    """ Render tasks due today. """

    logging.debug("OVERDUE")
    html: str = ""

    today = datetime.today().strftime('%Y-%m-%d')
    logging.debug("Today: %s", today)
    overdue = [dated_node
               for dated_node in dated_nodes
               if dated_node.date < today
               and not dated_node.checked]
    if not overdue:
        return ""

    html += "<h1>Overdue</h1>"
    html += "<ul>"
    for item in overdue:
        html += render_list_item(item)
    html += "</ul>"

    return html


def render_due_soon(dated_nodes: List[DatedNode]) -> str:
    """ Render tasks due today. """

    logging.debug("DUE SOON")
    html: str = ""

    today = datetime.today().strftime('%Y-%m-%d')
    logging.debug("Today: %s", today)
    week_from_now = (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')
    logging.debug("Week from Now: %s", week_from_now)
    due_soon = [dated_node
                for dated_node in dated_nodes
                if dated_node.date > today
                and dated_node.date < week_from_now
                and not dated_node.checked]
    if not due_soon:
        return ""

    html += "<h1>Due Soon</h1>"
    html += "<ul>"
    for item in due_soon:
        html += render_list_item(item)
    html += "</ul>"

    return html


def render_list_item(item: DatedNode) -> str:
    """ Renders a single item as an html list item """
    logging.debug(item.node["content"])
    html: str = ""
    html += "<li>"
    html += item.node["content"]
    html += " <a href='" + item.link + "'>Link</a>"
    if item.node["note"]:
        html += "<br/>"
        html += "<small>" + item.node["note"]
    html += "</li>"
    return html


def send_email(message, trace: bool):
    """ Send reminder email """

    email_server = os.getenv("EMAIL_SERVER")
    if not email_server:
        logging.error("Please provide environment variable EMAIL_SERVER.")
        sys.exit(1)

    email_username = os.getenv("EMAIL_USERNAME")
    if not email_username:
        logging.error("Please provide environment variable EMAIL_USERNAME.")
        sys.exit(1)

    email_password = os.getenv("EMAIL_PASSWORD")
    if not email_password:
        logging.error("Please provide environment variable EMAIL_PASSWORD.")
        sys.exit(1)


    logging.debug("Connecting to email server...")
    with smtplib.SMTP_SSL(email_server) as smtp:
        if trace:
            smtp.set_debuglevel(2)
        smtp.login(email_username, email_password)
        smtp.send_message(message)


if __name__ == "__main__":
    main()

# vim: foldmethod=indent
