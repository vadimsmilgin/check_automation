#!/usr/bin/python

import os
import re
from lxml import etree

automation_files_path = '.\\sample\\retrieveUnpackaged'
flows_path = '.\\sample\\retrieveUnpackaged\\flows'
workflows_path = '.\\sample\\retrieveUnpackaged\\workflows'
retrieve_sobjects_path = '.\\sample\\retrieveSObjects'

folder_name_flows = 'flows'
folder_name_workflows = 'workflows'

generalFolder = os.getcwd()


def get_sobject_name_from_pbs_and_workflows():
    try:
        automations_dir = os.listdir(path=automation_files_path)
        set_sobjects = set()
        if folder_name_flows in automations_dir:
            flows_dir = os.listdir(path=flows_path)
            if len(flows_dir) > 0:
                os.chdir(flows_path)
                for file in flows_dir:
                    with open(file, "r") as fh:
                        sobject_name = re.search(
                            r'(?<=<name>ObjectType</name>\n\s{8}<value>\n\s{12}<stringValue>).*?(?=</stringValue>)',
                            fh.read()
                        )
                        if sobject_name is not None:
                            set_sobjects.add(sobject_name.group(0))
            os.chdir(generalFolder)
        if folder_name_workflows in automations_dir:
            workflows_dir = os.listdir(path=workflows_path)
            if len(workflows_dir) > 0:
                for fileName in workflows_dir:
                    sObjectName = re.search(r'.*?(?=\.)', fileName).group(0)
                    set_sobjects.add(sObjectName)
        create_package_xml(set_sobjects)
    except FileNotFoundError:
        print('Directory /sample/retrieveUnpackaged is not found')


def create_package_xml(*args):
    s_objects = args[0]

    page = etree.Element("Package")
    page.set("xmlns", "http://soap.sforce.com/2006/04/metadata")

    for s_object in s_objects:
        types = etree.Element("types")
        page.append(types)

        members = etree.SubElement(types, "members")
        members.text = s_object

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
    if os.path.exists(retrieve_sobjects_path) is False:
        os.mkdir(retrieve_sobjects_path)
    os.chdir(retrieve_sobjects_path)

    with open("package.xml", "w") as package:
        package.write(result)


if __name__ == "__main__":
    get_sobject_name_from_pbs_and_workflows()







