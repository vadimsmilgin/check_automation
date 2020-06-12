#!/usr/bin/python

import os
import re
from context import Context
import utils


class WorkWithAutomation:
    def __init__(self, context: Context) -> None:
        self._context = context

    def get_sobjects_name_from_pbs_and_workflows(self) -> set:
        set_s_objects = set()

        try:
            automations_dir = os.listdir(path=self._context.get_automation_files_path())
            if utils.folder_name_flows in automations_dir:
                flows_dir = os.listdir(path=self._context.get_flows_path())
                if len(flows_dir) > 0:
                    os.chdir(self._context.get_flows_path())
                    for flow in flows_dir:
                        with open(flow, "r") as file:
                            s_object_name = re.search(utils.regexp_s_object_name, file.read())
                            if s_object_name is not None:
                                set_s_objects.add(s_object_name.group(0))
                os.chdir(utils.rootFolder)
            if utils.folder_name_workflows in automations_dir:
                workflows_dir = os.listdir(path=self._context.get_workflows_path())
                if len(workflows_dir) > 0:
                    for fileName in workflows_dir:
                        s_object_name = re.search(utils.regexp_s_object_name_from_file_name, fileName).group(0)
                        set_s_objects.add(s_object_name)
            return set_s_objects
        except FileNotFoundError:
            print('Directory ./sample/retrieveUnpackaged is not found')

    def get_dict_s_objects_pbs(self) -> dict:
        dict_s_objects_and_pb = {}

        os.chdir(utils.rootFolder)
        automations_dir = os.listdir(path=self._context.get_automation_files_path())
        if utils.folder_name_flows in automations_dir:
            flows_dir = os.listdir(path=self._context.get_flows_path())
            if len(flows_dir) > 0:
                os.chdir(self._context.get_flows_path())
                for flow in flows_dir:
                    with open(flow, "r") as file:
                        s_object_name = re.search(utils.regexp_s_object_name, file.read())
                        if s_object_name is not None:
                            utils.set_key(dict_s_objects_and_pb, s_object_name.group(0), flow)
        os.chdir(utils.rootFolder)
        return dict_s_objects_and_pb

    def get_dict_wfs(self) -> dict:
        dict_s_objects_and_wfs = {}

        os.chdir(utils.rootFolder)
        automations_dir = os.listdir(path=self._context.get_automation_files_path())
        if utils.folder_name_workflows in automations_dir:
            workflows_dir = os.listdir(path=self._context.get_workflows_path())
            if len(workflows_dir) > 0:
                for fileName in workflows_dir:
                    s_object_name = re.search(utils.regexp_s_object_name_from_file_name, fileName).group(0)
                    dict_s_objects_and_wfs[s_object_name] = [fileName]
        os.chdir(utils.rootFolder)
        return dict_s_objects_and_wfs

    def check_pb(self, name_pb, lookup_fields) -> list:
        list_errors = []
        list_warnings = []
        dict_errors = {}
        dict_warnings = {}
        list_result = []

        os.chdir(utils.rootFolder)
        flows_dir = os.listdir(path=self._context.get_flows_path())
        if name_pb in flows_dir:
            os.chdir(self._context.get_flows_path())
            with open(name_pb, "r") as file:
                str_file = file.read()
                # check pb's all rules for errors and warnings
                rules = re.findall(utils.regexp_rules, str_file, re.M | re.S)
                for rule in rules:
                    errors = re.findall(
                         r'\.' + lookup_fields + utils.regexp_pb_is_null_true,
                         rule,
                         re.M | re.S
                    )
                    errors2 = re.findall(
                        utils.regexp_pb_is_null_true_start + lookup_fields + utils.regexp_pb_is_null_true_end,
                        rule,
                        re.M | re.S
                    )

                    list_unique_errors = list(set(errors))
                    list_unique_errors2 = list(set(errors2))

                    if len(list_unique_errors) > 0 or len(list_unique_errors2) > 0:
                        if len(list_unique_errors) > 0:
                            list_errors += list_unique_errors
                        if len(list_unique_errors2) > 0:
                            list_errors += list_unique_errors2
                        continue
                    else:
                        is_changed_rules = re.findall(utils.regexp_pb_name_of_is_changed_rule, rule, re.M | re.S)
                        if len(is_changed_rules) > 0:
                            for is_changed_rule in is_changed_rules:
                                fields_arent_null = re.findall(
                                    r'\.' + lookup_fields + utils.regexp_pb_is_not_null,
                                    rule,
                                    re.M | re.S
                                )
                                fields_arent_null_2 = re.findall(
                                    utils.regexp_pb_is_not_null_start + lookup_fields + utils.regexp_pb_is_not_null_end,
                                    rule,
                                    re.M | re.S
                                )
                                if len(fields_arent_null) == 0 and len(fields_arent_null_2) == 0:
                                    warning = re.findall(
                                        utils.regexp_pb_is_changed_rule_start + is_changed_rule + utils.regexp_pb_is_changed_rule_end,
                                        str_file,
                                        re.M | re.S
                                    )
                                    if len(warning) == 1:
                                        warn = re.findall(r'\.' + lookup_fields, warning[0], re.M | re.S)
                                        list_warnings += warn

                list_errors = list(set(list_errors))
                list_warnings = list(set(list_warnings))

                # check pb's formulas for errors and warnings
                formulas = re.findall(
                    utils.regexp_formulas,
                    str_file,
                    re.M | re.S
                )
                for formula in formulas:
                    errors_equal_null = re.findall(
                        r'\.' + lookup_fields + utils.regexp_pb_equal_null,
                        formula,
                        re.M | re.S
                    )
                    list_unique_errors_equal_null = list(set(errors_equal_null))
                    if len(list_unique_errors_equal_null) > 0:
                        desc = re.findall(
                            utils.regexp_description,
                            formula,
                            re.M | re.S
                        )
                        errors = {'fields': list_unique_errors_equal_null, 'description': desc}
                        list_errors += [errors]

                    errors_isblank_or_isnull = re.findall(
                        utils.regexp_pb_isblank_or_isnull + lookup_fields,
                        formula,
                        re.M | re.S
                    )
                    list_unique_errors_isblank_or_isnull = list(set(errors_isblank_or_isnull))
                    if len(list_unique_errors_isblank_or_isnull) > 0:
                        desc = re.findall(
                            utils.regexp_description,
                            formula,
                            re.M | re.S
                        )
                        errors = {'fields': list_unique_errors_isblank_or_isnull, 'description': desc}
                        list_errors += [errors]

                    if len(list_unique_errors_equal_null) > 0 or len(list_unique_errors_isblank_or_isnull) > 0:
                        continue

                    warnings_is_changed = re.findall(
                        utils.regexp_pb_is_changed + lookup_fields,
                        formula,
                        re.M | re.S
                    )
                    if len(warnings_is_changed) > 0:
                        desc = re.findall(
                            utils.regexp_description,
                            formula,
                            re.M | re.S
                        )
                        warnings = {'fields': list(set(warnings_is_changed)), 'description': desc}
                        list_warnings += [warnings]

                utils.get_pb_result(dict_errors, name_pb, list_errors)
                utils.get_pb_result(dict_warnings, name_pb, list_warnings)

                list_result.append(dict_errors)
                list_result.append(dict_warnings)
        os.chdir(utils.rootFolder)
        return list_result

    def check_wf(self, name_wf, regexp_with_lookup_fields) -> dict:
        dict_result = {}

        os.chdir(utils.rootFolder)
        workflows_dir = os.listdir(path=self._context.get_workflows_path())
        if name_wf in workflows_dir:
            os.chdir(self._context.get_workflows_path())
            with open(name_wf, "r") as file:
                rules = re.findall(utils.regexp_rules, file.read(), re.M | re.S)
                for rule in rules:
                    errors = re.findall(regexp_with_lookup_fields, rule, re.M | re.S)
                    if len(errors) > 0:
                        rule_name = re.findall(utils.regexp_full_name, rule, re.M | re.S)[0]
                        formula = re.findall(utils.regexp_formula, rule, re.M | re.S)
                        criteria = re.findall(utils.regexp_criteria_items, rule, re.M | re.S)
                        if len(formula) > 0:
                            utils.get_wf_result(dict_result, name_wf, rule_name, errors, formula)
                        elif len(criteria) > 0:
                            utils.get_wf_result(dict_result, name_wf, rule_name, errors, criteria)
        os.chdir(utils.rootFolder)
        return dict_result

    def find_pbs_vulnerabilities(self, dict_s_objects_lookup_fields) -> list:
        pb_error_list = []
        pb_warnings_list = []
        pb_full_list = []

        dict_s_objects_pbs = self.get_dict_s_objects_pbs()

        for key in dict_s_objects_lookup_fields:
            if key in dict_s_objects_pbs:
                if len(dict_s_objects_lookup_fields[key]) > 0:
                    lookup_fields = dict_s_objects_lookup_fields[key]
                    for pb in dict_s_objects_pbs[key]:
                        result = self.check_pb(pb, utils.get_str_for_regexp(lookup_fields))
                        utils.add_dict_to_list(pb_error_list, result[0])
                        utils.add_dict_to_list(pb_warnings_list, result[1])
        pb_full_list.append(pb_error_list)
        pb_full_list.append(pb_warnings_list)
        return pb_full_list

    def find_wfs_vulnerabilities(self, dict_s_objects_lookup_fields) -> list:
        wf_error_list = []
        wf_warnings_list = []
        wf_full_list = []

        dict_s_objects_wfs = self.get_dict_wfs()

        for key in dict_s_objects_lookup_fields:
            if key in dict_s_objects_wfs:
                if len(dict_s_objects_lookup_fields[key]) > 0:
                    lookup_fields = dict_s_objects_lookup_fields[key]
                    error_regexp = utils.regexp_wf_isnull_isblank_start \
                                   + utils.get_str_for_regexp(lookup_fields) \
                                   + utils.regexp_wf_isnull_isblank_end \
                                   + utils.get_str_for_regexp(lookup_fields) \
                                   + utils.regexp_wf_equal_null
                    warning_regexp = utils.regexp_wf_is_changed \
                                     + utils.get_str_for_regexp(lookup_fields)
                    for wf in dict_s_objects_wfs[key]:
                        utils.add_dict_to_list(wf_error_list, self.check_wf(wf, error_regexp))
                        utils.add_dict_to_list(wf_warnings_list, self.check_wf(wf, warning_regexp))
        wf_full_list.append(wf_error_list)
        wf_full_list.append(wf_warnings_list)
        return wf_full_list
