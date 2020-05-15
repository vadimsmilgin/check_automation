#!/usr/bin/python

import os
import re
import Utils


def get_lookup_fields():
    map_s_object_and_lookup_fields = {}
    s_objects_dir = os.listdir(path=Utils.s_objects_path)
    if len(s_objects_dir) > 0:
        os.chdir(Utils.s_objects_path)
        for s_object_file in s_objects_dir:
            s_object_name = re.search(Utils.regexp_find_s_object_name_from_file_name, s_object_file).group(0)
            with open(s_object_file, "r") as file:
                look_up_fields = re.findall(Utils.regexp_find_lookup_fields, file.read(), re.M | re.S)
                if look_up_fields is not None:
                    map_s_object_and_lookup_fields[s_object_name] = look_up_fields
    os.chdir(Utils.rootFolder)
    return map_s_object_and_lookup_fields
