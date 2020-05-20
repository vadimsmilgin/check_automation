#!/usr/bin/python

import os
import re
from lxml import etree
import work_with_automation as wwa
import utils


def create_package_xml():
    s_object_names = wwa.get_sobjects_name_from_pbs_and_workflows()

    document = etree.Element("Package")
    document.set("xmlns", "http://soap.sforce.com/2006/04/metadata")

    for s_object_name in s_object_names:
        types = etree.Element("types")
        document.append(types)

        members = etree.SubElement(types, "members")
        members.text = s_object_name

        name = etree.SubElement(types, "name")
        name.text = "CustomObject"

    version = etree.SubElement(document, "version")
    version.text = "48.0"

    etree.indent(document, space="    ")
    tree = etree.ElementTree(document)

    result = re.sub(
        r'\'',
        '\"',
        etree.tostring(tree.getroot(), encoding="UTF-8", xml_declaration=True, pretty_print=True).decode("utf-8")
    )
    if os.path.exists(utils.retrieve_sobjects_path) is False:
        os.mkdir(utils.retrieve_sobjects_path)
    os.chdir(utils.retrieve_sobjects_path)

    with open("package.xml", "w") as package:
        package.write(result)


if __name__ == "__main__":
    create_package_xml()
