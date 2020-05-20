#!/usr/bin/python

import json
import utils
import work_with_automation as wwa
import work_with_s_objects as wws


def validation():
    result = {}
    if len(find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())) > 0:
        result['Process_Builders'] = find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())
    if len(find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())) > 0:
        result['Workflows'] = find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())
    print(json.dumps(result, indent=4))


def find_pbs_vulnerabilities(dict_s_objects_lookup_fields, dict_s_objects_pbs):
    pb_list = []
    for key in dict_s_objects_lookup_fields:
        if key in dict_s_objects_pbs:
            if len(dict_s_objects_lookup_fields[key]) > 0:
                lookup_fields = dict_s_objects_lookup_fields[key]
                regexp = utils.get_str_for_regexp(lookup_fields) + utils.regexp_find_pb_vulnerable_conditionals
                for pb in dict_s_objects_pbs[key]:
                    utils.add_dict_to_list(pb_list, wwa.check_pb(pb, regexp))
    return pb_list


def find_wfs_vulnerabilities(dict_s_objects_lookup_fields, dict_s_objects_wfs):
    wf_list = []
    for key in dict_s_objects_lookup_fields:
        if key in dict_s_objects_wfs:
            if len(dict_s_objects_lookup_fields[key]) > 0:
                lookup_fields = dict_s_objects_lookup_fields[key]
                regexp = utils.regexp_find_wf_vulnerable_conditionals_1 \
                         + utils.get_str_for_regexp(lookup_fields) \
                         + utils.regexp_find_wf_vulnerable_conditionals_2
                for wf in dict_s_objects_wfs[key]:
                    utils.add_dict_to_list(wf_list, wwa.check_wf(wf, regexp))
    return wf_list


if __name__ == "__main__":
    validation()
