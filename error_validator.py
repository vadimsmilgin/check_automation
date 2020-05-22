#!/usr/bin/python

import json
import utils
import work_with_automation as wwa
import work_with_s_objects as wws


def validation():
    errors = {}
    warnings = {}
    full_result = {}
    if len(find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())[0]) > 0:
        errors['Process_Builders'] = find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())[0]
    if len(find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())[0]) > 0:
        errors['Workflows'] = find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())[0]

    if len(find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())[1]) > 0:
        warnings['Process_Builders'] = find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())[1]
    if len(find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())[1]) > 0:
        warnings['Workflows'] = find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())[1]

    full_result['Errors'] = errors
    full_result['Warnings'] = warnings
    print(json.dumps(full_result, indent=4))


def find_pbs_vulnerabilities(dict_s_objects_lookup_fields, dict_s_objects_pbs):
    pb_error_list = []
    pb_warnings_list = []
    pb_full_list = []
    for key in dict_s_objects_lookup_fields:
        if key in dict_s_objects_pbs:
            if len(dict_s_objects_lookup_fields[key]) > 0:
                lookup_fields = dict_s_objects_lookup_fields[key]
                error_regexp = utils.get_str_for_regexp(lookup_fields) + utils.regexp_find_pb_vulnerable_conditionals
                warning_regexp = utils.get_str_for_regexp(lookup_fields)
                for pb in dict_s_objects_pbs[key]:
                    utils.add_dict_to_list(pb_error_list, wwa.check_pb(pb, error_regexp))
                    utils.add_dict_to_list(pb_warnings_list, wwa.check_pb(pb, warning_regexp))
    pb_full_list.append(pb_error_list)
    pb_full_list.append(pb_warnings_list)
    return pb_full_list


def find_wfs_vulnerabilities(dict_s_objects_lookup_fields, dict_s_objects_wfs):
    wf_error_list = []
    wf_warnings_list = []
    wf_full_list = []
    for key in dict_s_objects_lookup_fields:
        if key in dict_s_objects_wfs:
            if len(dict_s_objects_lookup_fields[key]) > 0:
                lookup_fields = dict_s_objects_lookup_fields[key]
                error_regexp = utils.regexp_find_wf_error_start \
                                + utils.get_str_for_regexp(lookup_fields) \
                                + utils.regexp_find_wf_error_end
                warning_regexp = utils.regexp_find_wf_warning_start \
                                 + utils.get_str_for_regexp(lookup_fields) \
                                 + utils.regexp_find_wf_error_end
                for wf in dict_s_objects_wfs[key]:
                    utils.add_dict_to_list(wf_error_list, wwa.check_wf(wf, error_regexp))
                    utils.add_dict_to_list(wf_warnings_list, wwa.check_wf(wf, warning_regexp))
    wf_full_list.append(wf_error_list)
    wf_full_list.append(wf_warnings_list)
    return wf_full_list


if __name__ == "__main__":
    validation()
