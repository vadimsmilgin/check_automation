#!/usr/bin/python

import os
import re
import Utils


def get_sobjects_name_from_pbs_and_workflows():
    set_s_objects = set()
    try:
        automations_dir = os.listdir(path=Utils.automation_files_path)
        if Utils.folder_name_flows in automations_dir:
            flows_dir = os.listdir(path=Utils.flows_path)
            if len(flows_dir) > 0:
                os.chdir(Utils.flows_path)
                for flow in flows_dir:
                    with open(flow, "r") as file:
                        s_object_name = re.search(Utils.regexp_find_s_object_name, file.read())
                        if s_object_name is not None:
                            set_s_objects.add(s_object_name.group(0))
            os.chdir(Utils.rootFolder)
        if Utils.folder_name_workflows in automations_dir:
            workflows_dir = os.listdir(path=Utils.workflows_path)
            if len(workflows_dir) > 0:
                for fileName in workflows_dir:
                    s_object_name = re.search(Utils.regexp_find_s_object_name_from_file_name, fileName).group(0)
                    set_s_objects.add(s_object_name)
        return set_s_objects
    except FileNotFoundError:
        print('Directory ./sample/retrieveUnpackaged is not found')


def get_dict_s_objects_pbs():
    map_s_objects_and_pb = {}
    os.chdir(Utils.rootFolder)
    automations_dir = os.listdir(path=Utils.automation_files_path)
    if Utils.folder_name_flows in automations_dir:
        flows_dir = os.listdir(path=Utils.flows_path)
        if len(flows_dir) > 0:
            os.chdir(Utils.flows_path)
            for flow in flows_dir:
                with open(flow, "r") as file:
                    s_object_name = re.search(Utils.regexp_find_s_object_name, file.read())
                    if s_object_name is not None:
                        Utils.set_key(map_s_objects_and_pb, s_object_name.group(0), flow)
    os.chdir(Utils.rootFolder)
    return map_s_objects_and_pb


def get_dict_wfs():
    map_s_objects_and_wfs = {}
    os.chdir(Utils.rootFolder)
    automations_dir = os.listdir(path=Utils.automation_files_path)
    if Utils.folder_name_workflows in automations_dir:
        workflows_dir = os.listdir(path=Utils.workflows_path)
        if len(workflows_dir) > 0:
            for fileName in workflows_dir:
                s_object_name = re.search(Utils.regexp_find_s_object_name_from_file_name, fileName).group(0)
                map_s_objects_and_wfs[s_object_name] = [fileName]
    os.chdir(Utils.rootFolder)
    return map_s_objects_and_wfs


def check_pb(name_pb, regexp_with_lookup_fields):
    os.chdir(Utils.rootFolder)
    flows_dir = os.listdir(path=Utils.flows_path)
    if name_pb in flows_dir:
        os.chdir(Utils.flows_path)
        with open(name_pb, "r") as file:
            errors = re.findall(regexp_with_lookup_fields, file.read(), re.M | re.S)
            if len(errors) > 0:
                print(name_pb)
                print(errors)
    os.chdir(Utils.rootFolder)


def check_wf(name_wf, regexp_with_lookup_fields):
    os.chdir(Utils.rootFolder)
    workflows_dir = os.listdir(path=Utils.workflows_path)
    if name_wf in workflows_dir:
        os.chdir(Utils.workflows_path)
        with open(name_wf, "r") as file:
            errors = re.findall(regexp_with_lookup_fields, file.read(), re.M | re.S)
            if len(errors) > 0:
                print(name_wf)
                print(errors)
    os.chdir(Utils.rootFolder)
