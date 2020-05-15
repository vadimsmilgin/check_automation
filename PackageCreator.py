#!/usr/bin/python

import os
import re
from lxml import etree
import Utils
import WorkWithAutomation as WWA


def create_package_xml():
    s_object_names = WWA.get_sobjects_name_from_pbs_and_workflows()

    page = etree.Element("Package")
    page.set("xmlns", "http://soap.sforce.com/2006/04/metadata")

    for s_object_name in s_object_names:
        types = etree.Element("types")
        page.append(types)

        members = etree.SubElement(types, "members")
        members.text = s_object_name

        name = etree.SubElement(types, "name")
        name.text = "CustomObject"

    version = etree.SubElement(page, "version")
    version.text = "48.0"

    etree.indent(page, space="    ")
    tree = etree.ElementTree(page)

    result = re.sub(
        r'\'',
        '\"',
        etree.tostring(tree.getroot(), encoding="UTF-8", xml_declaration=True, pretty_print=True).decode("utf-8")
    )
    if os.path.exists(Utils.retrieve_sobjects_path) is False:
        os.mkdir(Utils.retrieve_sobjects_path)
    os.chdir(Utils.retrieve_sobjects_path)

    with open("package.xml", "w") as package:
        package.write(result)


if __name__ == "__main__":
    create_package_xml()
