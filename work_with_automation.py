#!/usr/bin/python

import os
import re
import utils


def get_sobjects_name_from_pbs_and_workflows():
    set_s_objects = set()
    try:
        automations_dir = os.listdir(path=utils.automation_files_path)
        if utils.folder_name_flows in automations_dir:
            flows_dir = os.listdir(path=utils.flows_path)
            if len(flows_dir) > 0:
                os.chdir(utils.flows_path)
                for flow in flows_dir:
                    with open(flow, "r") as file:
                        s_object_name = re.search(utils.regexp_find_s_object_name, file.read())
                        if s_object_name is not None:
                            set_s_objects.add(s_object_name.group(0))
            os.chdir(utils.rootFolder)
        if utils.folder_name_workflows in automations_dir:
            workflows_dir = os.listdir(path=utils.workflows_path)
            if len(workflows_dir) > 0:
                for fileName in workflows_dir:
                    s_object_name = re.search(utils.regexp_find_s_object_name_from_file_name, fileName).group(0)
                    set_s_objects.add(s_object_name)
        return set_s_objects
    except FileNotFoundError:
        print('Directory ./sample/retrieveUnpackaged is not found')


def get_dict_s_objects_pbs():
    dict_s_objects_and_pb = {}
    os.chdir(utils.rootFolder)
    automations_dir = os.listdir(path=utils.automation_files_path)
    if utils.folder_name_flows in automations_dir:
        flows_dir = os.listdir(path=utils.flows_path)
        if len(flows_dir) > 0:
            os.chdir(utils.flows_path)
            for flow in flows_dir:
                with open(flow, "r") as file:
                    s_object_name = re.search(utils.regexp_find_s_object_name, file.read())
                    if s_object_name is not None:
                        utils.set_key(dict_s_objects_and_pb, s_object_name.group(0), flow)
    os.chdir(utils.rootFolder)
    return dict_s_objects_and_pb


def get_dict_wfs():
    dict_s_objects_and_wfs = {}
    os.chdir(utils.rootFolder)
    automations_dir = os.listdir(path=utils.automation_files_path)
    if utils.folder_name_workflows in automations_dir:
        workflows_dir = os.listdir(path=utils.workflows_path)
        if len(workflows_dir) > 0:
            for fileName in workflows_dir:
                s_object_name = re.search(utils.regexp_find_s_object_name_from_file_name, fileName).group(0)
                dict_s_objects_and_wfs[s_object_name] = [fileName]
    os.chdir(utils.rootFolder)
    return dict_s_objects_and_wfs


def check_pb(name_pb, regexp_with_lookup_fields):
    dict_result = {}
    os.chdir(utils.rootFolder)
    flows_dir = os.listdir(path=utils.flows_path)
    if name_pb in flows_dir:
        os.chdir(utils.flows_path)
        with open(name_pb, "r") as file:
            errors = re.findall(regexp_with_lookup_fields, file.read(), re.M | re.S)
            list_unique_errors = list(set(errors))
            if len(list_unique_errors) > 0:
                utils.get_pb_result(dict_result, name_pb, list_unique_errors)
    os.chdir(utils.rootFolder)
    return dict_result


def check_wf(name_wf, regexp_with_lookup_fields):
    dict_result = {}
    os.chdir(utils.rootFolder)
    workflows_dir = os.listdir(path=utils.workflows_path)
    if name_wf in workflows_dir:
        os.chdir(utils.workflows_path)
        with open(name_wf, "r") as file:
            rules = re.findall(utils.regexp_find_rules, file.read(), re.M | re.S)
            for rule in rules:
                error = re.findall(regexp_with_lookup_fields, rule, re.M | re.S)
                if len(error) > 0:
                    utils.get_wf_result(dict_result, name_wf, error)
    os.chdir(utils.rootFolder)
    return dict_result
