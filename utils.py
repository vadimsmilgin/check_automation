#!/usr/bin/python

import os
import re

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

regexp_find_lookup_fields = '(?<=<fields>)\n\s{8}<fullName>([a-zA-Z0-9_]+)</fullName>(?:(?!<fields>)(?!</fields>).)*?(?=<type>Lookup</type>\n\s{4}</fields>)'
#(?<=<fullName>)([a-zA-Z0-9_]+)(?:(?!<fields>)(?!</fields>).)*?(?=<type>Lookup</type>)

regexp_find_pb_vulnerable_conditionals = '<\/leftValueReference>\n\s{16}<operator>IsNull<\/operator>' + \
                                         '\n\s{16}<rightValue>\n\s{20}<booleanValue>true'

regexp_find_wf_error_start = '<fullName>(.*?)</fullName>.*?<formula>.*?(?:ISNULL|ISCHANGED).*?'
regexp_find_wf_error_end = '.*?</formula>'
regexp_find_rules = '(?<=<rules>)(.*?)(?=</rules>)'
regexp_find_wf_warning_start = '<fullName>(.*?)</fullName>.*?<formula>.*?'
regexp_find_wf_warning_end = '.*?</formula>'

def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = [value]
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)


def get_str_for_regexp(lookup_fields_list):
    sepatator = '|'
    return '(' + sepatator.join(lookup_fields_list) + ')'


def add_dict_to_list(current_list, dictionary):
    if bool(dictionary) is True:
        current_list.append(dictionary)


def get_pb_result(dictionary, name, errors):
    dictionary['name'] = re.search(regexp_find_s_object_name_from_file_name, name).group(0)
    dictionary['lookup_fields'] = errors


def get_wf_result(dictionary, name, errors):
    dictionary['sObject'] = re.search(regexp_find_s_object_name_from_file_name, name).group(0)
    error_list = []
    for error in errors:
        dict_error = {'name': error[0], 'lookup_field': error[1]}
        error_list.append(dict_error)
    dictionary['workflows'] = error_list
