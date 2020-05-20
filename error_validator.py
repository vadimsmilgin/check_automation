#!/usr/bin/python

import utils
import work_with_automation as WWA
import work_with_s_objects as WWS


def validation():
    find_pbs_vulnerabilities(WWS.get_lookup_fields(), WWA.get_dict_s_objects_pbs())
    print('============================================================================')
    find_wfs_vulnerabilities(WWS.get_lookup_fields(), WWA.get_dict_wfs())


def find_pbs_vulnerabilities(dict_s_objects_lookup_fields, dict_s_objects_pbs):
    for key in dict_s_objects_lookup_fields:
        if key in dict_s_objects_pbs:
            if len(dict_s_objects_lookup_fields[key]) > 0:
                lookup_fields = dict_s_objects_lookup_fields[key]
                regexp = utils.get_str_for_regexp(lookup_fields) + utils.regexp_find_pb_vulnerable_conditionals
                for pb in dict_s_objects_pbs[key]:
                    WWA.check_pb(pb, regexp)


def find_wfs_vulnerabilities(dict_s_objects_lookup_fields, dict_s_objects_wfs):
    for key in dict_s_objects_lookup_fields:
        if key in dict_s_objects_wfs:
            if len(dict_s_objects_lookup_fields[key]) > 0:
                lookup_fields = dict_s_objects_lookup_fields[key]
                regexp = utils.regexp_find_wf_vulnerable_conditionals_1 \
                         + utils.get_str_for_regexp(lookup_fields) \
                         + utils.regexp_find_wf_vulnerable_conditionals_2
                for wf in dict_s_objects_wfs[key]:
                    WWA.check_wf(wf, regexp)


if __name__ == "__main__":
    validation()
