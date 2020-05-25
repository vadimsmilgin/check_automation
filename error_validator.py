#!/usr/bin/python

import json
import platform
from work_with_automation import WorkWithAutomation
from work_with_s_objects import WorkWithSObjects
from context import Context, Windows, MacOS


def validation():
    errors = {}
    warnings = {}
    full_result = {}

    if platform.system() == 'Windows':
        context1 = Context(Windows())
    if platform.system() == 'Darwin':
        context1 = Context(MacOS())

    wwa = WorkWithAutomation(context1)
    wws = WorkWithSObjects(context1)

    if len(wwa.find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())[0]) > 0:
        errors['Process_Builders'] = wwa.find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())[0]
    if len(wwa.find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())[0]) > 0:
        errors['Workflows'] = wwa.find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())[0]

    if len(wwa.find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())[1]) > 0:
        warnings['Process_Builders'] = wwa.find_pbs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_s_objects_pbs())[1]
    if len(wwa.find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())[1]) > 0:
        warnings['Workflows'] = wwa.find_wfs_vulnerabilities(wws.get_lookup_fields(), wwa.get_dict_wfs())[1]

    full_result['Errors'] = errors
    full_result['Warnings'] = warnings
    print(json.dumps(full_result, indent=4))


if __name__ == "__main__":
    validation()
