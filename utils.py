#!/usr/bin/python

import os
import re


rootFolder = os.getcwd()
folder_name_flows = 'flows'
folder_name_workflows = 'workflows'


regexp_find_s_object_name = '(?<=<name>ObjectType</name>\n\s{8}<value>\n\s{12}<stringValue>).*?(?=</stringValue>)'
regexp_find_s_object_name_from_file_name = '.*?(?=\.)'

regexp_find_lookup_fields = '(?<=<fields>)\n\s{8}<fullName>([a-zA-Z0-9_]+)</fullName>' \
                            '(?:(?!<fields>)(?!</fields>).)*?(?=<type>(?:Lookup|Hierarchy)</type>\n\s{4}</fields>)'
#(?<=<fullName>)([a-zA-Z0-9_]+)(?:(?!<fields>)(?!</fields>).)*?(?=<type>Lookup</type>)
#(?<=<fields>)\n\s{8}<fullName>([a-zA-Z0-9_]+)</fullName>(?:(?!<fields>)(?!</fields>).)*?(?=<type>Lookup</type>\n\s{4}</fields>)
#(?<=<fields>)\n\s{8}<fullName>([a-zA-Z0-9_]+)</fullName>(?:(?!<fields>)(?!</fields>).)*?(?=<type>(?:Lookup|Hierarchy)</type>\n\s{4}</fields>)

regexp_find_pb_error = '</leftValueReference>\n\s{16}<operator>IsNull</operator>' + \
                       '\n\s{16}<rightValue>\n\s{20}<booleanValue>true' #error 100%

regexp_find_wf_error_start = '<fullName>(.*?)</fullName>.*?<formula>.*?(?:ISNULL).*?'
regexp_find_wf_error_end = '.*?</formula>'
regexp_find_rules = '(?<=<rules>)(.*?)(?=</rules>)'

regexp_find_pb_not_error = '</leftValueReference>\n\s{16}<operator>IsNull</operator>' + \
                           '\n\s{16}<rightValue>\n\s{20}<booleanValue>false'

regexp_find_is_changed_rule = '<leftValueReference>(isChanged.*?)</leftValueReference>'
regexp_find_is_changed_1 = '<rules>\n\s{12}<name>'
regexp_find_is_changed_2 = '.*?</rules>'

regexp_find_wf_warning_start = '<fullName>(.*?)</fullName>.*?<formula>.*?(?:ISCHANGED).*?'
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
    if len(errors) > 0:
        dictionary['name'] = re.search(regexp_find_s_object_name_from_file_name, name).group(0)
        dictionary['lookup_fields'] = errors


def get_wf_result(dictionary, name, errors):
    if 'sObject' not in dictionary:
        dictionary['sObject'] = re.search(regexp_find_s_object_name_from_file_name, name).group(0)
    error_list = []
    dict_error = {}
    for error in errors:
        dict_error = {'name': error[0], 'lookup_field': error[1]}
        error_list.append(dict_error)
    if 'workflows' not in dictionary:
        dictionary['workflows'] = error_list
    else:
        dictionary['workflows'].append(dict_error)
