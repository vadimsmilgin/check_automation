#!/usr/bin/python

import os
import re
import xml.dom.minidom
import xml.etree.ElementTree as xmll

staticPath = '.\sample\\retrieveUnpackaged'
folderFlows = '.\sample\\retrieveUnpackaged\\flows'
folderWorkflows = '.\sample\\retrieveUnpackaged\workflows'

folderNameFlows = 'flows'
folderNameWorkflows = 'workflows'

generalFolder = os.getcwd()

encodingUTF8 = ' encoding="UTF-8" ?>'


def createPackageXMLWithSObjects(*args):
    sObjects = args[0]
    os.chdir(generalFolder)

    root = xmll.Element("Package")
    root.set('xmlns', 'http://soap.sforce.com/2006/04/metadata')

    for sObject in sObjects:
        types = xmll.Element("types")
        root.append(types)

        members = xmll.SubElement(types, "members")
        members.text = sObject

        name = xmll.SubElement(types, "name")
        name.text = "CustomObject"

    version = xmll.SubElement(root, "version")
    version.text = "48.0"

    tree = xmll.ElementTree(root)

    xmlstr = xml.dom.minidom.parseString(xmll.tostring(tree.getroot(), encoding="UTF-8")).toprettyxml()
    result = re.sub(r'\s.>', encodingUTF8, xmlstr)
    with open("test.xml", "w") as fh:
        fh.write(result)


try:
    dirs = os.listdir(path=staticPath)
    setSobjects = set()
    setSobjectsFromWorkflows = set()
    if folderNameFlows in dirs:
        dirsFlows = os.listdir(path=folderFlows)
        if len(dirsFlows) > 0:
            os.chdir(folderFlows)
            for file in dirsFlows:
                with open(file, "r") as fh:
                    string = fh.read()
                    #print(string)
                    result = re.search(
                        r'(?<=<name>ObjectType</name>\n\s{8}<value>\n\s{12}<stringValue>).*?(?=</stringValue>)',
                        string
                    )
                    result2 = re.search(
                        r'(?<=<name>ObjectType</name>\n\s{16}<value>\n\s{20}<stringValue>).*?(?=</stringValue>)',
                        string
                    )
                    if result != None:
                        print(result.group(0))
                    else:
                        print(result2.group(0))
                    #break
                # try:
                #     doc = xml.dom.minidom.parse(file)
                #     processMetadataValues = doc.getElementsByTagName("processMetadataValues")
                #     for processMetadataValuesChild in processMetadataValues:
                #         child = processMetadataValuesChild.childNodes
                #         if child[1].childNodes[0].nodeValue == 'ObjectType':
                #             sObject = child[3].childNodes[1].childNodes[0].nodeValue
                #             setSobjects.add(sObject)
                # except Exception as e:
                #     print(str(e))
            #createPackageXMLWithSObjects(setSobjects)
            print('pbs sobjects:')
            print(setSobjects)
        os.chdir(generalFolder)
    if folderNameWorkflows in dirs:
        dirsWorkflows = os.listdir(path=folderWorkflows)
        if len(dirsWorkflows) > 0:
            for fileName in dirsWorkflows:
                sObjectName = re.search(r'.*?(?=\.)', fileName).group(0)
                setSobjectsFromWorkflows.add(sObjectName)
            print('workflows sobjects:')
            print(setSobjectsFromWorkflows)

except FileNotFoundError:
    print('Directory /sample/retrieveUnpackaged is not found')


def find_sobjects(*args):
    path = args[0]
    dirs = os.listdir(path=path)
    if len(dirs) > 0:
        os.chdir(path)
        for file in dirs:
            try:
                doc = xml.dom.minidom.parse(file)
                processMetadataValues = doc.getElementsByTagName("processMetadataValues")
                for processMetadataValuesChild in processMetadataValues:
                    child = processMetadataValuesChild.childNodes
                    if child[1].childNodes[0].nodeValue == 'ObjectType':
                        sObject = child[3].childNodes[1].childNodes[0].nodeValue
                        setSobjects.add(sObject)
            except Exception as e:
                print(str(e))



#(?<=<name>objectType</name>
                # <value>
                #     <stringValue>).*?(?=</stringValue>)







