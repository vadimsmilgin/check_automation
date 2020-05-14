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

regexp_find_s_object_name = '(?<=<name>ObjectType</name>\n\s{8}<value>\n\s{12}<stringValue>).*?(?=</stringValue>)'
regexp_find_s_object_name_from_file_name = '.*?(?=\.)'
map_s_objects_and_pb = {}


def get_sobject_name_from_pbs_and_workflows():
    try:
        automations_dir = os.listdir(path=automation_files_path)
        set_sobjects = set()
        if folder_name_flows in automations_dir:
            flows_dir = os.listdir(path=flows_path)
            if len(flows_dir) > 0:
                os.chdir(flows_path)
                for flow in flows_dir:
                    with open(flow, "r") as file:
                        s_object_name = re.search(regexp_find_s_object_name, file.read())
                        if s_object_name is not None:
                            set_sobjects.add(s_object_name.group(0))
                            pb_name = re.search(regexp_find_s_object_name_from_file_name, flow).group(0)
                            set_key(map_s_objects_and_pb, s_object_name.group(0), pb_name)
            os.chdir(generalFolder)
        if folder_name_workflows in automations_dir:
            workflows_dir = os.listdir(path=workflows_path)
            if len(workflows_dir) > 0:
                for fileName in workflows_dir:
                    s_object_name = re.search(regexp_find_s_object_name_from_file_name, fileName).group(0)
                    set_sobjects.add(s_object_name)
        create_package_xml(set_sobjects)
        print(map_s_objects_and_pb)
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


def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]


if __name__ == "__main__":
    get_sobject_name_from_pbs_and_workflows()
