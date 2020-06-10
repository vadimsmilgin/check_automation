#!/usr/bin/python

import os
import platform
import re
from lxml import etree
from context import Context, Windows, MacOS
from work_with_s_objects import WorkWithSObjects


def create_package_xml():
    if platform.system() == 'Windows':
        _context = Context(Windows())
    if platform.system() == 'Darwin':
        _context = Context(MacOS())
    wws = WorkWithSObjects(_context)

    s_object_name = wws.get_lookup_fields()
    keys = s_object_name.keys()

    document = etree.Element("Package")
    document.set("xmlns", "http://soap.sforce.com/2006/04/metadata")

    types = etree.Element("types")
    members = etree.SubElement(types, "members")
    members.text = '*'
    name = etree.SubElement(types, "name")
    name.text = "Flow"

    for key in keys:
        types = etree.Element("types")
        document.append(types)

        members = etree.SubElement(types, "members")
        members.text = key

        name = etree.SubElement(types, "name")
        name.text = "Workflow"

    version = etree.SubElement(document, "version")
    version.text = "48.0"

    etree.indent(document, space="    ")
    tree = etree.ElementTree(document)

    result = re.sub(
        r'\'',
        '\"',
        etree.tostring(tree.getroot(), encoding="UTF-8", xml_declaration=True, pretty_print=True).decode("utf-8")
    )
    os.chdir(_context.get_automation_files_path())

    with open("package.xml", "w") as package:
        package.write(result)


if __name__ == "__main__":
    create_package_xml()
