#!/usr/bin/python

import os

rootFolder = os.getcwd()
automation_files_path = '.\\sample\\retrieveUnpackaged'
flows_path = '.\\sample\\retrieveUnpackaged\\flows'
workflows_path = '.\\sample\\retrieveUnpackaged\\workflows'
retrieve_sobjects_path = '.\\sample\\retrieveSObjects'
s_objects_path = '.\\sample\\retrieveSObjects\\objects'

folder_name_flows = 'flows'
folder_name_workflows = 'workflows'


regexp_find_s_object_name = '(?<=<name>ObjectType</name>\n\s{8}<value>\n\s{12}<stringValue>).*?(?=</stringValue>)'
regexp_find_s_object_name_from_file_name = '.*?(?=\.)'
regexp_find_lookup_fields = '(?<=<fullName>)([a-zA-Z0-9_]+)(?:(?!<fields>)(?!</fields>).)*?(?=<type>Lookup</type>)'
regexp_find_s_object_name_from_file_name = '.*?(?=\.)'
regexp_find_pb_vulnerable_conditionals = '<\/leftValueReference>\n\s{16}<operator>IsNull<\/operator>' + \
                                         '\n\s{16}<rightValue>\n\s{20}<booleanValue>true'
regexp_find_wf_vulnerable_conditionals_1 = '<rules>\n\s{8}<fullName>(.*?)</fullName>.*?<formula>.*?ISNULL.*?'
regexp_find_wf_vulnerable_conditionals_2 = '.*?</formula>.*?</rules>'


def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = [value]
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)


def get_str_for_regexp(lookup_fields_list):
    sepatator = '|'
    return '(' + sepatator.join(lookup_fields_list) + ')'