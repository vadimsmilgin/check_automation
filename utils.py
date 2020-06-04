#!/usr/bin/python

import os
import re

rootFolder = os.getcwd()
folder_name_flows = 'flows'
folder_name_workflows = 'workflows'

regexp_s_object_name = '(?<=<name>ObjectType</name>\n\s{8}<value>\n\s{12}<stringValue>).*?(?=</stringValue>)'
regexp_s_object_name_from_file_name = '.*?(?=\.)'
regexp_rules = '(?<=<rules>)(.*?)(?=</rules>)'
regexp_full_name = '<fullName>(.*?)</fullName>'

regexp_find_lookup_fields = '(?<=<fields>)\n\s{8}<fullName>([a-zA-Z0-9_]+)</fullName>' \
                            '(?:(?!<fields>)(?!</fields>).)*?(?=<type>(?:Lookup|Hierarchy)</type>\n\s{4}</fields>)'

regexp_pb_is_null_true = '</leftValueReference>\n\s{16}<operator>IsNull</operator>' + \
                  '\n\s{16}<rightValue>\n\s{20}<booleanValue>true'

regexp_pb_is_null_true_start = '<stringValue>GlobalConstant</stringValue>\n\s{20}</value>' \
                               '\n\s{16}</processMetadataValues>\n\s{16}<leftValueReference>.*?\.'
regexp_pb_is_null_true_end = '</leftValueReference>\n\s{16}<operator>EqualTo</operator>'

regexp_pb_is_null_true_in_formula = '\s*==\s*(?:NULL|null)'

regexp_pb_is_not_null = '</leftValueReference>\n\s{16}<operator>IsNull</operator>' + \
                        '\n\s{16}<rightValue>\n\s{20}<booleanValue>false'

regexp_pb_is_not_null_start = '<stringValue>GlobalConstant</stringValue>\n\s{20}</value>' \
                              '\n\s{16}</processMetadataValues>\n\s{16}<leftValueReference>.*?\.'
regexp_pb_is_not_null_end = '</leftValueReference>\n\s{16}<operator>NotEqualTo</operator>'

regexp_pb_name_of_is_changed_rule = '<leftValueReference>(isChanged.*?)</leftValueReference>'

regexp_pb_is_changed_rule_start = '<rules>\n\s{12}<name>'
regexp_pb_is_changed_rule_end = '.*?</rules>'

regexp_wf_is_null_true_start = '<fullName>(.*?)</fullName>.*?<formula>.*?(?:ISNULL).*?'
regexp_wf_is_null_true_end = '.*?</formula>'

regexp_wf_is_changed = 'ISCHANGED\s*\(\s*'


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
        dictionary['name'] = re.search(regexp_s_object_name_from_file_name, name).group(0)
        dictionary['lookup_fields'] = errors


def get_wf_result(dictionary, wf_name, rule_name, errors, desc):
    if 'sObject' not in dictionary:
        dictionary['sObject'] = re.search(regexp_s_object_name_from_file_name, wf_name).group(0)

    dict_rule = {'name': rule_name, 'lookup_fields': errors, 'description': desc[0]}

    if 'workflows' not in dictionary:
        list_list = [dict_rule]
        dictionary['workflows'] = list_list
    else:
        dictionary['workflows'].append(dict_rule)
