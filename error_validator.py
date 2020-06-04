#!/usr/bin/python

import json
import platform
from datetime import datetime
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

    pbs_errors_warnings = wwa.find_pbs_vulnerabilities(wws.get_lookup_fields())
    wfs_errors_warnings = wwa.find_wfs_vulnerabilities(wws.get_lookup_fields())

    if len(pbs_errors_warnings[0]) > 0:
        errors['Process_Builders'] = pbs_errors_warnings[0]
    if len(wfs_errors_warnings[0]) > 0:
        errors['Workflows'] = wfs_errors_warnings[0]

    if len(pbs_errors_warnings[1]) > 0:
        warnings['Process_Builders'] = pbs_errors_warnings[1]
    if len(wfs_errors_warnings[1]) > 0:
        warnings['Workflows'] = wfs_errors_warnings[1]

    full_result['Errors'] = errors
    full_result['Warnings'] = warnings
    print(json.dumps(full_result, indent=4))

    name = 'result_' + datetime.now().strftime("%m_%d_%Y-%H.%M.%S") + '.txt'

    with open(name, "w") as package:
        package.write(json.dumps(full_result, indent=4))


if __name__ == "__main__":
    validation()
